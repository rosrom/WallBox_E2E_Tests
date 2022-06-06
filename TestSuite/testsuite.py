__author__ = 'rosaroman'

import json
from nose.tools import nottest
from TestSuite.common_methods import *


class BaseAPI:
    """Base class to initialize"""
    def __init__(self):
        self.common_methods = CommonMethods()
        self.token_user = self.common_methods.set_token(user, user_pass)
        self.token_admin = self.common_methods.set_token(admin, admin_pass)
        self.wrong_token = {"Authorization": "Bearer " + 'wrongtoken1234'}


class TestsLogin(BaseAPI):

    def test00_api_is_running(self):
        """Test00: Healthcheck to verify API is up and running"""
        response = self.common_methods.healthcheck()
        assert response.status_code == 200, 'API is KO'

    def test01_correct_login_as_admin(self):
        """Test01: As an admin, I can log in and get a token"""
        response = self.common_methods.login(admin, admin_pass)
        assert response.json()['jwt'], 'A token has not been created'
        assert response.json()['email'] == admin, 'Logged in user is not correct'

    def test02_correct_login_as_user(self):
        """Test02: As a user, I can log in a get a token"""
        response = self.common_methods.login(user, user_pass)
        assert response.json()['jwt'], 'A token has not been created'
        assert response.json()['email'] == user, 'Logged in user is not correct'

    def test03_not_log_in_with_wrong_credentials(self):
        """Test03: As a user/admin, I can not log in with incorrect password"""
        response = self.common_methods.login(admin, user_pass)
        assert response.status_code == 401, 'Response should have been 401 Unauthorized'

    def test04_not_log_in_with_empty_credentials(self):
        """Test04: As a user/admin, I can not log in with empty credentials"""
        response = self.common_methods.login(admin, '')
        assert response.status_code == 400, 'Response should have been 400 code'

class TestsChargers(BaseAPI):

    def test05_get_list_of_chargers_as_user(self):
        """Test05: As a user, I can get a list of chargers linked to me"""
        response = self.common_methods.get_chargers(self.token_user)
        assert response.status_code == 200, 'Status code is not correct'
        #assert response.json()['chargers'], ' Chargers are not returned' #returning 0 as there are no chargers created
    def test06_get_list_of_chargers_as_admin(self):
        """Test06: As an admin, I can get a list of all chargers"""
        response = self.common_methods.get_chargers(self.token_admin)
        assert response.status_code == 200, 'Status code is not correct'
        #assert response.json()['chargers'], ' Chargers are not returned' #returning 0 as there are no chargers created

    def test07_not_logged_in_can_not_see_chargers(self):
        """Test07: [negative] As a non logged in user, I can not see the list of existing chargers"""
        response = self.common_methods.get_chargers(self.wrong_token)
        assert response.status_code == 401, 'Unauthorized user is seen list of chargers'

    @nottest
    def test08_create_charger_as_admin(self):
        """Test08: As an admin, I can create a charger"""
        response = self.common_methods.create_charger(self.token_admin, serial_number1, model1)
        assert response.status_code == 200, 'Charger has not been created' #Not working, not sure if because I am
        #using wrong values for model, or if it is not working as documented
        #assert response.json()['chargers'][]

    @nottest
    def test09_update_charger_as_admin(self):
        """Test09: As an admin, I can modify a charger. This can not be executed as create charger is not working, so
        there is nothing to update. When create charger works, chargeruid returned in response when created a request
         can be used to be updated"""
        response = self.common_methods.update_charger(self.token_admin, chargeruid, serial_number2, model2)
        assert response.status_code == 200, 'Charger has not been modified'
        #assert response.json()['chargers'][]

    @nottest
    def test10_delete_charger_as_admin(self):
        """Test10: As an admin, I can delete a charger. This can not be executed as create charger is not working, so
        there is nothing to delete. When create charger works, chargeruid returned in response when created a request
         can be used to be deleted"""
        response = self.common_methods.delete_charger(self.token_admin, chargeruid)
        assert response.status_code == 200, 'Charger has not been modified'

class TestUsers(BaseAPI):

    def test11_get_users_as_admin(self):
        """Test11: As an admin, I can get a list of users, that includes all users and myself but no other admins"""
        response = self.common_methods.get_users(self.token_admin)
        assert response.status_code == 200, 'Response is errored'
        assert response.json()['users'], 'No users have been listed'

    def test12_get_users_as_user(self):
        """Test12: As a user, I can get a list of users, that only includes myself"""
        response = self.common_methods.get_users(self.token_user)
        users_returned = json.loads(response.text)['users']
        assert response.status_code == 200, 'Response is errored'
        assert response.json()['users'][0]['role'] == 'user', 'Returned user is not the expected one'
        assert response.json()['users'][0]['email'] == user, 'Returned user is not the expected one'
        for user_id in users_returned:
            assert not user_id['role'] == 'admin'

    def test13_admin_can_create_admin_user(self):
        """Test13: As an admin, I can create an admin user"""
        email = self.common_methods.generate_random_email()
        response = self.common_methods.create_user(self.token_admin, email, password_tocreate, 'admin')
        assert response.status_code == 200, 'Response is errored'
        assert response.json()['user']['email'] == email, 'Created user does not have correct email'
        assert response.json()['user']['role'] == 'admin', 'Created user does not have correct role'

    def test14_admin_can_create_user_user(self):
        """Test14: As an admin, I can create a user user"""
        email = self.common_methods.generate_random_email()
        response = self.common_methods.create_user(self.token_admin, email, password_tocreate, 'user')
        assert response.status_code == 200, 'Response is errored'
        assert response.json()['user']['email'] == email
        assert response.json()['user']['role'] == 'user'
        uid = response.json()['user']['uid']
        assert self.common_methods.get_user(self.token_admin, uid), 'User has not been created correctly'

    def test15_admin_can_modify_user(self):
        """Test15: As an admin, I can modify a user
        ToDo: Create user in order to modify it (request not working ATM)"""
        #precondition: create user to modify:
        email = self.common_methods.generate_random_email()
        email_modified = self.common_methods.generate_random_email()
        user_to_modify = self.common_methods.create_user(self.token_admin, email, password_tocreate, 'user')
        params_to_update = {
            'email': email_modified,
            'pass': 'modified_pass'
        }
        useruid = user_to_modify.json()['user']['uid']
        response = self.common_methods.modify_user(self.token_admin, useruid, params_to_update)
        assert response.status_code == 200, 'Status code is not correct'
        assert json.loads(response.text)['user']['email'] == email_modified, 'User not modified correctly'
        assert self.common_methods.get_user(self.token_admin, useruid).json()['email']  == email_modified

    def test16_admin_can_delete_user(self):
        """Test16: As an admin, I can delete a user. Failing, returns 204, but it should return a 200 there are users"""
        #precondition: create user to delete:
        email = self.common_methods.generate_random_email()
        user_to_delete = self.common_methods.create_user(self.token_admin, email, password_tocreate, 'user')
        useruid = user_to_delete.json()['user']['uid']
        response = self.common_methods.delete_user(self.token_admin, useruid)
        assert response.status_code == 204, 'Response is incorrect'
        assert not self.common_methods.get_user(self.token_admin, useruid), 'User has not been deleted'

    def test17_user_can_not_create_user(self):
        """Test17: [negative] As a user, I can not create another user"""
        response = self.common_methods.create_user(self.token_user, user_email_tocreate2, password_tocreate, 'user')
        assert response.status_code == 401, 'Response code should have been 401 Forbidden'

    def test18_admin_can_delete_admin(self):
        """Test18: As an admin, I can delete my account"""
        #precondition: create admin in order to delete it
        email = self.common_methods.generate_random_email()
        user_to_delete = self.common_methods.create_user(self.token_admin, email, password_tocreate, 'admin')
        useruid = user_to_delete.json()['user']['uid']
        token_admin_new = self.common_methods.set_token(email, password_tocreate)
        response = self.common_methods.delete_user(token_admin_new, useruid)
        assert response.status_code == 204, 'Response is not correct'
        assert not self.common_methods.get_user(self.token_admin, useruid), 'User has not been deleted'

    def test19_user_can_not_delete_itself(self):
        """Test19: As a user, I can NOT delete my account"""
        """ToDo: Verify if this is working as specified"""
        #precondition: create user in order to delete it
        email = self.common_methods.generate_random_email()
        user_to_delete = self.common_methods.create_user(self.token_admin, email, password_tocreate, 'user')
        useruid = user_to_delete.json()['user']['uid']
        token_user_new = self.common_methods.set_token(email, password_tocreate)
        response = self.common_methods.delete_user(token_user_new, useruid)
        assert response.status_code == 401, 'Response should be authorization error'
        assert self.common_methods.get_user(self.token_admin, useruid), 'User has been incorrectly deleted'

    def test20_get_user_as_admin(self):
        """Test20: As an admin, I can get a specific user by UID"""
        useruid = self.common_methods.get_a_random_user(self.token_admin, 'user')['uid']
        response = self.common_methods.get_user(self.token_admin, useruid)
        assert response.status_code == 200, 'Response is errored'
        assert response.json()['uid'] == useruid, 'Retrieved user is incorrect'

    def test21_get_user_as_user(self):
        """Test21: As a user, I can get a specific user by UID"""
        """ToDo: I think I can get only myself, fix"""
        useruid = self.common_methods.get_a_random_user(self.token_user, 'user')['uid']
        response = self.common_methods.get_user(self.token_user, useruid)
        assert response.status_code == 200, 'Response is errored'
        assert response.json()['uid'] == useruid, 'Retrieved user is incorrect'

    def test22_get_admin_as_user(self):
        """Test22: As a user, I can  NOT get a specific admin by UID"""
        useruid = self.common_methods.get_a_random_user(self.token_admin, 'admin')['uid']
        response = self.common_methods.get_user(self.token_user, useruid)
        assert response.status_code == 403, 'User should not be able to access'

    def test23_admin_can_not_get_other_admin_info(self):
        """Test23: [negative] Verify that as an admin, I can not get information about a different admin """
        #precondition: create user in order
        email = self.common_methods.generate_random_email()
        user_to_retrieve = self.common_methods.create_user(self.token_admin, email, password_tocreate, 'admin')
        useruid = user_to_retrieve.json()['user']['uid']
        response = self.common_methods.get_user(self.token_admin, useruid)
        assert response.status_code == 403, 'Response should be cannot access that resource 403'

    def test24_user_can_not_get_other_user_info(self):
        """Test24: [negative] Verify that as a user, I can not get information about a different user"""
        email = self.common_methods.generate_random_email()
        user_to_retrieve = self.common_methods.create_user(self.token_admin, email, password_tocreate, 'user')
        useruid = user_to_retrieve.json()['user']['uid']
        response = self.common_methods.get_user(self.token_user, useruid)
        assert response.status_code == 403, 'Response should be cannot access that resource 403'

    def test25_not_logged_user_can_not_get_user_info(self):
        """ Test25: [negative] Verify that as a non logged user I can not get user info"""
        email = self.common_methods.generate_random_email()
        user_to_retrieve = self.common_methods.create_user(self.token_admin, email, password_tocreate, 'user')
        useruid = user_to_retrieve.json()['user']['uid']
        response = self.common_methods.get_user(self.wrong_token, useruid)
        assert response.status_code == 401, 'Response should be unauthorized'

#class TestChargers(BaseAPI):

