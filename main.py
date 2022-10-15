from infixExpressionToPostfix import infixExpressionToPostfix

# Change these to whatever expressions you want to solve
EXPRESSIONS = [
	"1 + 2",
	"-(1 + 2)",
	"-(1 + 2) / -6",
	"22 * (33 + 44 * 55 ) / (66 - 77) - 88",
	"15 & 8",
	"sqrt(121) + cos(0)",
	"-0x200 + (16 / 77)",
	"v1 + v2"
]


def main():
	for i in EXPRESSIONS:
		val = infixExpressionToPostfix(i)
		print (val)

main()
