import voluptuous as vol

import esphomeyaml.config_validation as cv
from esphomeyaml.components import light
from esphomeyaml.const import CONF_BLUE, CONF_DEFAULT_TRANSITION_LENGTH, CONF_GAMMA_CORRECT, \
    CONF_GREEN, CONF_MAKE_ID, CONF_NAME, CONF_RED, CONF_WHITE
from esphomeyaml.helpers import App, get_variable, variable

PLATFORM_SCHEMA = cv.nameable(light.LIGHT_PLATFORM_SCHEMA.extend({
    cv.GenerateID(CONF_MAKE_ID): cv.declare_variable_id(light.MakeLight),
    vol.Required(CONF_RED): cv.use_variable_id(None),
    vol.Required(CONF_GREEN): cv.use_variable_id(None),
    vol.Required(CONF_BLUE): cv.use_variable_id(None),
    vol.Required(CONF_WHITE): cv.use_variable_id(None),
    vol.Optional(CONF_GAMMA_CORRECT): cv.positive_float,
    vol.Optional(CONF_DEFAULT_TRANSITION_LENGTH): cv.positive_time_period_milliseconds,
}))


def to_code(config):
    red = None
    for red in get_variable(config[CONF_RED]):
        yield
    green = None
    for green in get_variable(config[CONF_GREEN]):
        yield
    blue = None
    for blue in get_variable(config[CONF_BLUE]):
        yield
    white = None
    for white in get_variable(config[CONF_WHITE]):
        yield
    rhs = App.make_rgbw_light(config[CONF_NAME], red, green, blue, white)
    light_struct = variable(config[CONF_MAKE_ID], rhs)
    light.setup_light(light_struct.Pstate, light_struct.Pmqtt, config)
