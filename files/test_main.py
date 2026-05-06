import sys
import os
import json
import pytest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from unittest.mock import MagicMock
from main import hello_cloud


def make_request(method="GET", args=None, json_body=None):
    """Helper to create a mock Flask request."""
    req = MagicMock()
    req.method = method
    req.args = args or {}
    req.get_json = MagicMock(return_value=json_body)
    return req


class TestHelloCloud:

    def test_get_default(self):
        req = make_request("GET")
        body, status, headers = hello_cloud(req)
        data = json.loads(body)
        assert status == 200
        assert "Hello, World!" in data["message"]
        assert data["status"] == "success"

    def test_get_with_name(self):
        req = make_request("GET", args={"name": "Alice"})
        body, status, headers = hello_cloud(req)
        data = json.loads(body)
        assert status == 200
        assert "Alice" in data["message"]

    def test_post_with_body(self):
        req = make_request("POST", json_body={"name": "Bob", "data": {"key": "value"}})
        body, status, headers = hello_cloud(req)
        data = json.loads(body)
        assert status == 200
        assert "Bob" in data["message"]
        assert data["received"] == {"key": "value"}

    def test_post_empty_body(self):
        req = make_request("POST", json_body=None)
        body, status, headers = hello_cloud(req)
        data = json.loads(body)
        assert status == 200
        assert "World" in data["message"]

    def test_cors_headers(self):
        req = make_request("GET")
        body, status, headers = hello_cloud(req)
        assert headers["Access-Control-Allow-Origin"] == "*"

    def test_options_preflight(self):
        req = make_request("OPTIONS")
        body, status, headers = hello_cloud(req)
        assert status == 204

    def test_unsupported_method(self):
        req = make_request("DELETE")
        body, status, headers = hello_cloud(req)
        assert status == 405

    def test_timestamp_present(self):
        req = make_request("GET")
        body, status, _ = hello_cloud(req)
        data = json.loads(body)
        assert "timestamp" in data
        assert data["timestamp"].endswith("Z")
