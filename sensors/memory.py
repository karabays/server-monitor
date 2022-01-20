import json
import psutil

from loguru import logger

class Sensor:

    def __init__(self, device_name, topic_prefix, params=None) -> None:
        self.name = device_name + ' Memory Usage'
        self.id = self.name.replace(" ", "_").lower()
        self.conf_topic = topic_prefix + 'sensor/' + self.id + "/config"
        self.state_topic = topic_prefix + 'sensor/' + self.id + "/state"

    @property
    def config_msg(self):
        config_dict = {}
        config_dict['topic'] = self.conf_topic
        config_dict['payload'] = json.dumps({"name": self.name, "unique_id": self.id,
            "state_topic": self.state_topic,
            "icon": "mdi:memory",
            "value_template": "{{ value_json.used_memory_perc }}",
            "unit_of_measurement": "%",
            "json_attributes_topic": self.state_topic,
            "json_attributes_template": "{{value_json | tojson }}" })
        return config_dict

    @property
    def state_msg(self):
        mem = psutil.virtual_memory()
        used_perc = round((mem.used / mem.total)*100, 2)
        state_dict = {}
        state_dict['topic'] = self.state_topic
        state_dict['payload'] = json.dumps({"used_memory_perc": used_perc,
            "available_memory_GB": round(mem.available / 1073741824.0 ,2),
            "total_memory_GB": round(mem.total / 1073741824.0 ,2)})
        logger.debug(state_dict)
        logger.info(state_dict["payload"])
        return state_dict

    def get_stats(self):
        return (self.config_msg, self.state_msg)
