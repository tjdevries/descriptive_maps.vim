
let s:_map_arguments = [
            \ '<buffer>',
            \ '<nowait>',
            \ '<silent>',
            \ '<special>',
            \ '<script>',
            \ '<expr>',
            \ '<unique>'
            \ ]
let s:_tracked_descriptors = [
            \ 'mode',
            \ 'lhs',
            \ 'rhs',
            \ 'description',
            \ 'args',
            \ 'executed',
            \ ]

""
" Store information about the mapping in {command_string}
" Also executes the command if {to_exec} is v:true
function! descriptive_maps#describe(command_string, to_exec)
    let l:cmd_split = split(a:command_string)

    let l:map_command = l:cmd_split[0]

    " Parse the arguments. Use our map arguments
    let l:list_args = []
    let l:ind = 1
    while (l:ind < len(l:cmd_split)) && (index(s:_map_arguments, l:cmd_split[l:ind]) >= 0)
        call add(l:list_args, l:cmd_split[l:ind])
        let l:ind = l:ind + 1
    endwhile
    if len(l:list_args) > 0
        let l:map_args = join(l:list_args, ' ')
    else
        let l:map_args = ''
    endif

    let l:lhs = l:cmd_split[l:ind]

    let l:description_split_location = index(l:cmd_split, g:_description_separator)
    if l:description_split_location >= 0
        let l:rhs = join(l:cmd_split[l:ind + 1: l:description_split_location - 1], ' ')
        let l:description = join(l:cmd_split[l:description_split_location + 1:], ' ')
    else
        let l:rhs = join(l:cmd_split[l:ind + 1:], ' ')
        let l:description = g:_description_unknown
    endif

    call descriptive_maps#handle_arguments(l:map_command, l:map_args, l:lhs, l:rhs, l:description)
endfunction


function! descriptive_maps#handle_arguments(map_command, map_args, lhs, rhs, description)
    " echom a:map_command . a:map_args . a:lhs . a:rhs . a:description

    if index(keys(g:descriptive_maps), a:map_command) >= 0
        let g:descriptive_maps[a:map_command] = g:descriptive_maps[a:map_command]
    else
        let g:descriptive_maps[a:map_command] = get(g:descriptive_maps, a:map_command, {})
    endif

    let g:descriptive_maps[a:map_command][a:lhs] = {
                \ 'mode': a:map_command,
                \ 'lhs': a:lhs,
                \ 'rhs': a:rhs,
                \ 'description': a:description,
                \ 'args': a:map_args,
                \ 'executed': g:_description_execute,
                \ }

    let g:last_handled = a:map_command  . ' ' . a:map_args . ' ' . a:lhs . ' ' . a:rhs

    if g:_description_execute
        execute g:last_handled
    endif
endfunction

""
" Return information required about the various commands
" For each characteristic, it returns:
"   max_length (int): the longest string in the category
function! descriptive_maps#understand(maps)
    let l:understood = {}
    for l:tracked in s:_tracked_descriptors
        let l:understood[l:tracked] = {}
        let l:understood[l:tracked]['max_length'] = 0
    endfor

    " Find the max length
    for l:mode in keys(g:descriptive_maps)
        let l:maps = keys(g:descriptive_maps[l:mode])

        for l:map in l:maps
            for l:tracked in s:_tracked_descriptors
                " v:true and v:false don't work with length
                " so we just use the longer of the two, which is 7.
                " Might have to do more with this later
                try
                    let l:current_length = len(g:descriptive_maps[l:mode][l:map][l:tracked])
                catch
                    let l:current_length = 7
                endtry

                " TODO: Handle args correctly
                let l:understood[l:tracked]['max_length'] = max([
                            \ l:understood[l:tracked]['max_length'],
                            \ l:current_length
                            \ ])
            endfor
        endfor
    endfor

    return l:understood
endfunction

function! s:format_line(descriptor, understood)
    let l:format = printf(
                \ '%' . a:understood['description']['max_length'] . 's' .
                \ ': ' .
                \ '%' . a:understood['mode']['max_length'] . 's | ' .
                \ '%' . a:understood['lhs']['max_length'] . 's  --> ' .
                \ '%' . a:understood['rhs']['max_length'] . 's' .
                \ '  | ' .
                \ '%' . a:understood['args']['max_length'] . 's',
                \
                \ a:descriptor['description'],
                \ a:descriptor['mode'],
                \ a:descriptor['lhs'],
                \ a:descriptor['rhs'],
                \ a:descriptor['args']
                \ )

    return l:format
endfunction

function! s:get_formatted_lines()
    let l:understood = descriptive_maps#understand(g:descriptive_maps)

    let l:lines = []

    for l:mode in sort(copy(keys(g:descriptive_maps)))
        let l:maps = sort(keys(g:descriptive_maps[l:mode]))

        for l:map in l:maps
            let l:temp = g:descriptive_maps[l:mode][l:map]
            call add(l:lines, s:format_line(
                        \ l:temp,
                        \ l:understood
                        \ ))
        endfor
    endfor

    return l:lines
endfunction

function! descriptive_maps#report_lines()
    let l:lines = []

    let l:understood = descriptive_maps#understand(g:descriptive_maps)
    " echo l:understood

    let l:name_dictionary = {
                \ 'description': 'description',
                \ 'lhs': 'lhs',
                \ 'rhs': 'rhs',
                \ 'mode': 'mode',
                \ 'args': 'args',
                \ }
    call add(l:lines, s:format_line(l:name_dictionary, l:understood))
    call add(l:lines, repeat('-', len(s:format_line(l:name_dictionary, l:understood))))

    call extend(l:lines, s:get_formatted_lines())


    for l:line in l:lines
        echo l:line
    endfor

    return l:lines
endfunction

function! descriptive_maps#complete_description(prefix)
    " let l:understood = descriptive_maps#understand(g:descriptive_maps)

    let l:compl_list = []
    for key in keys(g:descriptive_maps['nnoremap'])
        call add(l:compl_list, key)
    endfor

    call complete(col('.'), l:compl_list)
    return ''
endfunction


