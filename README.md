# Bucketlist API [![Build Status](https://travis-ci.org/andela-ashuaib/bucketlist-api.svg)](https://travis-ci.org/andela-ashuaib/bucketlist-api) [![Coverage Status](https://coveralls.io/repos/andela-ashuaib/bucketlist-api/badge.svg?branch=master&service=github)](https://coveralls.io/github/andela-ashuaib/bucketlist-api?branch=master)


## Description

A Flask API for a bucket list service. The bucketlist service is a service that allows users to create and manage one o r more bucket lists. Users can have multiple bucket lists and bucket lists can have multiple items. This is a RESTful Flask API, it uses a Token Based Authentication system to authenticate users and therefore gives access rights to only registered users. The MultiPurpose Internet Mail Extention MIME type used for the bucket list service is application/json.


## Endpoints
All endpoints must be prefixed by ```/api/:version/``` where ```:version``` represents the API version in use. For example, in the API v1, the login endpoint would be ```/api/v1/auth/login```.

The available endpoints are listed below:

EndPoint |Functionality|Public Access
---------|-------------|--------------
POST /auth/register|Registers a new user on the service|TRUE
POST /auth/login|Logs a user in|TRUE
GET /auth/logout|Logs out this user|FALSE
GET /user/|Get the profile of this user|FALSE
PUT /user/|Update the profile of this user|FALSE
DELETE /user/|Delete this user account|FALSE
POST /bucketlists/|Create a new bucket list|FALSE
GET /bucketlists/|List all the created bucket lists|FASLE
GET /bucketlists/:id|Get single bucket list (along with it's items)|FALSE
PUT /bucketlists/:id|Update this bucket list|FALSE
DELETE /bucketlists/:id|Delete this single bucket list|FALSE
POST /bucketlists/:id/items/|Create a new item in bucket list|FALSE
PUT /bucketlists/:id/items/:item_id|Update a bucket list item|FALSE
DELETE /bucketlists/:id/items/:item_id|Delete an item in a bucket list|FALSE