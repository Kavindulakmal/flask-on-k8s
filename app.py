from flask import Flask, request, jsonify
from flask_mysql_connector import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

@app.route('/users', method=['GET'])
def get_users():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id =%s",(id,))
    row = cursor.fetchone()
    cursor.close()
    return jsonify(row)

@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO users(name, email) VALUES(%s, %s)", (data['name'], data['email']))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "User added successfully!"}), 201


@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (data['name'], data['email'], id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "User updated successfully!"})

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "User deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
