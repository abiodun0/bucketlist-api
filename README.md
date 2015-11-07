# Bucketlist API [![Build Status](https://travis-ci.org/andela-ashuaib/bucketlist-api.svg)](https://travis-ci.org/andela-ashuaib/bucketlist-api) [![Coverage Status](https://coveralls.io/repos/andela-ashuaib/bucketlist-api/badge.svg?branch=master&service=github)](https://coveralls.io/github/andela-ashuaib/bucketlist-api?branch=master)


## Description

A Flask API for a bucket list service. The bucketlist service is a service that allows users to create and manage one o r more bucket lists. Users can have multiple bucket lists and bucket lists can have multiple items. This is a RESTful Flask API, it uses a Token Based Authentication system to authenticate users and therefore gives access rights to only registered users. The MultiPurpose Internet Mail Extention MIME type used for the bucket list service is application/json.


## Endpoints
All endpoints must be prefixed by ```/api/:version/``` where ```:version``` represents the API version in use. For example, in the API v1, the login endpoint would be ```/api/v1/auth/login```.

The available endpoints are listed below:

EndPoint |Functionality|Public Access
---------|-------------|--------------
POST /api/v1/auth/register|Registers a new user on the service|TRUE
POST /api/v1/auth/login|Logs a user in|TRUE
POST /api/v1/auth/logout|Logs out this user|FALSE
POST /api/v1/bucketlists/|Create a new bucket list|FALSE
GET /api/v1/bucketlists/|List all the created bucket lists|FASLE
GET /api/v1/bucketlists/:id|Get single bucket list (along with it's items)|FALSE
PUT /api/v1/bucketlists/:id|Update this bucket list|FALSE
DELETE /api/v1/bucketlists/:id|Delete this single bucket list|FALSE
POST /api/v1/bucketlists/:id/items/|Create a new item in bucket list|FALSE
PUT /api/v1/bucketlists/:id/items/:item_id|Update a bucket list item|FALSE
DELETE /api/v1/bucketlists/:id/items/:item_id|Delete an item in a bucket list|FALSE