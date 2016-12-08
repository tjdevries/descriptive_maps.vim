import neovim
from .prompt.prompt import STATUS_ACCEPT


@neovim.plugin
class DescriptiveMaps:
    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.function('_descriptive_start', sync=True)
    def start(self, args):
        print(STATUS_ACCEPT)
        print(args)
