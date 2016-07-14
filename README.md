# descriptive_maps.vim
Do you sometimes forget your mappings? Fear not. Descriptive Maps is here.

## Current Powers

- [x] Simple interface
- [x] Some way of outputting command information
- [x] Small amount of understanding about what is inside of the dictionary

## Planned Powers

- [ ] Remove `Describe` and still have a valid command / mapping
- [ ] Add a real-time "completion" option, so that you can see what mappings are possible
- [ ] Integrate with github.com/tjdevries/nyaovim-popup-menu for really nice completion
- [ ] Integrate with something similar to Damian Conway's HUDigraphs

```vim

" Simply call:
:call Show_description()

" and get, echoed out to you

                       description:     mode |       lhs  -->                            rhs  |  with args:     args
--------------------------------------------------------------------------------------------------------------------
                Tells me something:     nmap | <leader>h  -->     :echo("WOW! SO COOL!")<CR>  |  with args: <silent>
Silly boy, that's now how you move: nnoremap |    <Down>  -->        :echom "--> j <-- "<CR>  |  with args:
Silly boy, that's now how you move: nnoremap |    <Left>  -->        :echom "--> h <-- "<CR>  |  with args:
Silly boy, that's now how you move: nnoremap |   <Right>  -->        :echom "--> l <-- "<CR>  |  with args:
Silly boy, that's now how you move: nnoremap |      <Up>  -->        :echom "--> k <-- "<CR>  |  with args:
```

This plugin is meant to ease your problems for those of us who have a lot of useful mappings, but sometimes either forget about them, or just don't quite get around to using them enough when we first learn them.

It is simple to add to your existing mappings.

```vim

" Go from this
nmap <silent> <leader>h :echo("WOW! SO COOL!")<CR>
nnoremap    <Down> :echom "--> j <-- "<CR>
nnoremap    <Left> :echom "--> h <-- "<CR>
nnoremap   <Right> :echom "--> l <-- "<CR>
nnoremap      <Up> :echom "--> k <-- "<CR> 

" To this
Describe nmap <silent> <leader>h :echo("WOW! SO COOL!")<CR>
Describe nnoremap    <Down> :echom "--> j <-- "<CR>
Describe nnoremap    <Left> :echom "--> h <-- "<CR>
Describe nnoremap   <Right> :echom "--> l <-- "<CR>
Describe nnoremap      <Up> :echom "--> k <-- "<CR> 

" And you're done!
```

