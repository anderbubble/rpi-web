from pyramid.view import view_config

from . import model


def format_value (value):
    if value is 1:
        return 'HIGH'
    elif value is 0:
        return 'LOW'
    else:
        return 'unknown'


@view_config(route_name='get_gpio_inputs', renderer='templates/inputs.pt')
def get_gpio_inputs(request):
    inputs = model.get_gpio_inputs()
    return {'inputs': inputs, 'format_value': format_value}


@view_config(route_name='post_gpio_inputs', renderer='templates/inputs.pt')
def post_gpio_inputs(request):
    action = request.params['action']
    pin = request.params['pin']
    if action == 'setup':
        model.setup_gpio_input(pin)
    return get_gpio_inputs(request)



@view_config(route_name='get_gpio_outputs', renderer='templates/outputs.pt')
def get_gpio_outputs(request):
    outputs = model.get_gpio_outputs()
    return {'outputs': outputs, 'format_value': format_value}


@view_config(route_name='post_gpio_outputs', renderer='templates/outputs.pt')
def post_gpio_outputs(request):
    action = request.params['action']
    pin = request.params['pin']
    if action == 'setup':
        model.setup_gpio_output(pin)
    elif action == 'toggle':
        model.toggle_gpio_output(pin)
    return get_gpio_outputs(request)
