import logging

from elasticsearch import Elasticsearch

from core.config import settings

# connect to ES
es = Elasticsearch(settings.elastic_search_host)


class ElasticsearchHandler(logging.Handler):
    def emit(self, record):
        """
        Called every time logger.info()/error() runs
        """

        try:
            # convert log record → dict
            log_data = {
                "time": self.format(record),
                "level": record.levelname,
                "message": record.getMessage(),
                "service": record.name,
            }

            # include extras
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
                    log_data[key] = value

            # send to ES
            es.index(index="logs", document=log_data)

        except Exception:
            pass  # NEVER break app because of logging
