from pathlib import Path
import json

from loguru import logger

class Sensor:

    def __init__(self, device_name, topic_prefix, params=None) -> None:
        self.name = device_name + ' restart needed'
        self.id = self.name.replace(" ", "_").lower()
        self.conf_topic = topic_prefix + 'binary_sensor/' + self.id + "/config"
        self.state_topic = topic_prefix + 'binary_sensor/' + self.id + "/state"

    @property
    def config_msg(self):
        config_dict = {}
        config_dict['topic'] = self.conf_topic

        payload = {}
        payload["name"] = self.name
        payload["unique_id"] = self.id
        payload["state_topic"] = self.state_topic
        payload["icon"] = "mdi:update"
        config_dict['payload'] = json.dumps(payload)

        return config_dict

    @property
    def state_msg(self):
        state_dict = {'topic':self.state_topic}
        if Path('/var/run/reboot-required').exists():
            state_dict['payload'] = "ON"
        else:
            state_dict['payload'] = "OFF"
        logger.debug(state_dict)
        logger.info(state_dict["payload"])
        return state_dict

