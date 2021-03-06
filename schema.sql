CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255),
    email VARCHAR(255),
    lead BOOLEAN NOT NULL,
    follow BOOLEAN NOT NULL,
    signup_date DATE NOT NULL,
    last_seen_date DATE NOT NULL,
    note STRING
);

-- Future feature?
CREATE TABLE IF NOT EXISTS customer_properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING NOT NULL,
    type INTEGER NOT NULL, -- Used to implement custom logic. Internal for now.
    description STRING
);

-- Future feature?
CREATE TABLE IF NOT EXISTS customer_property_map (
    customer_id INTEGER KEY,
    customer_property INTEGER KEY NOT NULL,
    value INTEGER,
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(customer_property) REFERENCES customer_properties(id),
    PRIMARY KEY (customer_id, customer_property)
);

CREATE TABLE IF NOT EXISTS mailinglists (
    id INTEGER PRIMARY KEY autoincrement,
    name STRING NOT NULL,
    description STRING
);

CREATE TABLE IF NOT EXISTS customer_mailinglist_map (
    customer_id INTEGER KEY,
    mailing_id INTEGER KEY,
    status TINYINTEGER NOT NULL,
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(mailing_id) REFERENCES mailinglists(id),
    PRIMARY KEY (customer_id, mailing_id)
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    name STRING NOT NULL,
    description STRING
);

CREATE TABLE IF NOT EXISTS event_attendence (
    event_id INTEGER KEY,
    customer_id INTEGER KEY,
    entry_time DATETIME NOT NULL,
    amount INTEGER NOT NULL,
    coupon_id INTEGER,
    sku INTEGER,
    FOREIGN KEY(event_id) REFERENCES events(id),
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(sku) REFERENCES sku(id),
    PRIMARY KEY (event_id, customer_id)
);

CREATE TABLE IF NOT EXISTS coupons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING NOT NULL,
    value INTEGER NOT NULL,
    description STRING
);

-- Add meta value for 
CREATE TABLE IF NOT EXISTS sku (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING NOT NULL,
    price INTEGER NOT NULL,
    description STRING
);

-- Future feature
-- create table class
