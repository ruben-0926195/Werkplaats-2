# extensions.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Create Limiter instance (not yet bound to app)
limiter = Limiter(key_func=get_remote_address)
