# Item Catalog Web App
By Madisetty Prathyusha
This web app is a project for the Udacity [FSND Course](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## About
This project is a RESTful web application utilizing the Flask framework which accesses a SQL database that populates book categories and their editions. OAuth2 provides authentication for further CRUD functionality on the application. Currently OAuth2 is implemented for Google Accounts.

## In This Project
This project has one main Python module `main_file.py` which runs the Flask application. A SQL database is created using the `Setup_file.py` module and you can populate the database with test data using `Init_file.py`.
The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of the application.

# Setup_file.py
This file completes the creation of 2 tables.One table consists of the columns category name and id.The second table consists of the columns bookname,published year,booktype,author,price and id.
# Init_file.py
This file consists of sample data for the tables created.When we execute this file,the sample data will be successfully inserted into tables created. 
# main_file.py
This files contains code of all the functions for add,edit and delete book categories and book details.
## Skills Required
1. Python
2. HTML
3. CSS
4. OAuth
5. Flask Framework
6. DataBaseModels
## Installation
There are some dependancies and a few instructions on how to run the application.
Seperate instructions are provided to get GConnect working also.

## Dependencies
- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)



## How to Install
1. Download and install Vagrant.

2. Download and install VirtualBox.

3. Clone or download the Vagrant VM configuration file from here.

4. Open the above directory and navigate to the vagrant/ sub-directory.

5. Open terminal, and type

     vagrant up
	 
   This will cause Vagrant to download the Ubuntu operating system and install it. This may take quite a while depending on how fast your Internet connection is.

6. After the above command succeeds, connect to the newly created VM by typing the following command:

     vagrant ssh
	 
7. Type cd /vagrant/ to navigate to the shared repository.
8. The app imports requests which is not on this vm. Run pip install requests

    Or you can simply Install the dependency libraries (Flask, sqlalchemy, requests,psycopg2 and oauth2client)

9.  Setup application database `python /bookhub/Setup_file.py`
10. *Insert sample data `python /bookhub/Init_file.py`
11. Run application using `python /bookhub/main_file.py`
12. Access the application locally using http://localhost:9000

*Optional step(s)

## Using Google Login
To get the Google login working there are a few additional steps:

1. Go to [Google Dev Console](https://console.developers.google.com)
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'bookhub'
7. Authorized JavaScript origins = 'http://localhost:9000'
8. Authorized redirect URIs = 'http://localhost:9000/login' && 'http://localhost:9000/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the `data-clientid` in login.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Place JSON file in bookhub directory that you cloned from here
14. Run application using `python /bookhub/main_file.py`

## JSON Endpoints
The following are open to the public:

Books Catalog JSON: `/Bookhub/JSON`
    - Displays the whole books models catalog. Book Categories and all models.

Book Categories JSON: `/bookhub/bookColumns/JSON`
    - Displays all Book categories
All Book Editions: `/bookhub/editions/JSON`
	- Displays all Book Models

Book Edition JSON: `/bookhub/<path:book_name>/editions/JSON`
    - Displays Book models for a specific Book category

Book Category Edition JSON: `/bookhub/<path:book_name>/<path:edition_name>/JSON`
    - Displays a specific Book category Model.
	
## How to use
* You can browse through the website to find out the different categories of books.
* You can also create you own items after you login.
* Only the users who created the item have the ability to add, edit, and delete it.
* You can edit an item that you created.
* You can also delete the item that you created.
* Once you log out. You can lost your right to change it.
