def _select_next_candidate(descriptor, params):
    line, col = descriptor.nvim.current.window.cursor
    descriptor.nvim.call('cursor', [line + 1, col])


def _select_previous_candidate(descriptor, params):
    line, col = descriptor.nvim.current.window.cursor
    descriptor.nvim.call('cursor', [line - 1, col])


DEFAULT_ACTION_RULES = [
    ('descriptor:select_next_candidate', _select_next_candidate),
    ('descriptor:select_previous_candidate', _select_previous_candidate),
]


DEFAULT_ACTION_KEYMAP = [
    ('<C-n>', '<descriptor:select_next_candidate>', 'noremap'),
    ('<C-p>', '<descriptor:select_previous_candidate>', 'noremap'),
]
