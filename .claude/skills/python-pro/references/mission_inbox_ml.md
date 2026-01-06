# Reference: {{PROJECT_NAME}} ML System

## Quick Reference

| Model | File | Predicts | Method |
|-------|------|----------|--------|
| OR (Open Rate) | `ml/models/or_model.cbm` | Open rate % | CatBoost ML |
| CTR (Click Rate) | `ml/models/ctr_model.cbm` | Click rate % | CatBoost ML |
| EPC | N/A | Revenue per click | Historical lookup (NOT ML) |

**Important:** EPC is NOT an ML model - it uses historical averages from `EPCLookup`.

---

## File Locations

```
backend/
├── ml/
│   ├── train_models.py              # Main training script
│   ├── train_models_from_excel.py   # Train from Excel export
│   └── models/
│       ├── or_model.cbm             # Open Rate CatBoost model
│       ├── ctr_model.cbm            # Click Rate CatBoost model
│       ├── or_features.json         # OR model features (110)
│       ├── ctr_features.json        # CTR model features
│       └── metrics.json             # Training metrics (R², MAE)
│
├── app/tools/
│   ├── ml_models.py                 # MLPredictor class (serving)
│   ├── feature_builder.py           # FeatureBuilder class
│   └── epc_lookup.py                # EPCLookup (historical, not ML)
│
└── app/agents/analyst/
    └── prompts.py                   # Uses predictions in scoring
```

---

## Training Models

### Run Training
```bash
cd backend

# Train OR and CTR models (default)
python ml/train_models.py

# Also train EPC model (optional, not used in production)
TRAIN_EPC_MODEL=1 python ml/train_models.py
```

### Training Configuration
```python
# From ml/train_models.py
CATBOOST_PARAMS = {
    'iterations': 500,
    'depth': 6,
    'learning_rate': 0.05,
    'loss_function': 'RMSE',
    'random_seed': 42,
    'early_stopping_rounds': 50,
}

# Target metrics
# R² > 0.3 (minimum acceptable)
# R² > 0.6 (goal)
```

### Data Source
Training data comes from the `Campaign` database table:
```python
from app.models.database import Campaign
from app.database.connection import SessionLocal

session = SessionLocal()
campaigns = session.query(Campaign).all()
```

---

## Feature Builder

### Usage
```python
from app.tools.feature_builder import FeatureBuilder

builder = FeatureBuilder()
features_df = builder.build_features(campaigns_df)

# Get feature names
print(builder.feature_columns)      # All 110 features
print(builder.categorical_features) # ['quarter', 'month', 'day_of_week_num']
```

### Feature Categories (110 total)

| Category | Count | Examples |
|----------|-------|----------|
| List features | 15 | `list_is_30d_opener`, `list_is_gmail`, `list_ctr_mean` |
| Offer features | 12 | `offer_epc_mean`, `offer_conv_sum`, `offer_popularity` |
| IP features | 6 | `ip_health_score`, `ip_is_risky`, `ip_complaint_rate_mean` |
| Temporal features | 10 | `day_of_week_num`, `is_weekend`, `days_since_last_send` |
| Interaction features | 15 | `list_offer_epc_mean`, `list_offer_fatigue_score` |
| Historical features | 10 | `list_or_rate_7d_avg`, `offer_epc_30d_avg` |
| Correlation features | 20 | `combo_novelty_score`, `sustainability_score` |
| Creative features | 22 | `creative_ctr_mean`, `subject_has_urgency` |

### Key Features for List Segmentation
```python
# Domain detection (affects EPC significantly)
'list_is_gmail'       # Gmail = lower EPC
'list_is_yahoo'       # Yahoo = higher EPC
'list_is_aol'         # AOL = higher EPC
'list_is_outlook'     # Outlook = medium EPC

# Engagement type
'list_is_30d_opener'  # Opened in last 30 days
'list_is_1hr_opener'  # Opened within 1 hour
'list_is_7d_clicker'  # Clicked in last 7 days
'list_is_fresh'       # Recently added subscribers
```

---

## Model Serving (MLPredictor)

### How Analyst Agent Uses Models

```python
from app.tools.ml_models import MLPredictor

# Initialize predictor (loads models once)
predictor = MLPredictor()

# Predict for a candidate
result = predictor.predict({
    'list_id': 'GM_30D_Opener',
    'offer_id': 'offer_123',
    'subject_line': 'Limited Time Offer!',
    # ... other features
})

# Result contains:
# {
#     'or_prediction': 12.5,      # Open rate %
#     'ctr_prediction': 2.3,      # Click rate %
#     'epc_estimate': 0.45,       # From historical lookup
#     'confidence': 'high'
# }
```

### MLPredictor Class Structure
```python
class MLPredictor:
    """
    Loads CatBoost models for OR/CTR.
    EPC is served via historical EPCLookup.
    """

    def __init__(self):
        self.or_model = self._load_model('or_model.cbm')
        self.ctr_model = self._load_model('ctr_model.cbm')
        self.epc_lookup = create_epc_lookup_from_db()

    def predict(self, features: dict) -> dict:
        # Build feature vector
        feature_vector = self._build_features(features)

        # Get predictions
        or_pred = self.or_model.predict(feature_vector)
        ctr_pred = self.ctr_model.predict(feature_vector)
        epc_est = self.epc_lookup.get_expected_epc(
            features['offer_id'],
            features['list_id']
        )

        return {
            'or_prediction': or_pred,
            'ctr_prediction': ctr_pred,
            'epc_estimate': epc_est
        }
```

---

## EPC Lookup (NOT ML!)

**Critical:** EPC uses historical averages, not ML prediction.

```python
from app.tools.epc_lookup import EPCLookup, create_epc_lookup_from_db

# Create lookup from database
lookup = create_epc_lookup_from_db()

# Get expected EPC for offer+list combo
epc = lookup.get_expected_epc(
    offer_id='offer_123',
    list_id='GM_30D_Opener'
)

# Fallback hierarchy:
# 1. Exact offer+list combo average
# 2. Offer average across all lists
# 3. List domain average (Gmail, Yahoo, etc.)
# 4. Global average
```

Why not ML for EPC?
- Revenue happens AFTER click (conversion on advertiser site)
- Too many external factors (advertiser payout changes, seasonality)
- Historical lookup is more stable and accurate

---

## Database Tables

### Campaign Table (Primary)
```sql
-- Main training data source
SELECT
    list_name,          -- e.g., 'GM_30D_Opener'
    offer_id,           -- e.g., 'offer_123'
    subject_line,
    from_name,
    creative_id,
    ip_number,
    send_date,
    open_rate,          -- Target for OR model
    click_rate,         -- Target for CTR model
    epc,                -- Used for historical lookup
    delivered,
    complaint_rate
FROM campaigns;
```

### Daily Stats Table (Aggregates)
```sql
-- Used for trend features
SELECT
    date,
    list_name,
    offer_id,
    avg_open_rate,
    avg_click_rate,
    avg_epc,
    total_delivered
FROM daily_stats;
```

---

## Debugging Models

### Check Model Performance
```python
import json
from pathlib import Path

metrics_path = Path('ml/models/metrics.json')
metrics = json.loads(metrics_path.read_text())

print(f"OR Model R²: {metrics['or']['r2_score']:.3f}")
print(f"CTR Model R²: {metrics['ctr']['r2_score']:.3f}")
```

### Feature Importance
```python
from catboost import CatBoostRegressor

model = CatBoostRegressor()
model.load_model('ml/models/or_model.cbm')

# Top 10 important features
importance = dict(zip(
    model.feature_names_,
    model.feature_importances_
))
top_10 = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:10]
for name, score in top_10:
    print(f"{name}: {score:.4f}")
```

### Validate Predictions
```python
from app.tools.ml_models import MLPredictor

predictor = MLPredictor()

# Test prediction
test_features = {
    'list_name': 'GM_30D_Opener',
    'offer_id': 'test_offer',
    'subject_line': 'Test Subject',
    'ip_number': 1,
    'send_date': '2025-01-15'
}

result = predictor.predict(test_features)
print(f"OR: {result['or_prediction']:.2f}%")
print(f"CTR: {result['ctr_prediction']:.2f}%")
print(f"EPC: ${result['epc_estimate']:.2f}")
```
