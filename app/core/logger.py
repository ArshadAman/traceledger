import json
import logging


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "service": record.name,
        }
        # include extras
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        for key, value in record.__dict__.items():
            if key not in (
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "exc_info",
                "exc_text",
                "stack_info",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
                "name",
            ):
                log_record[key] = value
        return json.dumps(log_record)


# create logger instance
logger = logging.getLogger("traceledger")

# set minimum level (ingore debug logs in production if needed)
logger.setLevel(logging.INFO)
logger.propagate = False
# create console handler (prints logs to terminal)
console_handler = logging.StreamHandler()

# define log format
# formatter = logging.Formatter(
#     "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
# )
#
formatter = JsonFormatter()
console_handler.setFormatter(formatter)

# add handler to logger
logger.addHandler(console_handler)
