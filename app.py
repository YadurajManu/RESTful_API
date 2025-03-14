from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Storage for API data (in-memory for demonstration)
# In a production environment, you would use a database
data_store = []

@app.route('/')
def home():
    """Home endpoint that returns a welcome message."""
    return render_template('index.html')

@app.route('/api/data', methods=['POST'])
def add_data():
    """Endpoint to add any data to the API."""
    try:
        # Get the data from the request
        content = request.json
        
        # If no JSON was provided, try to get form data
        if content is None:
            content = request.form.to_dict()
            
        # If still no data, try to get raw data
        if not content:
            try:
                content = json.loads(request.data.decode('utf-8'))
            except:
                content = {"raw_data": request.data.decode('utf-8')}
        
        # Generate a simple ID (in production, use a more robust ID generation method)
        new_id = len(data_store) + 1
        
        # Store the data with an ID
        item = {"id": new_id, "data": content}
        data_store.append(item)
        
        logger.info(f"Added new data with ID: {new_id}")
        
        # Return the created item with its ID
        return jsonify({"message": "Data added successfully", "item": item}), 201
    
    except Exception as e:
        logger.error(f"Error adding data: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/api/data', methods=['GET'])
def get_all_data():
    """Endpoint to retrieve all stored data."""
    return jsonify({"data": data_store})

@app.route('/api/data/<int:item_id>', methods=['GET'])
def get_data(item_id):
    """Endpoint to retrieve specific data by ID."""
    for item in data_store:
        if item["id"] == item_id:
            return jsonify({"item": item})
    
    return jsonify({"error": "Item not found"}), 404

@app.route('/api/data/<int:item_id>', methods=['PUT'])
def update_data(item_id):
    """Endpoint to update specific data by ID."""
    try:
        # Find the item to update
        for i, item in enumerate(data_store):
            if item["id"] == item_id:
                # Get the updated data
                content = request.json
                
                # If no JSON was provided, try to get form data
                if content is None:
                    content = request.form.to_dict()
                
                # If still no data, try to get raw data
                if not content:
                    try:
                        content = json.loads(request.data.decode('utf-8'))
                    except:
                        content = {"raw_data": request.data.decode('utf-8')}
                
                # Update the item
                data_store[i] = {"id": item_id, "data": content}
                
                logger.info(f"Updated data with ID: {item_id}")
                
                return jsonify({"message": "Data updated successfully", "item": data_store[i]})
        
        return jsonify({"error": "Item not found"}), 404
    
    except Exception as e:
        logger.error(f"Error updating data: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/api/data/<int:item_id>', methods=['DELETE'])
def delete_data(item_id):
    """Endpoint to delete specific data by ID."""
    for i, item in enumerate(data_store):
        if item["id"] == item_id:
            deleted_item = data_store.pop(i)
            logger.info(f"Deleted data with ID: {item_id}")
            return jsonify({"message": "Data deleted successfully", "item": deleted_item})
    
    return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    logger.info("Starting the API server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
