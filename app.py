# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from six.moves.urllib.parse import urlencode
import json
from functools import wraps
from flask_cors import CORS
from auth.auth import AuthError, requires_auth
from models import setup_db, Job, Contractor, Client
from sqlalchemy import exc
import json


# AUTH0_DOMAIN = 'dvcoffee.us.auth0.com'
# API_AUDIENCE = 'http://localhost:5000'
# ALGORITHMS = ["RS256"]

# ----------------------------------------------------------------------------#
# App Config
# ----------------------------------------------------------------------------#
def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def health():
        return jsonify({'health': 'Running!!'}), 200

    @app.route('/contractors', methods=['GET'])
    @requires_auth('get:anything')
    def contractors(payload):
        try:
            contractors = Contractor.query.all()

            return jsonify({
                'success': True,
                'contractors': [contractor.long()
                                for contractor in contractors]
            })

        except Exception:
            abort(500)

    @app.route('/contractors/<int:contractor_id>', methods=['GET'])
    @requires_auth('get:anything')
    def show_contractor(payload, contractor_id):
        try:
            contractor = Contractor.query.get(contractor_id)

            return jsonify({
                'success': True,
                'contractor': contractor.long()
            })

        except Exception:
            abort(404)

    @app.route('/contractors', methods=['POST'])
    @requires_auth('post:anything')
    def add_contractor(payload):
        body = request.get_json()

        if (body['name'].strip() == "") or (body['phone'].strip() == ""):
            abort(400)

        try:
            new_contractor = Contractor(name=body['name'].strip(),
                                        phone=body['phone'].strip())
            new_contractor.insert()

        except Exception:
            abort(500)

        return jsonify({
            'success': True,
            'added': new_contractor.id
        })

    @app.route('/contractors/<int:contractor_id>', methods=['DELETE'])
    @requires_auth('delete:anything')
    def delete_contractor(payload, contractor_id):

        contractor = Contractor.query.get(contractor_id)
        if contractor is None:
            abort(404)

        try:
            contractor.delete()

        except Exception:
            abort(500)

        return jsonify({
            'success': True,
            'contractor': contractor.id
        })

    @app.route('/contractors/<int:contractor_id>', methods=['PATCH'])
    @requires_auth('patch:anything')
    def edit_contractor(payload, contractor_id):
        contractor = Contractor.query.get(contractor_id)
        if contractor is None:
            abort(404)

        data = request.get_json()
        if 'name' in data:
            contractor.name = data['name']

        if 'phone' in data:
            contractor.phone = data['phone']

        try:
            contractor.update()
        except Exception:
            abort(500)

        return jsonify({
            'success': True,
            'contractor': contractor.id
        }), 200

    @app.route('/clients', methods=['GET'])
    @requires_auth('get:anything')
    def clients(payload):
        try:
            clients = Client.query.all()
            if not clients:
                abort(404)

            return jsonify({
                'success': True,
                'clients': [client.long() for client in clients]
            })

        except Exception:
            abort(500)

    @app.route('/clients/<int:client_id>', methods=['GET'])
    @requires_auth('get:anything')
    def show_client(payload, client_id):
        try:
            client = Client.query.get(client_id)

            return jsonify({
                'success': True,
                'client': client.long()
            })

        except Exception:
            abort(404)

    @app.route('/clients', methods=['POST'])
    @requires_auth('post:anything')
    def add_client(payload):
        body = request.get_json()

        if (body['name'].strip() == "") or (body['phone'].strip() == ""):
            abort(400)

        try:
            new_client = Client(name=body['name'].strip(),
                                phone=body['phone'].strip(),
                                address=body['address'].strip())
            new_client.insert()

        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'added': new_client.id
        })

    @app.route('/clients/<int:client_id>', methods=['DELETE'])
    @requires_auth('delete:anything')
    def delete_client(payload, client_id):

        client = Client.query.get(client_id)
        if client is None:
            abort(404)

        try:
            client.delete()

        except Exception:
            abort(500)

        return jsonify({
            'success': True,
            'client': client.id
        })

    @app.route('/clients/<int:client_id>', methods=['PATCH'])
    @requires_auth('patch:anything')
    def edit_client(payload, client_id):
        client = Client.query.get(client_id)
        if client is None:
            abort(404)

        data = request.get_json()
        if 'name' in data:
            client.name = data['name']

        if 'phone' in data:
            client.phone = data['phone']

        if 'address' in data:
            client.address = data['address']

        try:
            client.update()

        except Exception:
            abort(500)

        return jsonify({
            'success': True,
            'client': client.id
        }), 200

    @app.route('/jobs', methods=['GET'])
    @requires_auth('get:anything')
    def jobs(payload):
        try:
            jobs = Job.query.all()

            return jsonify({
                'success': True,
                'jobs': [job.long() for job in jobs]
            })

        except Exception:
            abort(500)

    @app.route('/jobs/<int:job_id>', methods=['GET'])
    @requires_auth('get:anything')
    def show_job(payload, job_id):
        job = Job.query.get(job_id)

        if not job:
            abort(404)

        else:
            try:

                return jsonify({
                    "success": True,
                    "job": [job.long()]

                })

            except Exception:
                abort(500)

    @app.route('/jobs', methods=['POST'])
    @requires_auth('post:anything')
    def add_job(payload):
        body = request.get_json()

        if (body['contractor id'] == "") or (body['client id'] == ""):
            abort(400)

        try:
            new_job = Job(contractor_id=body['contractor id'],
                          client_id=body['client id'],
                          start_time=body['start time'])
            new_job.insert()

        except Exception:
            abort(500)

        return jsonify({
            'success': True,
            'added': new_job.id
        })

    @app.route('/jobs/<int:job_id>', methods=['PATCH'])
    @requires_auth('patch:anything')
    def edit_job(payload, job_id):
        job = Job.query.get(job_id)

        if job is None:
            abort(404)

        data = request.get_json()
        if 'client id' in data:
            job.client_id = data['client id']

        if 'contractor id' in data:
            job.contractor_id = data['contractor id']

        if 'start time' in data:
            job.start_time = data['start time']

        try:
            job.update()
        except Exception:
            abort(500)

        return jsonify({
            'success': True,
            'job': job.id
        }), 200

    @app.route('/jobs/<int:job_id>', methods=['DELETE'])
    @requires_auth('delete:anything')
    def delete_job(payload, job_id):

        job = Job.query.get(job_id)
        if job is None:
            abort(404)

        try:
            job.delete()
        except Exception:
            abort(500)

        return jsonify({
            'success': True,
            'job': job.id
        })


# ----------------------------------------------------------------------------#
# Error Handlers
# ----------------------------------------------------------------------------#

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad Request'
        }), 400

    @app.errorhandler(401)
    def unauthorised(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": 'Unauthorised'
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": 'Not Found'
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Internal Server Error'
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), 401

    return app


app = create_app()

if __name__ == '__main__':
    APP.run()
