from variable_types.scoreboard_var import scoreboard_var

class sel_vector_var_expr(object):
	def __init__(self, sel, id):
		self.sel = sel
		self.id = id
		
	def compile(self, func, assignto):
		return_components = []
		for i in range(3):
			return_components.append(scoreboard_var(self.sel, '_{}_{}'.format(self.id, i)))
		
		func.get_vector_path(self.sel, self.id)
		
		return return_components