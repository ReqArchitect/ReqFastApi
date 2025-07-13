# Import enhanced modules
from .enhanced_main import app, startup_event, shutdown_event

# Re-export the app for compatibility
__all__ = ['app'] 