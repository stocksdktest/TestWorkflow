import jsonpatch


def get_value_from_path(record, path):
	# 字符串是否表示一个数字
	# TODO eval is dangerous
	def is_str_integer(str):
		res = False
		try:
			res = type(eval(str)) == int
		except ZeroDivisionError as e:
			print(e)
		finally:
			return res

	path_list = path.lstrip('/').split('/')
	src_a = record
	# print('src_a:', src_a)
	for key in path_list:
		# print('key:',key)
		if isinstance(src_a, list) and is_str_integer(key):
			src_a = src_a[int(key)]
		elif isinstance(src_a, dict):
			src_a = src_a[key]
		else:
			raise TypeError("Error in json path")
	return src_a

def ordered(obj):
	if isinstance(obj, dict):
		return sorted((k, ordered(v)) for k, v in obj.items())
	if isinstance(obj, list):
		return sorted(ordered(x) for x in obj)
	else:
		return obj

def record_compare(record1, record2):
	res = (record1 == record2)
	resInfo = []
	if res == True:
		print("Easy Json Dict , PASS")
	else:
		'''若嵌套了List，要忽略list的顺序,自上而下排序'''
		try:
			res = ordered(record1) == ordered(record2)
			print("Easy Json Dict With List")
		except TypeError as e:
			res = my_obj_cmp(record1, record2)
			print("Hard Json Dict With List")
		finally:
			if res == False:
				''' 如果出现不一致，就使用json_patch进行不一致的寻找'''
				patch = jsonpatch.make_patch(record1, record2)
				patches = patch.patch
				false_cnts = 0  # record the real false numbers
				try:
					for item in patches:
						# print("-----------There is a option " + item['op'])
						if item['op'] == 'replace':
							# TODO:
							# print("op is replace")
							src_a = get_value_from_path(record1, item['path'])
							src_b = item['value']

							''' if it's numbers '''
							# TODO: eval is dangerous so annotate it now
							# numbers = False
							# try:
							# 	if isinstance(src_a, str) and isinstance(src_b, str):
							# 		t1 = type(eval(src_a.strip('%')))
							# 		t2 = type(eval(src_b.strip('%')))
							# 		if t1 == t2:
							# 			if t1 == int or t1 == float:
							# 				numbers = True
							# # print('Element val : ', src_a, src_b)
							# except SyntaxError as e1:
							# 	numbers = False
							# except NameError as e2:
							# 	numbers = False
							# finally:
							# 	if src_a != src_b:
							# 		false_cnts += 1

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
								# print("op is remove") # TODO
								# print("path is {}".format(item['path']))
								# print("record1 is {}".format(record1))
								# print("record2 is {}".format(record2))
								try:
									src_a = get_value_from_path(record1, item['path'])
								except IndexError as e:
									# TODO: Better solution
									print("IndexError when remove, because it must been add")
									continue

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

							try:
								src_a = get_value_from_path(record1, item['from'])
							except IndexError as e:
								# TODO: Better solution
								print("IndexError when {}, because it must been add".format(item['op']))
								continue

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
				except TypeError as e:
					print("Compare TypeError", e)
					resInfo = patches
				except KeyError as e:
					print("Compare KeyError", e)
					resInfo = patches
				# except IndexError as e:
				# 	print("Compare IndexError", e)
				# 	resInfo = patches

	result = {
		"result": res,
		"details": resInfo
	}
	return result


def my_list_cmp(list1, list2):
	if (list1.__len__() != list2.__len__()):
		return False

	for l in list1:
		found = False
		for m in list2:
			res = my_obj_cmp(l, m)
			if (res):
				found = True
				break

		if (not found):
			return False

	return True


def my_obj_cmp(obj1, obj2):
	# print('My Obj Cmp : ', obj1, obj2)
	if isinstance(obj1, list):
		''' 若obj1为list，首先判断obj2是否也为list,是则继续调用my_list_cmp函数 '''
		if (not isinstance(obj2, list)):
			return False
		return my_list_cmp(obj1, obj2)
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
				if (not my_list_cmp(val1, val2)):
					return False
			elif isinstance(val1, dict):
				if (not my_obj_cmp(val1, val2)):
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