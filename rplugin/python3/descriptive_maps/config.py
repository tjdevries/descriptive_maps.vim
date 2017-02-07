import sys

KEY_PREFIX = 'descriptor#'
LEN_KEY_PREFI = len(KEY_PREFIX)

DEFAULTS = {
    'immediate_result': True,
}

class DescriptorConfig:
    def __init__(self, config_dict: dict):
        for key, value in config_dict.items():
            self.set('_' + key, value)

    def set(self, key, value):
        key = key[LEN_KEY_PREFIX:]
        setattr(self, '_' + str(key), value)

    def _default(self, name):
        if not hasattr(self, '_' + name):
            setattr(self, '_' + name, DEFAULTS[name])

    @property
    def immediate_result(self):
        self._default(sys._getframe().f_code.co_name)

        return self._immediate_result
