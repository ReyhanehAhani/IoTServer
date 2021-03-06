DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS records;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE record (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  ir INTEGER NOT NULL,
  light INTEGER NOT NULL,
  moisture INTEGER NOT NULL,
  temperature INTEGER NOT NULL,
  FOREIGN KEY (device_id) REFERENCES user (id)
);