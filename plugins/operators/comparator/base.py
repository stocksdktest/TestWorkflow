from enum import Enum

CompareResult = Enum('CompareResult', ('Pass', 'Data Inconsistency', 'Data Amount Inconsistency'))

class RecordComparator(object):


    def compare(self, record_a, record_b):
        """
        :param record_a:
        :param record_b:
        :return: CompareResult
        """
        if record_a == record_b:
            return CompareResult['Pass']
        else:
            return CompareResult['Data Inconsistency']
