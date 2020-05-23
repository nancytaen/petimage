from flask import session


def top_level_nav(login=False, signup=False):
    """
    returns a list of pages to be displayed on navigation bar
    Parameters indicate the page user is currently on
    :param login: if set to True, Login is bolded on the navigation bar
    :param signup: if set to True, Signup is bolded on the navigation bar
    :return:
    """
    return [{'name': 'Create Account', 'url': '/signup', 'status': signup},
            {'name': 'Login', 'url': '/login', 'status': login}
            ]


def logged_in_nav(timeline=False, feed=False, create=False):
    """
    navigation bar content for logged in pages
    :return:
    """
    return [{'name': 'Timeline', 'url': '/post/timeline', 'status': timeline},
            {'name': 'My Feed', 'url': '/post/feed/' + session['username'], 'status': feed},
            {'name': 'Create Post', 'url': '/post/create', 'status': create}]


def logged_in_user():
    return {'username': session['username'],
            'edit_url': '/user/account',
            'profile_img': session['profile_img'],
            'logout_url': '/logout'
            }
