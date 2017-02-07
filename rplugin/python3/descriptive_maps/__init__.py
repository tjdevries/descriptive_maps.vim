import neovim
from .prompt.prompt import STATUS_ACCEPT


@neovim.plugin
class DescriptiveMaps:
    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.function('_descriptive_start', sync=True)
    def start(self, args):
        status = self.desc.start()

        if status == STATUS_ACCEPT:
            self.nvim.call('execute', 'close')
            # self.nvim.call('append', 0, ['hello world'])
            return self.nvim.call('nvim_input', self.desc.text)

    @property
    def desc(self):
        self._desc = getattr(self, '_desc', None)

        # if self._desc is None:
        from .descriptor import Descriptor
        self._desc = Descriptor(self.nvim, {})

        return self._desc
