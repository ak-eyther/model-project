# Email Marketing AI: Domain Patterns

## The Business Model

### Revenue Flow

```
Email Sent → Delivered → Opened → Clicked → Converted → Revenue
   │            │          │         │          │           │
   └── Bounced  └── Spam   └── Ignored└── Bounced└── Abandoned
```

**THE MONEY METRIC: Conversions (Conv)**
- Advertisers pay for completed actions
- Revenue = Conv × Payout
- Everything else is a proxy

### Key Metrics

| Metric | Formula | Good | Warning | Bad |
|--------|---------|------|---------|-----|
| Open Rate | Opens / Delivered | >15% | 10-15% | <10% |
| CTR | Clicks / Opens | >5% | 2-5% | <2% |
| CCR | Conv / Clicks | >10% | 5-10% | <5% |
| EPC | Revenue / Clicks | >$0.50 | $0.20-0.50 | <$0.20 |
| Complaint Rate | Complaints / Delivered | <0.1% | 0.1-0.3% | >0.3% |
| Bounce Rate | Bounces / Sent | <2% | 2-5% | >5% |

---

## Deliverability: The Existential Risk

### Google/Yahoo 2024 Rules

**Hard limits** (crossing these kills deliverability):
- Complaint rate > 0.3% = severe impact
- No DKIM/SPF authentication = blocked
- No one-click unsubscribe = filtered

**Soft limits** (affects placement):
- Complaint rate > 0.1% = inbox degradation
- Low engagement = spam folder
- Sending pattern anomalies = throttled

### IP Reputation Lifecycle

```
New IP (Cold)
    │
    ▼
Warmup Phase (2-4 weeks)
    │ Send gradually increasing volume
    │ Monitor complaints closely
    ▼
Established IP
    │ Stable reputation
    │ Can handle volume
    ▼
Reputation Damage (if misused)
    │ High complaints
    │ Spam traps hit
    ▼
Recovery (difficult, slow)
    │ 30-90 days
    │ Very low volume
    │ Perfect hygiene
```

### Deliverability Monitoring

**Daily checks:**
- Complaint rate trend
- Bounce rate by domain
- IP reputation score
- Spam trap hits

**Weekly checks:**
- Inbox placement tests
- Blacklist status
- Authentication health

---

## List Segmentation Strategy

### Engagement-Based Segments

| Segment | Definition | Send Frequency | Risk |
|---------|------------|----------------|------|
| 1HR_Opener | Opened in last 1 hour | High | Low |
| 24HR_Opener | Opened in last 24 hours | High | Low |
| 7D_Opener | Opened in last 7 days | Medium | Low |
| 30D_Opener | Opened in last 30 days | Low | Medium |
| 90D_Opener | Opened in last 90 days | Very Low | High |
| Cold | No activity 90+ days | Avoid | Very High |

### Domain-Based Segments

| Prefix | Domain | Considerations |
|--------|--------|----------------|
| GM_ | Gmail | Strictest filters, highest volume |
| YH_ | Yahoo | Moderate filters |
| MS_ | Microsoft | Outlook, Hotmail |
| OT_ | Other | ISPs, corporate |

**Cross-reference**: GM_30D_Opener = Gmail users who opened in last 30 days

---

## List Fatigue Detection

### Signals

1. **Declining open rate** over 2+ weeks
2. **Rising complaint rate** even slightly
3. **Decreasing EPC** despite same offers
4. **Volume sensitivity** (more sends = worse performance)

### Fatigue Score Formula

```python
fatigue_score = (
    0.4 * open_rate_decline_7d +
    0.3 * complaint_rate_increase_7d +
    0.2 * epc_decline_7d +
    0.1 * send_frequency_score
)

# 0.0 = Healthy
# 0.5 = Moderate fatigue
# 1.0 = Severe fatigue
```

### Mitigation Strategies

| Fatigue Level | Action |
|---------------|--------|
| Low (0-0.3) | Continue, monitor |
| Medium (0.3-0.6) | Reduce frequency, rotate offers |
| High (0.6-0.8) | Rest 3-7 days, change creative approach |
| Severe (>0.8) | Rest 14+ days, re-engagement campaign |

---

## Offer Performance Patterns

### Offer Lifecycle

```
New Offer (0-2 weeks)
    │ Limited data
    │ Cold start problem
    ▼
Testing Phase (2-4 weeks)
    │ A/B testing
    │ Finding optimal segments
    ▼
Peak Performance (1-3 months)
    │ Best combinations identified
    │ Scaling volume
    ▼
Decline Phase (3-6 months)
    │ Audience saturation
    │ Creative fatigue
    ▼
Retirement or Refresh
```

### Cross-List Transfer Patterns

Some offers work across multiple lists. Pattern:

```python
# If offer X performs well on GM_30D_Opener
# Check: Does it transfer to GM_7D_Clicker?

transfer_confidence = calculate_transfer_score(
    source_performance=source_metrics,
    list_similarity=similarity_score,
    offer_versatility=versatility_score
)
```

### Hidden Gems Detection

Underutilized offers with high potential:

```python
hidden_gem_score = (
    performance_percentile *  # High performance
    (1 - usage_frequency) *   # Low usage
    data_confidence           # Enough data
)
```

---

## Subject Line Optimization

### What Works

✅ **Personalization**: "[First Name], your approval is waiting"
✅ **Urgency**: "Last chance" (but don't overuse)
✅ **Curiosity**: "The one thing banks don't want you to know"
✅ **Benefit-focused**: "Get up to $5,000 today"

### What Fails

❌ **Spam triggers**: "FREE!!!", "Act now!!!", excessive caps
❌ **Misleading**: "Re: Your application" (when there was none)
❌ **Too long**: >50 characters often truncated
❌ **Boring**: "Newsletter #47"

### Testing Strategy

```
Week 1: Test 5 subject lines on small segment (10K)
Week 2: Top 2 performers on larger segment (50K)
Week 3: Winner to full list
Week 4: Rotate, start testing new batch
```

---

## From Name Strategy

### Patterns That Work

| Type | Example | Use Case |
|------|---------|----------|
| Personal | "Sarah from QuickLoans" | Trust building |
| Brand | "QuickLoans" | Brand recognition |
| Action | "QuickLoans Approval Team" | Urgency |
| Hybrid | "Sarah at QuickLoans" | Balance |

### Rotation Strategy

Don't use the same from name repeatedly:
- Rotate 3-5 from names per week
- Match from name to offer type
- Test new from names on small segments first

---

## BFSI-Specific Patterns

### Payday/Personal Loan Offers

**Peak timing:**
- End of month (payday loan demand)
- Tax season (refund anticipation)
- Back to school (personal loan demand)

**Compliance requirements:**
- APR disclosure
- State restrictions
- Adverse action notices

### Credit Card Offers

**Audience signals:**
- Credit score indicators
- Recent credit inquiries
- Debt-to-income signals

**Creative approach:**
- Benefits-focused (rewards, cashback)
- Comparison positioning
- Pre-qualification messaging

---

## AI-Specific Patterns for Email Marketing

### Prediction Calibration

**Problem**: ML models predict average, not variation

```python
# Model predicts EPC = $0.45
# Reality: Actual EPC varies $0.20 - $0.70

# Solution: Confidence intervals
prediction = {
    "epc": 0.45,
    "lower_bound": 0.35,
    "upper_bound": 0.55,
    "confidence": "MEDIUM"
}
```

### Cold Start Handling

```python
if data_points < 10:
    return {
        "recommendation": similar_offer_performance,
        "confidence": "LOW",
        "warning": "Limited data - using similar offer baseline"
    }
```

### Seasonality Awareness

```python
# Don't recommend based on December data in January
if training_period_includes_holiday:
    apply_seasonality_adjustment()
    flag_seasonal_uncertainty()
```
