### faststock V1 项目简介

**特别说明：股市有风险投资需谨慎，本项目只能用于Python代码学习，股票分析仅作为本项目练手用途，不建议用于投资，如投资失利，与本开源项目无关**

**项目地址：https://github.com/cpaqyx/faststock**

### 学习和使用方法

## （1）python环境安装
安装python3.10及以上版本，推荐采用Anaconda3-2022.10以上版本，然后再Pycharm中设置采用Anaconda管理python环境。

## （2）IDE开发工具安装
安装Pycharm2022.x.x及以上版本，如2022.2.4。


## （3）数据库安装和初始化数据库
安装mysql5.7及以上版本，安装后，创建数据库fast_stock，并执行data\databaseScript\dump-fast-stock-xxxx.sql初始化数据库。

## （4）修改配置
打开configure\config.json修改数据库用户名、密码，ts_token, 请从官网tushare官网注册，并到个人中心复制该ts_token。

## （5）运行代码并查看效果
目前没有提供图形化界面，直接打开脚本运行，如要同步股票基本信息，则直接在Pycharm中找到datahub\sync_stock_basic.py运行即可，执行后，可以到数据库中查看stock_basic_info表中是否已插入了所有股票信息。


### 功能说明

| 功能项           | 代码文件 | 说明 |
|---------- |-----------|-------------------------------|
| 1，同步股票基本信息|datahub\sync_stock_basic.py     |  采集沪深股票基本信息息保存到表stock_basic_info|
| 2，同步每个股票日线交易数据| datahub\sync_stock_day.py    |  系统会自动记录同步状态，保证数据不重复也不缺失保存一份，每次同步时只会查询增量部分的日线数据，交易记录保存到stock_line_day表，状态更新到stock_basic_status  |


### 欢迎加入
本项目虽然是一个学习为主的项目，但代码质量要求达到或超过生产应用要求，不求功能强大，但追求代码高效、可靠、精练，这也是本人为什么创建该项目的原因，本来想利用其他开源项目代码，在其基础上来实现，但大部分项目商业性质太强，或者代码写得不忍直视。欢迎志同道合的朋友加入进来，一起打造一个轻量级全自动交易系统！