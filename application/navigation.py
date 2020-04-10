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


def logged_in_nav():
    """
    navigation bar content for logged in pages
    :return:
    """
    return [{'name': 'Logout', 'url': '/logout', 'status': False}]
