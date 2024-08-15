# Epic_event

EpicEvents is a CRM (Customer Relationship Management) application designed to manage clients, contracts, and events for a company.
The application uses a PostgreSQL as database and SQLAlchemy as ORM.

## Prerequisites

- Python 3.9 or higher
- PostgreSQL Server
- Git

## Installation

1. ***Clone the Repository***

Clone the repository from GitHub to your local machine.

```
git clone https://github.com/Guwoop00/Epic_event.git
```


2. ***Install dependencies***

Use requirements.txt to install all dependencies

```
pip install -r requirements.txt
```


3. ***Configure Environment Variables***

The `.env` file is used to configure database connection parameters and other settings.
Create a `.env` file in the root directory and enter your database info in it:



4. ***Initialize the Database***

Run the following command to initialize the database and create the first admin user, it will allow you to create your password:

```
python3 -m init_db
```


5. ***Run the app***

Run the following command to run the app

```
python3 -m main_controller 
```
