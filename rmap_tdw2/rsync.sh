# @Author: wakouboy
# @Date:   2018-08-03 15:39:58
# @Last Modified by:   wakouboy
# @Last Modified time: 2019-09-18 12:34:00
rsync -avz --exclude '.git' --exclude '.vscode' --exclude 'client' --exclude 'test' --exclude 'layout_test' --exclude 'data2' * shuai.chen@192.168.10.9:/var/www/html/weibova/rmap_tdw2/

# rsync -avz --exclude '.git' --exclude '.vscode' --exclude 'client' --exclude 'test' --exclude 'layout_test' --exclude 'data2' * shuai.chen@192.168.10.20:/home/shuai.chen/Projects/rmap/