import logging
from pythonjsonlogger import jsonlogger
import sys

class HealthCheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/health") == -1
    
class TaskNameFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        if hasattr(record, 'taskName'):
            del record.taskName
        return True

logger = logging.getLogger()

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(message)s",
    datefmt="%d/%m/%y - %H:%M:%S"))
stream_handler.addFilter(TaskNameFilter())
stream_handler.addFilter(HealthCheckFilter())

logger.handlers = [stream_handler]

logger.setLevel(logging.INFO)

