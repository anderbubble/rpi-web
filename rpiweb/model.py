import logging
log = logging.getLogger(__name__)


try:
    import RPi.GPIO as GPIO
except RuntimeError, ex:
    GPIO = None
    log.warn('RPi.GPIO module not loaded: {0}'.format(ex))


# BOARD pinout
GPIO_PINS = {
    'GPIO0': 11,
    'GPIO1': 12,
    'GPIO2': 13,
    'RPIO3': 15,
    'GPIO4': 16,
    'GPIO5': 18,
    'GPIO6': 22,
    'GPIO7': 7,
    }

gpio_outputs = {}


def gpio_init ():
    if GPIO:
        log.info('set GPIO mode to BOARD')
        GPIO.setmode(GPIO.BOARD)

        for channel in GPIO_PINS:
            log.info('set GPIO channel {0} to IN')
            GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    else:
        log.warn('GPIO not initialized: GPIO module not loaded')

    return GPIO_PINS


def get_gpio_inputs ():
    pins = set(GPIO_PINS) - set(gpio_outputs.iterkeys())
    channels = [GPIO_PINS[pin] for pin in pins]
    if GPIO:
        values = (GPIO.input(channel) for channel in channels)
    else:
        log.warn('input channels unavailable: GPIO module not loaded')
        values = (None for channel in channels)
    inputs = dict(zip(pins, values))
    return inputs


def setup_gpio_output (pin):
    channel = GPIO_PINS[pin]
    if GPIO:
        GPIO.setup(channel, GPIO.OUT)
        log.info('setup channel {0} as OUT'.format(channel))
        GPIO.output(channel, GPIO.LOW)
        gpio_outputs[pin] = False
        log.info('set default output for channel {0} to LOW'.format(channel))
    else:
        log.warn('channel {0} unconfigured: GPIO module not loaded'.format(channel))
        gpio_outputs[pin] = False


def toggle_gpio_output (pin):
    channel = GPIO_PINS[pin]
    starting_value = gpio_outputs[pin]

    if starting_value == False:
        gpio_outputs[pin] = True
    else:
        gpio_outputs[pin] = False

    if GPIO:
        if gpio_outputs[pin] is True:
            new_value = GPIO.HIGH
        else:
            new_value = GPIO.LOW
        GPIO.output(channel, new_value)
    else:
        log.warn('channel {0} unconfigured: GPIO module not loaded'.format(channel))
    return gpio_outputs[pin]


def get_gpio_outputs ():
    return gpio_outputs.copy()
