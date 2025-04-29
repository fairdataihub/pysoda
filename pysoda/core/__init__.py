import logging

from .permissions import has_edit_permissions



# Create a logger for the package
logger = logging.getLogger(__name__)
# Optional: Provide a default configuration if no handlers are set
logger.setLevel(logging.WARNING)