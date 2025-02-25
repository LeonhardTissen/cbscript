from block_types.block_base import block_base
import tellraw

class title_block(block_base):
	def __init__(self, line, subtype, selector, times, unformatted):
		self.line = line
		self.subtype = subtype
		self.selector = selector
		self.times = times
		self.unformatted = unformatted
		
	def compile(self, func):
		if self.times != None:
			func.add_command('/title {} times {}'.format(self.selector, ' '.join([str(t.get_value(func)) for t in self.times])))
		
		text = tellraw.formatJsonText(func, self.unformatted)
		command = '/title {} {} {}'.format(self.selector, self.subtype, text)
		func.add_command(command)
