import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import Contractor, Client, Job


class FsndCapstoneTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        # Test database name
        self.database_name = "capstone_test"
        self.database_path = "postgres://danievanrensburg:Danie427*@localhost:5432/" + self.database_name
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()



        # Test variables
        # TOKENS
        self.manager = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJCZnJJX2pDMm1lTF83SnFwU2JibyJ9.eyJpc3MiOiJodHRwczovL2R2Y29mZmVlLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1Zjg0MjNjNTg4YTI1YTAwNmJiZGI2OWMiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE2MDQzMDkyODksImV4cCI6MTYwNDM5NTY4OSwiYXpwIjoieldKZldnc09lbGNVWTF5WXd1cHZvZmMyb0NyN0pPNTIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphbnl0aGluZyIsImdldDphbnl0aGluZyIsInBhdGNoOmFueXRoaW5nIiwicG9zdDphbnl0aGluZyJdfQ.P0JVa8jiZeH0-myWVy_91C70fGgd9cVUveakz7vqslToGbOiObuNaMkhB94cU7d63hEblSgDzuNS-DAtJmHeYpIyvnvsqEcCU1k3Erq0qBCiDD82d1R7XKmUBYPrz9fnh2VkslisTy5BChPODGhej_rvv3xNwLVXD4_4JraEYV5whC_FDyN1cQS76785XzFGIQAgNHTq5JsRa7_-ii-pS0ccGBHhjUIdIrmKO6ih9yzobyQZU4Z_GYG9qMkMS_uMrZkGYFqjEYF-loeY6YyOqrAZPaQPoshhzGoe-1HhyVAm1igK-GLsX6O--m11zgPY50hkkJQFnkmRPISIifW3vA'
        self.employee = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJCZnJJX2pDMm1lTF83SnFwU2JibyJ9.eyJpc3MiOiJodHRwczovL2R2Y29mZmVlLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1Zjg1NjYxODljZmRiYzAwNmUwZWU1YjQiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE2MDQzMDkzOTUsImV4cCI6MTYwNDM5NTc5NSwiYXpwIjoieldKZldnc09lbGNVWTF5WXd1cHZvZmMyb0NyN0pPNTIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphbnl0aGluZyIsInBvc3Q6YW55dGhpbmciXX0.1O4QSF5amSlcxtfO16iFtaCFabAurLquifq1mUTuPlwb5OcmtSK-4UIs2BoJNF60HWUpvtZgokj3bJYlTItFh1z3S1ZtEwxpwp1y2AVUp-pKjzifjxj3l2HufKpRt8LgPh1vXvwE3NW0BWcwkSsdKNnXjGIc9mH_m7ZN1Giztt5BirZf_WELS6hQfPgWg6Z_RiSg4qkDg2A_yY4wULA-udChqwLER2hJcgKzFR2HnlGAKEysaGmbcgPwMtcuOLPahu8rs0lTU93Eqj_KMwGggrM5amie_4kXIL2nZnucjsT5o8HkQyke5FuCpmJMe-MaOTrIjz6GwamcvnRUz7A5pQ'
        self.badtoken = 'badtoken'

        # New Contractor
        self.new_contractor = {
            'name': 'Pawel Coetzer',
            'phone': '0514221935'
        }

        #Patch Contractor
        self.change_contractor_phone = {
            'phone': 'new phone'
        }

        # New Client
        self.new_client = {
            'name': "Louis Vuitton",
            'address': "20 William Nickel",
            'phone': "0103456789"
        }

        #Patch Client
        self.change_client_address = {
            'address': 'New Address'
        }

        # New job
        self.new_job = {
            "contractor id": 1,
            "client id": 1,
            "start time": "2020 11 25T12:00"
        }

        #Patch jobs
        self.change_job_time = {
            "start time": "2021 11 25T12:00"
        }

        #Add new restaurant if database is empty with good token and set current_rest_id
        #if Restaurant.query.filter(Restaurant.owner_id != 'badtoken').count() == 0:
        #    res = self.client().post('/restaurants', headers={"Authorization": "Bearer {}".format(self.manager)}, json=self.new_restaurant)
        #self.current_rest_id = Restaurant.query.order_by(Restaurant.id.desc()).filter(Restaurant.owner_id != 'badtoken').first().id

        # add new restaurant with bad token is it doesnt exist, and set bad_rest_id
        #if Restaurant.query.filter(Restaurant.owner_id == 'badtoken').count() == 0:
        #    bad_token_rest = Restaurant(name="Bad name", address="bad address", owner_id="badtoken")
        #    bad_token_rest.insert()
        #self.bad_rest_id = Restaurant.query.filter(Restaurant.owner_id == 'badtoken').first().id




    def tearDown(self):
        """Executed after each test"""
        pass



    # TESTS START HERE

    def test_homepage(self):
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)


#    def test_post_restaurant_with_valid_token(self):
#        res = self.client().post('/restaurants', headers={"Authorization": "Bearer {}".format(self.manager)}, json=self.new_restaurant)
#        data = json.loads(res.data)
#
#        self.assertEqual(res.status_code, 200)
#        self.assertEqual(data['success'], True)


#    def test_401_post_restaurant_with_invalid_token(self):
#        res = self.client().post('/restaurants', headers={"Authorization": "Bearer {}".format(self.badtoken)}, json=self.new_restaurant)
#        data = json.loads(res.data)

#        self.assertEqual(res.status_code, 401)
#        self.assertEqual(data['success'], False)



#    def test_get_restaurants(self):
#        res = self.client().get('/restaurants')
#        data = json.loads(res.data)

#        restaurants = Restaurant.query.order_by(Restaurant.id).all()
#        output = [restaurant.format() for restaurant in restaurants]

#        self.assertEqual(res.status_code, 200)
#        self.assertEqual(data['success'], True)
#        self.assertEqual(data['restaurants'], output)



#    def test_get_restaurant_by_id(self):
#        res = self.client().get('/restaurants/' + str(self.current_rest_id))
#        data = json.loads(res.data)

#        restaurant = Restaurant.query.get(self.current_rest_id)
#        format_rest = restaurant.format()

#        self.assertEqual(res.status_code, 200)
#        self.assertEqual(data['restaurants'], format_rest)



#    def test_patch_restaurant_by_id(self):
#        res = self.client().patch('/restaurants/' + str(self.current_rest_id), headers={"Authorization": "Bearer {}".format(self.manager)}, json=self.change_restaurant_address)
#        data = json.loads(res.data)

#        restaurant = Restaurant.query.get(self.current_rest_id)
#        format_rest = restaurant.format()

#        self.assertEqual(res.status_code, 200)
#        self.assertEqual(data['updated_restaurant']['address'], self.change_restaurant_address['address'])



#    def test_patch_restaurant_that_is_not_owners(self):
#        res = self.client().patch('/restaurants/' + str(self.bad_rest_id), headers={"Authorization": "Bearer {}".format(self.manager)}, json=self.change_restaurant_address)

#        self.assertEqual(res.status_code, 401)



#    def test_patch_restaurant_that_does_not_exist(self):
#        res = self.client().patch('/restaurants/' + str(self.current_rest_id + 1000), headers={"Authorization": "Bearer {}".format(self.manager)}, json=self.change_restaurant_address)

#        self.assertEqual(res.status_code, 422)



#    def test_post_reservation_with_vaild_customer(self):
#        res = self.client().post('/restaurants/' + str(self.current_rest_id)  + '/reservation', headers={"Authorization": "Bearer {}".format(self.customer)}, json=self.reservation_info)
#        data = json.loads(res.data)

#        self.assertEqual(res.status_code, 200)



#    def test_post_reservation_with_invaild_customer(self):
#        res = self.client().post('/restaurants/' + str(self.current_rest_id)  + '/reservation', headers={"Authorization": "Bearer {}".format(self.badtoken)}, json=self.reservation_info)
#        data = json.loads(res.data)

#        self.assertEqual(res.status_code, 401)



#    def test_post_reservation_with_non_existant_restaurant(self):
#        res = self.client().post('/restaurants/' + str(self.current_rest_id + 1000)  + '/reservation', headers={"Authorization": "Bearer {}".format(self.customer)}, json=self.reservation_info)
#        data = json.loads(res.data)

#        self.assertEqual(res.status_code, 422)



#    def test_delete_restaurant_with_valid_owner(self):
#        res = self.client().delete('/restaurants/' + str(self.current_rest_id), headers={"Authorization": "Bearer {}".format(self.manager)})

#        deleted_rest = Restaurant.query.get(self.current_rest_id)

#        self.assertEqual(res.status_code, 200)
#        self.assertEqual(deleted_rest, None)



#    def test_delete_non_existant_restaurant(self):
#        res = self.client().delete('/restaurants/' + str((self.current_rest_id + 10000)), headers={"Authorization": "Bearer {}".format(self.manager)})

#        deleted_rest = Restaurant.query.get(self.current_rest_id + 10000)

#        self.assertEqual(res.status_code, 422)
#        self.assertEqual(deleted_rest, None)





if __name__ == "__main__":
    unittest.main()
