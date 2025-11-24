---
name: react-production-patterns
description: Build production-ready React applications with performance optimization, code splitting, state management, and accessibility. Use for React components requiring optimization or complex state patterns.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# React Production Patterns

## Performance Optimization

```typescript
import { memo, useMemo, useCallback } from 'react'

// Memoized component
const ExpensiveComponent = memo(({ data }) => {
  const processedData = useMemo(() => {
    return data.map(item => expensiveOperation(item))
  }, [data])

  const handleClick = useCallback(() => {
    // Handler logic
  }, [])

  return <div onClick={handleClick}>{processedData}</div>
})
```

## Code Splitting

```typescript
import { lazy, Suspense } from 'react'

const HeavyComponent = lazy(() => import('./HeavyComponent'))

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </Suspense>
  )
}
```

## State Management (Zustand)

```typescript
import { create } from 'zustand'

interface Store {
  count: number
  increment: () => void
}

const useStore = create<Store>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}))

function Counter() {
  const { count, increment } = useStore()
  return <button onClick={increment}>{count}</button>
}
```

## Accessibility (ARIA)

```typescript
function AccessibleButton() {
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <button
      aria-expanded={isExpanded}
      aria-label="Toggle menu"
      onClick={() => setIsExpanded(!isExpanded)}
    >
      Menu
    </button>
  )
}
```

## Custom Hooks

```typescript
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => clearTimeout(handler)
  }, [value, delay])

  return debouncedValue
}
```
