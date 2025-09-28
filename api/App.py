from flask import Flask, request, jsonify

# Flask application instance
app = Flask(__name__)

# The secret code to unlock the app
SECRET_CODE = "1234"

@app.route('/api/check_code', methods=['POST'])
def check_code():
    """
    Checks if the entered code matches the secret code.
    This is the serverless endpoint called by the frontend.
    """
    try:
        data = request.json
        entered_code = data.get('code', '')

        # SECURITY: This check uses simple string comparison.
        if entered_code == SECRET_CODE:
            return jsonify({"success": True, "message": "Access granted"})
        else:
            return jsonify({"success": False, "message": "Invalid code"}), 401
    except Exception as e:
        # Handle cases where request body might be malformed
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

# The root route is not needed in the serverless function 
# since the frontend handles the HTML file.
# We only expose the /api/check_code endpoint.
