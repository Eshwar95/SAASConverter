def test_getUsers():
    # Test when the User.findAll() returns data
    data = [
        { 'id': 1, 'firstName': 'John', 'lastName': 'Doe' },
        { 'id': 2, 'firstName': 'Jane', 'lastName': 'Smith' }
    ]
    User.findAll = AsyncMock(return_value=data)
    result = await getUsers()
    assert result == responseHandler(True, data)
    
    # Test when the User.findAll() throws an exception
    User.findAll = AsyncMock(side_effect=Exception('Some error occurred'))
    with pytest.raises(Exception):
        await getUsers()

def test_getUserByID():
    # Test when the User.findByPk() returns a user
    user = { 'id': 1, 'firstName': 'John', 'lastName': 'Doe' }
    User.findByPk = AsyncMock(return_value=user)
    result = await getUserByID(1)
    assert result == responseHandler(True, user)

    # Test when the User.findByPk() returns None
    User.findByPk = AsyncMock(return_value=None)
    result = await getUserByID(2)
    assert result == responseHandler(False, errorMsgNotExist(2))

    # Test when the User.findByPk() throws an exception
    User.findByPk = AsyncMock(side_effect=Exception('Some error occurred'))
    with pytest.raises(Exception):
        await getUserByID(1)

def test_createUser():
    # Test when validateBody() returns validation fails
    validateBody = Mock(return_value={'error': 'Invalid body'})
    newUser = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john.doe@example.com',
        'catchphrase': 'Hello world'
    }
    result = await createUser(newUser)
    assert result == {'error': 'Invalid body'}
    
    # Test when validateBody() returns None
    validateBody = Mock(return_value=None)
    newUser = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john.doe@example.com',
        'catchphrase': 'Hello world'
    }

    # Test when all parameters are valid and no exceptions occur
    User = Mock()
    newUser = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john.doe@example.com',
        'catchphrase': 'Hello world'
    }
    result = await createUser(newUser)
    assert result == None