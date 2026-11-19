"""Shared test setup: every test run uses a throwaway data directory and key."""

import os
import tempfile

# Must be set before the app is imported.
_TMP = tempfile.mkdtemp(prefix="fr-test-")
os.environ["FR_ENVIRONMENT"] = "test"
os.environ["FR_DATA_DIR"] = _TMP
os.environ["FR_ENCRYPTION_KEY"] = "MDEyMzQ1Njc4OWFiY2RlZjAxMjM0NTY3ODlhYmNkZWY="
os.environ.pop("FR_DATABASE_URL", None)
