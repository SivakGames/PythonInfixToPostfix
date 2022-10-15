import re
import math
import numbers

from terminalHelpers.printError import printError, errorCount

#============================================================
#Single char math tokens for the initial parsing into tokens
MATH_TOKENS_SINGLE_CHAR = "+-*/%^&|<>~"

#Binary math tokens and their priority ranking (i.e. order of operations)
BINARY_TOKENS = {
	"*": 12,
	"/": 12,
	"%": 12,
	"+": 11,
	"-": 11,
	"<<": 10,
	">>": 10,
	"&": 7,
	"^": 6,
	"|": 5,
}

#Unary tokens
UNARY_TOKENS = {
	"¬": 15,  # Negation (i.e. * -1)
	"~": 15,  # One's complement
}

#============================================================
#Just for sample purposes. Would likely define these elsewhere in a real program
USER_DEF_VARS = {
	"v1": 50,
	"v2": 100,
}

#============================================================
#============================================================
# Will take a string that represents a mathematical expression, 
# parse all the tokens out of it and attempt to evaluate it

def infixExpressionToPostfix(expression: str):
	global errorCount
	errorCount = 0
	finalVal = None

	rawTokens = tokenizeValue(expression)

	infixTokens = initialParse(rawTokens)
	if(errorCount > 0):
		return None
	postfixTokens = infixTokensToPostfix(infixTokens)
	if (errorCount > 0):
		return None


	finalVal = evaluatePostfixTokens(postfixTokens)

	if (finalVal == None):
		printError("Could not evaluate!")

	return finalVal

#============================================================
# Take the string and parse it into raw tokens, 
# eliminating any whitespace from the edges of the tokens

def tokenizeValue(val):
	mathMode = bool(val[0] in MATH_TOKENS_SINGLE_CHAR)
	rawTokens = []
	token = ""

	for i in range(0, len(val)):
		char = val[i]

		#Left parens are special
		#In math mode, they are treated as basic parens.
		#In non-math mode, they can be a function
		if (char == '('):
			if (mathMode):
				token = token.strip()
				if (token):
					rawTokens.append(token)
				rawTokens.append(char)

			else:
				token += char
				rawTokens.append(token.strip())
			token = ''

		#Right parens are special
		elif (char == ')'):
			token = token.strip()
			if (token):
				rawTokens.append(token)
			rawTokens.append(char)
			token = ''

		#All other tokens
		elif (char == ' ' or (mathMode and char in MATH_TOKENS_SINGLE_CHAR) or (not mathMode and char not in MATH_TOKENS_SINGLE_CHAR)):
			token += char

		else:
			token = token.strip()

			#If a only series of spaces was found, don't append
			if (token):
				rawTokens.append(token)

			#Start anew from this character
			token = char
			mathMode = not mathMode

	#Append the last token unless it's spaces only (e.g. after right parentheses)
	token = token.strip()
	if (token):
		rawTokens.append(token)

	return rawTokens

#============================================================
#Parse what can be parsed at this point.
# Replace any variables with their appropriate numerical values
# Deterine if certain negative signs are unary
# Determine if any functions are void???

def initialParse(rawTokens):
	global errorCount
	parsedTokens = []
	
	for t in range(0, len(rawTokens)):
		subTokens = []
		token = rawTokens[t]

		#Check for decimal, hex, or binary numbers
		if (re.match(r"^\-?(?:0x|0b.+)|(?:[0-9].*)$", token)):
			negate = -1 if token[0:1] == "-" else 1
			token = token[1:] if token[0:1] == "-" else token

			match token[0:2]:
				case "0x":
					removeChars = 2
					base = 16
				case "0b":
					removeChars = 2
					base = 2
				case _:
					removeChars = 0
					base = 10

			try:
				token = int(token[removeChars:], base) * negate
			except ValueError:
				printError("Bad numeric value!", value=token)
				

		#Look for user defined vars
		#These can start with a letter or underscore
		elif (token[-1] != "(" and re.match(r"^[a-zA-Z_].*$", token[0])):
			if(token in USER_DEF_VARS):
				token = USER_DEF_VARS.get(token)
			else:
				printError("Label is undefined!", token)
				

		#Look for unary negative operators
		elif(bParseUnaries(t, token)):
			while(len(token) > 0 and bParseUnaries(t, token)):
				transformedToken = '¬' if token[-1] == "-" else token[-1]
				subTokens.insert(0, transformedToken)
				token = token[:-1].strip()

		#Append the token (or any remaining tokens)
		if (isinstance(token, numbers.Number) or len(token) > 0):
			subTokens.insert(0,token)
		
		parsedTokens.extend(subTokens)

	return parsedTokens

#Sub operation for determining if symbol needs to be parsed into unary
def bParseUnaries(index, token):
	unaries = "-~"
	return token[-1] in unaries and ((index == 0) or len(token) > 1)

#============================================================
#The main process - Take the tokens and convert them into a postfix array

def infixTokensToPostfix(infixTokens):
	global errorCount
	operations = []
	rawPostfixTokens = []
	closeParenErrCnt = 0
	openParenErrCnt = 0

	for t in range(0, len(infixTokens)):
		token = infixTokens[t]

		#Look for numbers and append to values (most common thing)
		if (isinstance(token, numbers.Number)):
			val = int(token)
			rawPostfixTokens.append(val)
			

		#Look for opening parens or functions
		elif (token[-1] == "("):
			operations.append(token)

		#Look for closing parens and pop operators until right parens are found
		# *Flags error if none are found
		elif (token == ')'):
			bRun = True
			while (len(operations) > 0 and bRun):
				operationsTopToken = operations.pop()

				#If we've found our opening paren, stop running
				bRun = operationsTopToken[-1] != '('

				#A bare opening paren will clear out it and the closing paren as they're not needed for postfix
				# If it is not bare (i.e. text in front), then it's a function and will be treated as such during final evaluation
				if (operationsTopToken == '('):
					break

				rawPostfixTokens.append(operationsTopToken)

			# If this is still "running" at this point then closing parens are mismatched/erroneous
			closeParenErrCnt += 1 if bRun else 0

		#Look for unary math operations and append them straight away
		elif (token in UNARY_TOKENS):
			operations.append(token)

		#Look for binary math operations
		elif (token in BINARY_TOKENS):
			while (len(operations) > 0):
				operationsTopToken = operations[-1]
				tokenValue = BINARY_TOKENS.get(token)
				topTokenValue = max(BINARY_TOKENS.get(operationsTopToken, 0), UNARY_TOKENS.get(operationsTopToken, 0))

				if (operationsTopToken[-1] == "(" or tokenValue > topTokenValue):
					break

				rawPostfixTokens.append(operationsTopToken)
				operations.pop()

			operations.append(token)
			

		# If NONE of the above, then it's either a variable/memory OR
		#  a bad/undef operator (will get flagged later if so)
		else:
			rawPostfixTokens.append(token)

	#---------------------
	#Retrieve any operations still on the stack
	while (len(operations) > 0):
		operation = operations.pop()
		if(operation[-1] == "("):
			closeParenErrCnt+=1
			operation += "("
		rawPostfixTokens.append(operation)

	openParenErrCnt = rawPostfixTokens.count('(')

	if (openParenErrCnt > 0):
		printError("Too many or incorrectly placed opening parentheses in expression!", value=openParenErrCnt, valueCaption="Number found")

	if (closeParenErrCnt > 0):
		printError("Too many or incorrectly placefd closing parentheses in expression!", value=closeParenErrCnt, valueCaption="Number found")
	
	errorCount += openParenErrCnt + closeParenErrCnt

	return rawPostfixTokens

#============================================================
#Finally, try and evaluate postfix into a value

def evaluatePostfixTokens(postfixTokens):
	global errorCount
	values = []
	while (len(postfixTokens) > 0):
		token = postfixTokens.pop(0)
		if (isinstance(token, numbers.Number)):
			values.append(token)
			continue

		operation = token

		#For unary operations, simply take the one value
		if(operation in UNARY_TOKENS):
			try:
				onlyVal = values.pop()

			except IndexError:
				printError("Unary mathmetical expression is missing a value!", hint="You likely have a misplaced " + operation + " symbol in your expression")
				
				break

			match operation:
				case '¬':
					onlyVal *= -1
				case '~':
					onlyVal = ~onlyVal
				
			values.append(onlyVal)

		#For binary operations, take two values
		elif(operation in BINARY_TOKENS):
			rightVal = None
			leftVal = None
			try:
				rightVal = values.pop()
				leftVal = values.pop()

			except IndexError:
				printError("Binary mathmetical expression needs 2 values!", hint="You likely have a missing or non-numeric value somewhere in your expression")
				
				break
		
			match operation:
				case '+':
					leftVal += rightVal
				case '-':
					leftVal -= rightVal
				case '*':
					leftVal *= rightVal
				case '/':
					try:
						leftVal /= rightVal
					except ZeroDivisionError:
						printError("Expression has division by 0!")
						
						break
				case '%':
					leftVal %= rightVal
				case "^":
					leftVal ^= rightVal
				case "&":
					leftVal &= rightVal
				case "|":
					leftVal |= rightVal
				case "<<":
					leftVal <<= rightVal
				case ">>":
					leftVal >>= rightVal

			values.append(leftVal)

		#Try functions
		elif(operation[-1] == "("):
			operation = operation[:-1]

			try:
				onlyVal = values.pop()

			except IndexError:
				printError("Value missing in " + operation + " function!")
				
				break
			
			match operation:
				case 'sqrt':
					onlyVal = math.sqrt(onlyVal)
				case 'sin':
					onlyVal = math.sin(math.radians(onlyVal))
				case 'cos':
					onlyVal = math.cos(math.radians(onlyVal))
				case _:
					printError("Undefined function", value=operation)
					
					
			values.append(onlyVal)

		else:
			printError(message="Irregular symbol/value found in mathmetical expression!!!", value=token, valueCaption="Found")
			

	try:
		finalValue = values[0] if len(values) == 1 and not errorCount > 0 else None
	except IndexError:
		finalValue = None

	return finalValue

