" rootp variable is used by python script to find root folder.
" path variable is used to create vimsvnscript.py path.
let s:path = fnamemodify(resolve(expand('<sfile>:p')), ':h') . '/vimsvnscript.py'
let s:rootp = fnamemodify(resolve(expand('<sfile>:p')), ':h')

function! ShowSVNDiff()
    execute 'py3file ' . s:path
    py3 showSVNDiff()
endfunc

nnoremap sd :call ShowSVNDiff()<CR>
nnoremap sa :tabclose<CR>
nnoremap sc za
