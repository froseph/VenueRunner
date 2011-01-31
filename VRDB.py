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

def customer_update(customer_id, first_name, last_name, email, lead, follow, signup_date, note):
  c = g.db.custor()
  c.execute(
      """
      UPDATE customers
      SET first_name = ?, last_name = ?
      email = ?, lead = ?, follow = ?,
      signup_date, note
      """,
      [first_name, last_name, email, lead, follow, signup_adte, note])
  g.db.commit()

def customer_delete(customer_id):
  c = g.db.cursor()
  c.execute('DELETE FROM customers WHERE customer_id = ?', [customer_id])
  g.db.commit()

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

#returns new event id
def event_add(name, date, description):
  c = g.db.cursor()
  c.execute(
      """
      INSERT INTO events (name, date, description)
      VALUES (?, ?, ?)
      """,
      [name, date, description])
  g.db.commit()
  return c.lastrowid

def event_update(event_id, name, date, description):
  c = g.db. cursor()
  c.execute(
      """
      UPDATE events
      SET name = ?, date = ?, description = ?
      WHERE event_id = ?
      """,
      [name, date, description, event_id])
  g.db.commit()

def event_delete(event_id):
  c = g.db.cursor()
  c.execute('DELETE FROM events where event_id = ?', [event_id])
  g.db.commit()

def event_attendence(event_id):
  return query_db(
      'SELECT customer_id, amount, coupon_id FROM event_attendence WHERE event_id = ?',
      [event_id])

def event_attendence_add(event_id, customer_id, amount, entry_time = None, coupon_id = None, sku_id = None):
  if entry_time is None:
    entry_time = time.time()

  c = g.db.cursor()
  c.execute(
      """
      INSERT INTO event_attendence
        (event_id, customer_id, entry_time, amount, coupon_id, sku)
      VALUES (?, ?, ?, ?, ?, ?)
      """,
      [event, customer_id, entry_time, amount, coupon_id, sku_id])
  g.db.commit()

def event_attendence_update(event_id, customer_id, amount, entry_time, coupon_id, sku_id):
  c = g.db.cursor()
  c.execute(
      """
      UPDATE event_attendence
      SET entry_time = ?, amount = ?, coupon_id = ?, sku = ?
      WHERE event_id = ? AND customer_id = ?
      """,
      [entry_time, amount, coupon_id, sku, event_id, customer_id])
  g.db.commit()

def event_attendence_delete(event_id, customer_id):
  c = g.db.cursor()
  c.execute(
    """
    DELETE FROM event_attendence WHERE event_id = ? and customer_id = ?
    """,
    [event_id, customer_id])
  g.db.execute()
