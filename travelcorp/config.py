import os

BLAZE_DEMO_BASE = "https://blazedemo.com"

# Override if ReqRes routes your project to another host (see their docs).
REQRES_USERS_URL = os.environ.get(
    "REQRES_USERS_URL",
    "https://reqres.in/api/users",
).rstrip("/")
