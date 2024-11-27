# Donify - Fundraising Platform

Donify is a fundraising platform designed to manage multiple target projects efficiently. It facilitates donations from users and distributes them among various projects based on priority and funding requirements.

## Project Description

Donify enables users to contribute to different projects by making donations. Each project has a title, description, and a funding goal. Once a project reaches its funding goal, it is marked as closed, and donations are then redirected to the next project in line.

## Key Features

- Multiple Target Projects
- First In, First Out Donation Principle
- User Donations: Users can make donations to the fund and view their donation history.

## Technologies

- FastAPI - for creating the web application.
- SQLAlchemy - ORM for working with the database.
- SQLite - database for storing links.
- Redoc - for documentation and API visualization.

## Installation and Usage

Clone the repository and navigate to it on the command line:

```
git clone
```

```
cd cat_charity_fund
```

Create and activate a virtual environment:

```
python3 -m venv venv
```

*If you have Linux/macOS

```
source venv/bin/activate
```

*If you have windows

```
source code venv/scripts/activate
```

Install depending on the require.txt file:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Run the script:

```
uvicorn app.main:app (--reload)
```

## Query examples

### Get All Charity Projects.
#### GET - http://127.0.0.1:8000/charity_project/

```
#RESPONSE
{
  "name": "Project_1",
  "description": "desc of project",
  "full_amount": 40000,
  "id": 1,
  "invested_amount": 8000,
  "fully_invested": false,
  "create_date": "2024-05-13T10:00"
}
```

### Create Donation.
#### POST - http://127.0.0.1:8000/donation/

```
#REQUEST
{
  "full_amount": 10,
  "comment": "string"
}


#RESPONSE
{
  "name": "Project_1",
  "description": "desc of project",
  "full_amount": 40000,
  "id": 1,
  "invested_amount": 8000,
  "fully_invested": false,
  "create_date": "2024-05-13T10:00"
}
```


### Get User Donations.
#### GET - http://127.0.0.1:8000/donation/my

```
#RESPONSE
  {
    "full_amount": 10,
    "comment": "string",
    "id": 1,
    "create_date": "2024-05-13T10:00"
  }
```


## Contacts

Backend by: Eric Ivanov
- e-mail: ldqfv@mail.ru