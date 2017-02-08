from descriptive_maps.prompt.prompt import (
    Prompt,
    STATUS_ACCEPT,
)

from .action import DEFAULT_ACTION_KEYMAP, DEFAULT_ACTION_RULES
from .config import DescriptorConfig, FilterCase
from .parser import parse, ParsedLine
from .util import assign_content, open_preview


def option_filter(options, text, config=FilterCase.default):
    if FilterCase.ignorecase:
        return [
            o for o in options
            if o.lhs.lower().startswith(text.lower())
        ]
    else:
        return [
            o for o in options
            if o.lhs.startswith(text)
        ]


class Descriptor(Prompt):
    def __init__(self, nvim, condition, config: DescriptorConfig):
        super().__init__(nvim)
        self.result = ''

        self.config = config

        self._map_raw = self.nvim.call('execute', ['verbose nmap']).split('\n')
        self.mapping_candidates = parse(self._map_raw)

        self.action.register_from_rules(DEFAULT_ACTION_RULES)
        self.keymap.register_from_rules(self.nvim, DEFAULT_ACTION_KEYMAP)

        # State variables
        self.requires_update = False
        self._lhs_mapping_length = None
        self._rhs_mapping_length = None
        self.config.max_display_lhs = 25
        self.config.max_display_rhs = 40

    def start(self):
        return super().start()

    def on_init(self):
        open_preview(self.nvim, 'Descriptor')

    def on_update(self, status):
        current_mode = 'n'

        applicable_keys = option_filter(self.mapping_candidates, self.text, self.config)

        result_string = '{mode}map {lhs:%s.%s} {rhs:%s.%s} || {comment}' % (
            self.lhs_mapping_length, self.lhs_mapping_length,
            self.rhs_mapping_length, self.rhs_mapping_length,
        )

        results = [
            result_string.format(
                mode=current_mode,
                lhs=candidate.lhs,
                rhs=candidate.rhs,
                comment=self._format_comment(candidate),
            )
            # TODO: Limit here instead of below in the assign content?
            # This could make things faster
            for candidate in applicable_keys
        ]

        assign_content(self.nvim, results[:100])

        src = self.nvim.new_highlight_source()
        buf = self.nvim.current.buffer

        for i in range(len(results)):
            buf.add_highlight('Comment', i, self.precomment_length, -1, src_id=src)

        self.result = applicable_keys[self.nvim.call('line', ['.']) - 1]

        if len(results) == 1 and self.config.immediate_result:
            return STATUS_ACCEPT
        else:
            return super().on_update(status)

    @property
    def precomment_length(self):
        return self.lhs_mapping_length + self.rhs_mapping_length + 7

    @property
    def lhs_mapping_length(self):
        if self._lhs_mapping_length is None or self.requires_update:
            self._lhs_mapping_length = max(len(x.lhs) for x in self.mapping_candidates) + 5

            self._lhs_mapping_length = min(
                self._lhs_mapping_length,
                self.config.max_display_lhs,
            )

        return self._lhs_mapping_length

    @property
    def rhs_mapping_length(self):
        if self._rhs_mapping_length is None or self.requires_update:
            self._rhs_mapping_length = max(len(x.rhs) for x in self.mapping_candidates)

            self._rhs_mapping_length = min(
                self._rhs_mapping_length,
                self.config.max_display_rhs,
            )

        return self._rhs_mapping_length

    def _format_comment(self, candidate: ParsedLine):
        comment_list = candidate.comments

        if len(comment_list) == 0:
            return ''

        comment_str = ', '.join(comment_list)
        return comment_str.replace('">', '').strip()
