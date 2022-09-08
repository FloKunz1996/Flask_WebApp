# Welcome to CarVentory!

**CarVentory** is an app that allows you to manage your vehicle inventory.


# How to run the application

First navigate to the directory where the code is, and run

    pip install -r requirements.txt
Next, log into your MySQL environment, create a database, then copy, paste and run the scripts in `db.sql`.
Afterwards, edit the python code with the correct MySQL details.

    SQL_USERNAME = "root"
    SQL_PASSWORD = "put your password here"
    SQL_HOST = "localhost" ## if not running on localhost, put the IP address of the database server here.
    SQL_DATABASE = "database name"

Save the file, then run the app.

    python app.py

# Details about the Application
- The SQL script used to create the database is called db.sql.
- The ADMIN account credentials are: 
	- Username: "ADMIN"
	- Password: "Password_123"
- The application URL is http://localhost:7080/
- The app runs on your local machine (Localhost), on port 7080. 
- The passwords are encrypted using SHA_256.

# How to run through Docker
Pre-requisites:
* Docker
* docker-compose

Execute `docker-compose -f docker-compose.yml up api mysql`

The first time the API container will be built. After the first time both containers start normally.