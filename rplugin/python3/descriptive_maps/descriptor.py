from descriptive_maps.prompt.prompt import (
    Prompt
)

from .util import assign_content


class Descriptor(Prompt):
    def __init__(self, nvim, condition):
        super().__init__(nvim)
        self._map_raw = self.nvim.call('execute', ['verbose nmap ,']).split('\n')

        with open('/home/dexter/descriptor.log', 'w') as f:
            f.write(str(self._map_raw))

        self._map_dict = self.nvim.call('descriptive_maps#parse', self._map_raw)

    def start(self):
        return super().start()

    def on_init(self):
        self.nvim.command('noautocmd keepjumps enew')
        self.nvim.current.buffer.options['buftype'] = 'nofile'
        self.nvim.current.buffer.options['bufhidden'] = 'wipe'
        self.nvim.current.buffer.options['buflisted'] = False
        self.nvim.current.window.options['spell'] = False
        self.nvim.current.window.options['foldenable'] = False
        self.nvim.current.window.options['colorcolumn'] = ''
        self.nvim.current.window.options['cursorline'] = True
        self.nvim.current.window.options['cursorcolumn'] = False

    def on_update(self, status):
        self.nvim.call('cursor', [1, self.nvim.current.window.cursor[1]])

        content = ['hello', 'world', 'how are you']
        content.extend(self._map_dict['n'].keys())
        assign_content(self.nvim, content)
        return super().on_update(status)
