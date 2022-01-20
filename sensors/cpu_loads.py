import json
import psutil

from loguru import logger

class Sensor:

    def __init__(self, device_name, topic_prefix, params=None) -> None:
        self.name = device_name + ' CPU Load'
        self.id = self.name.replace(" ", "_").lower()
        self.conf_topic = topic_prefix + 'sensor/' + self.id + "/config"
        self.state_topic = topic_prefix + 'sensor/' + self.id + "/state"

    @property
    def config_msg(self):
        config_dict = {}
        config_dict['topic'] = self.conf_topic
        config_dict['payload'] = json.dumps({"name": self.name, "unique_id": self.id,
            "state_topic": self.state_topic,
            "icon": "mdi:cpu-64-bit",
            "value_template": "{{ value_json.load_15 }}",
            "unit_of_measurement": "threads",
            "json_attributes_topic": self.state_topic,
            "json_attributes_template": "{{value_json | tojson }}" })
        return config_dict

    @property
    def state_msg(self):
        load1, load5, load15 = psutil.getloadavg()
        state_dict = {}
        state_dict['topic'] = self.state_topic
        state_dict['payload'] = json.dumps({"load_1": load1, "load_5": load5, "load_15": load15})
        logger.debug(state_dict)
        logger.info(state_dict["payload"])
        return state_dict

    def get_stats(self):
        return (self.config_msg, self.state_msg)
