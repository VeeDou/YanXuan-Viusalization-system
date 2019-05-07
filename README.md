# YanXuan-Viusalization-system

相关框架版本：    
Django :2.0.2   
d3js: https://d3js.org/d3.v4.min.js   

# 系统结构图
![系统结构图]( https://raw.githubusercontent.com/VeeDou/YanXuan-Viusalization-system/master/YanxuanViews/%E6%9E%B6%E6%9E%84%E5%9B%BE.png
)

爬虫模块主要负责爬取数据、简单去重、数据格式转换、简单数据过滤、转义及存储入库等。经过这些处理并存储后，通过Django后台查询数据，然后按照web页面图表要求的数据格式进行数据结构设计编写并传到前端页面上，在这里前端页面会接收到两部分数据，一部分可直接用于图表的呈现，另外一部分用于互动操作时候的数据筛选和更新，在用户互动操作后，会被监听捕捉到，接着进行相应的数据筛选，更新到当前图表实例上。    


# 爬虫设计
![爬虫设计]( https://raw.githubusercontent.com/VeeDou/YanXuan-Viusalization-system/master/YanxuanViews/%E7%88%AC%E8%99%AB%E8%AE%BE%E8%AE%A1.png
)
爬虫通过一个起始的url进行爬取，首先抓取一级类目和二级类目的id，接着将二级类目id拼接成二级类目对应页面，传递到下一层用来抓取对应类目商品的id，用获取到的商品id拼接商品详情页面和评论页面的url并传递到下一层去抓取对应的详情页面及评论。整个抓取过程经历3层的值传递，每层都是通过id拼接成的url的形式进行的数据抓取。其中有一个简单地去重工作，通过对已经入库的id进行排除或者更新。如果是爬取过程中断，在重新启动爬虫的时候就可以对入库的商品数据进行id的筛选，不对已爬取的商品进行详情和评论的爬取。如果是完整的爬取过程中遇到了重复的id，则会对数据进行爬取并更新   

# 功能架构图
![功能架构图]( https://raw.githubusercontent.com/VeeDou/YanXuan-Viusalization-system/master/YanxuanViews/%E5%8A%9F%E8%83%BD%E6%9E%B6%E6%9E%84.png
)
功能一共分为三部分：主页、一级分类和二级分类页面。主页中有三块可视化设计，分类的力导向图、商品数量的矩阵树图、以及商品详情的气泡图，其中矩阵树图和商品详情的气泡图数据是联动的，可以对两个图表的数据进行互动和探索。
