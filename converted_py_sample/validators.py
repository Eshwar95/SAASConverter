```python
from services import responseHandler

def checkBodyObjIsEmpty(body):
    return True if len(body) == 0 else False

def checkBodyObjPropertiesAreEmpty(body):
    return True if 'firstName' not in body or 'lastName' not in body or 'email' not in body or 'catchphrase' not in body else False

def validateBody(body):
    bodyIsEmpty = checkBodyObjIsEmpty(body)
    if bodyIsEmpty:
        return responseHandler(False, "The body can't be empty. An object with the fields: 'fist_name','last_name','email' and 'catchphrase' need to be send as body")

    propertiesAreEmpty = checkBodyObjPropertiesAreEmpty(body)
    if propertiesAreEmpty:
        return responseHandler(False, "The body need to have the properties: 'fist_name','last_name','email' and 'catchphrase'")
```