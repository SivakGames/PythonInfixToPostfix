class TerminalColors:
	def reset():
		return '\033[0m'

	def bold(): 
		return '\033[1m'
	
	def fade(): 
		return '\033[2m'
	
	def italic(): 
		return '\033[3m'

	def underline(): 
		return '\033[4m'
	
	def reverse(): 
		return '\033[7m'

	class fg: 
		black = '\033[30m'
		red = '\033[31m'
		green = '\033[32m'
		yellow = '\033[33m'
		blue = '\033[34m'
		magenta = '\033[35m'
		cyan = '\033[36m'
		lightgrey = '\033[36m'

	class bg:
		black = '\033[40m'
		red = '\033[41m'
		green = '\033[42m'
		yellow = '\033[43m'
		blue = '\033[44m'
		magenta = '\033[45m'
		cyan = '\033[46m'
		lightgrey = '\033[47m'
