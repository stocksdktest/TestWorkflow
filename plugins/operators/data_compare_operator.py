import datetime
from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults
from operators.stock_operator import StockOperator

from airflow.contrib.hooks.mongo_hook import MongoHook
from utils import *


class DataCompareOperator(StockOperator):
	@apply_defaults
	def __init__(self, runner_conf, task_id_list, *args, **kwargs):
		super(DataCompareOperator, self).__init__(queue='worker', runner_conf=runner_conf, *args, **kwargs)
		self.task_id_list = task_id_list
		self.mongo_hk = MongoHook(conn_id='stocksdktest_mongo')
		self.conn = self.mongo_hk.get_conn()

	def close_connection(self):
		self.mongo_hk.close_conn()

	def get_ios_data(self):
		return 0

	def get_android_data(self):
		return 0

	def execute(self, context):
		myclient = self.mongo_hk.client
		mydb = myclient[self.runner_conf.storeConfig.dbName]
		col = mydb[self.runner_conf.storeConfig.collectionName]

		id1 = self.xcom_pull(context, key=self.task_id_list[0])
		id2 = self.xcom_pull(context, key=self.task_id_list[1])

		print('xcom_pull', id1)
		print('xcom_pull', id2)

		# 对于直接在安卓测试的扩充
		print("-----------------------------Now Get Data From Mongo Directly--------------------------------")
		result = dict()
		cmp_result = dict()
		error_result = list()

		result['jobID'] = self.runner_conf.jobID
		result['dagID'] = self.dag_id
		result['runnerID1'] = id1
		result['runnerID2'] = id2
		result['compared'] = cmp_result
		result['error'] = error_result

		cmp_result['true'] = list()
		cmp_result['false'] = list()

		# 筛选规则
		rule_json_exist = {'$gt':{}}
		rule1 = {
			'runnerID': id1,
			'$or': [{'resultData': rule_json_exist}, 	{'exceptionData': rule_json_exist}]
		}
		rule2 = {
			'runnerID': id2,
			'$or': [{'resultData': rule_json_exist}, 	{'exceptionData': rule_json_exist}]
		}

		for x in col.find(rule1):
			# x test failure
			print('x', x)
			if x['isPass'] == False:
				print(id1,x['testcaseID'],'test failure')
				print(x)
				print('---------------------------')
				error_result.append(x)
				continue

			for y in col.find(rule2):
				# y test failure
				print('y',y)
				if y['isPass'] == False:
					print(id2, y['testcaseID'], 'test failure')
					print(y)
					print('---------------------------')
					error_result.append(y)
					continue

				# can use self.my_obj_cmp(x['paramData'], y['paramData']),but now is not necessary I think
				# TODO: now pramData is ignored
				# if case_equal(x['testcaseID'], y['testcaseID']) and x['paramData'] == y['paramData']:
				if case_equal(x['testcaseID'], y['testcaseID']) :
					
					if x['testcaseID'] == y['testcaseID'] and x['paramData'] != y['paramData']:
						continue

					testcaseID = x['testcaseID']
					print('testcaseID:', testcaseID)

					print('Compared record1:', x)
					print('Compared record2:', y)
					print('---------------------------')
					r1 = x['resultData']
					r2 = y['resultData']

					res = record_compare(r1, r2)
					print(res)
					res_item = dict()
					res_item['recordID1'] = x['recordID']
					res_item['recordID2'] = y['recordID']
					res_item['testcaseID1'] = x['testcaseID']
					res_item['testcaseID2'] = y['testcaseID']
					res_item['paramData1'] = x['paramData']
					res_item['paramData2'] = y['paramData']
					# TODO: 差一个时间，需要安卓那里支持一下endTime,先测试下endTime有没有问题
					if res['result'] == True:
						cmp_result['true'].append(res_item)
					else:
						res_item['result1'] = r1
						res_item['result2'] = r2
						res_item['details'] = res['details']
						cmp_result['false'].append(res_item)

		col_res = mydb[self.runner_conf.storeConfig.collectionName + '_test_result']
		try:
			col_res.insert_one(result)
		except TypeError as e:
			print(e)

if __name__ == '__main__':
	mongo_hk = MongoHook()
	mongo_hk.uri = 'mongodb://localhost:27017/'
	r1, r2 = get_two_testresult()
	a = DataCompareOperator(
		runner_conf='1',
		task_id='11',
		task_id_list=['a', 'b']
	)
	res = record_compare(r1, r2)
	print(res)
