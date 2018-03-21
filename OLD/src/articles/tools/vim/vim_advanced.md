#  

autocmd xxx


autocmd BufNewFile *.py 0r ~/.vim/templates/python.tlp


autocmd BufNewFile *.cpp,*.[ch],*.sh,*.rb,*.java,*.py exec ":call SetTitle()"

# 函数
