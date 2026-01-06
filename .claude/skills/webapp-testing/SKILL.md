---
name: webapp-testing
description: Complete testing toolkit for web applications - backend pytest, E2E Playwright, performance profiling, and local automation.
license: Complete terms in LICENSE.txt
---

# Web Application Testing

## Quick Reference

| Need | Section |
|------|---------|
| Test FastAPI endpoints | [Backend Testing](#1-backend-testing-pytest) |
| Test UI flows in browser | [E2E Testing](#2-e2e-testing-playwright) |
| Measure performance/CWV | [Performance Testing](#3-performance-testing) |
| Automate local webapps | [Local Automation](#4-local-webapp-automation) |

---

## {{PROJECT_NAME}} URLs + Auth

- Local UI: http://localhost:3000
- Staging App UI (Vercel): https://{{STAGING_FRONTEND_URL}}
- Production App UI (Vercel): https://{{FRONTEND_URL}}
- Production Marketing UI (Vercel): https://{{FRONTEND_URL}} (https://{{FRONTEND_URL}} redirects)
- Auth (Clerk primary): /sign-in and /sign-up; test admin vs member org roles
- Legacy NextAuth (deprecated): /login and /register
- Playwright base URL: set PLAYWRIGHT_TEST_BASE_URL to target staging/prod

---

## 1. Backend Testing (pytest)

### Basic Test

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
```

### Fixtures

```python
@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def test_user(db_session):
    user = User(email="test@example.com")
    db_session.add(user)
    db_session.commit()
    return user

def test_get_user(test_user):
    response = client.get(f"/users/{test_user.id}")
    assert response.json()["email"] == "test@example.com"
```

### Async Tests

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users/1")
    assert response.status_code == 200
```

### Database Test Isolation

```python
@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()  # Rollback after each test
    connection.close()
```

### Mocking External APIs

```python
from unittest.mock import patch, MagicMock

@patch('app.services.external_api.fetch_data')
def test_external_api_call(mock_fetch):
    mock_fetch.return_value = {"data": "mocked"}

    response = client.get("/external-data")
    assert response.json() == {"data": "mocked"}
    mock_fetch.assert_called_once()
```

### Parametrized Tests

```python
@pytest.mark.parametrize("email,expected_valid", [
    ("test@example.com", True),
    ("invalid-email", False),
    ("@example.com", False),
])
def test_email_validation(email, expected_valid):
    is_valid = validate_email(email)
    assert is_valid == expected_valid
```

---

## 2. E2E Testing (Playwright)

### Basic Test

```python
from playwright.sync_api import sync_playwright

def test_user_can_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto('http://localhost:3000/sign-in')
        page.fill('[name="email"]', 'user@example.com')
        page.fill('[name="password"]', 'password123')
        page.click('button[type="submit"]')

        page.wait_for_url('**/dashboard**')
        assert 'Welcome' in page.locator('h1').text_content()

        browser.close()
```

### Page Object Model

```python
class LoginPage:
    def __init__(self, page):
        self.page = page

    def goto(self):
        self.page.goto('/sign-in')

    def login(self, email: str, password: str):
        self.page.fill('[name="email"]', email)
        self.page.fill('[name="password"]', password)
        self.page.click('button[type="submit"]')

    def is_logged_in(self) -> bool:
        return '/dashboard' in self.page.url

# Usage in test
def test_login_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        login_page = LoginPage(page)
        login_page.goto()
        login_page.login('user@example.com', 'password123')

        assert login_page.is_logged_in()
        browser.close()
```

### Visual Regression

```python
def test_homepage_looks_correct():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('http://localhost:3000')
        page.wait_for_load_state('networkidle')

        # Take screenshot for comparison
        page.screenshot(path='screenshots/homepage.png')

        # Compare with baseline (using external tool like pixelmatch)
        # Or use pytest-playwright's built-in comparison
        browser.close()
```

### Authenticated Fixture Pattern

```python
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture
def authenticated_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Perform login
        page.goto('/sign-in')
        page.fill('[name="email"]', 'user@example.com')
        page.fill('[name="password"]', 'password123')
        page.click('button[type="submit"]')
        page.wait_for_url('**/dashboard**')

        yield page
        browser.close()

def test_dashboard_shows_data(authenticated_page):
    assert authenticated_page.locator('h1').text_content() == 'Dashboard'
```

---

## 3. Performance Testing

### Lighthouse CI

```bash
# Install
npm install -D @lhci/cli

# Run lighthouse
lhci autorun
```

```javascript
// lighthouserc.js
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000'],
      numberOfRuns: 3,
    },
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
      },
    },
  },
}
```

### Core Web Vitals (Python)

```python
def test_page_meets_core_web_vitals():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('http://localhost:3000')

        # Measure Core Web Vitals via JS
        metrics = page.evaluate('''() => {
            return new Promise((resolve) => {
                const results = {};

                new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (entry.entryType === 'largest-contentful-paint') {
                            results.lcp = entry.startTime;
                        }
                        if (entry.entryType === 'layout-shift' && !entry.hadRecentInput) {
                            results.cls = (results.cls || 0) + entry.value;
                        }
                    }
                    if (results.lcp) resolve(results);
                }).observe({ entryTypes: ['largest-contentful-paint', 'layout-shift'] });

                // Timeout fallback
                setTimeout(() => resolve(results), 5000);
            });
        }''')

        # Good LCP < 2.5s, Good CLS < 0.1
        assert metrics.get('lcp', 0) < 2500, f"LCP too slow: {metrics['lcp']}ms"
        assert metrics.get('cls', 0) < 0.1, f"CLS too high: {metrics['cls']}"

        browser.close()
```

### Performance Budget

```json
// budget.json
[
  {
    "path": "/*",
    "resourceSizes": [
      { "resourceType": "script", "budget": 300 },
      { "resourceType": "total", "budget": 500 }
    ]
  }
]
```

---

## 4. Local Webapp Automation

**Helper Scripts Available**:
- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)

**Always run scripts with `--help` first** to see usage. DO NOT read the source until you try running the script first.

### Decision Tree: Choosing Your Approach

```
User task --> Is it static HTML?
    |-- Yes --> Read HTML file directly to identify selectors
    |           |-- Success --> Write Playwright script using selectors
    |           +-- Fails/Incomplete --> Treat as dynamic (below)
    |
    +-- No (dynamic webapp) --> Is the server already running?
        |-- No --> Run: python scripts/with_server.py --help
        |          Then use the helper + write simplified Playwright script
        |
        +-- Yes --> Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

### Using with_server.py

**Single server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple servers (e.g., backend + frontend):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

### Automation Script Template

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')  # CRITICAL: Wait for JS

    # ... your automation logic

    browser.close()
```

### Reconnaissance-Then-Action Pattern

1. **Inspect rendered DOM**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   buttons = page.locator('button').all()
   ```

2. **Identify selectors** from inspection results

3. **Execute actions** using discovered selectors

### Common Pitfall

- **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
- **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

### Best Practices

- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`

---

## Reference Files

- **examples/** - Common patterns:
  - `element_discovery.py` - Discovering buttons, links, and inputs on a page
  - `static_html_automation.py` - Using file:// URLs for local HTML
  - `console_logging.py` - Capturing console logs during automation
