from fastapi import Request
from logger import logger
import time

async def log_middleware(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    process_time = time.time() - start

    body = await response.body()
    data = {
        "request": {
            "ip_address": request.client.host,
            "request_path": request.url.path,
            "request_body": body,
            "method": request.method,
            "status_code": response.status_code,
            "process_time": f"{process_time:.4f}"
        }
    }

    logger.info("custom json logger",extra=data)

    return response