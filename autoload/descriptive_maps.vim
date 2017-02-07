
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

function! descriptive_maps#find_variables()
  let l:variables = {}
  for var in filter(map(split(execute('let g:'), "\n"), "matchstr(v:val, '\\S\\+')"), "v:val =~# '^descriptive_map#'")
    let l:variables[var] = g:{var}
  endfor

  return l:variables
endfunction
