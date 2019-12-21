import uuid
import base64
import re
import os
import hashlib
import json
from threading import Event, Lock, Thread
from time import monotonic
import requests

def generate_id(prefix):
	return prefix + '-' + str(uuid.uuid4())

def base64_encode(data):
	return bytes.decode(base64.b64encode(data))

def base64_decode(data_str):
	return base64.b64decode(data_str)

def test_base64_str(test_str):
	return re.match(r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$', test_str)

def file_md5(file_path):
	hash_md5 = hashlib.md5()
	with open(file_path, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()

def download_file(url, file_path, md5=None, retry=3):
	os.makedirs(os.path.dirname(file_path), exist_ok=True)
	if md5 is not None and os.path.exists(file_path) and file_md5(file_path) == md5:
		print("file(%s) exist, md5(%s) match" % (file_path, md5))
		return

	with open(file_path, "wb") as f:
		while retry > 0:
			try:
				response = requests.get(url, stream=True, timeout=120)
				total_length = response.headers.get('content-length')

				if total_length is None or int(total_length) < 65536:  # no content length header
					f.write(response.content)
				else:
					download_length = 0
					total_length = int(total_length)
					for data in response.iter_content(chunk_size=65536):
						download_length += len(data)
						f.write(data)
						print('Downloading %s ... %.3f' % (url, float(download_length) / total_length))
				return
			except requests.exceptions.Timeout as e:
				retry -= 1
				print("Download retry %d: %s" % (retry, e))
				if retry <= 0:
					raise Exception("Download %s timeout" % url)

def bytes_to_dict(bytes_data):
	bytes = bytes_data
	if bytes.__len__() == 0:
		return
	str1 = str(bytes, encoding="utf-8")
	data = "raw data"
	try:
		data = eval(str1)
		print("---------------data = eval(str1)----------------")
	except NameError as ne:
		try:
			print("---------------data = json.loads(str1)----------------")
			data = json.loads(str1)
		except ValueError as ve:
			print(ve)
	finally:
		print(data)
	return data

def command_to_script(args, script_path):
	os.makedirs(os.path.dirname(script_path), exist_ok=True)
	with open(script_path, 'w') as sh:
		sh.write("#! /bin/bash\n")
		sh.write(" ".join(args))
		sh.close()

class LogChunkCache(object):
	def __init__(self):
		# chunk_id: data_string
		self._cache = dict()

	"""
	:return str
	if chunk has finished, return concat string, else return None
	"""
	def parse_chunk_data(self, raw_str):
		chunk_match = re.search(r'Chunk\.(.+)\.(\d+):', raw_str)
		# log has only one chunk
		if not chunk_match:
			return raw_str
		chunk_data = raw_str[chunk_match.span()[1]:]
		chunk_data = chunk_data.strip()
		chunk_id, idx = chunk_match.groups()
		print('chunk_data: ' + chunk_data)
		if chunk_id in self._cache:
			self._cache[chunk_id] += chunk_data
		else:
			self._cache[chunk_id] = chunk_data

		# chunks not finished
		if int(idx) > 0:
			return None
		return self._cache.pop(chunk_id, None)

class WatchdogTimer(Thread):
	"""Run *callback* in *timeout* seconds unless the timer is restarted."""

	def __init__(self, timeout, callback, *args, timer=monotonic, **kwargs):
		super().__init__(**kwargs)
		self.timeout = timeout
		self.callback = callback
		self.args = args
		self.timer = timer
		self.cancelled = Event()
		self.blocked = Lock()

	def run(self):
		self.restart() # don't start timer until `.start()` is called
		# wait until timeout happens or the timer is canceled
		while not self.cancelled.wait(self.deadline - self.timer()):
			# don't test the timeout while something else holds the lock
			# allow the timer to be restarted while blocked
			with self.blocked:
				if self.deadline <= self.timer() and not self.cancelled.is_set():
					return self.callback(*self.args)  # on timeout

	def restart(self):
		"""Restart the watchdog timer."""
		self.deadline = self.timer() + self.timeout

	def cancel(self):
		self.cancelled.set()

def case_equal(case1, case2):
	if case1 == case2:
		return True
	else:	
		flag1 = is_testcase_equal(case1, case2)
		flag2 = is_testcase_equal(case2, case1)
		if flag1 == True or flag2 == True:
			return True
		else:
			return False
	

def is_testcase_equal(androidTestCaseID,iOSTestCaseID):
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
#	 #盘后走势接口（科创板）2--传快照 ios无
#	 if x == 'AFTERHOURSCHART_2' and y == '':
#		  return True
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
#	 #集合竞价走势接口2--传快照 ios无
#	 if x == 'BIDCHART_1' and y == '':
#		  return True
	#经纪席位
	if x == 'BROKERINFO_1' and y == 'BrokerSeatTestCase':
		 return True
	#版块类股票行情
	if x == 'CATEQUOTE_1' and y == 'CategoryQuoteListTestCase':
		 return True
#	 #排序接口1
#	 if x == 'CATESORTING_1' and y == '':
#		  return True
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
#	 #走势数据3--传快照 ios无
#	 if x == 'CHARTV2TEST_3' and y == '':
#		  return True
	#走势数据4
	if x == 'CHARTV2TEST_4' and y == 'ChartTestCase':
		 return True
#	 #走势数据5--传快照 ios无
#	 if x == 'CHARTV2TEST_5' and y == '':
#		  return True
#	 #走势数据6--传快照 ios无
#	 if x == 'CHARTV2TEST_6' and y == '':
#		  return True
	#走势副图指标接口1
	if x == 'CHARTSUB_1' and y == 'ChartIndexTestCase':
		 return True
#	 #走势副图指标接口2
#	 if x == 'CHARTSUB_2' and y == '':
#		  return True
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
#	 #历史分时2--传快照 ios无
#	 if x == 'HISTORYCHART_2' and y == '':
#		  return True
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
#	 #分价2
#	 if x == 'MOREPRICE_1' and y == '':
#		  return True
	#要约收购接口请求1
	if x == 'OFFERQUOTE_1' and y == 'OfferQuoteTestCase':
		 return True
	#要约收购接口请求2
	if x == 'OFFERQUOTE_1' and y == 'OfferQuoteListTestCase':
		 return True
	#复权信息接口
	if x == 'OHLCSUB_1' and y == 'OHLCSubTestCase':
		 return True
#	 #历史K线
#	 if x == '' and y == '':
#		  return True
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
#	 #买卖队列1
#	 if x == 'ORDERQUANTITY_1' and y == '':
#		  return True
	#买卖队列2
	if x == 'ORDERQUANTITY_2' and y == 'OrderQuantityTestCase':
		 return True
	#走势叠加1
	if x == 'OVERLAYCHART_1' and y == 'ChartTestCase':
		 return True
#	 #走势叠加2--传快照 ios无
#	 if x == 'OVERLAYCHART_1' and y == '':
#		  return True
#	 #行情快照1
#	 if x == 'QUOTEDETAIL_1' and y == '':
#		  return True
	#行情快照2
	if x == 'QUOTEDETAIL_2' and y == 'SnapQuoteTestCase':
		 return True
	#证券行情列表1--无自定义栏位
	if x == 'QUOTE_1' and y == 'QuoteTestCase':
		 return True
	#证券行情列表2
	if x == 'QUOTE_2' and y == 'QuoteTestCase':
		 return True
#	 #股票查询
#	 if x == '' and y == '':
#		  return True
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
#	 #市场当年交易日1
#	 if x == '' and y == '':
#		  return True
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
#	 #大宗交易--ios无此接口
#	 if x == 'F10_BLOCKTRADE_1' and y == '':
#		  return True
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
#	 #财经资讯图片--ios无此接口
#	 if x == 'F10_FININFOIMAGE_1' and y == '':
#		  return True
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
#	 #财务报表2--仅限港股
#	 if x == '' and y == '':
#		  return True
	#财务指标1
	if x == 'F10_MAINFINAINDEXNAS_1' and y == 'FinancialSummaryTestCase':
		 return True
#	 #财务指标2--仅限港股
#	 if x == '' and y == '':
#		  return True
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
	
	return False
