
DROP DATABASE IF EXISTS barebones;
REVOKE ALL PRIVILEGES ON barebones.* FROM 'barebones'@'localhost';
DROP USER 'barebones'@'localhost';
FLUSH PRIVILEGES;
