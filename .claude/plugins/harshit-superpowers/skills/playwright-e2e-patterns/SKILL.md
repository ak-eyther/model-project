---
name: playwright-e2e-patterns
description: End-to-end testing with Playwright including page objects, fixtures, visual regression, and CI integration. Use for E2E test implementation or test architecture.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Playwright E2E Patterns

## Basic Test

```typescript
import { test, expect } from '@playwright/test'

test('user can login', async ({ page }) => {
  await page.goto('https://example.com/login')
  await page.fill('[name="email"]', 'user@example.com')
  await page.fill('[name="password"]', 'password123')
  await page.click('button[type="submit"]')
  
  await expect(page).toHaveURL(/dashboard/)
  await expect(page.locator('h1')).toContainText('Welcome')
})
```

## Page Object Model

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.page.fill('[name="email"]', email)
    await this.page.fill('[name="password"]', password)
    await this.page.click('button[type="submit"]')
  }

  async isLoggedIn() {
    return this.page.url().includes('/dashboard')
  }
}

// test
test('login flow', async ({ page }) => {
  const loginPage = new LoginPage(page)
  await loginPage.goto()
  await loginPage.login('user@example.com', 'password123')
  expect(await loginPage.isLoggedIn()).toBeTruthy()
})
```

## Fixtures

```typescript
import { test as base } from '@playwright/test'

type Fixtures = {
  authenticatedPage: Page
}

const test = base.extend<Fixtures>({
  authenticatedPage: async ({ page }, use) => {
    await page.goto('/login')
    await page.fill('[name="email"]', 'user@example.com')
    await page.fill('[name="password"]', 'password123')
    await page.click('button[type="submit"]')
    await use(page)
  },
})

test('authenticated user can view dashboard', async ({ authenticatedPage }) => {
  await expect(authenticatedPage.locator('h1')).toContainText('Dashboard')
})
```

## Visual Regression

```typescript
test('homepage looks correct', async ({ page }) => {
  await page.goto('/')
  await expect(page).toHaveScreenshot('homepage.png')
})
```

## Parallel Execution

```typescript
// playwright.config.ts
export default defineConfig({
  workers: process.env.CI ? 2 : undefined,
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
})
```
