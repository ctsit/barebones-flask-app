
-- Added the `Version` table

desc Version;
+----------+--------------+------+-----+-------------------+-----------------------------+
| Field    | Type         | Null | Key | Default           | Extra                       |
+----------+--------------+------+-----+-------------------+-----------------------------+
| verID    | varchar(255) | NO   | PRI |                   |                             |
| verStamp | timestamp    | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
| verInfo  | text         | NO   |     | NULL              |                             |
+----------+--------------+------+-----+-------------------+-----------------------------+
