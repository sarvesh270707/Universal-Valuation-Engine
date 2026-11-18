import uvicorn
import os

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "127.0.0.1")
    print(f"Starting Universal Multi-Company Valuation & DCF Engine on http://{host}:{port}")
    print(f"Interactive Web Portal: http://{host}:{port}/app")
    print(f"Swagger API Documentation: http://{host}:{port}/docs")
    uvicorn.run("backend.app.main:app", host=host, port=port, reload=False, log_level="info")
