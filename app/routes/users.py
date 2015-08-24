"""
Goal: Define the routes for the users

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

# from flask import request
from flask import render_template

from flask_login import current_user
from flask_principal import Principal, Permission, RoleNeed

from app.models.role_entity import ROLE_ADMIN, ROLE_TECHNICIAN
from app.main import app

# load the Principal extension
principals = Principal(app)

# define a permission
perm_admin = Permission(RoleNeed(ROLE_ADMIN))
perm_technician = Permission(RoleNeed(ROLE_TECHNICIAN))
perm_admin_or_technician = Permission(RoleNeed(ROLE_ADMIN),
                                      RoleNeed(ROLE_TECHNICIAN))


@app.route('/admin')
@perm_admin.require(http_exception=403)
def admin():
    """ Render the technician's home page
    from flask import abort
    abort(403)
    """
    return render_template('admin.html', user_links=get_user_links())


@app.route('/logs')
@perm_admin_or_technician.require(http_exception=403)
def logs():
    """ Render the logs for the user """
    return render_template('logs.html', user_links=get_user_links())


def get_highest_role():
    """ If a user has more than one role pick the `highest` role

    :rtype string
    :return the role name for the current_user or None
    """
    try:
        roles = current_user.get_roles()
    except Exception:
        return None

    if ROLE_ADMIN in roles:
        return ROLE_ADMIN
    if ROLE_TECHNICIAN in roles:
        return ROLE_TECHNICIAN
    return None


def get_user_links():
    """
    :rtype list
    :return the navigation menu options depending on the role or None if
        the current_user doe not have a role
    """
    pages = {
        'admin': ('admin', 'Manage Users'),
        'logs': ('logs', 'View Logs'),
        'logout': ('logout', 'Logout'),
    }
    role = get_highest_role()
    if role is None:
        return []

    print "highest role: {}".format(role)

    if ROLE_ADMIN == role:
        links = [pages['admin'],
                 pages['logs']]
    elif ROLE_TECHNICIAN == role:
        links = [pages['dashboard']]

    links.append(pages['logout'])
    return links


@app.route('/dashboard')
@perm_admin_or_technician.require(http_exception=403)
def dashboard():
    """ Render the technician's home page """
    return render_template('dashboard.html', user_links=get_user_links())


@app.route('/api')
@app.route('/api/')
def api():
    """ Display the list of valid paths under /api/ """
    # @TODO: protect with @perm_admin.require() when unit tests are fixed
    return render_template('api.html', user_links=get_user_links())
