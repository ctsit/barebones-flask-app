"""
Goal: Store helper functions not tied to a specific module

@authors:
    Andrei Sura             <sura.andrei@gmail.com>
    Ruchi Vivek Desai       <ruchivdesai@gmail.com>
    Sanath Pasumarthy       <sanath@ufl.edu>
"""

import os
import ast
import json
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer
from flask import flash, request, jsonify
from hashlib import sha512, sha256
import hmac
import base64
from subprocess import Popen
from subprocess import PIPE
import pytz as tz

FORMAT_US_DATE = "%x"
FORMAT_US_DATE_TIME = '%x %X'
FORMAT_US_DATE_TIME_ZONE = '%x %X %Z%z'
FORMAT_DATABASE_DATE_TIME = "%Y-%m-%d %H:%M:%S"

# @TODO: move to the configs
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'tiff',
                          'zip', 'tar', 'tgz', 'bz2'])

FLASH_CATEGORY_ERROR = 'error'
FLASH_CATEGORY_INFO = 'info'


def _get_remote_addr():
    """ Return the utf-8 encoded request address """
    address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if address is not None:
        address = address.encode('utf-8')
    return address


def _get_user_agent():
    """ Return the utf-8 encoded request user agent """
    user_agent = request.headers.get('User-Agent')
    if user_agent is not None:
        user_agent = user_agent.encode('utf-8')
    return user_agent


def _create_salt():
    """ Get the first 16 bytes of the sha256(rand:user_ip:user_agent) """
    rand = base64.b64encode(os.urandom(24))

    base = '{0}:{1}:{2}'.format(rand, _get_remote_addr(), _get_user_agent())
    if str is bytes:
        base = unicode(base, 'utf-8', errors='replace')  # pragma: no cover
    hasher = sha256()
    hasher.update(base.encode('utf8'))
    all64 = hasher.hexdigest()
    return all64[0:16]


def _generate_sha512_hmac(pepper, salt, data):
    """ Generate the SHA512 HMAC -- for compatibility with Flask-Security
    h = HMAC(pepper, salt+data)

    Where
        pepper: the global application key
        salt:   the 128bit (16bytes) obtained from sha256(rand:ip:agent)
        data:   the data to be protected

from passlib.context import CryptContext
self.password_crypt_context = CryptContext(schemes='bcrypt')
    """
    payload = '{}:{}'.format(salt.encode('utf-8'), data.encode('utf-8'))
    return base64.b64encode(hmac.new(pepper, payload, sha512).digest())


def generate_auth(pepper, password):
    """
    Return the salt and hashed password to be stored in the database.
    Execute once when the user account is created.

    Note: requires a request context.
    """
    salt = _create_salt()
    hashed_pass = _generate_sha512_hmac(pepper, salt, password)
    return (salt, hashed_pass)


def is_valid_auth(pepper, salt, candidate_password, correct_hash):
    """
    Return ``True`` if the candidate_password hashes to the same
    value stored in the database as correct_hash.

    :param pepper: the global application security key
    :param salt: the user-specific salt
    :param candidate_password

    :rtype Boolean
    :return password validity status
    """
    assert pepper is not None
    assert salt is not None
    assert candidate_password is not None
    candidate_hash = _generate_sha512_hmac(pepper, salt, candidate_password)
    return correct_hash == candidate_hash


def clean_str(dangerous):
    """ Return the trimmed string """
    if dangerous is None:
        return None
    return str(dangerous).strip()


def clean_int(dangerous):
    """
    Return None for non-integer input
    """
    if dangerous is None:
        return None

    dangerous = str(dangerous).strip()

    if "" == dangerous:
        return None

    if not dangerous.isdigit():
        return None

    return int(dangerous)


def get_safe_int(unsafe, default=1, min_allowed=1, max_allowed=None):
    """ Helper method for reading the user input

    :param unsafe: the user input to be interpreted as in
    :param default: the default to use if there is a problem converting the int
    :param min_allowed: the minimum value to use
    :param max_allowed: the maximum value to use (ignores None value)
    """
    unsafe = clean_int(unsafe)
    if unsafe is None:
        unsafe = default
    elif unsafe < min_allowed:
        unsafe = min_allowed
    elif max_allowed is not None and unsafe > max_allowed:
        unsafe = max_allowed
    return unsafe


def flash_error(msg):
    """ Put a message in the "error" queue for display """
    flash(msg, FLASH_CATEGORY_ERROR)


def flash_info(msg):
    """ Put a message in the "info" queue for display """
    flash(msg, FLASH_CATEGORY_INFO)


def pack(data):
    """
    Create a string represenation of data
    :param data -- dictionary
    """
    return json.dumps(data, sort_keys=True, indent=2)


def pack_error(msg):
    """ Format an error message to be json-friendly """
    return pack({'status': 'error', 'message': msg})


def jsonify_error(data):
    """ Format an error message to be json-friendly """
    return jsonify({'status': 'error', 'data': data})


def jsonify_success(data):
    """ Format a success message to be json-friendly """
    return jsonify({'status': 'success', 'data': data})


def get_db_friendly_date_time():
    """
    :rtype: string
    :return current time in format: "2014-06-24 01:23:24"
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def localize_datetime(value, zone_name='US/Eastern'):
    """ Localize the specified datetime value according to a zone"""
    # print(tz.all_timezones)
    if value is None:
        return ''
    timezone = tz.timezone(zone_name)
    localized_value = timezone.localize(value, is_dst=None)
    return localized_value


def localize_est_date(value):
    """ Format the datetime value as `FORMAT_US_DATE` """
    localized_value = localize_datetime(value)
    return localized_value.strftime(FORMAT_US_DATE)


def localize_est_datetime(value):
    """ Format the datetime value as `FORMAT_US_DATE_TIME` """
    localized_value = localize_datetime(value)
    if value is None or '' == value:
        return ''
    return localized_value.strftime(FORMAT_US_DATE_TIME)


def get_expiration_date(offset_days):
    """
    :param offset_days: how many days to shift versus today
    :rtype datetime
    :return the date computed with offset_days
    """
    return datetime.now() + timedelta(days=offset_days)


def compute_text_md5(text):
    """ Compute md5sum as hexdigest

    :param text: the input string
    :rtype string
    """
    import hashlib
    m = hashlib.md5()
    m.update(text)
    return m.hexdigest()


def get_email_token(email, salt, secret):
    """
    Generate a timestamped token from the specified email
    """
    ts = URLSafeTimedSerializer(secret)
    token = ts.dumps(email, salt=salt)
    return token


def get_email_from_token(token, salt, secret, max_age=86400):
    """
    Read an email from a timestamped token.
    Raises an exception if the token is more than 24 hours old or invalid
    """
    ts = URLSafeTimedSerializer(secret)
    email = ts.loads(token, salt=salt, max_age=max_age)
    return email


def redcap_api_call(url, token, content, fields, max_time):
    """
    Send an API request to the REDCap server.
    Notes:
        - when no fields are specified all fields are retrived
        - the underlining cURL process is limited to complete
            within `max_time` seconds

    :rtype: dict
    :return: the requested content if it is of valid type (event, record)
    """
    assert content in ['event', 'record']

    # @TODO: add config flag for enabling/disabling the ssl
    # certificate validation: curl -k
    cmd = 'curl -m {} -sX POST {} ' \
        ' -d token={} ' \
        ' -d format=json ' \
        ' -d content={} ' \
        ' -d fields="{}"' \
        ' -d returnFormat=json ' \
        ' | python -m json.tool ' \
        .format(max_time, url, token, content, fields)

    proc = Popen(cmd, shell=True, stdout=PIPE)
    (out, err) = proc.communicate()
    # print("redcap_api_call: {}\n{}".format(cmd, out))

    if err:
        print("redcap_api_call error: \n{}".format(err))

    data = []
    try:
        data = ast.literal_eval(out)
    except Exception as exc:
        print("redcap_api_call error parsing curl response:\n{}".format(exc))
    return data


def retrieve_redcap_subjects(url, token, fields, max_time=30):
    """Read the list of subjects from the REDCap instance using the API"""
    data = redcap_api_call(url, token, content='record',
                           fields=fields, max_time=max_time)
    # print("subjects: {}".format(data))
    return data


def retrieve_redcap_events(url, token, max_time=30):
    """Read the list of events from the REDCap instance using the API"""
    data = redcap_api_call(url, token, content='event',
                           fields={}, max_time=max_time)
    # print("events: {}".format(data))
    return data
