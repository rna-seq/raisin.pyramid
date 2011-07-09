from webob import Response
from webob.exc import HTTPNotFound

from pyramid.security import Allow
from pyramid.security import Everyone
from pyramid.security import authenticated_userid
from pyramid.static import static_view

import pyramid.renderers

from raisin.restyler.page import Page
from raisin.restyler.box import Box

from raisinpyramid import security

STATIC_VIEW_OF_ICO = static_view('raisin.page:templates/static/', cache_max_age=3600)


def box_view(request):
    logged_in = authenticated_userid(request)
    security.check_permission(request, logged_in)
    context = Box(request)
    context.__acl__ = [(Allow, Everyone, 'view homepage'),
                       (Allow, 'group:encode', 'view encode project'),
                       (Allow, 'group:big', 'view any project'),
                      ]

    if request['PATH_INFO'].endswith('.ico'):
        request.subpath = request['PATH_INFO'].split('/')
        return STATIC_VIEW_OF_ICO(context, request)
    elif request['PATH_INFO'].endswith('.csv') or request['PATH_INFO'].endswith('.json'):
        if context.body is None:
            return HTTPNotFound()
        else:
            response = Response()
            response.body = context.body
    else:
        box_renderer = pyramid.renderers.get_renderer('raisin.page:templates/box.pt')
        response = Response()
        response.unicode_body = box_renderer({'context': context, 'request': request}, request)
    return response


def page_view(request):
    logged_in = authenticated_userid(request)
    security.check_permission(request, logged_in)
    context = Page(request)
    return dict(
        context=context,
        logged_in=logged_in,
        )
