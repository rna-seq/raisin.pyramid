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
    config.add_route(name='page_' + page_key,
                     path=page_value['path'],
                     view=page_view,
                     renderer=page_value['renderer'])
    # Remove the trailing slash, so that pages are also rendered when they don't have it.
    config.add_route(name='samepage' + page_key,
                     path=page_value['path'][:-1],
                     view=page_view,
                     renderer=page_value['renderer'])
    # Register page boxes
    config.add_route(name='page_' + page_key + '_box',
                     path=page_value['path'] + ':box_id_with_extension',
                     view=box_view,
                     renderer=page_value['renderer'])

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.

    It is usually called by the PasteDeploy framework during ``paster serve``.
    """

    for key, value in ConfigObj(settings['users']).items():
        USERS[key] = value['password']
    
    for project, users in ConfigObj(settings['projects']).items():
        for user in users['users']:
            if PROJECTS.has_key(user):
                PROJECTS[user].append(project)
            else:
                PROJECTS[user] = [project]

    authentication_policy = AuthTktAuthenticationPolicy(secret = 'seekrit',
                                                        callback = security.groupfinder)
    authorization_policy = ACLAuthorizationPolicy()

    config = Configurator(authentication_policy = authentication_policy,
                          authorization_policy = authorization_policy,
                          settings = settings, 
                          root_factory = Root)
    config.begin()
    config.scan()
    config.add_route(name="login", 
                     path="login",
                     view = login.login,
                     view_renderer = "raisinpyramid:templates/login.pt")
    config.add_route(name="logout", 
                     path="logout",
                     view = login.logout)
    # Register pages
    for page_key, page_value in PAGES.items():
        register_page_and_boxes(config, page_key, page_value)

    # Register folder containing static material
    config.add_static_view(name="static", path="raisin.page:templates/static")  

    config.add_view(view = login.login, renderer="templates/login.pt", for_ = Forbidden)

    config.end()

    return config.make_wsgi_app()


