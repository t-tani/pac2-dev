import re
from typing import Dict

# Define operator precedence
precedence = {
    "==": 4,
    "!=": 4,
    ">": 4,
    "<": 4,
    ">=": 4,
    "<=": 4,
    "not": 3,
    "and": 2,
    "or": 1
}

# Define operator mapping
operator_mapping = {
    "==": "equals",
    ">=": "greaterOrEquals",
    "<=": "lessOrEquals",
    ">": "greater",
    "<": "less",
    "and": "and",
    "or": "or",
    "not": "not",
    "!=": "not_equals"
}

# Define the regular expression pattern for the tokenizer
# pattern = r"""
#     "(?:\\.|[^\\"])*"    # Match double quoted string with possible escaped double quotes
#     |
#     !=                  # Match '!=' operator
#     |
#     ==                  # Match '==' operator
#     |
#     >=                  # Match '>=' operator
#     |
#     <=                  # Match '<=' operator
#     |
#     [<>]                # Match '<' or '>' operator
#     |
#     \b(?:and|or|not|true|false)\b  # Match 'and', 'or', 'not' keywords
#     |
#     \(                  # Match '('
#     |
#     \)                  # Match ')' 
#     |
#     \b\d*\.\d+\b        # Match floating point numbers
#     |
#     \b\d+\b             # Match integers
#     |
#     [a-zA-Z0-9_-]+      # Match variable names
# """

# Tokenizer function
# def tokenizer(s):
#     return re.findall(pattern, s, re.VERBOSE)

def tokenizer(s):
    keywords = ['and', 'or', 'not', 'true', 'false']
    operators = ['!=', '==', '>=', '<=', '>', '<']
    tokens = []
    token = ''
    i = 0

    while i < len(s):
        char = s[i]

        if char == ' ':
            if token != '':
                tokens.append(token)
                token = ''
        elif char in operators or (i + 1 < len(s) and s[i:i+2] in operators):
            if token != '':
                tokens.append(token)
                token = ''
            operator = s[i:i+2] if i + 1 < len(s) and s[i:i+2] in operators else char
            tokens.append(operator)
            i += len(operator) - 1
        elif char in ('(', ')'):
            if token != '':
                tokens.append(token)
                token = ''
            tokens.append(char)
        elif char == '\"':
            if token != '':
                tokens.append(token)
                token = ''
            end_of_string = s.find('\"', i + 1)
            if end_of_string == -1:
                raise ValueError("Unterminated string literal")
            token = s[i:end_of_string+1]  # Include the quotes
            tokens.append(token)
            token = ''
            i = end_of_string
        elif char in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'):  # Digits and decimal point
            token += char
        elif char.isalpha() or char in ('-', '_'):  # Variables and boolean values
            token += char
            # If this token is a keyword and is followed by a non-alphanumeric character or end of string, append it
            if token in keywords and (i + 1 == len(s) or not s[i+1].isalnum()):
                tokens.append(token)
                token = ''
        else:
            raise ValueError("Unknown character: " + char)

        i += 1
    if token != '':
        tokens.append(token)

    return tokens

# Convert infix tokens to RPN using Shunting Yard algorithm
def infix_to_rpn(tokens):
    output_queue = []
    operator_stack = []
    for token in tokens:
        if token in precedence:  # If token is an operator
            while (operator_stack and operator_stack[-1] in precedence and
                   precedence[token] <= precedence[operator_stack[-1]]):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == "(":
            operator_stack.append(token)
        elif token == ")":
            while operator_stack and operator_stack[-1] != "(":
                output_queue.append(operator_stack.pop())
            operator_stack.pop()  # Remove the '('
        else:  # If token is a number or a variable
            output_queue.append(token)

    while operator_stack:  # Pop remaining operators from the stack
        output_queue.append(operator_stack.pop())

    return output_queue


# Create AST from RPN
def create_ast(rpn_tokens):
    stack = []
    for token in rpn_tokens:
        if token not in precedence and token not in ["==", "!=", ">", "<", ">=", "<="]:  # If token is a number or a variable
            stack.append({"type": "Literal", "value": token})
        else:  # If token is an operator
            if token in ["==", "!=", ">", "<", ">=", "<="]:  # binary operators
                right = stack.pop() if stack else None
                left = stack.pop() if stack else None
                if right is None or left is None:
                    raise ValueError('Malformed expression: insufficient operands for operator {}'.format(token))
                stack.append({"type": "BinaryExpression", "operator": token, "left": left, "right": right})
            elif token == "not":  # unary operator
                operand = stack.pop() if stack else None
                if operand is None:
                    raise ValueError('Malformed expression: insufficient operand for operator {}'.format(token))
                stack.append({"type": "UnaryExpression", "operator": token, "argument": operand})
            else:  # "and", "or" binary operators
                right = stack.pop() if stack else None
                left = stack.pop() if stack else None
                if right is None or left is None:
                    raise ValueError('Malformed expression: insufficient operands for operator {}'.format(token))
                stack.append({"type": "LogicalExpression", "operator": token, "left": left, "right": right})

    if len(stack) != 1:
        raise ValueError('Malformed expression: the final stack contained more than one element')
    return stack[0]  # Root of the AST


def ast_to_dict(node):
    node_type = node["type"]

    if node_type == "Literal":
        value = node["value"]
        if value == "true":
            return True
        elif value == "false":
            return False
        elif "\"" in value:
            value = value.replace("\"","")
            return value
        try:
            value = float(value) if '.' in value else int(value)
        except ValueError:
            value = f'@variables(\'{value}\')'
        return value
    elif node_type == "UnaryExpression":
        operator = operator_mapping[node["operator"]]
        argument = ast_to_dict(node["argument"])
        return {operator: argument}
    elif node_type in ["BinaryExpression", "LogicalExpression"]:
        operator = operator_mapping[node["operator"]]
        left = ast_to_dict(node["left"])
        right = ast_to_dict(node["right"])

        # Handle "not equals" operator
        if operator == "not_equals":
            return {"not": {"equals": [left, right]}}
        else:
            return {operator: [left, right]}

class Condition:
    """
    Conditionの条件式を定義するためのクラス.
    Condition式を入力すると以下のようなJSONを出力することを期待される.
        input: var2 == false
        output: "expression" : { "equals" : ["@variables('var2')", false] }
    """

    def __init__(self, expression:str) -> None:
        tokens = tokenizer(expression)
        rpn_tokens = infix_to_rpn(tokens)
        self.ast = create_ast(rpn_tokens)

    def export(self) -> Dict:
        return ast_to_dict(self.ast)

#s = '(var == "test" and var2 != "test2") or var3 > 1.22 or var4 < 2 or var5 >= 0.123 or var6 <= 6 or not var7 == 7'
#s = 'var == 1 or (var == "test" and var2 != "test2") or var3 > 1.22 or var4 < 2 or var5 >= 0.123 or var6 <= 6 or not var7 == 7'
#s  = 'a == true or b != false'

# C = Condition("(aaaho31lk1j2109 == .209122 ) and (Var2221 >= 10) and (false or var1 == (var02 == false))")
# print(C.export())