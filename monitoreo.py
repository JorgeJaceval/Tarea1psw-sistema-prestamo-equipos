"""Logs locales y reporte opcional de errores a Sentry."""
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


LOG_DIR = Path(__file__).resolve().parent / "logs"
logger = logging.getLogger(__name__)


def configurar_monitoreo():
    LOG_DIR.mkdir(exist_ok=True)
    archivo = str(LOG_DIR / "sistema.log")
    raiz = logging.getLogger()
    raiz.setLevel(logging.INFO)
    if not any(getattr(handler, "baseFilename", None) == archivo for handler in raiz.handlers):
        handler = RotatingFileHandler(
            archivo, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
        )
        handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        ))
        raiz.addHandler(handler)

    dsn = os.getenv("SENTRY_DSN", "").strip()
    if not dsn:
        logger.info("Sentry desactivado: SENTRY_DSN no configurado")
        return None

    try:
        import sentry_sdk
        from sentry_sdk.integrations.logging import LoggingIntegration
    except ImportError:
        logger.warning("Sentry no disponible: instale las dependencias de requirements.txt")
        return None

    try:
        sentry_sdk.init(
            dsn=dsn,
            environment=os.getenv("SENTRY_ENVIRONMENT", "desarrollo"),
            default_integrations=False,
            integrations=[LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)],
            send_default_pii=False,
            # Las variables y el contexto de código pueden contener credenciales.
            include_local_variables=False,
            include_source_context=False,
        )
    except (ValueError, TypeError):
        logger.warning("Sentry no se pudo iniciar: revise SENTRY_DSN y SENTRY_ENVIRONMENT")
        return None

    logger.info("Sentry activado")
    return sentry_sdk
