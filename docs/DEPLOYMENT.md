## Option A: Frontend on Vercel (static) + Backend on Render/Railway/Fly.io

This approach keeps secrets off Vercel and runs the Python backend on a dedicated host.

### 1) Prepare the backend (Flask) on Render/Railway/Fly.io

- Repo: this repository (no `.env` committed; secrets set in the host dashboard).
- Python version: 3.9+.
- Start command:
```
PYTHONPATH=/app python3 frontend/app.py
```
- Env vars (set in the host):
  - EMAIL_USER, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT
  - OLLAMA_BASE_URL, OLLAMA_MODEL (or your OPENAI_* if using OpenAI)
  - PINECONE_API_KEY (optional)
  - GOOGLE_ADS_* (only if launching real campaigns)
  - Any other existing config you use in `.env`
- Expose port: 15000 (or map to 80/443 via the platform).

After deploy you will have a backend URL like `https://your-backend.onrender.com`.

### 2) Prepare the frontend on Vercel (static)

- Create a new Vercel project from this Git repo.
- Framework preset: “Other”.
- Public directory: `frontend/templates`.
- Build command: none (static).
- Output: leave empty.
- Add a file `.vercelignore` (already included) so Vercel won’t upload `.env`, logs, tests, etc.

### 3) Point the frontend to your backend

The app reads `API_BASE` from `window.API_BASE` or `localStorage.API_BASE`.

Options:
- Quick (no rebuild): open your deployed site in the browser console and run:
```
localStorage.setItem('API_BASE','https://your-backend.onrender.com');
location.reload();
```
- Permanent (recommended): add a small inline script in Vercel Settings → Analytics/Head (or via a wrapper index) that sets:
```
<script>window.API_BASE='https://your-backend.onrender.com';</script>
```

### 4) CORS (if required)

If your host blocks cross-origin calls, enable CORS on the backend to allow your Vercel domain (e.g., `https://your-frontend.vercel.app`). You can add `flask-cors` and allow that origin.

### 5) Secrets and safety checks

- No secrets in git: `.env`, backups and `google-ads.yaml` are ignored.
- Vercel only serves static frontend; secrets remain on backend host.

### 6) Smoke test

1. Load the frontend URL on Vercel.
2. Set `API_BASE` (step 3) if not already injected.
3. Ejecuta un análisis y verifica `/status/{request_id}`.
4. “Haz una prueba” debe funcionar sin lanzar Google Ads reales.
5. Para lanzar campañas reales, abre el modal, ingresa credenciales y verifica en tu cuenta.

# Deployment Guide

## Overview

This guide covers deploying the Marketing Agent system in both development and production environments.

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (for containerized deployment)
- PostgreSQL (for production)
- Redis (for production)
- Cloud provider account (AWS, Azure, or GCP) for production

## Development Deployment

### Local Development

1. **Clone the repository:**
```bash
git clone <repository-url>
cd marketingagent
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run the application:**
```bash
python frontend/app.py
```

### Docker Development

1. **Build development image:**
```bash
docker build --target development -t marketing-agent:dev .
```

2. **Run with Docker Compose:**
```bash
docker-compose -f docker-compose.dev.yml up
```

## Production Deployment

### Docker Production

1. **Build production image:**
```bash
docker build --target production -t marketing-agent:prod .
```

2. **Set up environment variables:**
```bash
# Create production environment file
cat > .env.production << EOF
SECRETS_MANAGER_TYPE=env
SECRETS_PREFIX=MARKETING_AGENT_
POSTGRES_PASSWORD=your_secure_password
REDIS_PASSWORD=your_redis_password
EOF
```

3. **Deploy with Docker Compose:**
```bash
docker-compose up -d
```

### Cloud Deployment

#### AWS Deployment

1. **Set up AWS credentials:**
```bash
aws configure
```

2. **Create secrets in AWS Secrets Manager:**
```bash
aws secretsmanager create-secret \
  --name "marketing-agent/pinecone-api-key" \
  --secret-string "your-pinecone-key"

aws secretsmanager create-secret \
  --name "marketing-agent/google-ads-credentials" \
  --secret-string '{"developer_token":"xxx","client_id":"xxx","client_secret":"xxx","refresh_token":"xxx","login_customer_id":"xxx"}'
```

3. **Deploy with ECS:**
```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name marketing-agent

# Deploy service
aws ecs create-service \
  --cluster marketing-agent \
  --service-name marketing-agent-service \
  --task-definition marketing-agent-task \
  --desired-count 2
```

#### Azure Deployment

1. **Set up Azure credentials:**
```bash
az login
```

2. **Create Key Vault:**
```bash
az keyvault create \
  --name marketing-agent-vault \
  --resource-group marketing-agent-rg \
  --location eastus
```

3. **Store secrets:**
```bash
az keyvault secret set \
  --vault-name marketing-agent-vault \
  --name pinecone-api-key \
  --value "your-pinecone-key"
```

4. **Deploy with Container Instances:**
```bash
az container create \
  --resource-group marketing-agent-rg \
  --name marketing-agent \
  --image marketing-agent:prod \
  --cpu 2 \
  --memory 4 \
  --environment-variables \
    SECRETS_MANAGER_TYPE=cloud \
    CLOUD_SECRETS_PROVIDER=azure \
    AZURE_KEY_VAULT_URL=https://marketing-agent-vault.vault.azure.net/
```

#### Google Cloud Deployment

1. **Set up gcloud:**
```bash
gcloud auth login
gcloud config set project your-project-id
```

2. **Create secrets:**
```bash
echo -n "your-pinecone-key" | gcloud secrets create pinecone-api-key --data-file=-
```

3. **Deploy with Cloud Run:**
```bash
gcloud run deploy marketing-agent \
  --image gcr.io/your-project/marketing-agent:prod \
  --platform managed \
  --region us-central1 \
  --set-env-vars SECRETS_MANAGER_TYPE=cloud,CLOUD_SECRETS_PROVIDER=gcp
```

## Environment Configuration

### Required Environment Variables

```bash
# Application
SECRETS_MANAGER_TYPE=local|env|cloud
SECRETS_PREFIX=MARKETING_AGENT_

# LLM Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# Database (Production)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=marketing_agent
POSTGRES_USER=marketing_agent
POSTGRES_PASSWORD=your_password

# Redis (Production)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# Cloud Secrets (Production)
CLOUD_SECRETS_PROVIDER=aws|azure|gcp
AWS_REGION=us-east-1
AZURE_KEY_VAULT_URL=https://your-vault.vault.azure.net/
GCP_PROJECT_ID=your-project-id
```

### Optional Environment Variables

```bash
# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Performance
MAX_WORKERS=4
REQUEST_TIMEOUT=120
CACHE_TTL=3600

# Security
CORS_ORIGINS=https://yourdomain.com
RATE_LIMIT=100
```

## Database Setup

### PostgreSQL

1. **Install PostgreSQL:**
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Windows
# Download from https://www.postgresql.org/download/windows/
```

2. **Create database:**
```sql
CREATE DATABASE marketing_agent;
CREATE USER marketing_agent WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE marketing_agent TO marketing_agent;
```

### Redis

1. **Install Redis:**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Windows
# Download from https://github.com/microsoftarchive/redis/releases
```

2. **Configure Redis:**
```bash
# Edit /etc/redis/redis.conf
requirepass your_redis_password
maxmemory 256mb
maxmemory-policy allkeys-lru
```

## Monitoring and Logging

### Application Logs

```bash
# View logs
docker-compose logs -f marketing-agent

# View specific service logs
docker-compose logs -f marketing-agent redis postgres
```

### Health Checks

```bash
# Check application health
curl http://localhost:8080/performance

# Check database connection
docker-compose exec postgres pg_isready

# Check Redis connection
docker-compose exec redis redis-cli ping
```

### Monitoring Setup

1. **Prometheus Configuration:**
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'marketing-agent'
    static_configs:
      - targets: ['marketing-agent:8080']
```

2. **Grafana Dashboard:**
```json
{
  "dashboard": {
    "title": "Marketing Agent Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      }
    ]
  }
}
```

## Security Considerations

### Secrets Management

1. **Never commit secrets to version control**
2. **Use environment variables or secret management services**
3. **Rotate secrets regularly**
4. **Use least privilege access**

### Network Security

1. **Use HTTPS in production**
2. **Configure firewall rules**
3. **Use VPC for cloud deployments**
4. **Enable DDoS protection**

### Application Security

1. **Input validation and sanitization**
2. **Rate limiting**
3. **CORS configuration**
4. **Security headers**

## Backup and Recovery

### Database Backup

```bash
# Create backup
pg_dump -h localhost -U marketing_agent marketing_agent > backup.sql

# Restore backup
psql -h localhost -U marketing_agent marketing_agent < backup.sql
```

### Application Backup

```bash
# Backup application data
tar -czf marketing-agent-backup.tar.gz outputs/ logs/ secrets.encrypted

# Restore application data
tar -xzf marketing-agent-backup.tar.gz
```

## Troubleshooting

### Common Issues

1. **Port conflicts:**
```bash
# Check port usage
netstat -tulpn | grep :8080
lsof -i :8080
```

2. **Memory issues:**
```bash
# Check memory usage
docker stats
free -h
```

3. **Database connection issues:**
```bash
# Test database connection
psql -h localhost -U marketing_agent -d marketing_agent -c "SELECT 1;"
```

### Log Analysis

```bash
# Search for errors
docker-compose logs marketing-agent | grep ERROR

# Monitor real-time logs
docker-compose logs -f --tail=100 marketing-agent
```

## Performance Optimization

### Application Tuning

1. **Worker processes:**
```bash
# Increase workers
gunicorn --workers 4 --worker-class gevent frontend.app:app
```

2. **Database optimization:**
```sql
-- Create indexes
CREATE INDEX idx_requests_timestamp ON requests(timestamp);
CREATE INDEX idx_requests_status ON requests(status);
```

3. **Caching:**
```python
# Configure Redis caching
CACHE_TYPE = 'redis'
CACHE_REDIS_URL = 'redis://localhost:6379/0'
```

## Scaling

### Horizontal Scaling

1. **Load balancer configuration:**
```nginx
upstream marketing_agent {
    server marketing-agent-1:8080;
    server marketing-agent-2:8080;
    server marketing-agent-3:8080;
}
```

2. **Auto-scaling:**
```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: marketing-agent-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: marketing-agent
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Maintenance

### Regular Tasks

1. **Database maintenance:**
```sql
-- Vacuum database
VACUUM ANALYZE;

-- Update statistics
ANALYZE;
```

2. **Log rotation:**
```bash
# Configure logrotate
cat > /etc/logrotate.d/marketing-agent << EOF
/var/log/marketing-agent/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
}
EOF
```

3. **Security updates:**
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update base images
docker pull python:3.11-slim
```
