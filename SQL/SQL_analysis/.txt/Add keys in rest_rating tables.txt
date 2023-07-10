-- 1. Добавление ключей таблиц


-- restaurant_info definition
ALTER TABLE restaurant_info RENAME TO old_restaurant_info;
CREATE TABLE restaurant_info
(
  place_id INTEGER,
  latitude REAL,
  longitude REAL,
  name TEXT,
  address TEXT,
  city TEXT,
  state TEXT,
  country TEXT,
  alcohol TEXT,
  smoking_area TEXT,
  dress_code TEXT,
  accessibility TEXT,
  price TEXT,
  url TEXT,
  rambience TEXT,
  franchise TEXT,
  area TEXT,
  other_services TEXT,
  CONSTRAINT place_pk PRIMARY KEY (place_id)
);
INSERT INTO restaurant_info SELECT * FROM old_restaurant_info;


-- consumer_info definition
ALTER TABLE consumer_info RENAME TO old_consumer_info;
CREATE TABLE consumer_info (
	user_id TEXT,
	latitude REAL,
	longitude REAL,
	smoker TEXT,
	drink_level TEXT,
	dress_preference TEXT,
	ambience TEXT,
	transport TEXT,
	marital_status TEXT,
	hijos TEXT,
	birth_year INTEGER,
	interest TEXT,
	personality TEXT,
	religion TEXT,
	activity TEXT,
	color TEXT,
	weight INTEGER,
	budget TEXT,
	height REAL,
	CONSTRAINT user_pk PRIMARY KEY (user_id)
	
);
INSERT INTO consumer_info SELECT * FROM old_consumer_info;


-- consumer_cuisine definition
ALTER TABLE сonsumer_cuisine RENAME TO old_сonsumer_cuisine;
CREATE TABLE сonsumer_cuisine (
	line_number INTEGER,
  	user_id TEXT,
  	u_cuisine TEXT,
  	CONSTRAINT line_number_cc PRIMARY KEY (line_number),
  	FOREIGN KEY(user_id) REFERENCES consumer_info(user_id)
);
INSERT INTO сonsumer_cuisine SELECT * FROM old_сonsumer_cuisine;


-- consumer_payment definition
ALTER TABLE consumer_payment RENAME TO old_consumer_payment;
CREATE TABLE consumer_payment (
	line_number INTEGER,
  	user_id TEXT,
  	u_payment TEXT,
  	CONSTRAINT line_number_cp PRIMARY KEY (line_number),
  	FOREIGN KEY(user_id) REFERENCES consumer_info(user_id)
);
INSERT INTO consumer_payment SELECT * FROM old_consumer_payment;


-- rating definition
ALTER TABLE rating RENAME TO old_rating;
CREATE TABLE rating (
	line_number INTEGER,
	user_id TEXT,
	place_id INTEGER,
	rating INTEGER,
	food_rating INTEGER,
	service_rating INTEGER,
  	CONSTRAINT line_number_r PRIMARY KEY (line_number),
  	FOREIGN KEY(user_id) REFERENCES consumer_info(user_id),
  	FOREIGN KEY(place_id) REFERENCES restaurant_info(place_id)
);
INSERT INTO rating SELECT * FROM old_rating;


-- restaurant_cuisine definition
ALTER TABLE restaurant_cuisine RENAME TO old_restaurant_cuisine;
CREATE TABLE restaurant_cuisine (
	line_number INTEGER,
	place_id INTEGER,
	r_cuisine TEXT,
	CONSTRAINT line_number_rc PRIMARY KEY (line_number),
	FOREIGN KEY(place_id) REFERENCES restaurant_info(place_id)
);
INSERT INTO restaurant_cuisine SELECT * FROM old_restaurant_cuisine;


-- restaurant_parking definition
ALTER TABLE restaurant_parking RENAME TO old_restaurant_parking;
CREATE TABLE restaurant_parking (
	line_number INTEGER,
	place_id INTEGER,
	parking_lot TEXT,
	CONSTRAINT line_number_rp PRIMARY KEY (line_number),
	FOREIGN KEY(place_id) REFERENCES restaurant_info(place_id)
);
INSERT INTO restaurant_parking SELECT * FROM old_restaurant_parking;


-- restaurant_payment definition
ALTER TABLE restaurant_payment RENAME TO old_restaurant_payment;
CREATE TABLE restaurant_payment (
	line_number INTEGER,
	place_id INTEGER,
	r_payment TEXT,
	CONSTRAINT line_number_rpay PRIMARY KEY (line_number),
	FOREIGN KEY(place_id) REFERENCES restaurant_info(place_id)
);
INSERT INTO restaurant_payment SELECT * FROM old_restaurant_payment;


-- restaurant_working_time definition
ALTER TABLE  restaurant_working_time RENAME TO old_restaurant_working_time;
CREATE TABLE  restaurant_working_time (
	line_number INTEGER,
	place_id INTEGER,
  	hours TEXT,
  	days TEXT,
  	CONSTRAINT line_number_rwt PRIMARY KEY (line_number),
  	FOREIGN KEY(place_id) REFERENCES restaurant_info(place_id)
);
INSERT INTO restaurant_working_time SELECT * FROM old_restaurant_working_time;