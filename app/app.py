from flask import Flask, request, jsonify
import pyodbc
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

# Retrieve database connection string from Azure Key Vault
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url="https://cssecrets.vault.azure.net", credential=credential)
db_connection_string = secret_client.get_secret("dbconnect").value


# Routes for CRUD operations
@app.route('/api/items', methods=['GET'])
def get_items():
    conn = pyodbc.connect(db_connection_string)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, quantity FROM inventory_items")
    items = cursor.fetchall()
    item_data = [{'id': item.id, 'name': item.name, 'quantity': item.quantity} for item in items]
    return jsonify(item_data)

@app.route('/api/items', methods=['POST'])
def create_item():
    conn = pyodbc.connect(db_connection_string)
    cursor = conn.cursor()
    data = request.get_json()
    name = data['name']
    quantity = data['quantity']
    cursor.execute("INSERT INTO inventory_items (name, quantity) VALUES (?, ?)", name, quantity)
    conn.commit()
    conn.close()
    return jsonify({'message': 'Item created successfully'})



# Implement other CRUD operations similarly

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
