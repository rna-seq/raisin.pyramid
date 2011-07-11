"""Implement a Pyramid application

Contains the main method that registers

    * users in the USERS regstry

    * projects in the PROJECTS registry

Sets up a Pyramid configuration and adds the necessary routes.

"""

import os.path
from configobj import ConfigObj

from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.exceptions import Forbidden
from raisin.page import PAGES
from raisinpyramid.resources import Root
from raisinpyramid import login
from raisinpyramid import security
from raisinpyramid.views import box_view
from raisinpyramid.views import page_view
from security import USERS
from security import PROJECTS


def register_page_and_boxes(config, page_key, page_value):
    """Register pages and boxes so that Pyramid knows what to serve"""

    config.add_route(name='p1_' + page_key,
                     path=page_value['path'],
                     view=page_view,
                     renderer=page_value['renderer'])
    # Remove the trailing slash, so that pages are also rendered without.
    config.add_route(name='p2_' + page_key,
                     path=page_value['path'][:-1],
                     view=page_view,
                     renderer=page_value['renderer'])
    # Register page boxes
    config.add_route(name='p3_' + page_key + '_box',
                     path=page_value['path'] + ':box_id_with_extension',
                     view=box_view,
                     renderer=page_value['renderer'])


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.

    It is usually called by the PasteDeploy framework during ``paster serve``.
    """

    # The global configuration contains the folder path of the configuration
    # file used to start the server.
    here = global_config['here']

    # Choose which users configuration file to use
    if 'users' in settings:
        # If it is defined in the settings, use this one
        users_file = settings['users']
    else:
        # As a default, take the users configuration file from the local folder
        users_file = os.path.join(here, 'users.ini')

    if not os.path.exists(users_file):
        raise IOError("File %s not found" % users_file)

    # Choose which projects configuration file to use
    if 'projects' in settings:
        # If it is defined in the settings, use this one
        projects_file = settings['projects']
    else:
        # As a default, take the users configuration file from the local folder
        projects_file = os.path.join(here, 'projects.ini')

    if not os.path.exists(projects_file):
        raise IOError("File %s not found" % projects_file)

    for key, value in ConfigObj(users_file).items():
        USERS[key] = value['password']

    for project, users in ConfigObj(projects_file).items():
        for user in users['users']:
            if user in PROJECTS:
                PROJECTS[user].append(project)
            else:
                PROJECTS[user] = [project]

    authentication_policy = AuthTktAuthenticationPolicy(secret='raisinseq')
    authorization_policy = ACLAuthorizationPolicy()

    config = Configurator(authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy,
                          settings=settings,
                          root_factory=Root)
    config.begin()
    config.scan()
    config.add_route(name="login",
                     path="login",
                     view=login.login,
                     view_renderer="raisinpyramid:templates/login.pt")
    config.add_route(name="logout",
                     path="logout",
                     view=login.logout)
    # Register pages
    for page_key, page_value in PAGES.items():
        register_page_and_boxes(config, page_key, page_value)

    # Register folder containing static material
    config.add_static_view(name="static",
                           path="raisin.page:templates/static")

    config.add_view(view=login.login,
                    renderer="templates/login.pt",
                    for_=Forbidden)

    config.end()

    return config.make_wsgi_app()
