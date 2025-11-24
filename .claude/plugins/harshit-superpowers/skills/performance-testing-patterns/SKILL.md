---
name: performance-testing-patterns
description: Performance testing using Chrome DevTools, Lighthouse, and Core Web Vitals monitoring. Use for performance profiling or optimization validation.
allowed-tools:
  - Read
  - Bash
---

# Performance Testing Patterns

## Lighthouse CI

```bash
# Install
npm install -D @lhci/cli

# Run lighthouse
lhci autorun

# lighthouse.config.js
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

## Core Web Vitals

```typescript
// Measure CWV in tests
test('page meets Core Web Vitals', async ({ page }) => {
  await page.goto('/')

  const metrics = await page.evaluate(() => {
    return new Promise((resolve) => {
      new PerformanceObserver((list) => {
        const entries = list.getEntries()
        const lcp = entries.find(e => e.entryType === 'largest-contentful-paint')
        const fid = entries.find(e => e.entryType === 'first-input')
        const cls = entries.find(e => e.entryType === 'layout-shift')
        
        resolve({ lcp: lcp?.startTime, fid: fid?.processingStart, cls: cls?.value })
      }).observe({ entryTypes: ['largest-contentful-paint', 'first-input', 'layout-shift'] })
    })
  })

  expect(metrics.lcp).toBeLessThan(2500) // Good LCP < 2.5s
})
```

## Bundle Analysis

```bash
# Next.js bundle analyzer
npm install -D @next/bundle-analyzer

# next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer({
  // config
})

# Run analysis
ANALYZE=true npm run build
```

## Performance Budget

```javascript
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
