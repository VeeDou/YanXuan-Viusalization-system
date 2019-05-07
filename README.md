# YanXuan-Viusalization-system

相关框架版本：
Django :2.0.2
d3js: https://d3js.org/d3.v4.min.js 
echarts:忘记了~~

![系统结构图]( https://raw.githubusercontent.com/VeeDou/YanXuan-Viusalization-system/master/YanxuanViews/%E6%9E%B6%E6%9E%84%E5%9B%BE.png
)

爬虫模块主要负责爬取数据、简单去重、数据格式转换、简单数据过滤、转义及存储入库等。经过这些处理并存储后，通过Django后台查询数据，然后按照web页面图表要求的数据格式进行数据结构设计编写并传到前端页面上，在这里前端页面会接收到两部分数据，一部分可直接用于图表的呈现，另外一部分用于互动操作时候的数据筛选和更新，在用户互动操作后，会被监听捕捉到，接着进行相应的数据筛选，更新到当前图表实例上。
![爬虫设计]( https://raw.githubusercontent.com/VeeDou/YanXuan-Viusalization-system/master/YanxuanViews/%E7%88%AC%E8%99%AB%E8%AE%BE%E8%AE%A1.png
)
