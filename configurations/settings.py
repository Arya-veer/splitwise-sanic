import os
import configurations.keyconfig as kc

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
AUTH_SECRET = kc.AUTH_SECRET
PASSWORD_SECRET = kc.PASSWORD_SECRET
