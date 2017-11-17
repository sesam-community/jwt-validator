# -*- coding: utf-8 -*-
from flask import Flask, request, Response
import requests
import jwt
import os
import hashlib
import logging

from werkzeug.exceptions import BadRequest

app = Flask (__name__)

@app.route('/<path:path>', methods=["POST"])
def receive(path):
    digest = checksums(request)
    sha256 = hashlib.sha256(request.data).hexdigest()
    endpoint = ""

    if digest == sha256:
        logger.info("jwt valid: sending to node")

        if os.environ.get('base_endpoint_url') is not None:
            endpoint = os.environ.get('base_endpoint_url') + path
        else:
            logger.info("base_endpoint_url is not provided")
            return Response(response="Sesam microservice error: Base url does not resolve", status=500, mimetype='application/json')

        if "node_jwt_token" in os.environ:
            r = requests.post(endpoint, data=request.data, headers={'Authorization':'bearer '+ os.environ.get("node_jwt_token")})
        else:
            r = requests.post(endpoint, data=request.data)
        if r.status_code == 200:
            return Response(response="Thanks", status=200, mimetype='application/json')
        else:
            return Response(response="Sesam node error", status=500, mimetype='application/json')
    else:
        return Response(response="Token did not validate", status=401, mimetype='application/json')

def checksums(request):
    parts = request.headers.get('Authorization').split()
    if parts[0].lower() != 'bearer':
        raise BadRequest('Invalid "Authorization"-header: Authorization header must start with Bearer')

    elif len(parts) == 1:
        raise BadRequest('Invalid "Authorization"-header: JSON Web Token not found')

    elif len(parts) > 2:
        raise BadRequest('Invalid "Authorization"-header: Authorization header must be Bearer + \s + token')

    token = parts[1]
    logger.info("checking jwt validity")
    jwt_parts = jwt.decode(token, os.environ.get('jwt_secret'), leeway=int(os.environ.get('jwt_leeway')), algorithms=['HS256'])

    return jwt_parts.get('sha256')

if __name__ == '__main__':
    format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logger = logging.getLogger('jwt-validator')
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(logging.Formatter(format_string))
    logger.addHandler(stdout_handler)
    logger.setLevel(logging.DEBUG)
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('port', 5000))