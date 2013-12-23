from pyramid.config import Configurator

from .model import (
    gpio_init,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    config.include('pyramid_chameleon')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/', request_method='GET')

    config.add_route('get_gpio_inputs', '/gpio/inputs', request_method='GET')

    config.add_route('get_gpio_outputs', '/gpio/outputs', request_method='GET')
    config.add_route('post_gpio_outputs', '/gpio/outputs', request_method='POST')

    config.add_route('post_gpio_output', '/gpio/outputs/{pin}', request_method='POST')
    config.scan()

    gpio_init()
    return config.make_wsgi_app()
