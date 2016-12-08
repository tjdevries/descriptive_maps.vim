" Vi  plugin for defining and viewing your maps
" Maintainer: TJ DeVries
" Thanks to Damian Conway for the idea

"" Use like this in your vimrc after sourcing
" Describe nmap <silent> <leader>h :call <SID>show_description()<CR> >>> Show_cool_stuff hello
" Describe nnoremap <leader>x :echo("hello")<CR>
" Describe nmap <silent> <leader>h :echo("WOW! SO COOL!")<CR> >>> Tells me something
" Describe vmap h :echo('vmap')<CR> >>> Another description
""

if exists('g:loaded_descriptive_maps')
    finish
endif
let g:loaded_descriptive_maps = 1

" let g:descriptive_maps = get(g:, 'descriptive_maps', {})

let g:descriptive_maps       = get(g:, 'descriptive_maps'       , {})
let g:_description_execute   = get(g:, '_description_execute'   , v:true)
let g:_description_separator = get(g:, '_description_separator' , '>>>')
let g:_description_unknown   = get(g:, '_description_unknown'   , 'Undocumented')


" inoremap ,cd <C-R>=descriptive_maps#complete_description("n")<CR>
" command! -nargs=1 Describe call descriptive_maps#describe(<f-args>, g:_description_execute)

function! DescrbeParse(m) abort
    return descriptive_maps#parse_source(a:m)
endfunction
