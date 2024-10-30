from flask import Flask, request, jsonify
from services import getUserByID, getUsers, createUser, updateUserByID, deleteUserByID

app = Flask(__name__)

# GET ALL USERS
@app.route('/users', methods=['GET'])
def get_users():
    # Call the function to get the users
    result = getUsers()
    # Return the response
    return jsonify(result)

# GET USER BY ID
@app.route('/users/<id>', methods=['GET'])
def get_user_by_id(id):
    # Call the function to get the user by Id
    resultbyId = getUserByID(id)
    # Return the response
    return jsonify(resultbyId)

# CREATE AN USER
@app.route('/users', methods=['POST'])
def create_user():
    # Get the body from the params
    postBody = request.json
    # Call the function to add the new user
    newUser = createUser(postBody)
    # Return the response
    return jsonify(newUser)

# UPDATE AN USER