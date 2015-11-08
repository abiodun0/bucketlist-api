# Bucketlist API [![Build Status](https://travis-ci.org/andela-ashuaib/bucketlist-api.svg)](https://travis-ci.org/andela-ashuaib/bucketlist-api) [![Coverage Status](https://coveralls.io/repos/andela-ashuaib/bucketlist-api/badge.svg?branch=master&service=github)](https://coveralls.io/github/andela-ashuaib/bucketlist-api?branch=master)


## Description

A Flask API for a bucket list service. The bucketlist service is a service that allows users to create and manage one o r more bucket lists. Users can have multiple bucket lists and bucket lists can have multiple items. This is a RESTful Flask API, it uses a Token Based Authentication system to authenticate users and therefore gives access rights to only registered users. The MultiPurpose Internet Mail Extention MIME type used for the bucket list service is application/json.

## How to use
Clone this repo into a folder, enter into the folder and run

```
$ pip install -r requirements.txt
```

Run this command to create the database setup

```
$ python manage.py db migrate

$ python manage.py db upgrade
```

Run this command to start the server

```
$ python manage.py runserver
```

## Endpoints
All endpoints must be prefixed by your localhost server and ```/app/v1/``` e.g```http:://localhost/api/v1/auth/login``` 

The available endpoints are listed below:

EndPoint |Request Body |Functionality|Public Access
---------|-------------|-------------|-------------
POST /auth/register|{<br>'username':'optional',<br> 'email':required,<br>'password':required<br>}|Registers a new user on the service|TRUE
POST /auth/login|{<br>'email':'required',<br>'password':'required'<br>}|Logs a user in|TRUE
GET /auth/logout|Empty|Logs out this user|FALSE
POST /bucketlists/|{<br>'bucketlist_name':required<br>}|Create a new bucket list|FALSE
GET /bucketlists/|Empty|List all the created bucket lists|FASLE
GET /user/:id|Empty|Get information of a particular user |FALSE
GET /bucketlists/:id|Empty|Get single bucket list (along with it's items)|FALSE
PUT /bucketlists/:id|{<br>'bucketlist_name':optional<br>}|Update this bucket list|FALSE
DELETE /bucketlists/:id|Empty|Delete this single bucket list|FALSE
POST /bucketlists/:id/items/|{<br>'item_name':'required'<br>}|Create a new item in bucket list|FALSE
PUT <br>/bucketlists/:id/items/:item_id|{<br>'item_name':'required',<br>'done':'optional'<br>}|Update a bucket list item|FALSE
DELETE <br>/bucketlists/:id/items/:item_id|Empty|Delete an item in a bucket list|FALSE
GET <br>/bucketlists/?limit=20|Empty|List 20 bucketlist collections|FALSE
GET <br>/bucketlists/?q=bucketlist|Empty|Search for bucketlist that contains bucketlist in its name|FALSE
GET <br>/bucketlists/:id/items/?limit=20|Empty|List 20 bucketlist collections items|FALSE
GET <br>/bucketlists/:id/items/?q=bucket|Empty|Search for bucketlist items that contains bucket in its name|FALSE


##Example Requests
```
$ curl -u abiodun2@golden0.com password -i http://localhost:5000/api/v1/bucketlist/1/items?page=2
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 1157
Server: Werkzeug/0.10.4 Python/2.7.10
Date: Sun, 08 Nov 2015 14:43:25 GMT

{
  "created_by": "abiodun2@golden0.com", 
  "current_page": 2, 
  "items": [
    {
      "date_created": "Sun, 08 Nov 2015 15:34:57 GMT", 
      "done": false, 
      "id": 5, 
      "last_modified": "Sun, 08 Nov 2015 15:34:57 GMT", 
      "name": "item 100 "
    }, 
    {
      "date_created": "Sun, 08 Nov 2015 15:34:57 GMT", 
      "done": false, 
      "id": 6, 
      "last_modified": "Sun, 08 Nov 2015 15:34:57 GMT", 
      "name": "item 20 "
    }, 
    {
      "date_created": "Sun, 08 Nov 2015 15:34:57 GMT", 
      "done": false, 
      "id": 7, 
      "last_modified": "Sun, 08 Nov 2015 15:34:57 GMT", 
      "name": "item 40 "
    }, 
    {
      "date_created": "Sun, 08 Nov 2015 14:15:42 GMT", 
      "done": false, 
      "id": 2, 
      "last_modified": "Sun, 08 Nov 2015 14:15:42 GMT", 
      "name": "item 50 "
    }, 
    {
      "date_created": "Sun, 08 Nov 2015 08:01:56 GMT", 
      "done": false, 
      "id": 1, 
      "last_modified": "Sun, 08 Nov 2015 08:01:56 GMT", 
      "name": "item 60 "
    }
  ], 
  "name": "bucketlist 1", 
  "next_page": null, 
  "prev_page": "http://localhost:5000/api/v1/bucketlist/1/items?page=1", 
  "total_item": 10
}
```


## Testing
* To run tests:  
``` python manage.py test ``` 

* For the coverage report:    
1. ``` coverage run --source=app manage.py test ```   
2. ``` python manage.py test --coverage```   

