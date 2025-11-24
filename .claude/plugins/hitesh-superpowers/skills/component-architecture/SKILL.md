---
name: component-architecture
description: Component design patterns including composition, render props, compound components, and design systems. Use for reusable component architecture.
allowed-tools:
  - Read
  - Write
  - Edit
---

# Component Architecture Patterns

## Composition Pattern

```typescript
function Card({ children }) {
  return <div className="card">{children}</div>
}

function CardHeader({ children }) {
  return <div className="card-header">{children}</div>
}

function CardBody({ children }) {
  return <div className="card-body">{children}</div>
}

// Usage
<Card>
  <CardHeader>Title</CardHeader>
  <CardBody>Content</CardBody>
</Card>
```

## Compound Components

```typescript
const Tabs = ({ children }) => {
  const [activeTab, setActiveTab] = useState(0)
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabsContext.Provider>
  )
}

Tabs.List = ({ children }) => <div className="tabs-list">{children}</div>
Tabs.Tab = ({ index, children }) => {
  const { activeTab, setActiveTab } = useTabsContext()
  return (
    <button
      className={activeTab === index ? 'active' : ''}
      onClick={() => setActiveTab(index)}
    >
      {children}
    </button>
  )
}
Tabs.Panel = ({ index, children }) => {
  const { activeTab } = useTabsContext()
  return activeTab === index ? <div>{children}</div> : null
}

// Usage
<Tabs>
  <Tabs.List>
    <Tabs.Tab index={0}>Tab 1</Tabs.Tab>
    <Tabs.Tab index={1}>Tab 2</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel index={0}>Content 1</Tabs.Panel>
  <Tabs.Panel index={1}>Content 2</Tabs.Panel>
</Tabs>
```

## Render Props

```typescript
function DataFetcher({ url, render }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(data => {
        setData(data)
        setLoading(false)
      })
  }, [url])

  return render({ data, loading })
}

// Usage
<DataFetcher
  url="/api/users"
  render={({ data, loading }) => 
    loading ? <div>Loading...</div> : <UserList users={data} />
  }
/>
```

## Headless Components

```typescript
function useDropdown() {
  const [isOpen, setIsOpen] = useState(false)
  const toggle = () => setIsOpen(!isOpen)
  const close = () => setIsOpen(false)

  return { isOpen, toggle, close }
}

// Usage - completely custom UI
function MyDropdown() {
  const { isOpen, toggle, close } = useDropdown()

  return (
    <div>
      <button onClick={toggle}>Toggle</button>
      {isOpen && (
        <div onClick={close}>
          Custom dropdown content
        </div>
      )}
    </div>
  )
}
```
