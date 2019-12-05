import json

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from operators.data_compare_operator import DataCompareOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from operators.android_runner_operator import AndroidRunnerOperator
from operators.android_release_operator import AndroidReleaseOperator

from datetime import timedelta
from airflow.utils import timezone

# TODO init RunnerConfig
def initRunnerConfig():
    runner_conf_list = []

    for i in range(2):
        runner_conf = RunnerConfig()
        #appKeyAndroid,API:应用程序接口,接口验证序号
        runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
        runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='
        runner_conf.sdkConfig.marketPerm.Level = "1"
        runner_conf.sdkConfig.marketPerm.HKPerms.extend(["hk10"])
        #环境配置
        if i == 0:
            runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["bj"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://114.80.155.134:22013"]))
            runner_conf.sdkConfig.serverSites["gf"].CopyFrom(Site(ips=["http://114.80.155.134:22013"]))
            runner_conf.sdkConfig.serverSites["pb"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["hk1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hk5"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hk10"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hka1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hkd1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hkaz"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hkdz"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
        else:
            runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
            runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
            runner_conf.sdkConfig.serverSites["bj"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
            runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
            runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://114.80.155.61:22013"]))
            runner_conf.sdkConfig.serverSites["gf"].CopyFrom(Site(ips=["http://114.80.155.61:22013"]))
            runner_conf.sdkConfig.serverSites["pb"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
            runner_conf.sdkConfig.serverSites["hk1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hk5"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hk10"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hka1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hkd1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hkaz"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hkdz"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
        case_list = []

         #历史k线 方法6
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'F10_BNDNEWSHARESCAL_1'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
           #005 
			json.dumps({
				'date': '2019-11-13',
				'src': 'd'
			}),
			#006
			json.dumps({
				'date': '2019-11-13',
				'src': 'd'
			}),
        ])
        case_list.append(case_conf)
       
        
        runner_conf.casesConfig.extend(case_list)
        print('i,case_list.length is ', case_list.__len__())
        runner_conf_list.append(runner_conf)

    return runner_conf_list

        #定义默认参数
with DAG(
       dag_id='android_test2',       #DAG名称
		default_args={
			'owner': 'test',     #流程所有者
			'depends_on_past': False,   # 是否依赖上一个自己的执行状态                  
            'email': ['wangzhenjun01@corp.netease.com'],  # 接收通知的email列表
            'email_on_failure': True,  # 是否在任务执行失败时接收邮件
            'email_on_retry': True,  # 是否在任务重试时接收邮件
            'retries': 3,  # 失败重试次数
            'retry_delay': timedelta(seconds=5), # 失败重试间隔   
            'start_date': timezone.datetime(2019, 11, 23, 7, 20), # 调度时间，utl时间，为了方便测试，一般设置为当前时间减去执行周期
			'end_date': timezone.datetime(2019, 11, 23, 7, 30), # 结束时间       
		},
		schedule_interval='@once', #执行周期，执行一次
        #schedule_interval="00, *, *, *, *"  # 执行周期，依次是分，时，天，月，年，此处表示每个整点执行
        #schedule_interval=timedelta(minutes=1)  # 执行周期，表示每分钟执行一次
) as dag:
    start_task = DummyOperator(  
        task_id='run_this_first',
        queue='worker',
       
    )

    run_this_last = DummyOperator(  
        task_id='run_this_last',
        queue='worker'
    )
    #DummyOperator空操作  执行器
    runner_conf_list = initRunnerConfig()  #提供各种runner_conf
    task_id_to_cmp_list = ['adb_shell_cmp_a', 'adb_shell_cmp_b']
    #过实例化Operator，定义各个测试任务  
    #AndroidReleaseOperator完成代码构建和打包APK的过程
    #AndroidRunnerOperator的作用是自动安装某个release版本的APK并运行测试样例进行测试
    android_release = AndroidReleaseOperator(
        task_id='android_release',#任务名
        provide_context=False,
        repo_name='stocksdktest/AndroidTestRunner',#创建Github仓库
        tag_id='release-20191202-0.0.2',
        tag_sha='0b0e32fe16c690957a7582d9f61bbc6d9eb3444e',#获取指定版本仓库
        runner_conf=runner_conf_list[0]
    )

    android_a = AndroidRunnerOperator(
        task_id=task_id_to_cmp_list[0],
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version='release-20191202-0.0.2',#apk_vesrion对应AndroidReleaseOperator中的tag_id 
        runner_conf=runner_conf_list[0]
    )

    android_b = AndroidRunnerOperator(
        task_id=task_id_to_cmp_list[1],
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version='release-20191202-0.0.2',
        runner_conf=runner_conf_list[0]
    )

    android_cmp = DataCompareOperator(
        task_id='data_compare',
        task_id_list=task_id_to_cmp_list,
        retries=3,
        provide_context=False,
        runner_conf=RunnerConfig,
        dag=dag
    )

    # android_cmp2 = DataCompareOperator(
    # 	task_id='data_compare2',
    # 	task_id_list=task_id_to_cmp_list,
    # 	retries=3,
    # 	provide_context=False,
    # 	runner_conf=RunnerConfig,
    # 	dag=dag
    # )

    start_task >> android_release >> [android_a, android_b] >> android_cmp >> run_this_last
# start_task >> android_release >> android_a >> android_cmp >> run_this_last

if __name__ == "__main__":
    dag.cli()
# ....................................a/i比较...................................
def isTestcaseEqual(androidTestCaseID,iOSTestCaseID):
   x = androidTestCaseID
   y = iOSTestCaseID
   if x == y:
       return True
   #测试例子
   if x == 'TESTCASE_0' and y == 'TESTCASE_0':
       return True
   #增值指标1
   if x == 'ADDVALUE_1' and y == 'MAddValuetTestCase':
       return True
   #增值指标2
   if x == 'ADDVALUE_2' and y == 'MAddValuetTestCase':
       return True
   #增值指标3--有自定义栏位
   if x == 'ADDVALUE_3' and y == 'AddValueTestCase':
       return True
   #盘后走势接口（科创板）1
   if x == 'AFTERHOURSCHART_1' and y == 'AfterHoursChartTestCase':
       return True
#    #盘后走势接口（科创板）2--传快照 ios无
#    if x == 'AFTERHOURSCHART_2' and y == '':
#        return True
   #AH股列表1
   if x == 'AHLIST_1' and y == 'AHQuoteListTestCase1':
       return True
   #AH股列表2
   if x == 'AHLIST_2' and y == 'AHQuoteListTestCase2':
       return True
   #AH联动
   if x == 'AHQUOTE_1' and y == 'AHQuoteTestCase':
       return True
   #个股所属板块行情
   if x == 'BANKUAIQUOTE_1' and y == 'SectionQuoteTestCase':
       return True
   #板块排序接口1--页码，笔数
   if x == 'BANKUAISORTING_1' and y == 'SectionSortingTestCase_1':
       return True
   #板块排序接口2--起始，结束位置
   if x == 'BANKUAISORTING_2' and y == 'SectionSortingTestCase_2':
       return True
   #集合竞价走势接口1
   if x == 'BIDCHART_1' and y == 'BidChartTestCase':
       return True
#    #集合竞价走势接口2--传快照 ios无
#    if x == 'BIDCHART_1' and y == '':
#        return True
   #经纪席位
   if x == 'BROKERINFO_1' and y == 'BrokerSeatTestCase':
       return True
   #版块类股票行情
   if x == 'CATEQUOTE_1' and y == 'CategoryQuoteListTestCase':
       return True
#    #排序接口1
#    if x == 'CATESORTING_1' and y == '':
#        return True
   #排序接口2
   if x == '' and y == 'CategorySortingTestCase_1':
       return True
   #排序接口3
   if x == '' and y == 'CategorySortingTestCase_2':
       return True
   #走势数据1
   if x == 'CHARTV2TEST_1' and y == 'ChartTestCase':
       return True
   #走势数据2
   if x == 'CHARTV2TEST_2' and y == 'ChartTestCase':
       return True
#    #走势数据3--传快照 ios无
#    if x == 'CHARTV2TEST_3' and y == '':
#        return True
   #走势数据4
   if x == 'CHARTV2TEST_4' and y == 'ChartTestCase':
       return True
#    #走势数据5--传快照 ios无
#    if x == 'CHARTV2TEST_5' and y == '':
#        return True
#    #走势数据6--传快照 ios无
#    if x == 'CHARTV2TEST_6' and y == '':
#        return True
   #走势副图指标接口1
   if x == 'CHARTSUB_1' and y == 'ChartIndexTestCase':
       return True
#    #走势副图指标接口2
#    if x == 'CHARTSUB_2' and y == '':
#        return True
   #涨跌分布请求接口
   if x == 'COMPOUNDUPDOWN_1' and y == 'CompoundUpdownsTestCase':
       return True
   #可转债溢价查询
   if x == 'CONVERTIBLE_1' and y == 'LinkQuoteTestCase':
       return True
   #CDR,GDR联动
   if x == 'DRLINKQUOTE_1' and y == 'DRlinkTestCase':
       return True
   #CDR,GDR列表
   if x == 'DRQUOTELIST_1' and y == 'DRQuoteListTestCase':
       return True
   #历史分时1
   if x == 'HISTORYCHART_1' and y == 'HistoryChartTestCase':
       return True
#    #历史分时2--传快照 ios无
#    if x == 'HISTORYCHART_2' and y == '':
#        return True
   #两市港股通额度资讯
   if x == 'HKMARINFO_1' and y == 'HKMarketInfoTestCase':
       return True
   #获取港股价差对照表
   if x == 'HKPRICEINFO_1' and y == 'HKPriceDiffTestCase':
       return True
   #港股其他
   if x == 'HKSTOCKINFO_1' and y == 'HKQuoteInfoTestCase':
       return True
   #节假日
   if x == 'HOLIDAY_1' and y == 'MarketHolidayTestCase':
       return True
   #沪股通和深股通额度
   if x == 'HSAMOUNT_1' and y == 'HSAmountTestCase':
       return True
   #L2单独逐笔接口
   if x == 'L2TICKDETAILV2_1' and y == 'L2TimeTickDetailTestCase':
       return True
   #L2单独分笔接口
   if x == 'L2TICKV2_1' and y == 'L2TimeTickTestCase':
       return True
   #沪深当日涨跌统计数据
   if x == 'MARKETUPDOWN_1' and y == 'MarketUpdownsTestCase':
       return True
   #分价1
   if x == 'MOREPRICE_1' and y == 'PriceVolumeTestCase':
       return True
#    #分价2
#    if x == 'MOREPRICE_1' and y == '':
#        return True
   #要约收购接口请求1
   if x == 'OFFERQUOTE_1' and y == 'OfferQuoteTestCase':
       return True
   #要约收购接口请求2
   if x == 'OFFERQUOTE_1' and y == 'OfferQuoteListTestCase':
       return True
   #复权信息接口
   if x == 'OHLCSUB_1' and y == 'OHLCSubTestCase':
       return True
#    #历史K线
#    if x == '' and y == '':
#        return True
   #期权-交割月
   if x == 'OPTIONEXPIRE_1' and y == 'ExpireMonthTestCase':
       return True
   #期权-标的行情
   if x == 'OPTIONLIST_1' and y == 'UnderlyingStockTestCase':
       return True
   #期权-商品行情
   if x == 'OPTIONQUOTE_1' and y == 'OptionTestCase':
       return True
   #期权-T型报价
   if x == 'OPTIONTQUOTE_1' and y == 'OptionTTestCase':
       return True
#    #买卖队列1
#    if x == 'ORDERQUANTITY_1' and y == '':
#        return True
   #买卖队列2
   if x == 'ORDERQUANTITY_2' and y == 'OrderQuantityTestCase':
       return True
   #走势叠加1
   if x == 'OVERLAYCHART_1' and y == 'ChartTestCase':
       return True
#    #走势叠加2--传快照 ios无
#    if x == 'OVERLAYCHART_1' and y == '':
#        return True
#    #行情快照1
#    if x == 'QUOTEDETAIL_1' and y == '':
#        return True
   #行情快照2
   if x == 'QUOTEDETAIL_2' and y == 'SnapQuoteTestCase':
       return True
   #证券行情列表1--无自定义栏位
   if x == 'QUOTE_1' and y == 'QuoteTestCase':
       return True
   #证券行情列表2
   if x == 'QUOTE_2' and y == 'QuoteTestCase':
       return True
#    #股票查询
#    if x == '' and y == '':
#        return True
   #新版股名在线搜索接口1
   if x == 'SEARV2TEST_1' and y == 'SearchV2TestCase':
       return True
   #新版股名在线搜索接口2--限制搜索条数
   if x == 'SEARV2TEST_2' and y == 'SearchV2TestCase':
       return True
   #次新债
   if x == 'SUBNEWBONDSTOCKRANKING_1' and y == 'SubnewBondRankingTestCase':
       return True
   #次新股
   if x == 'SUBNEWSTOCKRANKING_1' and y == 'SubnewStockRankingTestCase':
       return True
   #分时明细
   if x == 'TICK_1' and y == 'TimeTickTestCase':
       return True
#    #市场当年交易日1
#    if x == '' and y == '':
#        return True
   #市场当年交易日2
   if x == 'TRADEDATE_2' and y == 'TradeDateTestCase':
       return True
   #交易行情
   if x == 'TRADEQUOTE_1' and y == 'TradeQuoteTestCase':
       return True
   #uk市场快照单独接口
   if x == 'UKQUOTE_1' and y == 'UKQuoteTestCase':
       return True
   #沪深A股及指数涨跌平家数
   if x == 'UPDOWNS_1' and y == 'IndexUpdownsTestCase':
       return True      
   #资产配置
   if x == 'F10_ASSETALLOCATION_1' and y == 'FundAssetAllocationTestCase':
       return True
#    #大宗交易--ios无此接口
#    if x == 'F10_BLOCKTRADE_1' and y == '':
#        return True
   #债券回购
   if x == 'F10_BNDBUYBACKS_1' and y == 'BondBuyBacksTestCase':
       return True
   #付息情况
   if x == 'F10_BNDINTERESTPAY_1' and y == 'BondInterestPayTestCase':
       return True
   #当日新债
   if x == 'F10_BNDNEWSHARESCAL_1' and y == 'IPOCalendarTestCase':
       return True
   #新债详情
   if x == 'F10_BNDSHAREIPODETAI_1' and y == 'IPOShareDetailTestCase':
       return True
   #债券概况
   if x == 'F10_BONDBASIC_1' and y == 'BondBasicInfoTestCase':
       return True
   #新债日历
   if x == 'F10_BONDTRADINGDAY_1' and y == 'IPODateTestCase':
       return True
   #分红配送
   if x == 'F10_BONUSFINANCE_1' and y == 'BonusFinanceTestCase':
       return True
   #新股日历
   if x == 'F10_CALENDAR_1' and y == 'IPODateTestCase':
       return True
   #基本情况
   if x == 'F10_COMPANYINFO_1' and y == 'CompanyInfoTestCase':
       return True
   #主要业务
   if x == 'F10_COREBUSINESS_1' and y == 'CoreBusinessTestCase':
       return True
   #沪深---融资融券--分市场提供最近交易日
   if x == 'F10_FINANCEMRGNIN_1' and y == 'MarginInfoTestCase':
       return True
   #沪深---融资融券--融资融券差额
   if x == 'F10_FINANCEMRGNIN_2' and y == 'MarginInfoDiffTestCase':
       return True
   #沪深---融资融券--沪深个股融资融券
   if x == 'F10_FINANCEMRGNIN_3' and y == 'MarginInfoShareTestCase':
       return True
#    #财经资讯图片--ios无此接口
#    if x == 'F10_FININFOIMAGE_1' and y == '':
#        return True
   #基金分红
   if x == 'F10_FNDDIVIDEEND_1' and y == 'FundDividendTestCase':
       return True
   #基金财务
   if x == 'F10_FNDFINANCE_1' and y == 'FundFinanceTestCase':
       return True
   #基金净值(12月)
   if x == 'F10_FNDNAVINDEX_1' and y == 'FundValueTestCase':
       return True
   #机构评等
   if x == 'F10_FORECASTRATING_1' and y == 'ForecastRatingTestCase':
       return True
   #机构预测
   if x == 'F10_FORECASTYEAR_1' and y == 'ForecastYeareTestCase':
       return True
   #基金概况
   if x == 'F10_FUNDBASIC_1' and y == 'FundBasicInfoTestCase':
       return True
   #最新基金持股
   if x == 'F10_FUNDSHAREHOLDERINFO_1' and y == 'FundShareHolderInfoTestCase':
       return True
   #基金净值（五日）
   if x == 'F10_FUNDVALUE_1' and y == 'FundNetValueTestCase':
       return True
   #大事提醒
   if x == 'F10_IMPORTANTNOTICE_1' and y == 'BigEventNotificationTestCase':
       return True
   #行业组合
   if x == 'F10_INDUSTRYPORTFOLIO_1' and y == 'FundIndustryPortfolioTestCase':
       return True
   #管理层
   if x == 'F10_LEADERPERSONINFO_1' and y == 'LeaderPersonInfoTestCase':
       return True
   #财务报表1
   if x == 'F10_MAINFINADATANASS_1' and y == 'FinancialInfoTestCase':
       return True
#    #财务报表2--仅限港股
#    if x == '' and y == '':
#        return True
   #财务指标1
   if x == 'F10_MAINFINAINDEXNAS_1' and y == 'FinancialSummaryTestCase':
       return True
#    #财务指标2--仅限港股
#    if x == '' and y == '':
#        return True
   #最新指标
   if x == 'F10_NEWINDEX_1' and y == 'LatestIndexTestCase':
       return True
   #新股详情
   if x == 'F10_NEWSHAREDETAIL_1' and y == 'IPOShareDetailTestCase':
       return True
   #当日新股列表
   if x == 'F10_NEWSHARELIST_1' and y == 'IPOCalendarTestCase':
       return True
   #财经资讯列表
   if x == 'F10_NEWSLIST_1' and y == 'NewsListTestCase':
       return True
   #财经资讯明細
   if x == 'F10_NEWSHAREDETAIL_1' and y == 'NewsTestCase':
       return True
   #股东变动
   if x == 'F10_SHAREHOLDERHISTORYINFO_1' and y == 'ShareHolderHistoryInfoTestCase':
       return True
   #份额结构
   if x == 'F10_SHARESTRUCTURE_1' and y == 'FundShareStructTestCase':
       return True
   #个股/自选公告1
   if x == 'F10_STOCKBULLETINLIST_1' and y == 'StockBulletinListTestCase':
       return True
   #个股/自选公告2--自定义条数
   if x == 'F10_STOCKBULLETINLIST_2' and y == 'StockBulletinListTestCase':
       return True
   #个股公告内文
   if x == 'F10_STOCKBULLETIN_1' and y == 'StockBulletinTestCase':
       return True
   #个股/自选新闻1
   if x == 'F10_STOCKNEWSLIST_1' and y == 'StockNewsListTestCase':
       return True
   #个股/自选新闻2--自定义条数
   if x == 'F10_STOCKNEWSLIST_2' and y == 'StockNewsListTestCase':
       return True
   #个股新闻内文
   if x == 'F10_STOCKNEWS_1' and y == 'StockNewsTestCase':
       return True
   #股票组合
   if x == 'F10_STOCKPORTFOLIO_1' and y == 'FundStockPortfolioTestCase':
       return True
   #个股/自选研报1
   if x == 'F10_STOCKREPORTLIST_1' and y == 'StockReportListTestCase':
       return True
   #个股/自选研报2--自定义条数
   if x == 'F10_STOCKREPORTLIST_2' and y == 'StockReportListTestCase':
       return True
   #个股研报内文
   if x == 'F10_STOCKREPORT_1' and y == 'StockReportTestCase':
       return True
   #股本变动
   if x == 'F10_STOCKSHARECHANGEINFO_1' and y == 'StockShareChangeInfoTestCase':
       return True
   #股本结构
   if x == 'F10_STOCKSHAREINFO_1' and y == 'StockShareInfoTestCase':
       return True
   #分级基金
   if x == 'F10_STRUCTUREDFUND_1' and y == 'GradeFundTestCase':
       return True
   #最新十大流通股股东
   if x == 'F10_TOPLIQUIDSHAREHOLDER_1' and y == 'TopLiquidShareHolderTestCase':
       return True
   #最新十大股东
   if x == 'F10_TOPSHAREHOLDER_1' and y == 'TopShareHolderTestCase':
       return True
   #融资融券
   if x == 'F10_TRADEDETAIL_1' and y == 'TradeDetailInfoTestCase':
       return True
   #財汇沪深盘后接口1
   if x == 'F10V2TEST_1' and y == '':
       return True
   #財汇沪深盘后接口2
   if x == 'F10V2TEST_1' and y == '':
       return True
   #財汇沪深盘后接口3
   if x == 'F10V2TEST_1' and y == '':
       return True

