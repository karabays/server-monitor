from pathlib import Path
from time import sleep
import paho.mqtt.publish as mqtt
from loguru import logger
import click

from config import configuration
import messages

APP_FOLDER = Path(__file__).parent
MQTT_HOST = configuration.get('mqtt')['host']
logger.add(APP_FOLDER.joinpath("monitor.log"), rotation="1 week",
    level=configuration.get('log_level'))


@click.group()
def cli():
    pass

@cli.command()
def publish():

    logger.info("Start checking system.")

    config_msgs, state_msgs = messages.get_messages()
    mqtt.multiple(config_msgs, hostname=MQTT_HOST, keepalive=60)
    sleep(1)
    mqtt.multiple(state_msgs, hostname=MQTT_HOST, keepalive=60)

    logger.info('Sensors values sent to mqtt broker.')

@cli.command()
def delete():
    config_msgs, state_msgs = messages.get_messages()

    for msg in config_msgs:
        msg['payload'] = ''

    mqtt.multiple(config_msgs, hostname=MQTT_HOST, keepalive=60)
    logger.info("Delete messages sent to mqtt broker.")

if __name__ == '__main__':
    cli()
