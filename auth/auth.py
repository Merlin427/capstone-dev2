import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dvcoffee.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'http://localhost:5000'

## AuthError Exception

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
# Some code used from the BasicFlaskAuth project

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise Autherror({
        'code': 'invalid_claims',
        'description': 'Permissions not included in JWT.'

        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
        'code': 'unauthorised',
        'description': 'Permission not found'

        }, 401 )
    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def validate_auth_header(auth_header):
    splitted_header = auth_header.split()
    bearer_part = splitted_header[0]
    valid_auth = True
    if len(splitted_header) != 2:
        valid_auth = False
    if bearer_part.lower() != "bearer":
        valid_auth = False
    return valid_auth





def get_token():
    headers = request.headers
    if 'Authorization' in request.headers:
        auth_header = headers['Authorization']
        valid_header = validate_auth_header(auth_header)
        if not valid_header:
            print("INVALID")
            raise AuthError({
                'status': 401,
                'message': 'Unauthorized'
            }, status_code=401)
        token = auth_header.split()[1]
        return token
    raise AuthError({
        'status': 401,
        'message': 'Unauthorized'
    }, status_code=401)



def verify_decode_jwt(token):
    try:
        jwt_unverified_headers = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError({
            'status': 401,
            'message': 'invalid jwt token'
        }, status_code=401)
    public_keys_url = f' https://{AUTH0_DOMAIN}/.well-known/jwks.json'
    response = requests.get(public_keys_url)
    jwks = response.json() if response.status_code == 200 else None
    if 'kid' not in jwt_unverified_headers:
        raise AuthError({
            'status': 401,
            'message': 'invalid jwt token'
        }, status_code=401)
    if jwks:
        matched_key = {}
        if 'keys' in jwks:
            for key in jwks['keys']:
                if key['kid'] == jwt_unverified_headers['kid']:
                    matched_key = key
        if matched_key:
            try:
                issuer = f'https://{AUTH0_DOMAIN}/'
                decoded_jwt = jwt.decode(
                    token,
                    matched_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer=issuer
                )
                return decoded_jwt
            except jwt.ExpiredSignatureError:
                raise AuthError({
                    'status': 401,
                    'message': 'token has expired'
                }, status_code=401)
            except jwt.JWTClaimsError:
                raise AuthError({
                    'status': 401,
                    'message': 'invalid claim in jwt token'
                }, status_code=401)
            except jwt.JWTError:
                raise AuthError({
                    'status': 401,
                    'message': 'invalid signature'
                }, status_code=401)
            except Exception:
                print(sys.exc_info())
                raise AuthError({
                    'status': 401,
                    'message': 'invalid auth token'
                }, status_code=401)
        raise AuthError({
            'code': 'invalid token',
            'description': 'please provide a valid token.'
        }, 401)
    raise AuthError({
        'code': 'invalid token',
        'description': 'please provide a valid token.'
    }, 401)


def check_permissions(permission, jwt_payload):
    jwt_has_permissions = 'permissions' in jwt_payload
    if not jwt_has_permissions or (jwt_has_permissions and permission not in jwt_payload['permissions']):
        raise AuthError({
            'code': 'unauthorized',
            'description': 'you dnn\'t have permissions to view this resource .'
        }, 401)
    return True

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token()
            jwt_payload = verify_decode_jwt(token)
            check_permissions(permission, jwt_payload)
            return f(jwt_payload, **kwargs)
        return wrapper
    return requires_auth_decorator
