# PRODUCTION DEPLOYMENT & INFRASTRUCTURE GUIDE
## Universal Multi-Company Valuation & DCF Engine

---

## 1. Local Production Deployment (Uvicorn / FastAPI)

```bash
# 1. Install dependencies
pip install -r Finance_FP&A_Portfolio/shared/requirements.txt
pip install fastapi uvicorn pydantic pydantic-settings sqlalchemy scipy python-multipart httpx

# 2. Run the production server
python run_server.py
```
- Web Portal: `http://localhost:8000/app`
- API Documentation: `http://localhost:8000/docs`
- Health Endpoint: `http://localhost:8000/health`

---

## 2. Docker Container Deployment

```bash
# Build the production container
docker build -t universal-dcf-engine:latest .

# Run container with persistent data volume
docker run -d -p 8000:8000 --name dcf-engine universal-dcf-engine:latest

# Or using docker-compose
docker-compose up -d
```

---

## 3. Cloud Deployment (Render / Railway / AWS ECS)
- **Runtime**: Python 3.12
- **Build Command**: `pip install -r Finance_FP&A_Portfolio/shared/requirements.txt && pip install fastapi uvicorn pydantic pydantic-settings sqlalchemy scipy python-multipart`
- **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**:
  - `ENVIRONMENT=production`
  - `DEBUG=false`
  - `DATABASE_URL=sqlite:///./universal_dcf.db` (or PostgreSQL URI)
