---
name: tailwind-advanced-patterns
description: Advanced Tailwind CSS patterns including custom themes, responsive design, dark mode, animations, and component variants. Use for complex styling or design system implementation.
allowed-tools:
  - Read
  - Write
  - Edit
---

# Tailwind Advanced Patterns

## Custom Theme

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#0ea5e9',
          900: '#0c4a6e',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui'],
      },
    },
  },
}
```

## Dark Mode

```typescript
// app/layout.tsx
export default function Layout({ children }) {
  return (
    <html className="dark">
      <body className="bg-white dark:bg-gray-900">
        {children}
      </body>
    </html>
  )
}

// Component with dark mode
function Card() {
  return (
    <div className="bg-white dark:bg-gray-800 
                    text-gray-900 dark:text-white">
      Content
    </div>
  )
}
```

## Responsive Design

```typescript
function ResponsiveGrid() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {/* Cards */}
    </div>
  )
}
```

## Custom Animations

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
    },
  },
}
```

## Component Variants with clsx

```typescript
import clsx from 'clsx'

interface ButtonProps {
  variant: 'primary' | 'secondary'
  size: 'sm' | 'md' | 'lg'
}

function Button({ variant, size }: ButtonProps) {
  return (
    <button
      className={clsx(
        'rounded font-medium',
        {
          'bg-blue-500 text-white': variant === 'primary',
          'bg-gray-200 text-gray-900': variant === 'secondary',
          'px-2 py-1 text-sm': size === 'sm',
          'px-4 py-2 text-base': size === 'md',
          'px-6 py-3 text-lg': size === 'lg',
        }
      )}
    >
      Click me
    </button>
  )
}
```
