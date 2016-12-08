
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


function! descriptive_maps#parse(map_string) abort
  if type(a:map_string) == type('string')
    let l:map_list = split(a:map_string, "\n")
  elseif type(a:map_string) == type([])
    let l:map_list = a:map_string
  endif

  let l:map_dict = {
        \ 'n': {}
        \ }

  for l:line in l:map_list
    if l:line =~# '^n' 
      let l:mapped = descriptive_maps#parse_line(l:line)
      let l:map_dict[l:mapped['mode']][l:mapped['lhs']] = l:mapped
    elseif l:line =~? '\s*Last set from'
      let l:map_dict[l:mapped['mode']][l:mapped['lhs']]['source'] = descriptive_maps#parse_source(l:line)
    endif
  endfor

  for l:map in keys(l:map_dict['n'])
    " TODO: Try and fix this rather than just let it be.
    try
      let l:map_dict['n'][l:map]['comments'] = descriptive_maps#find_comments(l:map_dict['n'][l:map])
    catch
      let l:map_dict['n'][l:map]['comments'] = []
    endtry
  endfor

  return l:map_dict
endfunction

function! descriptive_maps#parse_line(line) abort
  let l:parse_string = '\(\S*\)'            " Get the mode atom
  let l:parse_string .= '\s*'               " Eliminate white space
  let l:parse_string .= '\(\S*\)'           " Get the lhs atom
  let l:parse_string .= '\s*'               " Eliminate white space
  let l:parse_string .= '\(\%[\*]\)'        " Optionally check for the map atom
  let l:parse_string .= '\(\%[&]\)'         " Optionally check for the script local atom
  let l:parse_string .= '\(\%[@]\)'         " Optionally check for the buffer-local atom
  let l:parse_string .= '\s*'               " Eliminate white space
  let l:parse_string .= '\(.*\)'            " Get the rhs atom

  let l:matched = matchlist(a:line, l:parse_string)[1:6]

  let l:mode_atom = 0
  let l:lhs_atom = 1
  let l:remap_atom = 2
  let l:script_atom = 3
  let l:remap_atom = 4
  let l:rhs_atom = 5

  return {
        \ 'raw': a:line,
        \ 'mode': l:matched[l:mode_atom],
        \ 'lhs': l:matched[l:lhs_atom],
        \ 'rhs': l:matched[l:rhs_atom],
        \ 'remap': l:matched[l:remap_atom] ==? '' ? v:false : v:true,
        \ 'source': '',
        \ }
endfunction

function! descriptive_maps#parse_source(line) abort
  return matchlist(a:line, '\(\s*Last set from \)\(.*\)')[2]
endfunction

function! descriptive_maps#find_comments(map_dict) abort
  if a:map_dict['source'] ==# ''
    return []
  endif

  if !filereadable(expand(a:map_dict['source']))
    return []
  endif

  let l:file_source = readfile(expand(a:map_dict['source']))

  if empty(l:file_source)
    return []
  endif

  let l:index = 0
  for l:file_line in l:file_source
    " if matchstr(l:file_line, printf('^%s\a*\s*%s\s%s.*',
    "       \ a:map_dict['mode'],
    "       \ a:map_dict['lhs'],
    "       \ a:map_dict['rhs'])) !=# ''
    "   return l:index
    " endif

    if len(l:file_line) > len(a:map_dict['rhs']) && matchstr(l:file_line, a:map_dict['rhs']) !=# ''
      let l:comments = []

      " Don't go below the end of the file source
      if l:index <= 1 || l:index >= len(l:file_source)
        return l:comments
      endif

      while l:file_source[l:index - 1] =~? '^\s*">'
        call insert(l:comments, l:file_source[l:index - 1])
        let l:index -= 1

        " Don't go below the end of the file source
        if l:index <= 1 || l:index >= len(l:file_source)
          return l:comments
        endif
      endwhile

      return l:comments
    endif

    let l:index += 1
  endfor

  return []
endfunction

function! descriptive_maps#hint(maps) abort
  let l:complete_result = ''

  pclose
  new +setlocal\ previewwindow|setlocal\ buftype=nofile|setlocal\ noswapfile|setlocal\ wrap
  exe 'normal z' . &previewheight . "\<cr>"

  let l:line_num = 1
  for l:key in keys(a:maps)
    call setline(l:line_num, l:key)
    let l:line_num += 1
  endfor
  redraw

  while v:true
    let l:temp = getchar()
    let l:complete_result .= nr2char(l:temp)
    echon '> ' . l:complete_result

    if l:temp ==? 13
      break
    endif

    pclose
    new +setlocal\ previewwindow|setlocal\ buftype=nofile|setlocal\ noswapfile|setlocal\ wrap
    exe 'normal z' . &previewheight . "\<cr>"

    let l:line_num = 1
    for l:key in keys(a:maps)
      if match(l:key, l:complete_result, 0) == 0
        if !empty(a:maps[l:key]['comments'])
          call setline(l:line_num, printf('%s: %s',
                \ l:key,
                \ string(a:maps[l:key]['comments'])
                \ ))
        else
          call setline(l:line_num, l:key)
        endif

        let l:line_num += 1
      endif
    endfor
    
    redraw
  endwhile
endfunction
