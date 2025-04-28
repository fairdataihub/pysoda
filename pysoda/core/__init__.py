import logging

from .permissions import has_edit_permissions



# Create a logger for the package
logger = logging.getLogger(__name__)

# Optional: Provide a default configuration if no handlers are set
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)