import sqlite3
from flask import Flask, g, render_template
from contextlib import closing

# Config - use separate file!
DEBUG = True # Remove in production code
DATABASE = 'venue.db'
PASSWORD = 'moo'
SECRET_KEY = 'SEKERETKEY'
SCHEMA_FILE = 'schema.sql'

app = Flask(__name__)
app.config.from_object(__name__)

#set up the application
def init_db():
  with closing(connect_db()) as db:
    with app.open_resource(app.config['SCHEMA_FILE']) as f:
      db.cursor().executescript(f.read())
    db.commit()

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

# Assume we always need db connection.
@app.before_request
def before_request():
  g.db = connect_db()

@app.after_request
def after_request(response):
  g.db.close()
  return response

@app.route('/')
def menu():
  return render_template('menu.html')

@app.route('/customer/<customerid>')
def customer():
  return render_template('customer.html')

@app.route('/list_customers')
def list_customers():
  return render_template('list_customers.html')

@app.route('/add_customer')
def list_customers():
  return render_template('add_customer.html')

@app.route('/event/<eventid>')
def event(eventid):
  return render_template('event.html')

@app.route('/list_events')
def list_events():
  return render_template('list_events.html')

@app.route('/add_event')
def add_event():
  return render_template('add_event.html')

if __name__ == '__main__':
  app.run()
