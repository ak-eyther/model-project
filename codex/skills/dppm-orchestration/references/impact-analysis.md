# Impact analysis guidance

Use this when listing file impact and drawing ASCII diagrams.

## File impact checklist
- UI: pages, layouts, components, styles
- API: route handlers, schemas, validators
- Data: models, migrations, queries
- Infra: configs, env, pipelines
- Tests: unit, integration, e2e

## ASCII diagram rules
- Keep to ASCII characters only.
- Show components and data flow with arrows.
- Include file or directory labels next to the nodes.

## ASCII diagram examples
```
[UI] --> [API] --> [DB]
 |         |
 v         v
app/     backend/app/
```

```
[Sidebar] ---> [Chat Page] ---> [Composer]
   |               |              |
components/      app/           components/
```
