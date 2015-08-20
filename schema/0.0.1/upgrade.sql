
-- Store database modification log
CREATE TABLE Version (
   version_id varchar(255) NOT NULL DEFAULT '',
   version_stamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   version_info text NOT NULL,
  PRIMARY KEY (version_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

INSERT INTO Version (version_id, version_info)
   VALUES('0.0.1', 'New tables: Version, Data')
;

CREATE TABLE Temperature (
    `id` int(10) NOT NULL DEFAULT '0',
    `temperature` int(10) DEFAULT NULL,
    `location` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
 PRIMARY KEY (id),
 KEY `loc_temp` (location, temperature),
 KEY (temperature)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci
;

CREATE TABLE User (
    usrID integer unsigned NOT NULL AUTO_INCREMENT,
    usrEmail varchar(255) NOT NULL DEFAULT '',
    usrFirst varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
    usrLast varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
    usrMI char(1) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
    usrAddedAt datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    usrModifiedAt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usrEmailConfirmedAt datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    usrIsActive tinyint NOT NULL DEFAULT 1,
    usrAccessExpiresAt datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    usrPasswordHash varchar(255) NOT NULL DEFAULT '',
 PRIMARY KEY (usrID),
 UNIQUE KEY (usrEmail),
 KEY (usrFirst, usrLast),
 KEY (usrAddedAt),
 KEY (usrModifiedAt),
 KEY (usrEmailConfirmedAt),
 KEY(usrAccessExpiresAt)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

-- Store possible roles
CREATE TABLE Role (
    rolID smallint unsigned NOT NULL AUTO_INCREMENT,
    rolName varchar(255) NOT NULL,
    rolDescription varchar(255) NOT NULL,
 PRIMARY KEY (rolID),
 UNIQUE KEY (rolName)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

-- Store user roles mapping
CREATE TABLE UserRole (
    urID integer unsigned NOT NULL AUTO_INCREMENT,
    usrID integer unsigned NOT NULL,
    rolID smallint unsigned NOT NULL,
    urAddedAt datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
 PRIMARY KEY (urID),
 CONSTRAINT `fk_User_usrID` FOREIGN KEY (usrID) REFERENCES User (usrID) ON DELETE CASCADE,
 CONSTRAINT `fk_UserRole_rolID` FOREIGN KEY (rolID) REFERENCES Role (rolID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;


-- user agent parsing http://werkzeug.pocoo.org/docs/0.10/utils/
CREATE TABLE UserAgent (
    uaID integer unsigned NOT NULL AUTO_INCREMENT,
    uaUserAgent varchar(32768) NOT NULL DEFAULT '',
    uaHash varchar(32) NOT NULL,
    uaPlatform varchar(255) NOT NULL,
    uaBrowser varchar(255) NOT NULL,
    uaVersion varchar(255) NOT NULL,
    uaLanguage varchar(255) NOT NULL,
 PRIMARY KEY (uaID),
 UNIQUE KEY (uaHash),
 KEY uaPlatform (uaPlatform),
 KEY (uaBrowser, uaVersion),
 KEY (uaLanguage)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

CREATE TABLE WebSession (
    webID integer unsigned NOT NULL AUTO_INCREMENT,
    webSessID varchar(255) NOT NULL DEFAULT '',
    usrID integer unsigned NOT NULL DEFAULT '0',
    webIP varchar(15) NOT NULL DEFAULT '',
    webDateTime datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    uaID integer unsigned NOT NULL DEFAULT '0',
 PRIMARY KEY (webID),
 KEY (usrID),
 KEY (webDateTime),
 KEY (uaID),
 CONSTRAINT `fk_WebSession_uaID` FOREIGN KEY (uaID) REFERENCES UserAgent (uaID)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

CREATE TABLE LogType (
    logtID integer unsigned NOT NULL AUTO_INCREMENT,
    logtType varchar(255) NOT NULL,
    logtDescription text NOT NULL,
 PRIMARY KEY (logtID),
 UNIQUE KEY (logtType)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

CREATE TABLE Log (
    logID integer unsigned NOT NULL AUTO_INCREMENT,
    logtID integer unsigned NOT NULL,
    webID integer unsigned NOT NULL,
    logDateTime datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    logDetails text NOT NULL,
 PRIMARY KEY (logID),
 KEY (logtID),
 KEY (webID),
 KEY (logDateTime),
 CONSTRAINT `fk_Log_logtID` FOREIGN KEY (logtID) REFERENCES LogType (logtID),
 CONSTRAINT `fk_Log_webID` FOREIGN KEY (webID) REFERENCES WebSession (webID)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;




SHOW TABLES;
SELECT * FROM Version;
