```python
def test_checkBodyObjIsEmpty():
    assert checkBodyObjIsEmpty([]) == True
    assert checkBodyObjIsEmpty([1, 2, 3]) == False
    assert checkBodyObjIsEmpty({}) == True
    assert checkBodyObjIsEmpty({"key": "value"}) == False

def test_checkBodyObjPropertiesAreEmpty():
    assert checkBodyObjPropertiesAreEmpty({"firstName": "John", "lastName": "Doe", "email": "johndoe@example.com", "catchphrase": "Hello"}) == False
    assert checkBodyObjPropertiesAreEmpty({"firstName": "John", "lastName": "Doe", "email": "johndoe@example.com"}) == True
    assert checkBodyObjPropertiesAreEmpty({"firstName": "John", "email": "johndoe@example.com", "catchphrase": "Hello"}) == True
    assert checkBodyObjPropertiesAreEmpty({"firstName": "John", "lastName": "Doe", "catchphrase": "Hello"}) == True

def test_validateBody():
    assert validateBody([]) == responseHandler(False, "The body can't be empty. An object with the fields: 'fist_name','last_name','email' and 'catchphrase' need to be send as body")
    assert validateBody({"firstName": "John", "lastName": "Doe", "email": "johndoe@example.com", "catchphrase": "Hello"}) == responseHandler(True, "Success")
    assert validateBody({"firstName": "John", "lastName": "Doe", "email": "johndoe@example.com"}) == responseHandler(False, "The body need to have the properties: 'fist_name','last_name','email' and 'catchphrase'")
    assert validateBody({"firstName": "John", "email": "johndoe@example.com", "catchphrase": "Hello"}) == responseHandler(False, "The body need to have the properties: 'fist_name','last_name','email' and 'catchphrase'")
    assert validateBody({"firstName": "John", "lastName": "Doe", "catchphrase": "Hello"}) == responseHandler(False, "The body need to have the properties: 'fist_name','last_name','email' and 'catchphrase'")
```