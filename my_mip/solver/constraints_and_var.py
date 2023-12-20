class Constraint:
    def __init__(self, expression, sense, rhs):
        if not isinstance(expression, Expression):
            raise ValueError("Expression must be of type Expression")
        self.expression = expression
        self.sense = sense  # '==', '<=', '>='
        self.rhs = rhs

    def __repr__(self):
        return f"{self.expression} {self.sense} {self.rhs}"


class Variable:
    def __init__(self, name, lb=0, ub=float('inf'), vtype='continuous'):
        self.name = name
        self.lb = lb
        self.ub = ub
        self.vtype = vtype  # 'continuous', 'integer', or 'binary'
    
    # Representation for debugging
    def __repr__(self):
        return f"Variable({self.name}, lb={self.lb}, ub={self.ub}, type={self.vtype})"

    def __add__(self, other):
        return Expression()._add_variable(self).__add__(other)

    def __radd__(self, other):
        return Expression()._add_variable(self).__add__(other)

    def __mul__(self, other):
        return Expression()._add_variable(self, other)

    def __rmul__(self, other):
        return Expression()._add_variable(self, other)

    def __le__(self, other):
        if isinstance(other, (int, float)):
            # Create an expression for the variable
            expr = Expression()._add_variable(self)
            # Return a constraint with the expression and the constant
            return Constraint(expr, '<=', other)
        else:
            raise TypeError("Right-hand side of <= must be a number")

    def __ge__(self, other):
        if isinstance(other, (int, float)):
            # Create an expression for the variable
            expr = Expression()._add_variable(self)
            # Return a constraint with the expression and the constant
            return Constraint(expr, '>=', other)
        else:
            raise TypeError("Right-hand side of <= must be a number")


class Expression:
    def __init__(self):
        self.terms = {}  # Dictionary to store variables and their coefficients

    def add_term(self, variable, coefficient):
        if variable in self.terms:
            self.terms[variable] += coefficient
        else:
            self.terms[variable] = coefficient

    def __iadd__(self, other):
        if isinstance(other, Variable):
            self.add_term(other, 1)
        elif isinstance(other, Expression):
            for var, coeff in other.terms.items():
                self.add_term(var, coeff)
        else:
            raise ValueError("Can only add Variable or Expression objects")
        return self

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise ValueError("Can only multiply by a scalar")
        result = Expression()
        for var, coeff in self.terms.items():
            result.add_term(var, coeff * other)
        return result

    def __rmul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        return " + ".join([f"{coeff}*{var.name}" for var, coeff in self.terms.items()])

    def _add_variable(self, variable, coefficient=1):
        self.add_term(variable, coefficient)
        return self

    def __add__(self, other):
        if isinstance(other, Expression):
            new_expr = Expression()
            for var, coeff in self.terms.items():
                new_expr.add_term(var, coeff)
            for var, coeff in other.terms.items():
                new_expr.add_term(var, coeff)
            return new_expr
        elif isinstance(other, Variable):
            return self._add_variable(other)
        elif isinstance(other, (int, float)):
            self.add_term(Variable(f"const_{other}", lb=other, ub=other, vtype='continuous'), other)
        return self
    
    def __radd__(self, other):
        return self.__add__(other)

    def __le__(self, other):
        return Constraint(self, '<=', other)

    def __ge__(self, other):
        return Constraint(self, '>=', other)

    def __eq__(self, other):
        return Constraint(self, '==', other)


class Objective:
    def __init__(self, expression, sense):
        self.expression = expression  # The linear expression to be optimized
        self.sense = sense            # 'minimize' or 'maximize'

    def __repr__(self):
        return f"Objective({self.expression}, {self.sense})"
