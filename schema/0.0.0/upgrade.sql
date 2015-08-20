
-- Create the user and grant privileges
CREATE USER 'barebones'@'localhost' IDENTIFIED BY 'insecurepassword';
GRANT
    INSERT, SELECT, UPDATE, DELETE
    , SHOW VIEW
ON
    barebones.*
TO
    'barebones'@'localhost';

FLUSH PRIVILEGES;


CREATE DATABASE barebones;
