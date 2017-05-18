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
            self.debug_msg('text', self.desc.text)
            self.debug_msg('result', self.desc.result)

            try:
                lhs = self.desc.result.lhs
            except Exception as e:
                lhs = ''

            return self.nvim.call('nvim_input', lhs)

    @neovim.function('DescriptiveDebug', sync=True)
    def debug(self, args):
        open_preview(self.nvim, 'DescriptiveDebug')
        assign_content(self.nvim, self.config.to_list())

    def debug_msg(self, name, item):
        if self.config.debug_mode:
            try:
                self.nvim.command('echom "[DESC:{0}] {1}"'.format(name, str(item)))
            except:
                self.nvim.command('echom "[DESC:{0}] Not able to convert'.format(name))

    @property
    def desc(self):
        self._desc = getattr(self, '_desc', None)

        if self._desc is None or self.requires_update:
            self.debug_msg('CREATE', 'Creating new Descriptor')
            from .descriptor import Descriptor
            self._desc = Descriptor(self.nvim, {}, self.config)

            self.requires_update = False

        return self._desc
