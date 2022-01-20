import json
import psutil

from loguru import logger

class Sensor:
    def __init__(self, device_name, topic_prefix, params=None) -> None:
        self.mount_points = []
        for mount in params:
            mount_point = MountPoint(device_name, topic_prefix, mount)
            self.mount_points.append(mount_point)

    @property
    def config_msg(self):
        return [m.config_msg for m in self.mount_points]

    @property
    def state_msg(self):
        return [m.state_msg for m in self.mount_points]


class MountPoint:
    def __init__(self, device_name, topic_prefix, mount) -> None:
        self.mount = mount['mount']
        self.name = f"{device_name} {mount['name']} storage used"
        self.id = self.name.replace(" ", "_").lower()
        self.conf_topic = topic_prefix + 'sensor/' + self.id + "/config"
        self.state_topic = topic_prefix + 'sensor/' + self.id + "/state"

    @property
    def config_msg(self):
        config_dict = {}
        config_dict['topic'] = self.conf_topic
        config_dict['payload'] = json.dumps({"name": self.name, "unique_id": self.id,
            "state_topic": self.state_topic,
            "icon": "mdi:harddisk",
            "value_template": "{{ value_json.disk_used_perc }}",
            "unit_of_measurement": "%",
            "json_attributes_topic": self.state_topic,
            "json_attributes_template": "{{value_json | tojson }}" })
        return config_dict

    @property
    def state_msg(self):
        disk = psutil.disk_usage(self.mount)
        state_dict = {}
        state_dict['topic'] = self.state_topic
        state_dict['payload'] = json.dumps({"disk_used": round(disk.used / 1073741824.0 ,2),
            'disk_used_perc': disk.percent,
            'disk_total': round(disk.total / 1073741824.0 ,2)})
        logger.debug(state_dict)
        logger.info(state_dict["payload"])
        return state_dict

    def get_stats(self):
        return (self.config_msg, self.state_msg)
