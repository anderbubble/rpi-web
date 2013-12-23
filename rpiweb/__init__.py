from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/', request_method='GET')
    config.add_route('inputs', '/inputs', request_method='GET')
    config.add_route('setup_output', '/outputs/{channel}', request_method='PUT')
    config.add_route('setup_output_post', '/outputs/{channel}',
                     request_method = 'POST',
                     request_param = 'METHOD=PUT',
                     )
    config.add_route('outputs', '/outputs', request_method='GET')
    config.add_route('outputs_post', '/outputs', request_method='POST')
    config.add_route('output_toggle', '/outputs/{channel}', request_method='POST')
    config.scan()
    return config.make_wsgi_app()
