"""
Goal: Delegate requests to the `/api` path to the appropriate controller

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
  Taeber Rapczak          <taeber@ufl.edu>
"""

# import math
from datetime import datetime
import collections

from flask import request
from flask import send_file
from flask import session
from flask import make_response
from flask_login import login_required

from app.main import app, db
from app import emails
from app import utils
from app.models.log_entity import LogEntity

from app.models.user_entity import UserEntity
from app.models.role_entity import RoleEntity

from app.routes.users import perm_admin, perm_admin_or_technician


@app.route('/api/save_user', methods=['POST'])
@login_required
def api_save_user():
    """ Save a new user to the database """
    email = request.form['email']
    first = request.form['first']
    last = request.form['last']
    minitial = request.form['minitial']
    roles = request.form.getlist('roles[]')

    email_exists = False
    try:
        existing_user = UserEntity.query.filter_by(email=email).one()
        email_exists = existing_user is not None
    except:
        pass

    if email_exists:
        return utils.jsonify_error(
            {'message': 'Sorry. This email is already taken.'})

    # @TODO: fix hardcoded values
    # salt, hashed_pass = generate_auth(app.config['SECRET_KEY'], password)
    added_date = datetime.today()
    access_end_date = utils.get_expiration_date(180)

    user = UserEntity.create(email=email,
                             first=first,
                             last=last,
                             minitial=minitial,
                             added_at=added_date,
                             modified_at=added_date,
                             access_expires_at=access_end_date,
                             password_hash="")

    user_roles = []
    try:
        for role_name in roles:
            role_entity = RoleEntity.query.filter_by(name=role_name).one()
            user_roles.append(role_entity)
    except Exception as exc:
        app.logger.debug("Problem saving user: {}".format(exc))

    [user.roles.append(rol) for rol in user_roles]
    user = UserEntity.save(user)
    app.logger.debug("saved user: {}".format(user))
    LogEntity.account_created(session['uuid'], user)
    return utils.jsonify_success({'user': user.serialize()})


@app.route('/api/list_users', methods=['POST', 'GET'])
@login_required
def api_list_users():
    """
    Retrieve the users cached in the local database
    :rtype: Response
    :return
    """
    if 'POST' == request.method:
        per_page = utils.get_safe_int(request.form.get('per_page'))
        page_num = utils.get_safe_int(request.form.get('page_num'))
    else:
        per_page = utils.get_safe_int(request.args.get('per_page'))
        page_num = utils.get_safe_int(request.args.get('page_num'))

    pagination = UserEntity.query.order_by(
        db.desc(UserEntity.id)).paginate(page_num, per_page, False)
    items = [i.serialize() for i in pagination.items]
    return utils.jsonify_success(
        {"total_pages": pagination.pages, "list_of_users": items})


@app.route('/api/list_logs', methods=['GET', 'POST'])
@login_required
def api_list_logs():
    """
    Render the specified page of event logs
    @TODO: show user-specific logs for non-admins?

    :rtype: string
    :return the json list of logs
    """
    if 'POST' == request.method:
        per_page = utils.get_safe_int(request.form.get('per_page'))
        page_num = utils.get_safe_int(request.form.get('page_num'))
    else:
        per_page = utils.get_safe_int(request.args.get('per_page'))
        page_num = utils.get_safe_int(request.args.get('page_num'))

    logs, total_pages = LogEntity.get_logs(per_page, page_num)

    return utils.jsonify_success(
        dict(list_of_events=logs, total_pages=total_pages))



@app.route('/api/activate_account', methods=['POST'])
@login_required
@perm_admin.require()
def api_activate_account():
    """
    Activate an user.
    @TODO: should change expiration date too?

    :rtype: Response
    :return the success or failed in json format
    """
    user_id = utils.get_safe_int(request.form.get('user_id'))
    user = UserEntity.get_by_id(user_id)
    user = UserEntity.update(user, active=True)
    LogEntity.account_modified(session['uuid'],
                               "User activated: {}".format(user))
    return utils.jsonify_success({"message": "User activated."})


@app.route('/api/deactivate_account', methods=['POST'])
@login_required
@perm_admin.require()
def api_deactivate_account():
    """
    De-activate an user.
    @TODO: should change expiration date too?

    :rtype: Response
    :return the success or failed in json format
    """
    user_id = utils.get_safe_int(request.form.get('user_id'))
    user = UserEntity.get_by_id(user_id)
    user = UserEntity.update(user, active=False)
    LogEntity.account_modified(session['uuid'],
                               "User deactivated: {}".format(user))
    return utils.jsonify_success({"message": "User deactivated."})


@app.route('/api/send_verification_email', methods=['POST'])
@login_required
@perm_admin.require()
def api_send_verification_email():
    """
    @TODO: Send Verification Email to user_id

    :rtype: Response
    :return the success or failed in json format
    """
    user_id = utils.get_safe_int(request.form.get('user_id'))
    user = UserEntity.get_by_id(user_id)

    try:
        emails.send_verification_email(user)
        return utils.jsonify_success(
            {"message": "Verification email was sent."})
    except Exception as exc:
        details = "Connection config: {}/{}:{}".format(
            app.config['MAIL_USERNAME'],
            app.config['MAIL_SERVER'],
            app.config['MAIL_PORT'])
        app.logger.debug(details)
        return utils.jsonify_error(
            {"message": "Unable to send email due: {} {}".format(exc, details)})


@app.route('/api/verify_email', methods=['GET', 'POST'])
def api_verify_email():
    """
    @TODO: add counter/log to track failed attempts

    :rtype: Response
    :return the success or failed in json format
    """
    if 'POST' == request.method:
        token = utils.clean_str(request.form.get('tok'))
    else:
        token = utils.clean_str(request.args.get('tok'))

    if not token:
        return utils.jsonify_error({'message': 'No token specified.'})

    try:
        email = utils.get_email_from_token(token,
                                           app.config["SECRET_KEY"],
                                           app.config["SECRET_KEY"])
    except Exception as exc:
        # @TODO: add dedicated log type
        app.logger.error("api_verify_email: {}".format(exc.message))
        return utils.jsonify_error({'message': exc.message})

    app.logger.debug("Decoded email from token: {}".format(email))
    user = UserEntity.query.filter_by(email=email).first()

    if user is None:
        app.logger.error("Attempt to verify email with incorrect token: {}"
                         .format(token))
        return utils.jsonify_error({'message': 'Sorry.'})

    user = UserEntity.update(user, email_confirmed_at=datetime.today())
    app.logger.debug("Verified token {} for user {}".format(token, user.email))

    # @TODO: add dedicated log type
    LogEntity.account_modified(session['uuid'],
                               "Verified token {} for user {}".format(
                                   token, user.email))
    return utils.jsonify_success(
        {"message": "Email was verified for {}.".format(email)})


@app.route('/api/expire_account', methods=['POST'])
@login_required
@perm_admin.require()
def api_expire_account():
    """
    Change the `User.usrAccessExpiresAt` to today's date and 00:00:00 time
    effectively blocking the user access.

    :rtype: Response
    :return the success or failed in json format
    """
    user_id = utils.get_safe_int(request.form.get('user_id'))
    user = UserEntity.get_by_id(user_id)
    today = datetime.today()
    today_start = datetime(today.year, today.month, today.day)
    user = UserEntity.update(user, access_expires_at=today_start)
    # @TODO: add dedicated log type
    LogEntity.account_modified(session['uuid'],
                               "User access was expired. {}".format(user.email))
    return utils.jsonify_success({"message": "User access was expired."})


@app.route('/api/extend_account', methods=['POST'])
@login_required
@perm_admin.require()
def api_extend_account():
    """
    Change the `User.usrAccessExpiresAt` to today's date + 180 days

    :rtype: Response
    :return the success or failed in json format
    """
    user_id = request.form.get('user_id')
    today_plus_180 = utils.get_expiration_date(180)
    user = UserEntity.get_by_id(user_id)
    user = UserEntity.update(user, access_expires_at=today_plus_180)
    # @TODO: add dedicated log type
    LogEntity.account_modified(session['uuid'],
                               "Updated expiration date to {}. {}".format(
                                   today_plus_180, user.email))
    return utils.jsonify_success(
        {"message": "Updated expiration date to {}".format(today_plus_180)})

