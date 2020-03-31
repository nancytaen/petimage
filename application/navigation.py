def top_level_nav(login=False, signup=False):
    return [{'name': 'Create Account', 'url': '/signup', 'status': signup},
            {'name': 'Login', 'url': '/login', 'status': login}
            ]
