import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Contractor, Client, Job


class FsndCapstoneTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        # Test database name
        # self.database_name = "capstone_test"
        # self.database_path = "postgres://danievanrensburg:\
        # Danie427*@localhost:5432/" + self.database_name
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Test variables
        # TOKENS
        self.manager_token = os.environ['manager_token']
        self.employee_token = os.environ['employee_token']

        # New Contractor
        self.new_contractor = {
            'name': 'Pawel Coetzer',
            'phone': '0514221935'
        }

        # Invalid new contractors
        self.invalid_new_contractor = {
            'name': "",
            'phone': '0531984567'
        }

        # Patch Contractor
        self.change_contractor_phone = {
            'phone': 'new phone'
        }

        # New Client
        self.new_client = {
            'name': "Louis Vuitton",
            'address': "20 William Nickel",
            'phone': "0103456789"
        }

        # Invalid new Client
        self.invalid_new_client = {
            'name': "",
            'address': "20 William Nickel",
            'phone': "0103456789"
        }

        # Patch Client
        self.change_client_address = {
            'address': 'New Address'
        }

        # New job
        self.new_job = {
            "contractor id": 2,
            "client id": 2,
            "start time": "2020 11 25T12:00"
        }

        # Invalid job
        self.invalid_new_job = {
            "contractor id": "",
            "client id": 2,
            "start time": "2020 11 25T12:00"
        }

        # Patch jobs
        self.change_job_time = {
            "start time": "2021 11 25T12:00"
        }

    def tearDown(self):
        """Executed after each test"""
        pass

    # TESTS START HERE

    def test_homepage(self):

        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('health', data)
        self.assertEqual(data['health'], 'Running!!')


# Tests for /contractor start

    def test_get_contractors_without_token(self):

        """Failing Test trying to make a call without token"""
        res = self.client().get('/contractors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_get_contractors(self):

        """Passing Test for GET /contractors"""
        res = self.client().get('/contractors', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn("contractors", data)
        self.assertTrue(len(data["contractors"]))

    def test_404_get_contractor_by_id(self):

        """Failing Test for GET /contractors/<int:contractor_id>"""
        res = self.client().get('/contractors/100', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_get_contractor_by_id(self):
        """Passing Test for GET /contractor/<int:contractor_id>"""
        res = self.client().get('/contractors/2', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('contractor', data)
        self.assertIn('name', data['contractor'])
        self.assertTrue(len(data["contractor"]["phone"]))

    def test_create_contractor_with_employee_token(self):
        """Passing Test for POST /contractors"""
        res = self.client().post('/contractors', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        }, json=self.new_contractor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('added', data)

    def test_400_create_invalid_contractor(self):
        """Failing Test for POST /contractors"""
        res = self.client().post('/contractors', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        }, json=self.invalid_new_contractor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_update_contractor_info(self):
        """Passing Test for PATCH /contractors/<int:contractor_id>"""
        res = self.client().patch('/contractors/2', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.change_contractor_phone)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('contractor', data)

    def test_404_update_contractor_info(self):
        """Failing Test for PATCH /contractors/<int:contractor_id>"""
        res = self.client().patch('/contractors/100', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.change_contractor_phone)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_401_update_contractor_info(self):
        """Failing Test for PATCH /contractors/<int:contractor_id>"""
        res = self.client().patch('/contractors/2', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        }, json=self.change_contractor_phone)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_401_delete_contractor_with_employee_token(self):
        """Failing Test for DELETE /contractors/<int:contractor_id>"""
        res = self.client().delete('/contractors/1', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_404_delete_contractor_with_manager_token(self):
        """Passing Test for DELETE /contractors/<int:contractor_id>"""
        res = self.client().delete('/contractors/100', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_delete_contractor_with_manager_token(self):
        """Passing Test for DELETE /contractors/<int:contractor_id>"""
        res = self.client().delete('/contractors/5', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('contractor', data)

# Tests for /client starts

    def test_get_client_without_token(self):
        """Failing Test trying to make a call without token"""
        res = self.client().get('/clients')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_get_clients(self):
        """Passing Test for GET /clients"""
        res = self.client().get('/clients', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn("clients", data)
        self.assertTrue(len(data["clients"]))

    def test_404_get_client_by_id(self):
        """Failing Test for GET /clients/<int:clients_id>"""
        res = self.client().get('/clients/100', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_get_client_by_id(self):
        """Passing Test for GET /clients/<int:client_id>"""
        res = self.client().get('/clients/2', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('client', data)
        self.assertIn('name', data['client'])
        self.assertTrue(len(data["client"]["phone"]))

    def test_create_client_with_employee_token(self):
        """Passing Test for POST /clients"""
        res = self.client().post('/clients', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        }, json=self.new_client)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('added', data)

    def test_400_create_invalid_client(self):
        """Failing Test for POST /clients"""
        res = self.client().post('/clients', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        }, json=self.invalid_new_client)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_update_client_info(self):
        """Passing Test for PATCH /clients/<int:client_id>"""
        res = self.client().patch('/clients/2', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.change_client_address)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('client', data)

    def test_404_update_client_info(self):
        """Failing Test for PATCH /clients/<int:client_id>"""
        res = self.client().patch('/clients/100', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.change_client_address)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_401_update_client_info(self):
        """Failing Test for PATCH /clients/<int:client_id>"""
        res = self.client().patch('/clients/2', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        }, json=self.change_client_address)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_401_delete_client_with_employee_token(self):
        """Failing Test for DELETE /clients/<int:client_id>"""
        res = self.client().delete('/clients/1', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_404_delete_client_with_manager_token(self):
        """Passing Test for DELETE /clients/<int:client_id>"""
        res = self.client().delete('/clients/100', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_delete_client_with_manager_token(self):
        """Passing Test for DELETE /clients/<int:client_id>"""
        res = self.client().delete('/clients/5', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('client', data)

# Tests for /jobs start.
    def test_get_jobs_without_token(self):
        """Failing Test trying to make a call without token"""
        res = self.client().get('/jobs')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_get_jobs(self):
        """Passing Test for GET /jobs"""
        res = self.client().get('/jobs', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn("jobs", data)
        self.assertTrue(len(data["jobs"]))

    def test_404_get_job_by_id(self):
        """Failing Test for GET /jobs/<int:job_id>"""
        res = self.client().get('/jobs/100', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_get_job_by_id(self):
        """Passing Test for GET /jobs/<int:job_id>"""
        res = self.client().get('/jobs/2', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('job', data)

    def test_create_job_with_employee_token(self):
        """Passing Test for POST /jobs"""
        res = self.client().post('/jobs', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        }, json=self.new_job)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('added', data)

    def test_400_create_invalid_job(self):
        """Failing Test for POST /jobs"""
        res = self.client().post('/jobs', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        }, json=self.invalid_new_job)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_update_job_info(self):
        """Passing Test for PATCH /jobs/<int:job_id>"""
        res = self.client().patch('/jobs/2', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.change_job_time)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('job', data)

    def test_404_update_job_info(self):
        """Failing Test for PATCH /jobs/<int:job_id>"""
        res = self.client().patch('/jobs/100', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.change_job_time)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_401_update_job_info(self):
        """Failing Test for PATCH /jobs/<int:job_id>"""
        res = self.client().patch('/jobs/2', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        }, json=self.change_job_time)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_401_delete_job_with_employee_token(self):
        """Failing Test for DELETE /jobs/<int:job_id>"""
        res = self.client().delete('/jobs/2', headers={
            'Authorization': "Bearer {}".format(self.employee_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_404_delete_job_with_manager_token(self):
        """Failing Test for DELETE /jobs/<int:job_id>"""
        res = self.client().delete('/jobs/100', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_delete_job_with_manager_token(self):
        """Passing Test for DELETE /jobs/<int:job_id>"""
        res = self.client().delete('/jobs/5', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('job', data)


if __name__ == "__main__":
    unittest.main()
