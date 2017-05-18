import enum
import sys

KEY_PREFIX = 'descriptive_maps#'
LEN_KEY_PREFIX = len(KEY_PREFIX)


class FilterCase(enum.Enum):
    ignorecase = 0
    default = 1


DEFAULTS = {
    'filter_case': {
        'type': FilterCase,
        'value': FilterCase.default
    },
    'force_refresh': {
        'type': bool,
        'value': True
    },
    'immediate_result': {
        'type': bool,
        'value': True
    },
    'max_display_lhs': {
        'type': int,
        'value': 25,
    },
    'max_display_rhs': {
        'type': int,
        'value': 40,
    },
    'debug_mode': {
        'type': bool,
        'value': True
    }
}


class DescriptorConfig:
    def __init__(self, config_dict: dict):
        for key, value in config_dict.items():
            self.set(key, value)

    def set(self, key, value):
        key = key[LEN_KEY_PREFIX:]

        if isinstance(DEFAULTS[key]['type'], enum.EnumMeta):
            result = getattr(DEFAULTS[key]['type'], value, None)

            # If we get a bad option, just set it to the default value
            if result is None:
                result = DEFAULTS[key]['value']
        else:
            result = value

        setattr(self, '_' + str(key), result)

    def _default(self):
        name = sys._getframe(1).f_code.co_name

        if not hasattr(self, '_' + name):
            setattr(self, '_' + name, DEFAULTS[name]['value'])

        return getattr(self, '_' + name)

    @property
    def filter_case(self):
        return self._default()

    @property
    def immediate_result(self):
        return self._default()

    @property
    def force_refresh(self):
        return self._default()

    @property
    def max_display_lhs(self):
        return self._default()

    @property
    def max_display_rhs(self):
        return self._default()

    @property
    def debug_mode(self):
        return self._default()

    def to_list(self):
        props = [
            name for name, value in vars(DescriptorConfig).items()
            if isinstance(value, property)
        ]

        props = sorted(props)
        prop_string = '{0:20} | {1}'
        return [
            prop_string.format(prop, getattr(self, prop))
            for prop in props
        ]
