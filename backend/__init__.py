__version__ = "0.0.0"

from backend.functions import get_env_var
from backend.pages import create_pages
from backend.api.http import create_http_api
from backend.api.websocket import create_websocket_api