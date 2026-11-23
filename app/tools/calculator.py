"""Second AgentForge tool: evaluate a short arithmetic expression safely.

No eval() and no names, attributes or function calls: only numbers,
+ - * / // % ** and parentheses. Huge operands are refused so an
expression like 9 ** 999999999 cannot hang the chat.
"""
import ast
import operator
import math

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}
_MAX_DIGITS = 20


def _count_digits(value):
    try:
        return len(str(abs(int(value))))
    except (OverflowError, ValueError):
        return _MAX_DIGITS + 1


def _evaluate(node):
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        if _count_digits(left) > _MAX_DIGITS or _count_digits(right) > _MAX_DIGITS:
            raise ValueError("numbers are too large")
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("exponent is too large (maximum 100)")
        result = _OPERATORS[type(node.op)](left, right)
        if isinstance(result, complex) or (isinstance(result, float) and not math.isfinite(result)):
            raise ValueError("result must be a finite real number")
        if _count_digits(result) > _MAX_DIGITS:
            raise ValueError("result is too large")
        return result
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
        return _UNARY[type(node.op)](_evaluate(node.operand))
    raise ValueError("only arithmetic with numbers is allowed")


def calculate(expression):
    """Return the value of a short arithmetic expression as text."""
    if expression is not None and not isinstance(expression, str):
        return "Cannot calculate: give a text expression"
    if not expression or not expression.strip():
        return "Nothing to calculate. Give an expression like: 2 + 3 * 4"
    if len(expression) > 500:
        return "Cannot calculate: expression is too long (maximum 500 characters)"
    try:
        value = _evaluate(ast.parse(expression, mode="eval"))
    except (SyntaxError, ValueError, TypeError, ZeroDivisionError, OverflowError, RecursionError) as exc:
        return f"Cannot calculate '{expression.strip()}': {exc}"
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return str(value)
