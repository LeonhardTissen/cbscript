from block_types.block_base import block_base
import math
from CompileError import CompileError

class python_tuple_assignment_block(block_base):
	def __init__(self, line, ids, val):
		self.line = line
		self.ids, self.val = ids, val
		
	def compile(self, func):
		val = self.val.get_value(func)
		try:
			val_len = len(val)
		except Exception as e:
			print(e)
			raise CompileError('Expression at line {} is not a tuple.'.format(self.line))
		
		if val_len != len(self.ids):
			raise CompileError('Expected {} values for tuple expression at line {}, got {}'.format(len(self.ids), self.line, len(val)))
		
		for idx in range(val_len):
			func.set_dollarid(self.ids[idx], val[idx])
