# JWT-validator

A small microservice to check if body of request is valid by checking checksum of body in JWT.

[![Build Status](https://travis-ci.org/sesam-community/jwt-valdator.svg?branch=master)](https://travis-ci.org/sesam-community/jwt-validator)

This microservice checks for JWT in header.
There is a sha checksum of the body inside the JWT that should be the same checksum of the request body. If this is true the JWT is valid. and can be forwarded to the endpoint.
The microservice needs to verify the signature of the JWT received with a jwt_secret.

base_endpoint_url is a parameter that points to the base of the url where the data is supposed to be sent.
the rest of the url is received on the POST request to the microservice.

Example:
base_endpoint_url = http://localhost:9042/api/receivers/
path param received = foobar/entities

##### Example configuration JWT:

```
{
  "_id": "jwt-validator",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "base_endpoint_url":"http://localhost:5002/api/receivers/"#the endpoint where the data is going to be sent,
      "jwt_secret": "$SECRET(jwt_secret)"# key to validate jwt received ,
      "node_jwt_token": "$SECRET(the_node_token)", #needed when speaking to Sesam node
    },
    "image": "sesambuild/jwt-validator:latest",
    "port": 5001
  }
}
```
