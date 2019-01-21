# Item-Catalog-Project
This project is a web app for the Udacity Full Stack Nanodegree Program.

### Description

A RESTful web application using the Python framework Flask along with implementing third-party OAuth authentication for further CRUD functionality. It accesses a SQL database that populates categories and their items. The application provides a list of items within a variety of categories as well as a user registration and authentication system (Google Accounts). Registered users will have the ability to post, edit and delete their own items.

### Required Libraries and Dependencies

* [Vagrant](https://www.vagrantup.com/)
* [Virtual Box](https://www.virtualbox.org/wiki/Downloads)
* [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)

### Installation

1. Install Vagrant and VirtualBox
2. Clone the Udacity Vagrantfile
3. Go to Vagrant directory and either clone this repo or download and place zip here
4. Launch the Vagrant VM (`vagrant up`)
5. Log into Vagrant VM (`vagrant ssh`)
6. Navigate to `cd/vagrant` as instructed in terminal
7. Run `sudo pip install requests` (the app imports requests that is not on this vm)
8. Navigate to folder location of cloned repo.
9. Setup application database `python database_setup.py`
10. Insert data `python hikingitems.py`
11. Run application using `python application.py`
12. Access the application locally using [http://localhost:8000]

### JSON Endpoint

Catalog JSON: [http://localhost:8000/catalog/JSON] - Displays the whole catalog.
