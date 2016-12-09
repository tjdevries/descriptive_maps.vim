import re

from descriptive_maps.prompt.prompt import (
    Prompt
)

from .action import DEFAULT_ACTION_KEYMAP, DEFAULT_ACTION_RULES
from .util import assign_content


class Descriptor(Prompt):
    def __init__(self, nvim, condition):
        super().__init__(nvim)
        self._map_raw = self.nvim.call('execute', ['verbose nmap']).split('\n')

        # with open('/home/dexter/descriptor.log', 'w') as f:
        #     f.write(str(self._map_raw))

        self._map_dict = self.nvim.call('descriptive_maps#parse', self._map_raw)

        self.action.register_from_rules(DEFAULT_ACTION_RULES)
        self.keymap.register_from_rules(self.nvim, DEFAULT_ACTION_KEYMAP)

        self._requires_update = False
        self._lhs_mapping_length = None
        self._rhs_mapping_length = None
        self.lhs_max_length = 25
        self.rhs_max_length = 40

    def start(self):
        return super().start()

    def on_init(self):
        self.nvim.command('new +setlocal previewwindow|setlocal buftype=nofile|setlocal noswapfile|setlocal wrap')
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

        options = self._map_dict['n'].keys()

        applicable_keys = [
            o for o in options
            if o.startswith(self.text)
        ]

        result_string = '{0:%s.%s} -> {1:%s.%s} || {2}' % (
            self.lhs_mapping_length, self.lhs_mapping_length,
            self.rhs_mapping_length, self.rhs_mapping_length,
        )

        results = [
            result_string.format(
                o,
                self._get_rhs(o),
                self._format_comment(o),
            )
            for o in applicable_keys
        ]

        assign_content(self.nvim, results)
        return super().on_update(status)

    @property
    def lhs_mapping_length(self):
        if self._lhs_mapping_length is None or self._requires_update:
            self._lhs_mapping_length = max(len(x) for x in self._map_dict['n'].keys()) + 5

            self._lhs_mapping_length = min(
                self._lhs_mapping_length,
                self.lhs_max_length,
            )

        return self._lhs_mapping_length

    @property
    def rhs_mapping_length(self):
        if self._rhs_mapping_length is None or self._requires_update:
            self._rhs_mapping_length = max(len(x['rhs']) for x in self._map_dict['n'].values())

            self._rhs_mapping_length = min(
                self._rhs_mapping_length,
                self.rhs_max_length,
            )

        return self._rhs_mapping_length

    def _get_rhs(self, key):
        return self._map_dict['n'][key]['rhs']

    def _format_comment(self, key):
        comment_list = self._map_dict['n'][key]['comments']

        if len(comment_list) == 0:
            return ''

        comment_str = ', '.join(re.sub(r'\A\s*"\s*', '', x) for x in comment_list)
        return comment_str.replace('">', '').strip()
