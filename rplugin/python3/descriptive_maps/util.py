def assign_content(nvim, content):
    """Assign content to the current buffer.
    Args:
        nvim (neovim.Nvim): A ``neovim.Nvim`` instance.
        content (str): A str content.

    Refernce:
        https://github.com/lambdalisue/lista.nvim/blob/master/rplugin/python3/lista/util.py
    """
    viewinfo = nvim.call('winsaveview')
    nvim.current.buffer.options['modifiable'] = True
    nvim.current.buffer[:] = content
    nvim.current.buffer.options['modifiable'] = False
    nvim.call('winrestview', viewinfo)


def open_preview(nvim, name):
    # Open and move to preview
    nvim.command('setlocal hidden')
    nvim.command('pedit ' + name)
    nvim.command('redraw!')

    preview = find_preview(nvim)

    if preview > 0:
        nvim.call('nvim_set_current_win', preview)

    # Set options
    nvim.current.buffer.options['buftype'] = 'nofile'
    nvim.current.buffer.options['bufhidden'] = 'wipe'
    nvim.current.buffer.options['buflisted'] = False
    nvim.current.window.options['spell'] = False
    nvim.current.window.options['foldenable'] = False
    nvim.current.window.options['colorcolumn'] = ''
    nvim.current.window.options['cursorline'] = True
    nvim.current.window.options['cursorcolumn'] = False
    nvim.command('set syntax=vim')


def find_preview(nvim):
    windows = nvim.call('nvim_list_wins')

    for window in windows:
        if is_preview(nvim, window):
            return window

    return -1


def is_preview(nvim, window):
    try:
        return nvim.call('nvim_win_get_option', int(window), 'previewwindow')
    except:
        return False
