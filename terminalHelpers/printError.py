from terminalHelpers.terminalColors import TerminalColors

errorCount = 0

#===================================================
#Simple Error Printing
def printError(message: str, value=None, valueCaption="Received", hint=None, warn=False):
	global errorCount

	# Display error message and value (if need be)
	print(TerminalColors.bg.red + TerminalColors.bold(), end="")
	if (warn):
		print(TerminalColors.bg.yellow + "  WARN ", end="")
	else:
		print(TerminalColors.bg.red + " ERROR ", end="")
		errorCount += 1

	print(TerminalColors.reset(), end=" ")
	print(message, end="")

	if (value != None):
		print(TerminalColors.fg.cyan, end=" | ")
		print(TerminalColors.reset(), end=valueCaption + ": ")
		print(TerminalColors.fg.yellow, end="")
		print("`" + str(value) + "`", end="")
		print(TerminalColors.reset(), end="")

	print(end="\n")

	if (hint != None):
		print(TerminalColors.fade() + TerminalColors.bg.lightgrey, end="  Note ")
		print(TerminalColors.reset(), str(hint))

	return
