### Flask application ###
###===================###

## IMPORTS
##==========
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
import datetime
# anti-forgery state token imports
from flask import session as login_session
import random, string
# GConnect imports
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

## FLASK
##========
# create instance of Flask class with name of running app as arg
app = Flask(__name__)

## GConnect CLIENT_ID
##=====================
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog App"

## DB CONNECTION
##================
# Create session and connect to DB
engine = create_engine('sqlite:///HikingCatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


## LOGIN
##========
# decorator wraps our function inside app.route() created by Flask
# if either route is sent by the browser, our defined function is executed
# @app.route will call the function that follows it whenever the webserver receives 
# a request with the url that matches its arg

# login - create a state token to prevent request forgery
# store it in the session for later validation
@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
	login_session['state'] = state
	# return "The current session state is %s" %login_session['state']
	return render_template('login.html', STATE=state)

# GConnect
@app.route('/gconnect', methods=['POST'])
def gconnect():
	# Validate state token
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	# Obtain authorization code, now compatible with Python3
	request.get_data()
	code = request.data.decode('utf-8')

	try:
		# Upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Check that the access token is valid.
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
	# Submit request, parse response - Python3 compatible
	h = httplib2.Http()
	response = h.request(url, 'GET')[1]
	str_response = response.decode('utf-8')
	result = json.loads(str_response)

	# If there was an error in the access token info, abort.
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is used for the intended user.
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is valid for this app.
	if result['issued_to'] != CLIENT_ID:
		response = make_response(json.dumps("Token's client ID does not match app's."), 401)
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response

	# Check to see if user is already logged in
	stored_access_token = login_session.get('access_token')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_access_token is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Store the access token in the session for later use.
	login_session['access_token'] = credentials.access_token
	login_session['gplus_id'] = gplus_id

	# Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()

	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']

	# see if user exists, if it doesn't add new one
	user_id = getUserID(login_session['email'])
	if not user_id:
		user_id = createUser(login_session)
	login_session['user_id'] = user_id

	output = ''
	output += '<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	output += '<img src="'
	output += login_session['picture']
	output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
	flash("you are now logged in as %s" % login_session['username'])
	print "done!"
	return output

# User Helper Functions
def createUser(login_session):
	newUser = User(name=login_session['username'], email=login_session['email'], image=login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email=login_session['email']).one()
	return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

 # DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
	# only disconnect a connected user
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        # response = make_response(json.dumps('Successfully disconnected.'), 200)
        # response.headers['Content-Type'] = 'application/json'
        response = redirect(url_for('showCategories'))
        flash("Successfully disconnected.")
      	return response
    else:
    	# for whatever reason, the given token was invalid
        response = make_response(
        	json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

## FLASK ROUTING
##================
# Homepage - show all categories
@app.route('/')
@app.route('/catalog/')
def showCategories():
	# return "This page will show all categories and latest items"
	categories = session.query(Category).all()
	items = session.query(Item).order_by(desc(Item.date)).limit(6)
	if 'username' not in login_session:
		return render_template('publiccatalog.html', categories = categories, items = items)
	else:
		return render_template('catalog.html', categories = categories, items = items)

# show all items in a specific category
@app.route('/catalog/<path:category_name>/items/')
def showCategory(category_name):
	# return "This page will show a specific category and all its items"
	categories = session.query(Category).all()
	category = session.query(Category).filter_by(name=category_name).one()
	items = session.query(Item).filter_by(category=category).all()
	count = session.query(Item).filter_by(category=category).count()
	return render_template('category.html', category = category.name, categories = categories, items = items, count = count)

# show a specific item
@app.route('/catalog/<path:category_name>/<path:item_name>/')
def showItem(category_name, item_name):
	# return "This page is will show specific item for category %s" % category_name
	categories = session.query(Category).all()
	item = session.query(Item).filter_by(name=item_name).one()
	creator = getUserInfo(item.user_id)
	if 'username' not in login_session or creator.id != login_session['user_id']:
		return render_template('publicitem.html', item = item, categories = categories, category = category_name, creator = creator)
	else:
		return render_template('item.html', item = item, categories = categories, category = category_name, creator = creator)

# add a new item
@app.route('/catalog/addnew/', methods=['GET', 'POST'])
def newItem():
	# return "This page will create a new item"
	if 'username' not in login_session:
		return redirect('/login')
	categories = session.query(Category).all()
	if request.method == 'POST':
		newItem = Item(
			name = request.form['name'], 
			description = request.form['description'],
			date = datetime.datetime.now(),
			user_id=login_session['user_id'], 
			category = session.query(Category).filter_by(name=request.form['category']).one())
		session.add(newItem)
		session.commit()
		flash("New Item Successfully Created!")
		return redirect(url_for('showCategories'))
	else:
		return render_template('newItem.html', categories = categories)

# edit an item
@app.route('/catalog/<path:category_name>/<path:item_name>/edit/', methods=['GET', 'POST'])
def editItem(category_name, item_name):
	# return "This page is for editing item %s" % item_name
	editedItem = session.query(Item).filter_by(name = item_name).one()
	categories = session.query(Category).all()
	if 'username' not in login_session:
		return redirect('/login')
	if editedItem.user_id != login_session['user_id']:
		flash("You are not authorized to edit items you have not created. Please add your own items in order to edit items.")
		return redirect(url_for('showCategories'))
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['description']
		if request.form['category']:
			category = session.query(Category).filter_by(name=request.form['category']).one()
			editedItem.category = category
			dateAdded = datetime.datetime.now()
			editedItem.date = dateAdded
		session.add(editedItem)
		session.commit()
		flash("Item Successfully Edited!")
		return redirect(url_for('showCategory', category_name=editedItem.category.name))
	else:
		return render_template('editItem.html', categories = categories, item = editedItem)

# delete an item
@app.route('/catalog/<path:category_name>/<path:item_name>/delete/', methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
	# return "This page is for deleting menu item %s" % item_name
	itemToDelete = session.query(Item).filter_by(name = item_name).one()
	category = session.query(Category).filter_by(name = category_name).one()
	categories = session.query(Category).all()
	if 'username' not in login_session:
		return redirect('/login')
	if itemToDelete.user_id != login_session['user_id']:
		flash("You are not authorized to delete items you have not created. Please add your own items in order to delete items.")
		return redirect(url_for('showCategories'))
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash("Item Successfully Deleted!")
		return redirect(url_for('showCategory', category_name=category.name))
	else:
		return render_template('deleteItem.html', item = itemToDelete)

## JSON
##========
# making an API Endpoint 
@app.route('/catalog/JSON')
def showCategoriesJSON():
	# return "This page will show all my categories"
	categories = session.query(Category).all()
	category_list = [c.serialize for c in categories]
	for c in range(len(category_list)):
		items = [i.serialize for i in session.query(Item).filter_by(category_id=category_list[c]["id"]).all()]
		if items:
			category_list[c]["Item"] = items
	return jsonify(Category=category_list)


# main app run by python interpreter gets a name var set to __main__
# if statement ensures server only runs if script is executed directly from python interpreter
if __name__ == '__main__':
	# create sessions for users
	app.secret_key = 'super_secret_key'
	# enables debug support to reload server in a code change
	app.debug = True
	# run the local server with our app, made publicly available by listening on all public IPs
	app.run(host = '0.0.0.0', port = 8000)