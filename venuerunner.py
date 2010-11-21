import sqlite3
from flask import Flask, g, render_template, request, redirect, url_for
from contextlib import closing

#VenueRunner classes
import VRForms

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
  db = sqlite3.connect(app.config['DATABASE'])
  #force database to use foreign keys
  #db.execute('PRAGMA foreign_keys = ON')
  return db

# Assume we always need db connection.
@app.before_request
def before_request():
  g.db = connect_db()

@app.after_request
def after_request(response):
  g.db.close()
  return response

@app.route('/favicon.ico')
def favicon():
  return app.send_static_file('favicon.ico')

@app.route('/')
def menu():
  return render_template('menu.html')

@app.route('/customer/<int:customerid>')
def customer(customerid):
  print customerid
  customer = query_db(
      """
      SELECT first_name, last_name, email, lead, follow, signup_date,
      last_seen_date, note FROM customers WHERE id = ?
      """, [customerid], True)
  return render_template('customer.html', customer=customer)

@app.route('/list_customers')
def list_customers():
  customers = query_db(
      """
      SELECT id, first_name, last_name, email, lead, follow, signup_date,
      last_seen_date, note FROM customers
      """)
  return render_template('list_customers.html', customers=customers)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
  form = VRForms.addcustomer()
  if form.validate_on_submit():
    c = g.db.cursor()
    c.execute(
        """
        INSERT INTO customers 
        (first_name, last_name,
         email, lead, follow,
         signup_date, last_seen_date,
         note)
         VALUES
        (?, ?,
         ?, ?, ?,
         ?, ?,
         ?)
        """,
        [request.form['firstname'], request.form['lastname'],
        request.form['email'], request.form.get('lead', False) == 'y', request.form.get('follow', False) == 'y',
        request.form['signup'], request.form['signup'],
        request.form['note']])
    g.db.commit()
    customerid = c.lastrowid
    return redirect(url_for('customer', customerid=customerid)) # do i want to do this?
  return render_template('add_customer.html', form=form)

@app.route('/event/<int:eventid>')
def event(eventid):
  event = query_db(
      'SELECT id, name, date, price, description  FROM events WHERE id = ?',
      [eventid], True)

  customers = query_db(
      """
      SELECT id, first_name, last_name, email, signup_date, last_seen_date FROM customers
      """)
  return render_template('event.html', event=event, customers=customers)

@app.route('/list_events')
def list_events():
  events = query_db(
      """
      SELECT id, name, date, price, description
        FROM events
        ORDER BY date DESC
      """)# limiit low, high
  return render_template('list_events.html', events=events)

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
  form = VRForms.addevent()
  if form.validate_on_submit():
    c = g.db.cursor()
    c.execute(
        """
        INSERT INTO events (name, date, price, description)
        VALUES (?, ?, ?, ?)
        """,
        [request.form['name'], request.form['date'],
         request.form['price'], request.form['description']])
    g.db.commit()
    eventid = c.lastrowid
    return redirect(url_for('event', eventid=eventid))
  return render_template('add_event.html', form=form)

def query_db(query, args=(), one=False):
  cur = g.db.execute(query, args)
  rv = [dict((cur.description[idx][0], value)
             for idx, value in enumerate(row)) for row in cur.fetchall()]
  return (rv[0] if rv else None) if one else rv

# dead code, but maybe use in the future
def smart_truncate(content, length=100, suffix='...'):
  if len(content) <= length:
    return content
  else:
    return content[:length].rsplit(' ', 1)[0]+suffix

def htmlify(content):
  content = content.strip()
  return content

if __name__ == '__main__':
  app.run()
