"""Views for boxes and pages"""

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


def box_view(request):
    """View for boxes"""
    logged_in = authenticated_userid(request)
    security.check_permission(request, logged_in)
    context = Box(request)

    file_extension = os.path.splitext(request['PATH_INFO'])[1]
    if file_extension == '.ico':
        request.subpath = request['PATH_INFO'].split('/')
        return STATIC_VIEW_OF_ICO(context, request)
    elif file_extension == '.html':
        template = 'raisin.page:templates/box.pt'
        box_renderer = pyramid.renderers.get_renderer(template)
        response = Response()
        value = {'context': context,
                 'request': request}
        response.unicode_body = box_renderer(value, request)
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
    logged_in = authenticated_userid(request)
    security.check_permission(request, logged_in)
    context = Page(request)

    return dict(
        context=context,
        logged_in=logged_in,
        )
