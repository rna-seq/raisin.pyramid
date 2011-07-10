from pyramid.exceptions import Forbidden

USERS = {}
PROJECTS = {}


# The groupfinder is currently not used to protect any view, because the 
# security is enforced solely in the check_permission method
def groupfinder(userid, request):
    if userid in USERS:
        return []


def check_permission(request, logged_in):
    project_name = request.matchdict.get('project_name', None)
    anonymous_projects = PROJECTS.get("anonymous", [])

    if request.matched_route.name == 'p1_homepage':
        # homepage
        pass
    elif project_name in anonymous_projects:
        # Anonymous can access
        pass
    elif logged_in == None:
        # Show the login page if the user is not logged in
        # For test purposes, no login is needed when accessing through localhost
        raise Forbidden
    else:
        if logged_in == 'admin':
            # Allow access to all projects to the admin user
            pass
        elif logged_in in USERS.keys():
            if project_name in PROJECTS[logged_in]:
                # User can access this project
                pass
            else:
                raise Forbidden
        else:
            raise Forbidden
