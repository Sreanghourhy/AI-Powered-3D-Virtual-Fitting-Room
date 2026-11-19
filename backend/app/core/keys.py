"""Print a new random encryption key: ``python -m app.core.keys``."""

import base64
import secrets


def new_key() -> str:
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()


if __name__ == "__main__":
    print(new_key())
