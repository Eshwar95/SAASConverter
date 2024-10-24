from db.models.users import User
from validators import validateBody

# GET ALL USERS
async def getUsers():
    try:
        data = await User.findAll()
        return responseHandler(True, data)
    except Exception as error:
        raise Exception('Unable to get the users')

# GET A USER BY ID
async def getUserByID(id):
    try:
        user = await User.findByPk(id)
        if not user:
            return responseHandler(False, errorMsgNotExist(id))
        else:
            return responseHandler(True, user)
    except Exception as error:
        raise Exception('Unable to get the user')

# CREATE A USER
async def createUser(newUser):
    # Validate the body of the request
    validationFails = validateBody(newUser)
    if validationFails:
        return validationFails

    # Destructuring the body
    firstName = newUser['firstName']
    lastName = newUser['lastName']
    email = newUser['email']
    catchphrase = newUser['catchphrase