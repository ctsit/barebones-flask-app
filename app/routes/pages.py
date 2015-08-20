"""
Goal: Define the routes for general pages

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>


@see https://flask-login.readthedocs.org/en/latest/
@see https://pythonhosted.org/Flask-Principal/
"""

import hashlib
import base64
import datetime
import uuid
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from app.models.log_entity import LogEntity
from app.models.web_session_entity import WebSessionEntity
from app.models.user_agent_entity import UserAgentEntity
from wtforms import Form, TextField, PasswordField, HiddenField, validators

from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user
from flask_principal import \
    Identity, AnonymousIdentity, identity_changed, identity_loaded, RoleNeed

from app.main import app
from app import utils
from app.models.user_entity import UserEntity

# set the login manager for the app
login_manager = LoginManager(app)

# Possible options: strong, basic, None
login_manager.session_protection = "strong"
login_manager.login_message = ""
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    """Return the user from the database"""
    return UserEntity.get_by_id(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    """ Returns a message for the unauthorized users """
    # return redirect('/')
    return 'Please <a href="{}">login</a> first.'.format(url_for('index'))


@app.errorhandler(403)
def page_not_found(e):
    """
    Redirect to login page if probing a protected resources before login
    """
    return redirect(url_for('index') + "?next={}".format(request.url))


class LoginForm(Form):
    """ Declare the validation rules for the login form """
    next = HiddenField(default='')

    # email = TextField('Email', [validators.Length(min=4, max=25)])
    email = TextField('Email')
    password = PasswordField(
        'Password', [
            validators.Required(), validators.Length(
                min=6, max=25)])


def get_user_agent():
    """Find an existing user agent or insert a new one"""
    # The raw user agent string received from the browser
    uag = request.user_agent
    hash = utils.compute_text_md5(uag.string)

    # The entity representing the user agent
    user_agent = UserAgentEntity.get_by_hash(hash)

    if user_agent is None:
        platform = uag.platform if uag.platform is not None else ''
        browser = uag.browser if uag.browser is not None else ''
        version = uag.version if uag.version is not None else ''
        language = uag.language if uag.language is not None else ''
        user_agent = UserAgentEntity.create(user_agent=uag.string,
                                            hash=hash,
                                            platform=platform,
                                            browser=browser,
                                            version=version,
                                            language=language)

    # app.logger.debug(user_agent)
    return user_agent


@app.before_request
def check_session_id():
    """
    Generate a UUID and store it in the session
    as well as in the WebSession table.
    """
    # TODO: Create UserAgentEntity and populate
    user_agent = get_user_agent()

    if 'uuid' not in session:
        session['uuid'] = str(uuid.uuid4())
        WebSessionEntity.create(session_id=session['uuid'],
                                user_id=current_user.get_id(),
                                ip=request.remote_addr,
                                date_time=datetime.datetime.now(),
                                user_agent=user_agent)
        return
    if current_user.is_authenticated():
        # update the user_id on the first request after login is completed
        session_id = session['uuid']
        web_session = WebSessionEntity.get_by_session_id(session_id)
        if web_session is not None:
            web_session = WebSessionEntity.update(
                web_session,
                user_id=current_user.get_id())
        else:
            app.logger.error("No row found for sess_id: {}".format(session_id))


@app.route('/', methods=['POST', 'GET'])
def index():
    """ Render the login page"""
    if app.config['LOGIN_USING_SHIB_AUTH']:
        return render_login_shib()
    return render_login_local()


def render_login_local():
    """ Render the login page with username/pass

    @see #index()
    @see #render_login_shib()
    """
    if current_user.is_authenticated():
        return redirect(get_role_landing_page())

    uuid = session['uuid']
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        email = form.email.data.strip(
            ) if form.email.data else "admin@example.com"
        password = form.password.data.strip() if form.password.data else ""
        app.logger.debug("{} password: {}".format(email, password))

        app.logger.debug("Checking email: {}".format(email))
        user = UserEntity.query.filter_by(email=email).first()

        if user:
            app.logger.debug("Found user object: {}".format(user))
        else:
            utils.flash_error("No such email: {}".format(email))
            LogEntity.login(uuid, "No such email: {}".format(email))
            return redirect(url_for('index'))

        # if utils.is_valid_auth(app.config['SECRET_KEY'], auth.uathSalt,
        # password, auth.uathPassword):
        if '' == user.password_hash:
            app.logger.info('Log login event for: {}'.format(user))
            LogEntity.login(uuid, 'Successful login via email/password')
            login_user(user, remember=False, force=False)

            # Tell Flask-Principal that the identity has changed
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.get_id()))
            return redirect(get_role_landing_page())
        else:
            app.logger.info('Incorrect pass for: {}'.format(user))
            LogEntity.login_error(uuid, 'Incorrect pass for: {}'.format(user))

    # When sending a GET request render the login form
    return render_template('index.html', form=form,
                           next_page=request.args.get('next'))


@app.route('/loginExternalAuth', methods=['POST', 'GET'])
def shibb_redirect():
    """
    Redirect to the local shibboleth instance where
    we can pass the return path.
    This route is reached when the user clicks the "Login" button.
    Note: This is equivalent to Apache's syntax:
        Redirect seeother /loginExternalAuth /Shibboleth.sso/Login?target=...

    @see #index()
    @see #shibb_return()
    """
    next_page = "/Shibboleth.sso/Login?target={}"\
                .format(url_for('shibb_return'))
    return redirect(next_page)


@app.route('/loginExternalAuthReturn', methods=['POST', 'GET'])
def shibb_return():
    """
    Read the Shibboleth headers returned by the IdP after
    the user entered the username/password.
    If the `eduPersonPrincipalName` (aka Eppn) for the user matches the
    usrEmail of an active user then let the user in,
    otherwise let them see the login page.

    @see #shibb_redirect()
    """
    if current_user.is_authenticated():
        # next_page = request.args.get('next') or get_role_landing_page()
        return redirect(get_role_landing_page())

    # fresh login...
    uuid = session['uuid']
    email = request.headers['Mail']
    glid = request.headers['Glid']  # Gatorlink ID
    app.logger.debug("Checking if email: {} is registered for glid: {}"
                     .format(email, glid))
    user = UserEntity.query.filter_by(email=email).first()

    if not user:
        utils.flash_error("No such user: {}".format(email))
        LogEntity.login_error(uuid,
                              "Shibboleth user is not registered for this app")

        return redirect(url_for('index'))

    if not user.is_active():
        utils.flash_error("Inactive user: {}".format(email))
        LogEntity.login_error(uuid, 'Inactive user tried to login')
        return redirect(url_for('index'))

    if user.is_expired():
        utils.flash_error("User account for {} expired on {}"
                          .format(email, user.access_expires_at))
        LogEntity.login_error(uuid, 'Expired user tried to login')
        return redirect(url_for('index'))

    # Log it
    app.logger.info('Successful login via Shibboleth for: {}'.format(user))
    LogEntity.login(uuid, 'Successful login via Shibboleth')

    login_user(user, remember=False, force=False)

    # Tell Flask-Principal that the identity has changed
    identity_changed.send(current_app._get_current_object(),
                          identity=Identity(user.get_id()))
    next_page = get_role_landing_page()
    return redirect(next_page)


def render_login_shib():
    """ Render the login page with button redirecting to
    Shibboleth /loginExternalAuth path
    """
    return render_template('login_shib.html', form=request.form)


def get_role_landing_page():
    """
    Get the landing page for a user with specific role
    :return None if the user has no roles
    """
    next_page = request.form.get('next')
    # Per Chris's request all users land on the same page
    if next_page is not None and next_page != 'None':
        return next_page

    return url_for('upload_files')


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    """ Describe what `needs` does this identity provide
    @TODO: add unit tests
        http://stackoverflow.com/questions/16712321/unit-testing-a-flask-principal-application
    """
    if type(current_user) == 'AnonymousUserMixin':
        return

    identity.user = current_user

    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            # app.logger.debug("Provide role: {}".format(role))
            identity.provides.add(RoleNeed(role.name))


@login_manager.request_loader
def load_user_from_request(req):
    """ To support login from both a url argument and from Basic Auth
     using the Authorization header

    @TODO: use for api requests?
        Need to add column `UserAuth.uathApiKey`
    """

    # first, try to login using the api_key url arg
    api_key = req.args.get('api_key')

    if not api_key:
        # next, try to login using Basic Auth
        api_key = req.headers.get('Authorization')
        if api_key:
            api_key = api_key.replace('Basic ', '', 1)
            try:
                api_key = base64.b64decode(api_key)
            except TypeError:
                pass

    if api_key:
        md5 = hashlib.md5()
        md5.update(api_key)
        app.logger.debug("trying api_key: {}".format(md5.digest()))
        user = UserEntity.query.filter_by(api_key=api_key).first()
        return user

    # finally, return None if neither of the api_keys is valid
    return None


@app.route('/logout')
def logout():
    """ Destroy the user session and redirect to the home page

    Shib:
        https://shib.ncsu.edu/docs/logout.html
        https://wiki.shibboleth.net/confluence/display/CONCEPT/SLOIssues
    """
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    # Log the logout
    LogEntity.logout(session['uuid'])
    # Also pop the session id
    session.pop('uuid')
    return redirect('/')
