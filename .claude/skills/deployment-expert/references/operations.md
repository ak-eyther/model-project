# Reference: Best Practices and Quick Commands

## Table of Contents
- Best Practices
  - Pre-Deployment Checklist
  - Health Checks
- Quick Reference Commands

## Best Practices

### Pre-Deployment Checklist

```bash
# 1. Test build locally
npm run build

# 2. Test with Railway/Vercel environment variables
railway run npm start
# or
vercel dev

# 3. Verify Dockerfile (if using)
docker build -t test-app .
docker run -p 3000:3000 test-app

# 4. Check environment variables are set
railway variables
# or
vercel env pull

# 5. Ensure database migrations are handled
# Add to railway.json or use pre-deploy script
```

### Health Checks

```javascript
// Express.js health check
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'healthy', timestamp: new Date() });
});

// With database check
app.get('/health', async (req, res) => {
  try {
    await db.query('SELECT 1');
    res.status(200).json({ status: 'healthy', database: 'connected' });
  } catch (error) {
    res.status(503).json({ status: 'unhealthy', error: error.message });
  }
});
```

---

## Quick Reference Commands

**Vercel:**
```bash
vercel                      # Deploy to preview
vercel --prod              # Deploy to production
vercel env pull            # Pull environment variables
vercel logs                # View logs (in dashboard)
vercel dev                 # Local development server
```

**Railway:**
```bash
railway up                 # Deploy
railway logs -f            # Follow logs
railway ssh                # SSH into service
railway variables          # List variables
railway status             # Check deployment status
```
