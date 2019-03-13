from flask import(
    Flask,
    render_template,
    url_for,
    request,
    redirect,
    flash,
    make_response,
    jsonify
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Setup_file import Base, BookYard, BookName, GmailUser
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

engine = create_engine('sqlite:///bookyard.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "BookStore"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery state token
library = session.query(BookYard).all()

# completed
# login


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    library = session.query(BookYard).all()
    obj2 = session.query(BookName).all()
    return render_template('login.html',
                           STATE=state, library=library, obj2=obj2)
# return render_template('myhome.html', STATE=state
# library=library,obj2=obj2)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
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

    # see if user exists, if it doesn't make a new one
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
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output

# completed
# User Helper Functions


def createUser(login_session):
    User1 = GmailUser(name=login_session['username'], email=login_session[
                   'email'])
    session.add(User1)
    session.commit()
    user = session.query(GmailUser).filter_by(
                         email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(GmailUser).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(GmailUser).filter_by(email=email).one()
        return user.id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session

# completed
# Home


@app.route('/')
@app.route('/home')
def home():
    library = session.query(BookYard).all()
    return render_template('myhome.html', library=library)

# completed
# Book Category for admins


@app.route('/Library')
def Library():
    try:
        if login_session['username']:
            name = login_session['username']
            library = session.query(BookYard).all()
            obj1 = session.query(BookYard).all()
            obj2 = session.query(BookName).all()
            return render_template('myhome.html', library=library,
                                   obj1=obj1, obj2=obj2, uname=name)
    except:
        return redirect(url_for('showLogin'))

# completed
# Showing book based on book category


@app.route('/Library/<int:objid>/AllCompanys')
def showBooks(objid):
    library = session.query(BookYard).all()
    obj1 = session.query(BookYard).filter_by(id=objid).one()
    obj2 = session.query(BookName).filter_by(bookyardid=objid).all()
    try:
        if login_session['username']:
            return render_template('showBooks.html', library=library,
                                   obj1=obj1, obj2=obj2,
                                   uname=login_session['username'])
    except:
        return render_template('showBooks.html',
                               library=library, obj1=obj1, obj2=obj2)


# Add New Book Category


@app.route('/Library/addBookName', methods=['POST', 'GET'])
def addBookName():
    if "username" not in login_session:
        flash("Please login first")
        return redirect(url_for("showLogin"))
    if request.method == 'POST':
        book = BookYard(name=request.form['name'],
                        user_id=login_session['user_id'])
        session.add(book)
        session.commit()
        return redirect(url_for('Library'))
    else:
        return render_template('addBookName.html', library=library)


# Edit Book Category
@app.route('/Library/<int:objid>/edit', methods=['POST', 'GET'])
def editBookName(objid):
    if "username" not in login_session:
        flash("Please login first")
        return redirect(url_for("showLogin"))
    editBook = session.query(BookYard).filter_by(id=objid).one()
    creator = getUserInfo(editBook.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot edit this Book Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('Library'))
    if request.method == "POST":
        if request.form['name']:
            editBook.name = request.form['name']
        session.add(editBook)
        session.commit()
        flash("Book Category Edited Successfully")
        return redirect(url_for('Library'))
    else:
        # library is global variable we can them in entire application
        return render_template('editBookName.html',
                               obj=editBook, library=library)


# Delete Book Category
@app.route('/Library/<int:objid>/delete', methods=['POST', 'GET'])
def deleteBookName(objid):
    if "username" not in login_session:
        flash("Please login first")
        return redirect(url_for("showLogin"))
    obj = session.query(BookYard).filter_by(id=objid).one()
    creator = getUserInfo(obj.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot Delete this Book Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('Library'))
    if request.method == "POST":
        session.delete(obj)
        session.commit()
        flash("Book Category Deleted Successfully")
        return redirect(url_for('Library'))
    else:
        return render_template('deleteBookName.html', obj=obj, library=library)


# Add New Book Name Details in a specific category
@app.route('/Library/addCompany/addBookInformation/<string:objname>/add',
           methods=['GET', 'POST'])
def addBookInformation(objname):
    if "username" not in login_session:
        flash("Please login first")
        return redirect(url_for("showLogin"))
    obj1 = session.query(BookYard).filter_by(name=objname).one()
    # See if the logged in user is not the owner of book
    creator = getUserInfo(obj1.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't add new book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showBooks', objid=obj1.id))
    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        booktype = request.form['booktype']
        author = request.form['author']
        price = request.form['price']
        bookdetails = BookName(name=name,
                               year=year,
                               booktype=booktype,
                               author=author,
                               price=price,
                               bookyardid=obj1.id,
                               gmailuser_id=login_session['user_id'])
        session.add(bookdetails)
        session.commit()
        return redirect(url_for('showBooks', objid=obj1.id))
    else:
        return render_template('addBookInformation.html',
                               objname=obj1.name, library=library)


# Edit Book details
@app.route('/Library/<int:objid>/<string:obj3name>/edit',
           methods=['GET', 'POST'])
def editBookInformation(objid, obj3name):
    if "username" not in login_session:
        flash("Please login first")
        return redirect(url_for("showLogin"))
    obj = session.query(BookYard).filter_by(id=objid).one()
    bookdetails = session.query(BookName).filter_by(name=obj3name).one()
    # See if the logged in user is not the owner of book
    creator = getUserInfo(obj.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't edit this book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showBooks', objid=obj.id))
    # POST methods
    if request.method == 'POST':
        bookdetails.name = request.form['name']
        bookdetails.year = request.form['year']
        bookdetails.booktype = request.form['booktype']
        bookdetails.author = request.form['author']
        bookdetails.price = request.form['price']
        session.add(bookdetails)
        session.commit()
        flash("Book Edited Successfully")
        return redirect(url_for('showBooks', objid=objid))
    else:
        return render_template('editbookInformation.html',
                               objid=objid, bookdetails=bookdetails,
                               library=library)


# Delte Book Details


@app.route('/Library/<int:objid>/<string:obj3name>/delete',
           methods=['GET', 'POST'])
def deleteBookInformation(objid, obj3name):
    if "username" not in login_session:
        flash("Please login first")
        return redirect(url_for("showLogin"))
    obj = session.query(BookYard).filter_by(id=objid).one()
    bookdetails = session.query(BookName).filter_by(name=obj3name).one()
    # See if the logged in user is not the owner of book
    creator = getUserInfo(obj.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't delete this book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showBooks', objid=obj.id))
    if request.method == "POST":
        session.delete(bookdetails)
        session.commit()
        flash("Deleted book Successfully")
        return redirect(url_for('showBooks', objid=objid))
    else:
        return render_template('deleteBookInformation.html',
                               objid=objid, bookdetails=bookdetails,
                               library=library)


# Logout from current user


@app.route('/logout')
def logout():
    access_token = login_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected....'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None,
                  headers={'content-type': 'application/x-www-form-urlencoded'}
                  )[0]

    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps(
                                'Successfully disconnected user..'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('home'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# completed
# Json


@app.route('/Library/JSON')
def allBooksJSON():
    bookcolumns = session.query(BookYard).all()
    category_dict = [c.serialize for c in bookcolumns]
    for c in range(len(category_dict)):
        books = [i.serialize for i in session.query(
                 BookName).filter_by(bookyardid=category_dict[c]["id"]).all()]
        if books:
            category_dict[c]["book"] = books
    return jsonify(BookYard=category_dict)

####


@app.route('/Library/bookColumns/JSON')
def categoriesJSON():
    books = session.query(BookYard).all()
    return jsonify(bookColumns=[c.serialize for c in books])

####


@app.route('/Library/book/JSON')
def itemsJSON():
    items = session.query(BookName).all()
    return jsonify(book=[i.serialize for i in items])

#####


@app.route('/Library/<path:book_name>/book/JSON')
def categoryItemsJSON(book_name):
    bookCat = session.query(BookYard).filter_by(name=book_name).one()
    books = session.query(BookName).filter_by(bookname=bookCat).all()
    return jsonify(bookEdtion=[i.serialize for i in books])

#####


@app.route('/Library/<path:book_name>/<path:edition_name>/JSON')
def ItemJSON(book_name, edition_name):
    bookCat = session.query(BookYard).filter_by(name=book_name).one()
    bookEdition = session.query(BookName).filter_by(
           name=edition_name, bookname=bookCat).one()
    return jsonify(bookEdition=[bookEdition.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=9000)
