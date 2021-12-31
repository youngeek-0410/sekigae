from pydantic import BaseModel


class LogConfig(BaseModel):
    """
    CRITICAL > ERROR > WARNING > INFO > DEBUG > NOSET
    """

    LOG_LEVEL: str = "DEBUG"
    LOG_HANDLER_LEVEL_NULL: str = "DEBUG"
    LOG_HANDLER_LEVEL_CONSOLE: str = "DEBUG"
    LOG_HANDLER_LEVEL_FILE: str = "DEBUG"
    LOG_FILE_MAX_BYTES: int = 1024 * 1024
    LOG_FILE_BACKUP_COUNT: int = 5
    LOG_HANDLER_FILE_PATH: str = "/fastapi.log"
    LOG_LOGGER_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d %(message)s"
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    }
    filters = {}
    handlers = {
        "null": {
            "level": LOG_HANDLER_LEVEL_NULL,
            "class": "logging.NullHandler",
        },
        "console": {
            "level": LOG_HANDLER_LEVEL_CONSOLE,
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "verbose",
        },
        "file": {
            "level": LOG_HANDLER_LEVEL_FILE,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_HANDLER_FILE_PATH,
            "formatter": "verbose",
            "maxBytes": LOG_FILE_MAX_BYTES,
            "backupCount": LOG_FILE_BACKUP_COUNT,
        },
    }
    loggers = {
        "gunicorn": {
            "handlers": ["null"],
            "propagate": True,
            "level": "WARNING",
        },
        "uvicorn": {
            "handlers": ["console", "file"],
            "propagate": True,
            "level": LOG_LOGGER_LEVEL,
        },
        "uvicorn.access": {
            "handlers": ["null"],
            "propagate": True,
            "level": "WARNING",
        },
        "sqlalchemy": {
            "handlers": ["null"],
            "propagate": True,
            "level": "WARNING",
        },
        "app": {
            "handlers": ["console", "file"],
            "level": LOG_LOGGER_LEVEL,
        },
    }
