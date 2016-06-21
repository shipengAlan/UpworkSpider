# Upwork众包网站数据爬取(https)
-   工人用户数据
    Login.py
    模拟登录才能调用工人信息API，每行是一个工人信息json格式
-   任务数据
    Tasks.py
    无需登录，用正则表达式进行匹配，获取json格式数据，每行是一个搜素页的10个任务的json数据
-	统计完成任务被Hire的人数：是否冗余
	TaskHire.py


 *依赖模块 pycurl lxml re time json StringIO random*