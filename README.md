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
GET /bucketlists/:id|Empty|Get single bucket list (along with it's items)|FALSE
PUT /bucketlists/:id|{<br>'bucketlist_name':optional<br>}|Update this bucket list|FALSE
DELETE /bucketlists/:id|Empty|Delete this single bucket list|FALSE
POST /bucketlists/:id/items/|{<br>'item_name':'required'<br>}|Create a new item in bucket list|FALSE
PUT <br>/bucketlists/:id/items/:item_id|{<br>'item_name':'required',<br>'done':'optional'<br>}|Update a bucket list item|FALSE
DELETE <br>/bucketlists/:id/items/:item_id|Empty|Delete an item in a bucket list|FALSE
GET <br>/bucketlists/?limit=20|Empty|List 20 bucketlist collections|FALSE
GET <br>/bucketlists/?q=bucketlist|Empty|Search for bucketlist that contains bucketlist in its name|FALSE
GET <br>/bucketlists/:id/items/?limit=20|Empty|List 20 bucketlist collections items|FALSE
GET <br>/bucketlists/:id/items/?q=bucketlist|Empty|Search for bucketlist items that contains bucketlist in its name|FALSE


##Example Requests
```
$ curl -u abiodun2@golden0.com password -i http://localhost:5000/api/v1/bucketlist/?limit=1
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 444
Server: Werkzeug/0.10.4 Python/2.7.10
Date: Sat, 07 Nov 2015 16:00:42 GMT

{
  "created_by": "abiodun2@golden0.com", 
  "current_page": 1, 
  "items": [
    {
      "created_by": "abiodun2@golden0.com", 
      "date_created": "Sat, 07 Nov 2015 16:51:58 GMT", 
      "id": 1, 
      "items": [], 
      "last_modified": "Sat, 07 Nov 2015 16:51:58 GMT", 
      "name": "No 1", 
      "no_of_items": 0
    }
  ], 
  "next_page": "http://localhost:5000/api/v1/bucketlist/?page=2", 
  "prev_page": null, 
  "total_item": 2
}
```


## Testing
* To run tests:  
``` python manage.py test ``` 

* For the coverage report:    
1. ``` coverage run --source=app manage.py test ```   
2. ``` python manage.py test --coverage```   

