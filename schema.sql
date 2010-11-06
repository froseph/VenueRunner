CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255),
    email VARCHAR(255),
    lead BOOL NOT NULL, -- could make this generic
    follow BOOL NOT NULL, -- could make this generic
    signup_date DATE NOT NULL,
    last_seen_date DATE NOT NULL,
    notes STRING
);

-- volunteer, comped, etc.
CREATE TABLE IF NOT EXISTS customer_flags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING NOT NULL,
    type STRING NOT NULL, -- is this needed? what is this needed for?
    description STRING
);

CREATE TABLE IF NOT EXISTS customer_flags_map (
    customer_id INTEGER KEY,
    customer_flag INTEGER NOT NULL,
    value INTEGER, -- is this needed, idea is to support things like work trade/purchase pack
    FOREIGN KEY(customer_id) REFERENCES custmoers(id),
    FOREIGN KEY(customer_flag) REFERENCES customer_flags(id),
    PRIMARY KEY (customer_id, customer_flag)
);

CREATE TABLE IF NOT EXISTS mailinglists (
    id INTEGER PRIMARY KEY autoincrement,
    name STRING NOT NULL,
    description STRING
);

CREATE TABLE IF NOT EXISTS user_mailinglist_map (
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
    price INTEGER,
    description STRING
);

CREATE TABLE IF NOT EXISTS coupons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING NOT NULL,
    value INTEGER NOT NULL,
    description STRING
);

CREATE TABLE IF NOT EXISTS event_attendence (
    event_id INTEGER KEY,
    customer_id INTEGER KEY,
    entrytime DATETIME NOT NULL,
    paid INTEGER NOT NULL,
    coupon_id INTEGER,
    FOREIGN KEY(event_id) REFERENCES events(id),
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    PRIMARY KEY (event_id, customer_id)
);
