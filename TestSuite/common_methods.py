__author__ = 'rosaroman'

import json
import random
import requests
import string

#Define some variables

api_url = "http://localhost:3000/"
api_name_signin = "signin/"
api_name_chargers = "chargers/"
api_name_users = "users/"
admin = "admin@wallbox.com"
admin_pass = "admin1234"
user = "user@wallbox.com"
user_pass = "user1234"
serial_number1 = "1"
model1 = "1"
serial_number2 = "2"
model2 = "copper"
chargeruid = "to_change" #To change, this should be gotten in the response given when creating a charger
admin_email_tocreate = "admin2@wallbox.com"
user_email_tocreate1 = "user2@wallbox.com"
user_email_tocreate2 = "user3@wallbox.com"
password_tocreate = "1234admin"



class CommonMethods:

    def set_url(self, path):
        return api_url + path

    def set_url_id(self, path, id):
        return api_url + path + id

    def healthcheck(self):
        return requests.get(api_url)

    def login(self, username, password):
        return requests.post(self.set_url(api_name_signin), json={'email':username, 'password':password})

    def set_token(self, username, password):
        token = self.login(username, password).json()['jwt']
        self.authorization = {"Authorization": "Bearer " + token}
        return self.authorization

    def get_chargers(self, auth_token):
        if auth_token:
            return requests.get(self.set_url(api_name_chargers), headers = auth_token)
        else:
            print("Error: No token received")

    def create_charger(self, auth_token, serial_number, model):
        return requests.post(self.set_url(api_name_chargers), headers = auth_token,
                             json = {'serialNumber':serial_number, 'model': model} )

    def update_charger(self, auth_token, chargeruid, serial_number, model):
        return requests.put(self.set_url_id(api_name_chargers, chargeruid), headers = auth_token,
                            json = {'serialNumber':serial_number, 'model': model} )

    def delete_charger(self, auth_token, chargeruid):
        return requests.delete(self.set_url_id(api_name_chargers, chargeruid), headers = auth_token)

    def get_users(self, auth_token):
        return requests.get(self.set_url(api_name_users), headers = auth_token)

    def get_user(self, auth_token, useruid):
        return requests.get(self.set_url_id(api_name_users, useruid), headers = auth_token )


    def get_a_random_user(self, auth_token, role):
        all_users = self.get_users(auth_token).json()['users']
        for user in all_users:
                if user['role'] == role:
                    return user

    def create_user(self, auth_token, email, password, role):
        return requests.post(self.set_url(api_name_users), headers = auth_token,
                            json = {'email':email, 'password':password, 'role':role, 'emailConfirmation':email,
                                    'passwordConfirmation':password})

    def modify_user(self, auth_token, useruid, params_to_update):
        return requests.put(self.set_url_id(api_name_users, useruid), headers = auth_token,
                            json= params_to_update)

    def delete_user(self, auth_token, useruid):
        url = self.set_url_id(api_name_users, useruid)
        return requests.delete(self.set_url_id(api_name_users, useruid), headers = auth_token)

    def generate_random_email(self):
        mail = ''.join(random.choice(string.ascii_lowercase) for _ in range(12))
        return 'mail_' + mail + '@mail.com'


