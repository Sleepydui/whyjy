从weiboevents中下载的数据放入data文件夹中

运行main.py

输入mid

处理好的数据放在dataTree文件夹中

如果有新的数据应当将main.py中的注释删掉

获取关注关系的时候要手动进行登录，将下面的url输入到浏览器中。在回调url中会有code字段，将code字段中的内容复制到console中。注意一个账号短期内只能爬取100次，如果出现用户调用api次数限制应当更换账号，如果出现ip限制应当更换ip，再重复上面的操作

https://api.weibo.com/oauth2/authorize?response_type=code&client_id=1234287835&redirect_uri=http://www.weibo.com