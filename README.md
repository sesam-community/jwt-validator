# JWT-validator

A small microservice to check if body of request is valid by checking checksum of body in JWT.

[![Build Status](https://travis-ci.org/sesam-community/jwt-valdator.svg?branch=master)](https://travis-ci.org/sesam-community/jwt-validator)

This microservice checks for JWT in header.
There is a sha checksum of the body inside the JWT that should be the same checksum of the request body. If this is true the JWT is valid. and can be forwarded to the endpoint.
The microservice needs to verify the signature of the JWT received with a jwt_secret.

##### Example configuration JWT:

```
{
  "_id": "jwt-validator",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "endpoint_url":"http://localhost:5002/foobar"#the endpoint where the data is going to be sent,
      "jwt_secret": "$SECRET(jwt_secret)"# key to validate jwt received ,
      "node_jwt_token": "$SECRET(the_node_token)", #needed when speaking to Sesam node
    },
    "image": "sesambuild/jwt-validator:latest",
    "port": 5001
  }
}
```
