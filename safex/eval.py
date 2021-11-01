"""
Evaluator module
Convert expressions to AST and then evaluate them.
"""
import ast
import operator
from typing import Mapping, Any, Optional


def eval_expression(expression: str, scope: Optional[Mapping[str, Any]] = None) -> Any:
    """
    Parses and evaluates expression.

    :param expression: Expression to evaluate
    :param scope: Mapping of names and values. Can be variables or functions.
    :return: Calculated values.
    :throw:
        ValueError: If the expression is invalid.
    """
    parsed = ast.parse(expression, mode="eval")
    return Evaluator(scope).visit(parsed)


class Evaluator(ast.NodeVisitor):
    """
    Evaluates parsed expression.

    :param scope: The local scope for evaluation
    """

    global_scope = {
        "True": True,
        "False": False,
        "all": all,
        "any": any,
        "max": max,
        "min": min,
        "sum": sum,
    }

    binary_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.LShift: operator.lshift,
        ast.RShift: operator.rshift,
        ast.BitOr: operator.or_,
        ast.BitXor: operator.xor,
        ast.BitAnd: operator.and_,
        ast.FloorDiv: operator.floordiv,
    }

    unary_operators = {
        ast.Invert: operator.invert,
        ast.Not: operator.not_,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    boolean_operators = {
        ast.And: all,
        ast.Or: any,
    }

    comparison_operators = {
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
        ast.In: lambda a, b: a in b,
        ast.NotIn: lambda a, b: a not in b,
    }

    def __init__(self, scope: Optional[Mapping[str, Any]] = None):
        self.local_scope = scope or {}

    def visit_Expression(self, node: ast.Expression) -> Any:
        """
        Evaluates expression body.

        :param node: Expression node
        :return: Evaluated expression
        """
        return self.visit(node.body)

    def visit_BinOp(self, node: ast.BinOp) -> Any:
        """
        Evaluates binary operator.

        :param node: binary operator node
        :return: Evaluated expression
        :throw:
            ValueError: If the operator is invalid.
        """
        operator_fn = self.binary_operators.get(type(node.op))
        if not operator_fn:
            raise ValueError(f"Invalid operator: {node.op}")
        left = self.visit(node.left)
        right = self.visit(node.right)
        return operator_fn(left, right)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        """
        Evaluates unary operator.

        :param node: unary operator node
        :return: Evaluated expression
        """
        operator_fn = self.unary_operators.get(type(node.op))
        return operator_fn(self.visit(node.operand))

    def visit_Compare(self, node: ast.Compare) -> bool:
        """
        Evaluates comparison.

        :param node: comparison node
        :return: comparison result
        """
        left = self.visit(node.left)
        for operation, comparator in zip(node.ops, node.comparators):
            operator_fn = self.comparison_operators.get(type(operation))
            right = self.visit(comparator)
            if not operator_fn(left, right):
                return False
            left = right
        return True

    def visit_Name(self, node: ast.Name) -> Any:
        """
        Evaluates a name lookup.

        :param node: name node
        :return: value of the name
        :throw:
            ValueError: If the name cannot be found
        """
        name = node.id
        value = self.local_scope.get(name) or self.global_scope.get(name)
        if not value:
            raise ValueError(f"Undefined name: {name}")
        return value

    def visit_BoolOp(self, node: ast.BoolOp) -> bool:
        """
        Evaluates boolean operator.

        :param node: boolean operator node
        :return: true or false
        :throw:
            ValueError: If the operator is invalid.
        """
        operator_fn = self.boolean_operators.get(type(node.op))
        return operator_fn(self.visit(value) for value in node.values)

    def visit_Call(self, node: ast.Call) -> Any:
        """
        Evaluates a function call.

        :param node: function call node
        :return: evaluated value
        """
        fn = self.visit(node.func)
        args = [self.visit(arg) for arg in node.args]
        kwargs = {keyword.arg: self.visit(keyword.value) for keyword in node.keywords}
        return fn(*args, **kwargs)

    def visit_IfExp(self, node: ast.IfExp) -> Any:
        """
        Evaluates if expression.
        :param node: if expression node
        :return: Evaluated expression
        """
        test = self.visit(node.test)
        return self.visit(node.body) if test else self.visit(node.orelse)

    def visit_List(self, node: ast.List) -> Any:
        """
        Evaluates list load.

        :param node: list node
        :return: evaluated list
        :throw:
            ValueError: If the name cannot be found
        """
        return [self.visit(element) for element in node.elts]

    def visit_Dict(self, node: ast.Dict) -> Any:
        """
        Evaluates dict load.
        :param node: dictionary node
        :return: dict value
        """
        return {
            self.visit(key): self.visit(value)
            for key, value in zip(node.keys, node.values)
        }

    def visit_Tuple(self, node: ast.Tuple) -> Any:
        """
        Evaluates tuple load.
        :param node: tuple node
        :return: evaluated tuple
        :throw:
            ValueError: If the name cannot be found
        """
        return tuple(self.visit(element) for element in node.elts)

    def visit_Subscript(self, node: ast.Subscript) -> Any:
        """
        Evaluates subscript.
        :param node: subscript node
        :return: subscript value
        :throw:
            ValueError: If the name cannot be found
        """
        return operator.getitem(self.visit(node.value), self.visit(node.slice))

    def visit_Slice(self, node: ast.Slice) -> Any:
        """
        Evaluates slice
        :param node: slice node
        :return: slice object
        """
        if node.lower and node.upper and node.step:
            return slice(
                self.visit(node.lower), self.visit(node.upper), self.visit(node.step)
            )
        elif node.lower and node.upper:
            return slice(self.visit(node.lower), self.visit(node.upper))
        elif node.lower:
            return slice(self.visit(node.lower), None)
        elif node.upper:
            return slice(self.visit(node.upper))

    def visit_Index(self, node: ast.Index) -> Any:
        """
        Evaluates index.

        :param node:  index node
        :return: index value
        """
        return self.visit(node.value)

    def visit_NameConstant(self, node: ast.NameConstant) -> Any:
        """
        Evaluates Name constant.
        :param node: name constant node
        :return: name constant value
        """
        return node.value

    def visit_Constant(self, node: ast.Constant) -> Any:
        """
        Evaluates constant node.

        :param node: constant node
        :return: constant value
        """
        return node.value

    def visit_Str(self, node: ast.Str) -> Any:
        """
        Evaluates str
        :param node: str node
        :return: str value
        """
        return node.s

    def visit_Num(self, node: ast.Num) -> Any:
        """
        Evaluates number
        :param node: num node
        :return: num value
        """
        return node.n

    def generic_visit(self, node: ast.AST) -> Any:
        """
        Generic visit
        :param node: node type
        :throw: ValueError
        """
        raise ValueError(f"Unknown node type: {node}")
