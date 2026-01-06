# Reference: Cross-Platform Deployment Strategies

## Table of Contents
- Cross-Platform Deployment Strategies
  - 1. Deployment Decision Tree
  - 2. Hybrid Architecture: Vercel Frontend + Railway Backend

## Cross-Platform Deployment Strategies

### 1. Deployment Decision Tree

**When to use Vercel:**
- ✅ Next.js, React, Vue, Svelte applications
- ✅ Static sites and JAMstack
- ✅ Serverless functions (Edge/Node.js)
- ✅ Need global CDN with edge computing
- ✅ Preview deployments for every PR
- ❌ Long-running processes
- ❌ WebSocket servers
- ❌ Background workers

**When to use Railway:**
- ✅ Backend APIs (Node.js, Python, Go, etc.)
- ✅ Databases (Postgres, MongoDB, Redis)
- ✅ Full-stack applications
- ✅ Docker-based deployments
- ✅ Long-running processes
- ✅ WebSocket servers
- ✅ Cron jobs and workers
- ❌ Need extensive global edge network
- ❌ Require serverless at scale

### 2. Hybrid Architecture: Vercel Frontend + Railway Backend

**Common Setup:**
```
Frontend (Vercel) → API (Railway) → Database (Railway)
```

**Vercel Side Configuration:**
```json
// vercel.json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://your-backend.railway.app/api/:path*"
    }
  ],
  "env": {
    "RAILWAY_API_URL": "https://your-backend.railway.app"
  },
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        }
      ]
    }
  ]
}
```

**Railway Side Configuration:**
```javascript
// Express.js backend
const cors = require('cors');

app.use(cors({
  origin: [
    'https://your-frontend.vercel.app',
    'http://localhost:3000'  // for development
  ],
  credentials: true
}));

// Health check for Vercel to ping
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});
```
