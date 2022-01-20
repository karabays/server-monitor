import json
import psutil
import humanize
from datetime import datetime as dt
from loguru import logger

class Sensor:

    def __init__(self, device_name, topic_prefix, params=None) -> None:
        self.name = device_name + ' Uptime'
        self.id = self.name.replace(" ", "_").lower()
        self.conf_topic = topic_prefix + 'sensor/' + self.id + "/config"
        self.state_topic = topic_prefix + 'sensor/' + self.id + "/state"

    @property
    def config_msg(self):
        config_dict = {}
        config_dict['topic'] = self.conf_topic
        config_dict['payload'] = json.dumps({"name": self.name, "unique_id": self.id,
            "state_topic": self.state_topic,
            "icon": "mdi:calendar-import",
            "value_template": "{{ value_json.uptime_hours }}",
            "unit_of_measurement": "hours",
            "json_attributes_topic": self.state_topic,
            "json_attributes_template": "{{value_json | tojson }}" })
        return config_dict

    @property
    def state_msg(self):
        boottime = dt.fromtimestamp(psutil.boot_time())
        boottime_str = boottime.strftime("%Y-%m-%d %H:%M:%S")
        delta = dt.now()-boottime
        uptime_hours = round(delta.total_seconds()/3600.0, 1)
        uptime = humanize.precisedelta(delta, minimum_unit='minutes')
        state_dict = {}
        state_dict['topic'] = self.state_topic
        state_dict['payload'] = json.dumps({"uptime_hours": uptime_hours,
            "uptime": uptime, "boot_time": boottime_str})
        logger.debug(state_dict)
        logger.info(state_dict["payload"])
        return state_dict

    def get_stats(self):
        return (self.config_msg, self.state_msg)
