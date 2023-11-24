-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS cariba_test_db;
CREATE USER IF NOT EXISTS 'cariba_test'@'localhost' IDENTIFIED BY 'cariba_test_pwd';
GRANT ALL PRIVILEGES ON `cariba_test_db`.* TO 'cariba_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'cariba_test'@'localhost';
FLUSH PRIVILEGES;
