import neovim

from .config import DescriptorConfig
from .prompt.prompt import STATUS_ACCEPT
from .util import assign_content, open_preview


@neovim.plugin
class DescriptiveMaps:
    def __init__(self, nvim):
        self.nvim = nvim
        self.requires_update = True

        self._config_raw = self.nvim.call('descriptive_maps#find_variables')
        self.config = DescriptorConfig(self._config_raw)

    @neovim.function('DescriptiveStart', sync=True)
    def start(self, args):
        # If we pass an argument, that's the forced refresh param
        # Otherwise, we'll use the value from the config
        if len(args) > 0:
            self.requires_update = bool(args[0])
        else:
            self.requires_update = self.config.force_refresh

        status = self.desc.start()

        if status == STATUS_ACCEPT:
            self.nvim.call('execute', 'close')
            return self.nvim.call('nvim_input', self.desc.result.lhs)

    @neovim.function('DescriptiveDebug', sync=True)
    def debug(self, args):
        open_preview(self.nvim, 'DescriptiveDebug')
        assign_content(self.nvim, self.config.to_list())

    @property
    def desc(self):
        self._desc = getattr(self, '_desc', None)

        if self._desc is None or self.requires_update:
            from .descriptor import Descriptor
            self._desc = Descriptor(self.nvim, {}, self.config)

        return self._desc
