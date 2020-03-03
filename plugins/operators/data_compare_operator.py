import datetime
import time
from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults
from operators.stock_operator import StockOperator

from airflow.contrib.hooks.mongo_hook import MongoHook
from utils import *
from pymongo.errors import DocumentTooLarge


class SdkMongoReader(object):
	def __init__(self, client) -> None:
		super().__init__()
		self.client = client

	def get_exception(self, runnerID1, runnerID2, dbName='stockSdkTest', collectionName='test_result'):
		mydb = self.client[dbName]
		col = mydb[collectionName]

		match = dict()
		group = dict()
		empty_param = dict() # paramData exists but resultData empty
		except_exist = dict() # exceptionData exists or no resultData
		runnerID_exist = dict() # from selected runnerID

		empty_param['$and'] = [
			{'resultData': {'$eq': {}}},
			{'paramData': {'$gt': {}}}
		]


		except_exist['$or'] = [
			{'exceptionData': {'$gt': {}}},
			empty_param
		]

		runnerID_exist['$or'] = [
			{'runnerID': {'$eq': runnerID1}},
			{'runnerID': {'$eq': runnerID2}}
		]

		match['$and'] = [
			except_exist,
			runnerID_exist
		]

		group['_id'] = {
			'testcaseID': '$testcaseID',
		}
		group['record'] = {
			'$push': '$$ROOT'
		}

		pipeline = [
			{'$match': match},
			{'$group': group},
		]

		cursor = col.aggregate(pipeline)
		res = list()
		for document in cursor:
			res.append(document)
		return res

	# group by testcaseID and paramDatas
	def get_result(self, runnerID, dbName='stockSdkTest', collectionName='test_result'):
		mydb = self.client[dbName]
		col = mydb[collectionName]

		match = dict()
		group = dict()
		result_exist = dict()

		result_exist['$and'] = [
			{'resultData': {'$gt': {}}},
			# {'resultData': {'$ne': None}},
		]

		match['runnerID'] = {'$eq': runnerID}
		match['$or'] = [
			result_exist,
		]

		group['_id'] = {
			'testcaseID': '$testcaseID',
			'paramStr': '$paramStr'
		}
		group['record'] = {
			'$push': '$$ROOT'
		}

		pipeline = [
			{'$match': match},
			{'$group': group},
		]

		cursor = col.aggregate(pipeline)
		res = list()
		for document in cursor:
			res.append(document)
		return res

	# group by testcaseID and paramDatas
	def get_results(self, runnerID1, runnerID2, dbName='stockSdkTest', collectionName='test_result'):
		mydb = self.client[dbName]
		col = mydb[collectionName]

		match = dict()
		group = dict()
		result_exist = dict()
		runnerID_exist = dict()

		result_exist['$and'] = [
			{'resultData': {'$gt': {}}},
		]

		runnerID_exist['$or'] = [
			{'runnerID': {'$eq': runnerID1}},
			{'runnerID': {'$eq': runnerID2}}
		]
		match['$and'] = [
			result_exist,
			runnerID_exist
		]

		group['_id'] = {
			'testcaseID': '$testcaseID',
			'paramStr': '$paramStr'
		}
		group['record'] = {
			'$push': '$$ROOT'
		}

		pipeline = [
			{'$match': match},
			{'$group': group},
		]

		cursor = col.aggregate(pipeline)
		res = list()
		for document in cursor:
			res.append(document)
		return res

	def prepare_param(self, runnerID1, runnerID2,  dbName='stockSdkTest', collectionName='test_result'):
		mydb = self.client[dbName]
		col = mydb[collectionName]
		rule = dict()
		rule['$or'] = [
			{'runnerID': {'$eq': runnerID1}},
			{'runnerID': {'$eq': runnerID2}}
		]
		rule['$and'] = [
			{'paramData': {'$gt': {} }}
		]

		hash_list = list()
		for x in col.find(rule):
			hash_list.append({
				'_id' : x['_id'],
				'paramData': x['paramData']
			})

		print(hash_list)

		for x in hash_list:
			dx = x['paramData']
			col.update(
				{'_id': x['_id']},
				{'$set': {'paramStr': sorted(dx.items()).__str__()}})


	def synchronizer(self, runnerID1, runnerID2,  dbName='stockSdkTest', collectionName='test_result', timeout = 10, sleep_time = 15):
		mydb = self.client[dbName]
		col = mydb[collectionName]
		cnt1 = 0
		cnt2 = 0
		cnt1_pre = 0
		cnt2_pre = 0
		counter = 0
		timer = 0
		max = timeout*60
		while col.find({'runnerID': runnerID1}).count() != cnt1 or col.find({'runnerID': runnerID2}).count() != cnt2 or cnt1!=cnt2:
			cnt1_pre = cnt1
			cnt2_pre = cnt2
			cnt1 = col.find({'runnerID': runnerID1}).count()
			cnt2 = col.find({'runnerID': runnerID2}).count()
			if cnt1_pre == cnt1 and cnt2_pre == cnt2:
				counter = counter+1
			else:
				counter = 0

			print('cnt1', cnt1, 'cnt2', cnt2)
			time.sleep(sleep_time)
			timer = timer + sleep_time
			if timer > max or counter > 3:
				print('---------------------Time out for %d Seconds---------------------'%max)
				break
			print('---------------------Synchronize MongoDB for %d Seconds---------------------'%timer)




class DataCompareOperator(StockOperator):
	@apply_defaults
	def __init__(self, runner_conf, task_id_list, *args, **kwargs):
		super(DataCompareOperator, self).__init__(queue='worker', runner_conf=runner_conf, *args, **kwargs)
		self.task_id_list = task_id_list
		self.mongo_hk = MongoHook(conn_id='stocksdktest_mongo')
		self.conn = self.mongo_hk.get_conn()
		self.mongo_reader = SdkMongoReader(client=self.mongo_hk.client)

	def close_connection(self):
		self.mongo_hk.close_conn()

	def get_ios_data(self):
		return 0

	def get_android_data(self):
		return 0

	def execute(self, context):
		id1 = self.xcom_pull(context, key=self.task_id_list[0])
		id2 = self.xcom_pull(context, key=self.task_id_list[1])
		print('xcom_pull', id1)
		print('xcom_pull', id2)
		print("-----------------------------Synchronize MongoDB--------------------------------")
		self.mongo_reader.synchronizer(
			runnerID1 = id1,
			runnerID2 = id2,
			dbName = self.runner_conf.storeConfig.dbName,
			collectionName = self.runner_conf.storeConfig.collectionName
		)
		print("-----------------------------Prepare for paramData to paramStr--------------------------------")
		self.mongo_reader.prepare_param(
			runnerID1 = id1,
			runnerID2 = id2,
			dbName = self.runner_conf.storeConfig.dbName,
			collectionName = self.runner_conf.storeConfig.collectionName
		)
		print("-----------------------------Now Get Data From Mongo Directly--------------------------------")
		result = dict()
		cmp_result = dict()
		error_result = list()
		mismatch_result = list()
		empty_result = list()

		result['jobID'] = self.runner_conf.jobID
		result['dagID'] = self.dag_id
		result['runnerID1'] = id1
		result['runnerID2'] = id2
		result['compared'] = cmp_result
		result['error'] = error_result
		result['mismatch'] = mismatch_result
		result['empty'] = empty_result

		cmp_result['true'] = list()
		cmp_result['false'] = list()

		result_exception = self.mongo_reader.get_exception(
			runnerID1 = id1,
			runnerID2 = id2,
			dbName = self.runner_conf.storeConfig.dbName,
			collectionName = self.runner_conf.storeConfig.collectionName
		)
		result_group = self.mongo_reader.get_results(
			runnerID1 = id1,
			runnerID2 = id2,
			dbName = self.runner_conf.storeConfig.dbName,
			collectionName = self.runner_conf.storeConfig.collectionName
		)

		print("----------------------------- Test Failure --------------------------------")
		if result_exception.__len__() != 0:
			for x in result_exception[0]['record']:
				if x['isPass'] == False:
					print(id1,'recordID', x['recordID'], x['testcaseID'], 'test failure')
					error_result.append(x)
				else:
					print(id1,'recordID', x['recordID'], x['testcaseID'], 'test empty')
					empty_result.append(x)

		print("----------------------------- Test Success --------------------------------")
		if result_group.__len__() != 0:
			for res in result_group:
				if res['record'].__len__() == 1:
					mismatch_result.append(res['record'][0])
					continue

				x = res['record'][0]
				y = res['record'][1]

				# prepare for res_item
				res_item = dict()
				res_item['recordID1'] = x['recordID']
				res_item['recordID2'] = y['recordID']
				res_item['testcaseID1'] = x['testcaseID']
				res_item['testcaseID2'] = y['testcaseID']
				res_item['paramData1'] = x['paramData']
				res_item['paramData2'] = y['paramData']
				res_item['endtime1'] = x['endTime']
				res_item['endtime2'] = y['endTime']

				r1 = x['resultData']
				r2 = y['resultData']
				res = record_compare(r1, r2)

				# print('testcaseID:', x['testcaseID'])
				# print('Compared record1:', x)
				# print('Compared record2:', y)
				# print('---------------------------')
				# print(res)

				if res['result'] == True:
					cmp_result['true'].append(res_item)
				else:
					res_item['result1'] = r1
					res_item['result2'] = r2
					res_item['details'] = res['details']
					cmp_result['false'].append(res_item)


		col_res = self.mongo_hk.client[self.runner_conf.storeConfig.dbName][self.runner_conf.storeConfig.collectionName + '_test_result']
		try:
			col_res.insert_one(result)
		except TypeError as e:
			print(e)
		except DocumentTooLarge as e:
			print("DocumentTooLarge Error")
			for item in result['compared']['false']:
				item.pop('result1')
				item.pop('result2')
			col_res.insert_one(result)

if __name__ == '__main__':
	mongo_hk = MongoHook(conn_id='stocksdktest_mongo')
	conn = mongo_hk.get_conn()
	myclient = mongo_hk.client
	mongo_reader = SdkMongoReader(client=myclient)
	dbName = 'stockSdkTest'
	collectionName = 'test_result'

	id1 = 'RUN--0083bd12-34f8-47c7-a854-7dc0c1dbf148'
	id2 = 'RUN--68ac0891-a15e-4901-a297-a75853d69226'

	rule = {}
	rule['$or'] = [
		{'runnerID': {'$eq': id1}},
		{'runnerID': {'$eq': id2}}
	]



	# r1, r2 = get_two_testresult()
	#
	from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
	runner_conf = RunnerConfig()
	runner_conf.jobID = 'TJ-1'
	runner_conf.runnerID = generate_id('RUN-A')
	runner_conf.storeConfig.mongoUri = 'mongodb://221.228.66.83:30617'
	runner_conf.storeConfig.dbName = dbName
	runner_conf.storeConfig.collectionName = collectionName
	runner_conf.storeConfig.restEndpoint = 'http://mongo-python-eve.sdk-test.svc.cluster.local:80'

	a = DataCompareOperator(
		runner_conf=runner_conf,
		task_id='11',
		task_id_list=['a', 'b']
	)
	res = a.execute("")
	# print(res)
	# mongo_reader.synchronizer(runnerID1=id1,runnerID2=id2,dbName=dbName,collectionName=collectionName)
	mongo_reader.prepare_param(runnerID1=id1,runnerID2=id2,dbName=dbName,collectionName=collectionName)
	exception = mongo_reader.get_exception(runnerID1=id1,runnerID2=id2,dbName=dbName,collectionName=collectionName)
	group = mongo_reader.get_results(runnerID1=id1,runnerID2=id2,dbName=dbName,collectionName=collectionName)

