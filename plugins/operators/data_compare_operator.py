from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.operators.python_operator import PythonOperator
from operators.stock_operator import StockOperator

from airflow.contrib.hooks.mongo_hook import MongoHook
from utils import *
import jsonpatch


class DataCompareOperator(BaseOperator):
	@apply_defaults
	def __init__(self, runner_conf, task_id_list, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.runner_conf = runner_conf
		self.task_id_list = task_id_list
		self.mongo_hk = MongoHook(conn_id='stocksdktest_mongo')
		self.conn = self.mongo_hk.get_conn()

	def close_connection(self):
		self.mongo_hk.close_conn()

	def get_ios_data(self):
		return 0

	def get_android_data(self):
		return 0

	def ordered(self, obj):
		if isinstance(obj, dict):
			return sorted((k, self.ordered(v)) for k, v in obj.items())
		if isinstance(obj, list):
			return sorted(self.ordered(x) for x in obj)
		else:
			return obj

	''' 返回两个记录的比较 '''
	def record_compare(self, record1, record2):
		res = (record1 == record2)
		patches = []
		if res == True:
			print("Easy Json Dict , PASS")
		else:
			'''若嵌套了List，要忽略list的顺序,自上而下排序'''
			try:
				res = self.ordered(record1) == self.ordered(record2)
				print("Easy Json Dict With List")
			except TypeError as e:
				res = self.my_obj_cmp(record1, record2)
				print("Hard Json Dict With List")
			finally:
				if res == False:
					''' 如果出现不一致，就使用json_patch进行不一致的寻找'''
					patch = jsonpatch.make_patch(record1, record2)
					patches = patch.patch
					resInfo = []
					false_cnts = 0  # record the real false numbers
					for item in patches:
						# print("-----------There is a option " + item['op'])
						if item['op'] == 'replace':
							path_list = item['path'].lstrip('/').split('/')
							src_a = record1
							for key in path_list:
								src_a = src_a[key]
							src_b = item['value']

							''' if it's numbers '''
							# TODO: Now it's toy
							numbers = False
							try:
								if isinstance(src_a, str) and isinstance(src_b, str):
									t1 = type(eval(src_a.strip('%')))
									t2 = type(eval(src_b.strip('%')))
									if t1 == t2:
										if t1 == int or t1 == float:
											numbers = True
							# print('Element val : ', src_a, src_b)
							except SyntaxError as e1:
								numbers = False
							except NameError as e2:
								numbers = False
							finally:
								if src_a != src_b:
									false_cnts += 1

							resInfo.append({
								'type': 'Data Inconsistency',
								'location': item['path'],
								'src_a': src_a,
								'src_b': src_b
							})
						elif item['op'] == 'add' or item['op'] == 'remove':
							src_a = "not exist in src_a"
							src_b = "nut exist in src_b"
							# print(item)
							if item['op'] == 'add':
								src_b = item['value']
							else:
								path_list = item['path'].lstrip('/').split('/')
								src_a = record1
								for key in path_list:
									src_a = src_a[key]

							resInfo.append({
								'type': 'Data Amount Inconsistency',
								'location': item['path'],
								'src_a': src_a,
								'src_b': src_b
							})
							false_cnts += 1
						elif item['op'] == 'move' or item['op'] == 'copy':
							''' move equals remove and add'''
							''' copy equals add the value in from to path '''
							from_list = item['from'].lstrip('/').split('/')
							src_a = record1
							for key in from_list:
								src_a = src_a[key]
							src_b = "nut exist in src_b"

							resInfo.append({
								'type': 'Data Amount Inconsistency',
								'location': item['from'],
								'src_a': src_a,
								'src_b': src_b
							})
							false_cnts += 1
						elif item['op'] == 'test':
							print("-----------There is a option Test TODO" + item['op'])
					# false_cnts += 1
					patches = resInfo

		result = {
			"Consistency Result": res,
			"More Infomations": patches
		}
		return result

	def my_list_cmp(self, list1, list2):
		if (list1.__len__() != list2.__len__()):
			return False

		for l in list1:
			found = False
			for m in list2:
				res = self.my_obj_cmp(l, m)
				if (res):
					found = True
					break

			if (not found):
				return False

		return True

	def my_obj_cmp(self, obj1, obj2):
		# print('My Obj Cmp : ', obj1, obj2)
		if isinstance(obj1, list):
			''' 若obj1为list，首先判断obj2是否也为list,是则继续调用my_list_cmp函数 '''
			if (not isinstance(obj2, list)):
				return False
			return self.my_list_cmp(obj1, obj2)
		elif (isinstance(obj1, dict)):
			''' 若obj1为dict，首先判断obj2是否也为dict,是则继续判断keys的集合是否一致，
				是则对每个k对应的value进行比对，若为list或者dict,则递归调用，
				否则直接比较
			'''
			if (not isinstance(obj2, dict)):
				return False
			exp = set(obj2.keys()) == set(obj1.keys())
			if (not exp):
				# print(obj1.keys(), obj2.keys())
				return False
			for k in obj1.keys():
				val1 = obj1.get(k)
				val2 = obj2.get(k)
				if isinstance(val1, list):
					if (not self.my_list_cmp(val1, val2)):
						return False
				elif isinstance(val1, dict):
					if (not self.my_obj_cmp(val1, val2)):
						return False
				else:
					numbers = False
					try:
						if isinstance(val1, str) and isinstance(val2, str):
							t1 = type(eval(val1.strip('%')))
							t2 = type(eval(val2.strip('%')))
							if t1 == t2:
								if t1 == int or t1 == float:
									numbers = True
									print('Element val : ', val1, val2)
					except SyntaxError as e1:
						numbers = False
					except NameError as e2:
						numbers = False
					finally:
						if val2 != val1:
							return False


		else:
			# print('Element obj : ', obj1, obj2)
			return obj1 == obj2

		return True

	def execute(self, context):
		myclient = self.mongo_hk.client
		mydb = myclient["stockSdkTest"]
		col1 = mydb[self.task_id_list[0]]
		col2 = mydb[self.task_id_list[1]]

		id1 = self.xcom_pull(context, key=self.task_id_list[0])
		id2 = self.xcom_pull(context, key=self.task_id_list[1])

		print('xcom_pull', id1)
		print('xcom_pull', id2)

		result = {}
		# TODO: Use Mongo To Selection, Maybe every DAG with a collection could be better?
		for x in col1.find():
			for y in col2.find():
				if x['paramData'] != None and y['paramData'] != None \
						and x['testcaseID'] == y['testcaseID'] \
						and x['runnerID'] == id1 and y['runnerID'] == id2:

					testcaseID = x['testcaseID']
					print(x)
					print(y)
					r1 = x['resultData']
					r2 = y['resultData']
					print(r1)
					print(r2)

					resDBItem = {}
					resDBItem['Result_1'] = r1
					resDBItem['RunnerID_1'] = id1
					resDBItem['JobID_1'] = x['jobID']
					resDBItem['Result_2'] = r2
					resDBItem['RunnerID_2'] = id2
					resDBItem['JobID_2'] = y['jobID']

					if x['exceptionData'] != None or y['exceptionData']!=None:
						print('Exception Explode in '+ testcaseID)
						resDBItem['Exception_Data_1'] = x['exceptionData']
						resDBItem['Exception_Data_2'] = y['exceptionData']
					else:
						res = self.record_compare(r1, r2)
						print(res)
						for k, v in res.items():
							resDBItem[k] = v

					if result.get(testcaseID) == None:
						result[testcaseID] = []
					result[testcaseID].append(resDBItem)


		print(result)  # {'OHLCV3_1': True, 'OHLCV3_2': True, 'OHLCV3_5': True}
		col_res = mydb['test_result']
		col_res.insert_one(result)


def genTwoCase():
	j1 = {
		'COUNT_': '392',
		'ENDDATE_': '2019-06-30',
		'list': [
			{
				'CHINAMEABBR_': '华夏上证50ETF',
				'PCTTOTALESHARE_': '0.36%',
				'HOLDINGVOL_': '10,249.64万股'
			},
			{
				'CHINAMEABBR_': '中证上海国企交易',
				'PCTTOTALESHARE_': '0.17%',
				'HOLDINGVOL_': '4,838.55万股'
			},
			{
				'CHINAMEABBR_': '华泰柏瑞沪深300',
				'PCTTOTALESHARE_': '0.12%',
				'HOLDINGVOL_': '3,451.88万股'
			},
			{
				'CHINAMEABBR_': '上证180ETF',
				'PCTTOTALESHARE_': '0.10%',
				'HOLDINGVOL_': '2,720.52万股'
			},
			{
				'CHINAMEABBR_': '华夏沪深300交易',
				'PCTTOTALESHARE_': '0.09%',
				'HOLDINGVOL_': '2,520.55万股'
			},
			{
				'CHINAMEABBR_': '鹏华银行分级',
				'PCTTOTALESHARE_': '0.09%',
				'HOLDINGVOL_': '2,495.02万股'
			},
			{
				'CHINAMEABBR_': '嘉实沪深300交易型开放式指数',
				'PCTTOTALESHARE_': '0.09%',
				'HOLDINGVOL_': '2,479.23万股'
			},
			{
				'CHINAMEABBR_': '上证上海改革发展主题交易型开放式指数发起式',
				'PCTTOTALESHARE_': '0.07%',
				'HOLDINGVOL_': '2,106.04万股'
			},
			{
				'CHINAMEABBR_': '工银瑞信上证50交易型开放式指数',
				'PCTTOTALESHARE_': '0.07%',
				'HOLDINGVOL_': '1,980.10万股'
			},
			{
				'CHINAMEABBR_': '上证180金融',
				'PCTTOTALESHARE_': '0.07%',
				'HOLDINGVOL_': '1,940.16万股'
			},
			{
				'CHINAMEABBR_': '华泰柏瑞量化增强混合',
				'PCTTOTALESHARE_': '0.04%',
				'HOLDINGVOL_': '1,188.52万股'
			},
			{
				'CHINAMEABBR_': '博时沪深300指数',
				'PCTTOTALESHARE_': '0.03%',
				'HOLDINGVOL_': '842.68万股'
			},
			{
				'CHINAMEABBR_': '华宝中证银行交易',
				'PCTTOTALESHARE_': '0.03%',
				'HOLDINGVOL_': '842.65万股'
			},
			{
				'CHINAMEABBR_': '易方达沪深300ETF',
				'PCTTOTALESHARE_': '0.03%',
				'HOLDINGVOL_': '835.81万股'
			},
			{
				'CHINAMEABBR_': '嘉实基本面50指数(LOF)',
				'PCTTOTALESHARE_': '0.02%',
				'HOLDINGVOL_': '607.91万股'
			},
			{
				'CHINAMEABBR_': '平安沪深300交易型开放式指数',
				'PCTTOTALESHARE_': '0.02%',
				'HOLDINGVOL_': '504.90万股'
			},
			{
				'CHINAMEABBR_': '华安中证银行指数分级',
				'PCTTOTALESHARE_': '0.02%',
				'HOLDINGVOL_': '495.22万股'
			},
			{
				'CHINAMEABBR_': '国寿安保沪深300交易型开放式指数',
				'PCTTOTALESHARE_': '0.02%',
				'HOLDINGVOL_': '451.43万股'
			},
			{
				'CHINAMEABBR_': '天弘中证银行指数',
				'PCTTOTALESHARE_': '0.01%',
				'HOLDINGVOL_': '404.96万股'
			},
			{
				'CHINAMEABBR_': '兴全沪深300指数',
				'PCTTOTALESHARE_': '0.01%',
				'HOLDINGVOL_': '399.89万股'
			}
		]
	}
	j2 = {
		'ENDDATE_': '2019-06-30',
		'COUNT_': '392',
		'list': [
			{
				'CHINAMEABBR_': '中证上海国企交易',
				'PCTTOTALESHARE_': '0.17%',
				'HOLDINGVOL_': '4,838.55万股'
			},
			{
				'CHINAMEABBR_': '华泰柏瑞沪深300',
				'PCTTOTALESHARE_': '0.12%',
				'HOLDINGVOL_': '3,451.88万股'
			},
			{
				'CHINAMEABBR_': '华夏上证50ETF',
				'PCTTOTALESHARE_': '0.36%',
				'HOLDINGVOL_': '10,249.64万股'
			},
			{
				'CHINAMEABBR_': '上证180ETF',
				'PCTTOTALESHARE_': '0.10%',
				'HOLDINGVOL_': '2,720.52万股'
			},
			{
				'CHINAMEABBR_': '华夏沪深300交易',
				'PCTTOTALESHARE_': '0.09%',
				'HOLDINGVOL_': '2,520.55万股'
			},
			{
				'CHINAMEABBR_': '鹏华银行分级',
				'PCTTOTALESHARE_': '0.09%',
				'HOLDINGVOL_': '2,495.02万股'
			},
			{
				'CHINAMEABBR_': '嘉实沪深300交易型开放式指数',
				'PCTTOTALESHARE_': '0.09%',
				'HOLDINGVOL_': '2,479.23万股'
			},
			{
				'CHINAMEABBR_': '上证上海改革发展主题交易型开放式指数发起式',
				'PCTTOTALESHARE_': '0.07%',
				'HOLDINGVOL_': '2,106.04万股'
			},
			{
				'CHINAMEABBR_': '工银瑞信上证50交易型开放式指数',
				'PCTTOTALESHARE_': '0.07%',
				'HOLDINGVOL_': '1,980.10万股'
			},
			{
				'CHINAMEABBR_': '上证180金融',
				'PCTTOTALESHARE_': '0.07%',
				'HOLDINGVOL_': '1,940.16万股'
			},
			{
				'CHINAMEABBR_': '华泰柏瑞量化增强混合',
				'PCTTOTALESHARE_': '0.04%',
				'HOLDINGVOL_': '1,188.52万股'
			},
			{
				'CHINAMEABBR_': '博时沪深300指数',
				'PCTTOTALESHARE_': '0.03%',
				'HOLDINGVOL_': '842.68万股'
			},
			{
				'CHINAMEABBR_': '华宝中证银行交易',
				'PCTTOTALESHARE_': '0.03%',
				'HOLDINGVOL_': '842.65万股'
			},
			{
				'CHINAMEABBR_': '易方达沪深300ETF',
				'PCTTOTALESHARE_': '0.03%',
				'HOLDINGVOL_': '835.81万股'
			},
			{
				'CHINAMEABBR_': '嘉实基本面50指数(LOF)',
				'PCTTOTALESHARE_': '0.02%',
				'HOLDINGVOL_': '607.91万股'
			},
			{
				'CHINAMEABBR_': '平安沪深300交易型开放式指数',
				'PCTTOTALESHARE_': '0.02%',
				'HOLDINGVOL_': '504.90万股'
			},
			{
				'CHINAMEABBR_': '华安中证银行指数分级',
				'PCTTOTALESHARE_': '0.02%',
				'HOLDINGVOL_': '495.22万股'
			},
			{
				'CHINAMEABBR_': '国寿安保沪深300交易型开放式指数',
				'PCTTOTALESHARE_': '0.02%',
				'HOLDINGVOL_': '451.43万股'
			},
			{
				'CHINAMEABBR_': '天弘中证银行指数',
				'PCTTOTALESHARE_': '0.01%',
				'HOLDINGVOL_': '404.96万股'
			},
			{
				'CHINAMEABBR_': '兴全沪深300指数',
				'PCTTOTALESHARE_': '0.01%',
				'HOLDINGVOL_': '399.89万股'
			}
		]
	}
	j3 = {
		"errors": [
			{"error": "invalid", "field": "email"},
			{"error": "required", "field": "name"},
			"a",
			1,
			True
		],
		"success": False
	}
	j4 = {
		"success": False,
		"errors": [
			"a",
			True,
			{"field": "name", "error": "required"},
			{"error": "invalid", "field": "email"},
			1
		]
	}
	j5 = {
		'dateTime': '201910140930',
		'riseCount': '2975',
		'fallCount': '354',
		'flatCount': '251',
		'stopCount': '11',
		'riseLimitCount': '19',
		'fallLimitCount': '2',
		'riseFallRange': [{'-10%': '0'}, {'-9%': '0'}, {'-8%': '0'}, {'-7%': '2'}, {'-6%': '1'}, {'-5%': '7'},
						  {'-4%': '14'}, {'-3%': '25'}, {'-2%': '73'}, {'-1%': '232'}, {'0%': '251'}, {'1%': '1991'},
						  {'2%': '801'}, {'3%': '95'}, {'4%': '33'}, {'5%': '22'}, {'6%': '5'}, {'7%': '4'},
						  {'8%': '3'}, {'9%': '2'}, {'10%': '19'}],
		'oneRiseLimitCount': '9',
		'natureRiseLimitCount': '10'
	}
	j6 = {
		'natureRiseLimitCount': '10',
		'dateTime': '201910140930',
		'oneRiseLimitCount': '9',
		'riseCount': '2975',
		'flatCount': '251',
		'fallCount': '354',
		'stopCount': '11',
		'riseLimitCount': '19',
		'fallLimitCount': '2',
		'riseFallRange': [{'-10%': '0'}, {'-9%': '0'}, {'-7%': '2'}, {'-8%': '0'}, {'-6%': '1'}, {'-4%': '14'},
						  {'-3%': '25'}, {'-5%': '7'}, {'-2%': '73'}, {'-1%': '232'}, {'0%': '251'}, {'1%': '1991'},
						  {'2%': '801'}, {'3%': '95'}, {'4%': '33'}, {'5%': '22'}, {'6%': '5'}, {'7%': '4'},
						  {'8%': '3'}, {'9%': '2'}, {'10%': '19'}]
	}
	dictObj = {"foo": "bar", "john": "doe"}
	reorderedDictObj = {"john": "doe", "foo": "bar"}
	dictObj2 = {"abc": "def"}
	dictWithListsInValue = {'A': [{'X': [dictObj2, dictObj]}, {'Y': 2}], 'B': dictObj2}
	reorderedDictWithReorderedListsInValue = {'B': dictObj2, 'A': [{'Y': 2}, {'X': [reorderedDictObj, dictObj2]}]}
	a = {"L": "M", "N": dictWithListsInValue}
	b = {"L": "M", "N": reorderedDictWithReorderedListsInValue}

	# return j1, j2
	# return j3,j4
	# return a,b
	r1 = {"1": j1, "2": j3, "3": a}
	r2 = {"1": j2, "2": j4, "3": b}
	return r1, r2


if __name__ == '__main__':
	mongo_hk = MongoHook()
	mongo_hk.uri = 'mongodb://localhost:27017/'
	r1, r2 = genTwoCase()
	a = DataCompareOperator(
		runner_conf='1',
		task_id='11',
		task_id_list=['a', 'b']
	)
	res = a.record_compare(r1, r2)
	print(res)
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
