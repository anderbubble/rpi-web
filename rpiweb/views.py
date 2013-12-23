from pyramid.view import view_config

import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)

GPIO_PINS = set([11, 12, 13, 15, 16, 18, 22, 7])
GPIO_OUTPUTS = {}

for channel in GPIO_PINS:
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'rpi-web'}


@view_config(route_name='inputs', renderer='templates/inputs.pt')
def inputs(request):
    inputs = GPIO_PINS - set(GPIO_OUTPUTS)
    channels = dict(
        (channel, GPIO.input(channel))
        for channel in inputs
        )
    return {'inputs': channels}


@view_config(route_name='outputs', renderer='templates/outputs.pt')
def outputs(request):
    return {'outputs': GPIO_OUTPUTS}


@view_config(route_name='outputs_post', renderer='json')
def output_post(request):
    channel = int(request.params['channel'])
    GPIO.setup(channel, GPIO.OUT)
    GPIO.output(channel, GPIO.LOW)
    GPIO_OUTPUTS[channel] = GPIO.LOW
    return outputs(request)


@view_config(route_name='output_toggle', renderer='json')
def output_toggle(request):
    channel = int(request.matchdict['channel'])
    starting_value = GPIO_OUTPUTS[channel]
    if starting_value == GPIO.LOW:
        new_value = GPIO.HIGH
    else:
        new_value = GPIO.LOW
    GPIO.output(channel, new_value)
    GPIO_OUTPUTS[channel] = new_value
    return outputs(request)
