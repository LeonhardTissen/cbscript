from block_types.block_base import block_base
import traceback
from CompileError import CompileError

class for_index_block(block_base):
	def __init__(self, line, var, fr, to, by, sub):
		self.line = line
		self.var = var
		self.fr = fr
		self.to = to
		self.by = by
		self.sub = sub
		
	def compile(self, func):
		var, fr, to, by, sub = self.var, self.fr, self.to, self.by, self.sub
		
		from_var = fr.compile(func, var.get_assignto(func))
		var.copy_from(func, from_var)
		
		to_var = to.compile(func).get_scoreboard_var(func)
			
		if by != None:
			by_var = by.compile(func)
			by_const = by_var.get_const_value(func)
			
			if by_const == None:
				by_var = by_var.get_scoreboard_var(func)
			else:
				by_const = int(by_const)
				
		unique = func.get_unique_id()
		loop_func_name = 'line{:03}/for{:03}'.format(self.line, unique)

		loop_func = func.create_child_function()
		func.register_function(loop_func_name, loop_func)	

		if var.uses_macro(func): 
			loop_func.has_macros = True

		if to_var.uses_macro(func):
			loop_func.has_macros = True

		if by != None and by_const == None and by_var.uses_macro(func):
			loop_func.has_macros = True
		
		try:
			loop_func.compile_blocks(sub)
		except CompileError as e:
			print(e)
			raise CompileError('Unable to compile for block contents at line {}'.format(self.line))
		except Exception as e:
			print(traceback.print_exc())
			raise CompileError('Unable to compile for block contents at line {}'.format(self.line))
		
		if by == None:
			# Use a temporary version of the counting var to work with the scoreboard
			temp_var = var.get_scoreboard_var(func)
			continue_command = 'execute if score {} <= {} run {}'.format(temp_var.get_selvar(func), to_var.get_selvar(func), loop_func.get_call())
			func.add_command(continue_command)
			
			# Add 1 to the counter variable
			loop_func.add_command('scoreboard players add {0} 1'.format(temp_var.get_selvar(func)))
			var.copy_from(func, temp_var)
			
			loop_func.add_command(continue_command)
		else:
			# Use a temporary version of the counting var to work with the scoreboard
			temp_var = var.get_scoreboard_var(func)
			
			if by_const:
				continue_command = 'execute if score {} {} {} run {}'.format(temp_var.get_selvar(func), '>=' if by_const < 0 else '<=', to_var.get_selvar(func), loop_func.get_call())
				func.add_command(continue_command)

				loop_func.add_command('scoreboard players {} {} {}'.format('add' if by_const > 0 else 'remove', temp_var.get_selvar(func), abs(by_const)))
			else:
				continue_negative_command = 'execute if score {} matches ..-1 if score {} >= {} run {}'.format(by_var.get_selvar(func), temp_var.get_selvar(func), to_var.get_selvar(func), loop_func.get_call())
				continue_positive_command = 'execute if score {} matches 1.. if score {} <= {} run {}'.format(by_var.get_selvar(func), temp_var.get_selvar(func), to_var.get_selvar(func), loop_func.get_call())
				func.add_command(continue_negative_command)
				func.add_command(continue_positive_command)

				loop_func.add_command('scoreboard players operation {} += {}'.format(temp_var.get_selvar(func), by_var.get_selvar(func)))
				
			var.copy_from(func, temp_var)
			
			if by_const:
				loop_func.add_command(continue_command)
			else:
				loop_func.add_command(continue_negative_command)
				loop_func.add_command(continue_positive_command)				
			
		to_var.free_scratch(func)
		from_var.free_scratch(func)
		if by != None:
			by_var.free_scratch(func)
