from __future__ import print_function

import logging
from datetime import datetime

import paho.mqtt.client as mqtt

from esphomeyaml.const import CONF_BROKER, CONF_DISCOVERY_PREFIX, CONF_ESPHOMEYAML, CONF_LOGGER, \
    CONF_LOG_TOPIC, CONF_MQTT, CONF_NAME, CONF_PASSWORD, CONF_PORT, CONF_TOPIC_PREFIX, \
    CONF_USERNAME

_LOGGER = logging.getLogger(__name__)


def initialize(config, subscriptions, on_message, username, password, client_id):
    def on_connect(client, userdata, flags, return_code):
        for topic in subscriptions:
            client.subscribe(topic)

    client = mqtt.Client(client_id or u'')
    client.on_connect = on_connect
    client.on_message = on_message
    if username is None:
        if config[CONF_MQTT].get(CONF_USERNAME):
            client.username_pw_set(config[CONF_MQTT][CONF_USERNAME],
                                   config[CONF_MQTT][CONF_PASSWORD])
    elif username:
        client.username_pw_set(username, password)
    client.connect(config[CONF_MQTT][CONF_BROKER], config[CONF_MQTT][CONF_PORT])

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        pass
    return 0


def show_logs(config, topic=None, username=None, password=None, client_id=None):
    if topic is not None:
        pass  # already have topic
    elif CONF_LOG_TOPIC in config.get(CONF_LOGGER, {}):
        topic = config[CONF_LOGGER][CONF_LOG_TOPIC]
    elif CONF_TOPIC_PREFIX in config[CONF_MQTT]:
        topic = config[CONF_MQTT][CONF_TOPIC_PREFIX] + u'/debug'
    else:
        topic = config[CONF_ESPHOMEYAML][CONF_NAME] + u'/debug'
    _LOGGER.info(u"Starting log output from %s", topic)

    def on_message(client, userdata, msg):
        time = datetime.now().time().strftime(u'[%H:%M:%S] ')
        print(time + msg.payload)

    return initialize(config, [topic], on_message, username, password, client_id)


def clear_topic(config, topic, username=None, password=None, client_id=None):
    if topic is None:
        discovery_prefix = config[CONF_MQTT].get(CONF_DISCOVERY_PREFIX, u'homeassistant')
        name = config[CONF_ESPHOMEYAML][CONF_NAME]
        topic = u'{}/+/{}/#'.format(discovery_prefix, name)
    _LOGGER.info(u"Clearing messages from %s", topic)

    def on_message(client, userdata, msg):
        if not msg.payload:
            return
        print(u"Clearing topic {}".format(msg.topic))
        client.publish(msg.topic, None, retain=True)

    return initialize(config, [topic], on_message, username, password, client_id)