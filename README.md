# RESTApi
Created a RESTful API using FastAPI that allows users to manage a collection of books with user authentication and password hashing.

      Setup and Run
Prerequisites
Python 3.7+
Pip (Python package installer)
                      Installation
Clone the repository:
sh
Copy code
git clone <repository_url>
cd <repository_name>

Create and activate a virtual environment:

sh
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install the required dependencies:

sh
Copy code
pip install -r requirements.txt
Running the API
Start the FastAPI server:

sh
Copy code
uvicorn main:app --reload
The API will be accessible at http://127.0.0.1:8000.

API Endpoints

          Books
Get All Books
Endpoint: /books
Method: GET
      Response:
json
Copy code
{
    "books": [
        {
            "id": "string",
            "title": "string",
            "author": "string",
            "published_date": "string",
            "isbn": "string"
        },
        ...
    ]
}
        Get Book by Index
Endpoint: /books/{id}
Method: GET
        Response:
json
Copy code
{
    "id": "string",
    "title": "string",
    "author": "string",
    "published_date": "string",
    "isbn": "string"
}
      Add a New Book
Endpoint: /books
Method: POST
Authentication: Required
      Request Body:
json
Copy code
{
    "title": "string",
    "author": "string",
    "published_date": "string",
    "isbn": "string"
}
Response:
json
Copy code
{
    "book_id": "string"
}
      Update a Book
Endpoint: /books/{id}
Method: PUT
Authentication: Required
      Request Body:
json
Copy code
{
    "title": "string",
    "author": "string",
    "published_date": "string",
    "isbn": "string"
}
Response:
json
Copy code
{
    "id": "string",
    "title": "string",
    "author": "string",
    "published_date": "string",
    "isbn": "string"
}
        Delete a Book
Endpoint: /books/{id}
Method: DELETE
Authentication: Required
      Response:
json
Copy code
{
    "id": "string",
    "title": "string",
    "author": "string",
    "published_date": "string",
    "isbn": "string"
}
Authentication

      Register a New User
Endpoint: /register
Method: POST
      Request Body:
json
Copy code
{
    "username": "string",
    "email": "user@example.com",
    "password": "string"
}
Response:

json
Copy code
{
    "message": "User registered successfully"
}
        Login
Endpoint: /token
Method: POST
      Request Body:
json
Copy code
{
    "username": "string",
    "password": "string"
}
Response:
json
Copy code
{
    "access_token": "string",
    "token_type": "bearer"
}

