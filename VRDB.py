from flask import g

#TODO error handling
#TODO objectify?

#utility functions
def query_db(query, args=(), one=False):
  cur = g.db.execute(query, args)
  rv = [dict((cur.description[idx][0], value)
             for idx, value in enumerate(row)) for row in cur.fetchall()]
  return (rv[0] if rv else None) if one else rv

#customer functions
def customers():
  return query_db(
      """
      SELECT id, first_name, last_name, email, lead, follow, signup_date,
      last_seen_date, note FROM customers
      """)

def customer(customer_id):
  return query_db(
      """
      SELECT first_name, last_name, email, lead, follow, signup_date,
      last_seen_date, note FROM customers WHERE id = ?
      """, [customer_id], True)

# returns the new customer id
def customer_add(first_name, last_name, email, lead, follow, signup_date, note):
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
        [first_name, last_name, email, lead, follow, signup_date, signup_date,
        note])
    g.db.commit()
    return c.lastrowid

#event functions

def events():
  return query_db(
      """
      SELECT id, name, date, price, description
        FROM events
        ORDER BY date DESC
      """)

def event(event_id):
  return query_db(
      'SELECT id, name, date, price, description  FROM events WHERE id = ?',
      [event_id], True)

def event_attendence(event_id):
  return query_db(
      'SELECT customer_id, paid, coupon_id FROM event_attendence WHERE event_id = ?',
      [event_id])

#returns new event id
def event_add(name, date, price, description):
  c = g.db.cursor()
  c.execute(
      """
      INSERT INTO events (name, date, price, description)
      VALUES (?, ?, ?, ?)
      """,
      [name, date, price, description])
  g.db.commit()
  return c.lastrowid
