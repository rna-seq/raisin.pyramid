"""Views for boxes and pages"""

import re
import os.path
from webob import Response
from webob.exc import HTTPNotFound

from pyramid.security import authenticated_userid
from pyramid.static import static_view

import pyramid.renderers

from raisin.restyler.page import Page
from raisin.restyler.box import Box

from raisinpyramid import security

STATIC_VIEW_OF_ICO = static_view('raisin.page:templates/static/',
                                 cache_max_age=3600)

VALID_KEY = re.compile('^[A-Za-z_]*$')
VALID_VALUE = re.compile('^[A-Za-z0-9-_.]*$')


def validate(matchdict):
    """Validate the matchdict"""
    for key, value in matchdict.items():
        if not VALID_KEY.match(key):
            raise AttributeError
        if not VALID_VALUE.match(value):
            raise AttributeError


def box_view(request):
    """View for boxes"""
    validate(request.matchdict)
    logged_in = authenticated_userid(request)
    security.check_permission(request, logged_in)
    context = Box(request)

    file_extension = os.path.splitext(request.environ['PATH_INFO'])[1]
    if file_extension == '.ico':
        request.subpath = request.environ['PATH_INFO'].split('/')
        return STATIC_VIEW_OF_ICO(context, request)
    elif file_extension == '.html':
        template = 'raisin.page:templates/box.pt'
        box_renderer = pyramid.renderers.get_renderer(template)
        response = Response()
        value = {'context': context,
                 'request': request}
        response.unicode_body = box_renderer(value, request.environ)
    elif file_extension == '.csv':
        if context.body is None:
            return HTTPNotFound()
        else:
            response = Response()
            response.body = context.body
    else:
        raise AttributeError(file_extension)

    return response


def page_view(request):
    """View for pages"""
    validate(request.matchdict)
    logged_in = authenticated_userid(request)
    security.check_permission(request, logged_in)
    context = Page(request)

    return dict(
        context=context,
        logged_in=logged_in,
        )
