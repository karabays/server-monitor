import importlib

from config import configuration

device_name = configuration.get('device_name')
topic_prefix = configuration.get('mqtt')['topic_prefix']


def get_messages():
    config_msgs = []
    state_msgs = []

    for sensor in configuration.get('sensors'):
        for key, value in sensor.items():
            module = importlib.import_module('.'+key, package='sensors')
            mod = getattr(module, 'Sensor')
            sensor = mod(device_name, topic_prefix, value)

            conf_msg = sensor.config_msg
            stat_msg = sensor.state_msg

            if isinstance(conf_msg, list):
                config_msgs.extend(conf_msg)
            else:
                config_msgs.append(conf_msg)

            if isinstance(stat_msg, list):
                state_msgs.extend(stat_msg)
            else:
                state_msgs.append(stat_msg)

    return (config_msgs, state_msgs)


if __name__ == '__main__':
    confs, states = get_messages()
    #print(states)
    