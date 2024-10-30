import unittest
from unittest.mock import patch
from flask import Flask
from flask import request
from flask import jsonify
import main

class TestApp(unittest.TestCase):
  
  @patch('main.getUsers')
  def test_get_users(self, mock_getUsers):
    mock_getUsers.return_value = {'users': ['user1', 'user2']}
    
    with main.app.test_request_context('/users', method='GET'):
      response = main.get_users()
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.json, {'users': ['user1', 'user2']})
  
  @patch('main.getUserByID')
  def test_get_user_by_id(self, mock_getUserByID):
    mock_getUserByID.return_value = {'user': 'user1'}
    
    with main.app.test_request_context('/users/1', method='GET'):
      response = main.get_user_by_id(1)
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.json, {'user': 'user1'})
  
  @patch('main.createUser')
  def test_create_user(self, mock_createUser):
    mock_createUser.return_value = {'user': 'user1'}
    
    with main.app.test_request_context('/users', method='POST', json={'name': 'user1'}):
      response = main.create_user()
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.json, {'user': 'user1'})
  
  @patch('main.updateUserByID')
  def test_update_user_by_id(self, mock_updateUserByID):
    mock_updateUserByID.return_value = {'user': 'user1'}
    
    with main.app.test_request_context('/users/1', method='PUT', json={'name': 'user1'}):
      response = main.update_user_by_id(1)
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.json, {'user': 'user1'})
  
  @patch('main.deleteUserByID')
  def test_delete_user_by_id(self, mock_deleteUserByID):
    mock_deleteUserByID.return_value = {'message': 'User deleted'}
    
    with main.app.test_request_context('/users/1', method='DELETE'):
      response = main.delete_user_by_id(1)
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.json, {'message': 'User deleted'})

if __name__ == '__main__':
    unittest.main()