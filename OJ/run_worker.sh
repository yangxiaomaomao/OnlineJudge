###
 # @Descripttion: Online Judge
 # @version: ^_^
 # @Author: Jingbin Yang
 # @Date: 2021-10-01 12:31:01
 # @LastEditors: Jingbin Yang
 # @LastEditTime: 2021-10-01 12:33:18
###
export PATH="~/.local/bin/:$PATH"
celery -A celery_app worker --loglevel=debug --workdir=judge --logfile=info.log
