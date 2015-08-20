
INSERT INTO User (usrEmail, usrFirst, usrLast, usrAddedAt, usrAccessExpiresAt, usrIsActive, usrEmailConfirmedAt)
VALUES
    ('user1@example.com',   'User',     'A',    NOW(), NOW(), 1, NOW()),
    ('user2@example.com',   'User',     'B',    NOW(), NOW(), 1, NOW()),
    ('user3@example.com',   'User',     'C',    NOW(), NOW(), 1, NOW())
;

INSERT INTO Role (rolName, rolDescription)
VALUES
    ('admin', 'Can add/edit users, roles'),
    ('user', 'Can not add/edit users, roles')
;

INSERT INTO UserRole (usrID, rolID, urAddedAt)
      SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'user1@example.com' AND rolName = 'admin'
UNION SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'user2@example.com' AND rolName = 'admin'
UNION SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'user3@example.com' AND rolName = 'user'
;

-- Logging

-- add event types
INSERT INTO LogType
    (logtType, logtDescription)
VALUES
    ('account_created', ''),
    ('login', ''),
    ('logout', ''),
    ('login_error', ''),
    ('account_modified', '')
;

INSERT INTO UserAgent(uaUserAgent, uaHash, uaPlatform, uaBrowser, uaVersion, uaLanguage)
    VALUES ('Firefox 123', md5('Firefox 123'), 'OS X', 'Firefox', '123', 'EN')
;
