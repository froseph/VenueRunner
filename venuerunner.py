import sqlite3
from flask import Flask, g, render_template, request, redirect, url_for 
from werkzeug.datastructures import MultiDict
from contextlib import closing

#VenueRunner classes
import VRForms
import VRDB

# Config - TODO use separate file!
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

#TODO write save functionality
@app.route('/customer/<int:customer_id>', methods=['GET', 'POST'])
def customer(customer_id):
  customer = VRDB.customer(customer_id)
  form = VRForms.addcustomer(MultiDict(customer))
  return render_template('customer.html', form=form)

@app.route('/list_customers')
def list_customers():
  customers = VRDB.customers()
  return render_template('list_customers.html', customers=customers)

#posts form and redirects to the new customer. Really should let the app
# decide what is best to do rather than redirect!
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
  form = VRForms.addcustomer()
  if form.validate_on_submit():
    lead = request.form.get('lead', False) == 'y'
    follow = request.form.get('follow', False) == 'y'
    customer_id = VRDB.customer_add(first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        email=request.form['email'],
        lead=lead,
        follow=follow,
        signup_date=request.form['signup'],
        note=request.form['note'])
    return redirect(url_for('customer', customer_id=customer_id))
  return render_template('add_customer.html', form=form)

#REST thingy to add customers
@app.route('/customer/add', methods=['POST'])
def post_add_customer():
  form = VRForms.addcustomer()
  customer_id = -1;
  errors = None;
  if form.validate_on_submit():
    lead = request.form.get('lead', False) == 'y'
    follow = request.form.get('follow', False) == 'y'
    customer_id = customer_add(first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        email=request.form['email'],
        lead=lead,
        follow=follow,
        signup_date=request.form['signup'],
        note=request.form['note'])
  return jsonify(errors=errors, customer_id =customer_id)

#TODO write save functionality
@app.route('/event/<int:event_id>')
def event(event_id):
  event = VRDB.event(event_id)
  form = VRForms.addevent(MultiDict(event))
  customers = VRDB.customers()
  attendence = VRDB.event_attendence(event_id)

  return render_template('event.html', form=form, customers=customers)

@app.route('/list_events')
def list_events():
  events = VRDB.events()
  return render_template('list_events.html', events=events)

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
  form = VRForms.addevent()
  if form.validate_on_submit():
    event_id = VRDB.event_add(name=request.form['name'], date=request.form['date'],
        description=request.form['description'])
    app.logger.debug('moo') # XXX
    return redirect(url_for('event', event_id=event_id))
  return render_template('add_event.html', form=form)

@app.route('/event/record_attendence', methods=['POST'])
def record_attendence():
  #validate
  #record
  # structure
  # list
  #     customer id
  #     price
  #     event
  return jsonify(success=true)


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
