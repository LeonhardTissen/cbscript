from vector_expressions.vector_binop_base import vector_binop_base
from variable_types.scoreboard_var import scoreboard_var

class vector_binop_vector_expr(vector_binop_base):
	def calc_op(self, func, return_components):
		right_component_vars = self.rhs.compile(func, None)
		
		if right_component_vars == None:
			return None
			
		for i in range(3):
			right_var = right_component_vars[i].get_scoreboard_var(func)
			func.add_command('scoreboard players operation {} {} {}= {} {}'.format(return_components[i].selector, return_components[i].objective, self.op, right_var.selector, right_var.objective))
			right_component_vars[i].free_scratch(func)
