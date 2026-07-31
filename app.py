from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Backend Data Persistence Layer (In-Memory Data Store)
items_db = []

@app.route('/')
def home():
    return render_template('index.html')

# =====================================================================
# 1. GET ALL ITEMS ENDPOINT (HTTP Status: 200 OK)
# =====================================================================
@app.route('/api/items', methods=['GET'])
def get_all_items():
    return jsonify({
        "status": "success",
        "count": len(items_db),
        "data": items_db
    }), 200


# =====================================================================
# 2. POST CREATE ITEM ENDPOINT WITH DATA VALIDATION (HTTP Status: 201 / 400)
# =====================================================================
@app.route('/api/items', methods=['POST'])
def create_item():
    try:
        data = request.get_json()

        # Validation Rule 1: Check if body exists
        if not data:
            return jsonify({
                "status": "error",
                "error": "Bad Request",
                "message": "Invalid JSON payload provided."
            }), 400  # 400 Bad Request

        title = data.get('title')
        category = data.get('category')

        # Validation Rule 2: Check required fields
        if not title or not category:
            return jsonify({
                "status": "error",
                "error": "Validation Error",
                "message": "Fields 'title' and 'category' are strictly required."
            }), 400  # 400 Bad Request

        # Validation Rule 3: Check string length constraint
        if len(str(title).strip()) < 3:
            return jsonify({
                "status": "error",
                "error": "Validation Error",
                "message": "Field 'title' must be at least 3 characters long."
            }), 400  # 400 Bad Request

        # Save to Backend State
        new_item = {
            "id": len(items_db) + 1,
            "title": str(title).strip(),
            "category": str(category).strip()
        }
        items_db.append(new_item)

        # Success Response with HTTP Status 201 Created
        return jsonify({
            "status": "success",
            "message": "Item created successfully!",
            "data": new_item
        }), 201  # 201 Created

    except Exception as e:
        # Error Protocol: HTTP Status 500
        return jsonify({
            "status": "error",
            "error": "Internal Server Error",
            "message": str(e)
        }), 500  # 500 Internal Error


# =====================================================================
# 3. GET SINGLE ITEM BY ID (HTTP Status: 200 / 404)
# =====================================================================
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_single_item(item_id):
    # Find item in DB
    item = next((item for item in items_db if item["id"] == item_id), None)

    # Status 404 handling if item does not exist
    if not item:
        return jsonify({
            "status": "error",
            "error": "Not Found",
            "message": f"Item with ID {item_id} was not found in system."
        }), 404  # 404 Not Found

    return jsonify({
        "status": "success",
        "data": item
    }), 200  # 200 OK


if __name__ == '__main__':
    app.run(debug=True)