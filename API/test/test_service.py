import os, sys

BASE_DIR = os.path.dirname(os.path.abspath("API"))
sys.path.extend([BASE_DIR])

import pytest
import json
import my_settings
from app import create_app

@pytest.fixture
def api():
    app = create_app(my_settings.TEST_CONFIG)
    app.config['TESTING'] = True
    api = app.test_client()

    return api

