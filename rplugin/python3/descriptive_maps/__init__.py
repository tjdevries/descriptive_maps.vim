import neovim
from .prompt.prompt import STATUS_ACCEPT


@neovim.plugin
class DescriptiveMaps:
    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.function('_descriptive_start', sync=True)
    def start(self, args):
        from .descriptor import Descriptor

        desc = Descriptor(self.nvim, {})
        status = desc.start()

        if status == STATUS_ACCEPT:
            self.nvim.call('append', 0, ['hello world'])
