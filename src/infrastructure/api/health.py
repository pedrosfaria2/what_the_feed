from fastapi import APIRouter, status
import platform
import sys
import psutil
import time
from datetime import datetime

from src.infrastructure.config.settings import settings
from src.infrastructure.schemas.health import (
    HealthResponse,
    PythonInfo,
    SystemInfo,
    MemoryInfo,
)


class HealthAPI:
    def __init__(self, app):
        self.router = APIRouter()
        self.start_time = time.time()
        self._configure_routes()
        app.include_router(self.router)

    def _configure_routes(self):
        @self.router.get(
            "/health",
            response_model=HealthResponse,
            status_code=status.HTTP_200_OK,
            tags=["Health"],
            summary="Check service health",
            description="Returns detailed health information about the service",
        )
        async def health_check():
            return HealthResponse(
                status="healthy",
                environment=settings.ENVIRONMENT,
                version=settings.APP_VERSION,
                timestamp=datetime.utcnow().isoformat(),
                uptime=time.time() - self.start_time,
                python_info=PythonInfo(
                    version=str(sys.version),
                    implementation=str(platform.python_implementation()),
                    compiler=str(platform.python_compiler()),
                ),
                system_info=SystemInfo(
                    platform=str(platform.platform()),
                    architecture=str(platform.machine()),
                    processor=str(platform.processor()) or "Unknown",
                    cpu_count=str(psutil.cpu_count()),
                    cpu_usage=str(psutil.cpu_percent(interval=0.1)),
                ),
                memory_info=MemoryInfo(
                    total=int(psutil.virtual_memory().total),
                    available=int(psutil.virtual_memory().available),
                    user_percent=float(psutil.virtual_memory().percent),
                ),
            )
