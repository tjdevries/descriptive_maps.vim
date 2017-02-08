
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

function! descriptive_maps#find_variables()
  let l:variables = {}
  for var in filter(map(split(execute('let g:'), "\n"), "matchstr(v:val, '\\S\\+')"), "v:val =~# '^descriptive_maps#'")
    let l:variables[var] = g:{var}
  endfor

  return l:variables
endfunction
