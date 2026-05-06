import functions_framework
import json
from datetime import datetime


@functions_framework.http
def hello_cloud(request):
    """
    HTTP Cloud Function entry point.
    Handles GET and POST requests.
    """
    # Set CORS headers for browser clients
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type": "application/json",
    }

    # Handle CORS preflight
    if request.method == "OPTIONS":
        return ("", 204, headers)

    # --- GET Request ---
    if request.method == "GET":
        name = request.args.get("name", "World")
        response = {
            "message": f"Hello, {name}! 👋",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "method": "GET",
            "status": "success",
        }
        return (json.dumps(response), 200, headers)

    # --- POST Request ---
    if request.method == "POST":
        try:
            body = request.get_json(silent=True) or {}
            name = body.get("name", "World")
            data = body.get("data", {})

            response = {
                "message": f"Hello, {name}! Data received ✅",
                "received": data,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "method": "POST",
                "status": "success",
            }
            return (json.dumps(response), 200, headers)

        except Exception as e:
            error_response = {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
            return (json.dumps(error_response), 400, headers)

    # Unsupported method
    return (json.dumps({"status": "error", "message": "Method not allowed"}), 405, headers)
