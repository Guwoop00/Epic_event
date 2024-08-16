import functools
import os
import sentry_sdk
from dotenv import load_dotenv

load_dotenv()

sentry_dsn = os.getenv('SENTRY_DSN')

sentry_sdk.init(
    dsn=sentry_dsn,
    traces_sample_rate=1.0
)


def sentry_exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise
    return wrapper
