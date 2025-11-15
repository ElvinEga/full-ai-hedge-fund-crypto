# Deployment Guide

## Production Deployment for AI Hedge Fund Crypto

This guide covers deploying your full-stack application to production environments.

## Prerequisites

- GitHub account (for code hosting)
- Domain name (optional but recommended)
- API keys for:
  - Binance
  - OpenAI/Anthropic/other LLM providers

## Architecture Overview

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Vercel    │ ──────► │   Railway    │ ──────► │   Binance   │
│  (Frontend) │         │  (Backend)   │         │     API     │
└─────────────┘         └──────────────┘         └─────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │  PostgreSQL  │
                        │  (Database)  │
                        └──────────────┘
```

## Part 1: Backend Deployment (Railway)

### Step 1: Prepare Backend for Production

1. **Create Dockerfile** (already exists in root):
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv pip install -e . --system

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Create .dockerignore**:
```
.venv/
__pycache__/
*.pyc
.env
.git/
frontend/
*.db
cache/
imgs/
```

### Step 2: Deploy to Railway

1. **Install Railway CLI**:
```bash
npm install -g @railway/cli
```

2. **Login to Railway**:
```bash
railway login
```

3. **Initialize Project**:
```bash
railway init
```

4. **Set Environment Variables**:
```bash
railway variables set BINANCE_API_KEY=your_key
railway variables set BINANCE_API_SECRET=your_secret
railway variables set OPENAI_API_KEY=your_key
railway variables set ANTHROPIC_API_KEY=your_key
# Add other API keys as needed
```

5. **Deploy**:
```bash
railway up
```

6. **Get Your Backend URL**:
```bash
railway domain
# Example output: https://your-app.railway.app
```

### Alternative: Deploy to Fly.io

1. **Install Fly CLI**:
```bash
curl -L https://fly.io/install.sh | sh
```

2. **Login**:
```bash
fly auth login
```

3. **Launch App**:
```bash
fly launch
```

4. **Set Secrets**:
```bash
fly secrets set BINANCE_API_KEY=your_key
fly secrets set BINANCE_API_SECRET=your_secret
fly secrets set OPENAI_API_KEY=your_key
```

5. **Deploy**:
```bash
fly deploy
```

## Part 2: Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

1. **Update Environment Variable**:
Create `frontend/.env.production`:
```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app/api
```

2. **Test Production Build Locally**:
```bash
cd frontend
bun run build
bun run start
```

### Step 2: Deploy to Vercel

#### Option A: Via Vercel Dashboard (Recommended)

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `bun run build`
   - **Output Directory**: `.next`
5. Add Environment Variable:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://your-backend.railway.app/api`
6. Click "Deploy"

#### Option B: Via Vercel CLI

1. **Install Vercel CLI**:
```bash
npm install -g vercel
```

2. **Login**:
```bash
vercel login
```

3. **Deploy**:
```bash
cd frontend
vercel --prod
```

4. **Set Environment Variable**:
```bash
vercel env add NEXT_PUBLIC_API_URL production
# Enter: https://your-backend.railway.app/api
```

### Alternative: Deploy to Netlify

1. **Create netlify.toml** in frontend directory:
```toml
[build]
  command = "bun run build"
  publish = ".next"

[[plugins]]
  package = "@netlify/plugin-nextjs"
```

2. **Deploy via Netlify CLI**:
```bash
npm install -g netlify-cli
netlify login
netlify deploy --prod
```

## Part 3: Database Migration (Optional)

### Migrate from SQLite to PostgreSQL

1. **Add PostgreSQL to Railway**:
```bash
railway add postgresql
```

2. **Update database.py**:
```python
# src/database.py
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./backtests.db"
).replace("postgres://", "postgresql://")  # Railway fix

engine = create_engine(DATABASE_URL)
```

3. **Install psycopg2**:
```bash
uv pip install psycopg2-binary
```

4. **Redeploy**:
```bash
railway up
```

## Part 4: Domain Configuration

### Custom Domain for Backend

**Railway**:
1. Go to Railway dashboard
2. Select your project
3. Click "Settings" → "Domains"
4. Add custom domain: `api.yourdomain.com`
5. Add CNAME record in your DNS:
   - Name: `api`
   - Value: `your-app.railway.app`

**Fly.io**:
```bash
fly certs add api.yourdomain.com
```

### Custom Domain for Frontend

**Vercel**:
1. Go to Vercel dashboard
2. Select your project
3. Click "Settings" → "Domains"
4. Add domain: `yourdomain.com`
5. Follow DNS configuration instructions

## Part 5: Monitoring & Logging

### Backend Monitoring

1. **Add Logging**:
```python
# api.py
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response
```

2. **Railway Logs**:
```bash
railway logs
```

3. **Fly.io Logs**:
```bash
fly logs
```

### Frontend Monitoring

**Vercel Analytics** (Built-in):
- Automatically enabled
- View in Vercel dashboard

**Add Sentry** (Optional):
```bash
cd frontend
bun add @sentry/nextjs
```

## Part 6: CI/CD Setup

### GitHub Actions for Backend

Create `.github/workflows/deploy-backend.yml`:
```yaml
name: Deploy Backend

on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'api.py'
      - 'pyproject.toml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        run: |
          npm install -g @railway/cli
          railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

### Automatic Frontend Deployment

Vercel automatically deploys on every push to main branch.

## Part 7: Security Checklist

- [ ] All API keys in environment variables
- [ ] CORS configured for production domain
- [ ] HTTPS enabled (automatic on Vercel/Railway)
- [ ] Database connection encrypted
- [ ] Rate limiting implemented (optional)
- [ ] Input validation on all endpoints
- [ ] Error messages don't expose sensitive info
- [ ] Health check endpoint working
- [ ] Logs don't contain secrets

## Part 8: Performance Optimization

### Backend

1. **Enable Gzip Compression**:
```python
# api.py
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

2. **Add Caching** (Optional):
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
```

### Frontend

1. **Already Optimized**:
   - Next.js automatic code splitting
   - Image optimization
   - Static generation where possible

2. **Add CDN** (Automatic with Vercel)

## Part 9: Backup Strategy

### Database Backups

**Railway**:
- Automatic daily backups
- Manual backup:
```bash
railway run pg_dump > backup.sql
```

**Fly.io with PostgreSQL**:
```bash
fly postgres backup create
```

### Code Backups

- GitHub repository (primary)
- Regular commits
- Tagged releases

## Part 10: Monitoring URLs

After deployment, monitor these endpoints:

- **Frontend**: `https://yourdomain.com`
- **Backend API**: `https://api.yourdomain.com`
- **Health Check**: `https://api.yourdomain.com/api/health`
- **API Docs**: `https://api.yourdomain.com/docs`

## Estimated Costs

### Free Tier (Development)

- **Vercel**: Free for personal projects
- **Railway**: $5/month credit (enough for small apps)
- **Fly.io**: Free tier available

### Production (Recommended)

- **Vercel Pro**: $20/month
- **Railway**: ~$10-20/month (usage-based)
- **Domain**: ~$12/year
- **Total**: ~$30-40/month

## Troubleshooting

### Backend Won't Start

1. Check logs:
```bash
railway logs
```

2. Verify environment variables:
```bash
railway variables
```

3. Test locally with production settings:
```bash
export DATABASE_URL=your_prod_url
uvicorn api:app
```

### Frontend Can't Connect to Backend

1. Check CORS settings in `api.py`
2. Verify `NEXT_PUBLIC_API_URL` is correct
3. Check browser console for errors
4. Test API directly: `curl https://api.yourdomain.com/api/health`

### Database Connection Issues

1. Check DATABASE_URL format
2. Verify PostgreSQL is running
3. Check connection limits
4. Review database logs

## Rollback Procedure

### Backend

**Railway**:
```bash
railway rollback
```

**Fly.io**:
```bash
fly releases
fly deploy --image <previous-version>
```

### Frontend

**Vercel**:
1. Go to Deployments
2. Find previous deployment
3. Click "Promote to Production"

## Maintenance

### Regular Tasks

- [ ] Monitor error logs weekly
- [ ] Review performance metrics
- [ ] Update dependencies monthly
- [ ] Backup database weekly
- [ ] Review and rotate API keys quarterly
- [ ] Check disk usage
- [ ] Monitor costs

### Updates

1. **Backend Updates**:
```bash
git pull
railway up
```

2. **Frontend Updates**:
```bash
git push  # Vercel auto-deploys
```

## Support Resources

- **Railway**: https://docs.railway.app
- **Vercel**: https://vercel.com/docs
- **Fly.io**: https://fly.io/docs
- **FastAPI**: https://fastapi.tiangolo.com
- **Next.js**: https://nextjs.org/docs

## Conclusion

Your application is now deployed and accessible worldwide! 🚀

Remember to:
- Monitor your application regularly
- Keep dependencies updated
- Review logs for errors
- Scale resources as needed
- Maintain backups

For production trading, consider:
- Adding authentication
- Implementing rate limiting
- Setting up alerts
- Adding more comprehensive logging
- Implementing proper error tracking
