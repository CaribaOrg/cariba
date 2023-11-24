-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS cariba_dev_db;
CREATE USER IF NOT EXISTS 'cariba_dev'@'localhost' IDENTIFIED BY 'cariba_dev_pwd';
GRANT ALL PRIVILEGES ON `cariba_dev_db`.* TO 'cariba_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'cariba_dev'@'localhost';
FLUSH PRIVILEGES;
