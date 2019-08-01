# evaluates expressions that are given as a list
import math, string, copy
from tkinter import *

################################################################################
## EVALUATOR
################################################################################

## Simple Expressions
def evaluateSimpleExpression(expression):
    express = copy.copy(expression)
    firstOperator, operatorIndex = findFirstOperator(express)
    length = len(express)
    while firstOperator!=None:
        try:
            # negative
            if firstOperator=="~":
                express = express[:operatorIndex] +\
                    [-express[operatorIndex+1]] +\
                    express[operatorIndex+2:]
            # standard binary operators
            elif firstOperator=="^":
                express = express[:operatorIndex-1] +\
                    [express[operatorIndex-1]**express[operatorIndex+1]] +\
                    express[operatorIndex+2:]
            elif firstOperator=="*":
                express = express[:operatorIndex-1] +\
                    [express[operatorIndex-1]*express[operatorIndex+1]] +\
                    express[operatorIndex+2:]
            elif firstOperator=="/":
                express = express[:operatorIndex-1] +\
                    [express[operatorIndex-1]/express[operatorIndex+1]] +\
                    express[operatorIndex+2:]
            elif firstOperator=="+":
                express = express[:operatorIndex-1] +\
                    [express[operatorIndex-1]+express[operatorIndex+1]] +\
                    express[operatorIndex+2:]
            elif firstOperator=="-":
                express = express[:operatorIndex-1] +\
                    [express[operatorIndex-1]-express[operatorIndex+1]] +\
                    express[operatorIndex+2:]
            
            # trig functions
            elif firstOperator=="sin":
                express = express[:operatorIndex] +\
                    [math.sin(express[operatorIndex+1])] +\
                    express[operatorIndex+2:]
            elif firstOperator=="cos":
                express = express[:operatorIndex] +\
                    [math.cos(express[operatorIndex+1])] +\
                    express[operatorIndex+2:]
            elif firstOperator=="tan":
                express = express[:operatorIndex] +\
                    [math.tan(express[operatorIndex+1])] +\
                    express[operatorIndex+2:]
            elif firstOperator=="csc":
                express = express[:operatorIndex] +\
                    [1 / (math.sin(express[operatorIndex+1]))] +\
                    express[operatorIndex+2:]
            elif firstOperator=="sec":
                express = express[:operatorIndex] +\
                    [1 / (math.cos(express[operatorIndex+1]))] +\
                    express[operatorIndex+2:]
            elif firstOperator=="cot":
                express = express[:operatorIndex] +\
                    [1 / (math.tan(express[operatorIndex+1]))] +\
                    express[operatorIndex+2:]
            # inverse trig functions
            elif firstOperator=="asin":
                express = express[:operatorIndex] +\
                    [math.asin(express[operatorIndex+1])] +\
                    express[operatorIndex+2:]
            elif firstOperator=="acos":
                express = express[:operatorIndex] +\
                    [math.acos(express[operatorIndex+1])] +\
                    express[operatorIndex+2:]
            elif firstOperator=="atan":
                express = express[:operatorIndex] +\
                    [math.atan(express[operatorIndex+1])] +\
                    express[operatorIndex+2:]
            elif firstOperator=="acsc":
                express = express[:operatorIndex] +\
                    [math.asin(1/express[operatorIndex+1])] +\
                    express[operatorIndex+2:]
            elif firstOperator=="asec":
                express = express[:operatorIndex] +\
                    [math.acos(1/express[operatorIndex+1])] +\
                    express[operatorIndex+2:]
            elif firstOperator=="acot":
                express = express[:operatorIndex] +\
                    [math.atan(1/express[operatorIndex+1])] +\
                    express[operatorIndex+2:]
            
            # other functions
            elif firstOperator=="mod":
                express = express[:operatorIndex-1] +\
                    [express[operatorIndex-1]%express[operatorIndex+1]] +\
                    express[operatorIndex+2:]
            elif firstOperator=="log":
                express = express[:operatorIndex] +\
                    [math.log(express[operatorIndex+2],\
                        express[operatorIndex+1])] +\
                    express[operatorIndex+3:]
            elif firstOperator=="sqrt":
                result = express[operatorIndex+1]**0.5
                if isinstance(result, complex):
                    assert(False)
                express = express[:operatorIndex] +\
                    [result] + express[operatorIndex+2:]
            elif firstOperator=="ceil":
                express = express[:operatorIndex] +\
                    [math.ceil(express[operatorIndex+1])] +\
                    express[operatorIndex+2:]
            elif firstOperator=="floor":
                express = express[:operatorIndex] +\
                    [math.floor(express[operatorIndex+1])] +\
                    express[operatorIndex+2:]
            elif firstOperator=="abs":
                express = express[:operatorIndex] +\
                    [math.abs(express[operatorIndex+1])] +\
                    express[operatorIndex+2:]
        except:
            return None
        firstOperator, operatorIndex = findFirstOperator(express)
        if len(express)>=length:
            return None
        length = len(express)
    if len(express)!=1:
        return None
    return express

## Other Stuff
# verifies: amount of rightParens so far never exceeds amount of leftParens
#           equal total amount of leftParens and rightParens
#           two different types of parens are never adjacent
# def verifyParens(equation):
#     leftParenCount = 0
#     rightParenCount = 0
#     prevEntry = None
#     for i in range(len(equation)):
#         if equation[i]=="(":
#             leftParenCount += 1
#         elif equation[i]==")":
#             rightParenCount += 1
#         if leftParenCount < rightParenCount:
#             return "paren error"
#         if (prevEntry=="(" and equation[i]==")") or\
#             (prevEntry==")" and equation[i]=="("):
#             return "paren error"
#         prevEntry = equation[i]
#     if leftParenCount != rightParenCount:
#         return "paren error"
#     return "good"

# gets innermost expression (nested the deepest inside due to parentheses)
# returns (innermostExpression, startIndex, endIndex) = None, None, None
#       if there is no innermostExpression (no leftParens)
def getInnermostExpression(expression):
    deepestIndex = None
    deepest = 0
    depth = 0
    for i in range(len(expression)):
        if expression[i]=="(":
            depth += 1
        elif expression[i]==")":
            depth -= 1
        if depth > deepest:
            deepestIndex = i
            deepest = depth
    if deepestIndex==None:
        return (None, None, None)
    innermostExpression = []
    startIndex = deepestIndex+1
    endIndex = startIndex
    while expression[endIndex] != ")":
        innermostExpression.append(expression[endIndex])
        endIndex += 1
    endIndex -= 1
    return (innermostExpression, startIndex, endIndex)

# orders operators by which is evaluated first, higher means earlier
def precedence(operator):
    if operator=="~":
        return 5
    elif operator=="^":
        return 4
    elif operator in ["mod", "log", "sqrt",\
        "sin", "cos", "tan", "csc", "sec", "cot",\
        "asin", "acos", "atan", "acsc", "asec", "acot",\
        "ceil", "floor", "abs"]:
        return 3
    elif operator in ["*", "/"]:
        return 2
    elif operator in ["+", "-"]:
        return 1
    else:
        # not an operator
        return 0

# finds firstOperator and its corresponding index
def findFirstOperator(expression):
    operatorIndex = None
    maxPrecedence = 0
    firstOperator = None
    for i in range(len(expression)):
        currentPrecedence = precedence(expression[i])
        if currentPrecedence>maxPrecedence:
            operatorIndex = i
            maxPrecedence = currentPrecedence
            firstOperator = expression[i]
    return (firstOperator, operatorIndex)

# evaluates an expression (list of strings)
def evaluateExpression(expression):
    innermostExpression, startIndex, endIndex =\
        getInnermostExpression(expression)
    while innermostExpression != None:
        try:
            evaluatedInnerExpression =\
                evaluateSimpleExpression(innermostExpression)
            expression = expression[:startIndex-1] +\
                evaluatedInnerExpression +\
                expression[endIndex+2:]
            innermostExpression, startIndex, endIndex =\
                getInnermostExpression(expression)
        except:
            return None
    expression = evaluateSimpleExpression(expression)[0]
    if type(expression) not in [float, int]:
        return None
    return expression

################################################################################
## TEST FUNCTIONS
################################################################################

def testEvaluateExpression():
    print("Testing evaluateExpression()...", end=" ")
    assert(evaluateExpression([0]) == 0)
    assert(evaluateExpression([2, "+", 3]) == 5)
    assert(evaluateExpression([2, "+", 3, "-", "(", "sin", "(", math.pi, "/", 2, ")", ")"]) == 4)
    print("Passed!")


# def testVerifyParens():
#     print("Testing verifyParens()...", end=" ")
#     assert(verifyParens(["(",")"]) == "paren error")
#     assert(verifyParens(["1", "2", "x", ")"]) == "paren error")
#     assert(verifyParens([")", 1, "("]) == "paren error")
#     assert(verifyParens(["(", 1, ")"]) == "good")
#     assert(verifyParens(["(", 1, ")"]) == "good")
#     assert(verifyParens(["1", "(", "(", 1, ")"]) == "paren error")
#     assert(verifyParens(["1", "(", "(", 1, ")", ")"]) == "good")
#     assert(verifyParens(["(", "(", 1, ")", 0, ")"]) == "good")
#     assert(verifyParens(["(", "(", ")", ")"]) == "paren error")
#     assert(verifyParens(["(", "(", 1, ")", ")"]) == "good")
#     assert(verifyParens(["(", 2, ")", "(", 1, ")"]) == "paren error")
#     print("Passed!")

def testAll():
    # testVerifyParens()
    testEvaluateExpression()

# testAll()
