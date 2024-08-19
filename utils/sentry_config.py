import functools
import os
import sentry_sdk
from dotenv import load_dotenv
from typing import Callable, Any

# Load environment variables from a .env file
load_dotenv()

# Get the Sentry DSN (Data Source Name) from environment variables
sentry_dsn: str = os.getenv('SENTRY_DSN')

# Initialize Sentry with the DSN and a 100% traces sample rate
sentry_sdk.init(
    dsn=sentry_dsn,
    traces_sample_rate=1.0
)


def sentry_exception_handler(func: Callable) -> Callable:
    """
    Decorator to capture exceptions with Sentry.

    If the decorated function raises an exception, the exception is sent to Sentry
    and then re-raised.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise
    return wrapper
