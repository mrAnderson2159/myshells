import os
import sys
import numpy as np

sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from utils import install_if_missing

try:
	from switch import *
	from typing import *
	from debug import debug
	from colors import *
	from paths import *
	from utils import indent_lines
	from pyerrors import *
except ModuleNotFoundError as e:
	install_if_missing(e)


class Transformer:
	def __init__(self, regex: str, rules: str, closing: str = '', replacements: list = None):
		if replacements is None:
			replacements = []
		self.regex = regex
		self.rules = rules
		self.closing = closing
		self.replacements = [
			('cdot', '\\cdot'), ('sum^', '\\sum^'), ('sum_', '\\sum_'),
			('𝛩', '\\Theta'), ('log_', '\\log_'), ('log{', '\\log{')
		]
		self.replacements.extend(replacements)

	def convert(self, string: str):
		# debug(self.replacements)
		match = re.match(self.regex, string)
		reps = self.rules.count('£')
		res = self.rules
		if not match:
			return None
		groups = match.groups()
		if reps != len(groups):
			e = ValueError(f"string must have as much groups as specified in rules, groups={len(groups)}, rules={reps}")
			raise e
		for group in groups:
			res = res.replace('£', group, 1)
		for replacement in self.replacements:
			# debug([replacement, res])
			res = res.replace(*replacement)
		# debug(res)
		return res


def clear():
	os.system('clear')


def feature(name: str) -> None:
	clear()
	cyan(f"Latex - {name}")


def get_code(feature_name: str) -> List[str]:
	pseudocode = list()

	def screen():
		feature(feature_name)
		print("Scrivi il codice, cancella la riga precedente con -1 e termina con \"end\"")
		for line in pseudocode:
			print(f'> {line}')

	screen()
	while True:
		current_line = input('> ')
		if current_line == 'end':
			break
		if current_line == '-1':
			pseudocode.pop()
		elif current_line:
			pseudocode.append(current_line)
		screen()
	return pseudocode


def convert_code(pscd: List[str], commands: Dict[str, Transformer], print_function: callable = print) -> None:
	for line in pscd:
		# debug(line)
		for command in commands.values():
			# debug(command.regex)
			res = command.convert(line)
			if res:
				print_function(res)
				break


def edit() -> None:
	""" Permette di aprire il programma in atom al fine di editarlo
	"""
	os.system(f'atom "{__file__}"')


def usage(indentation: int = 0) -> str:
	""" Definisce un manuale per il programma
	:param indentation: prende un valore di identazione per il testo
						per stamparlo sul terminale alla posizione desiderata
	"""
	usage = f'\n{c_green("USAGE")}: {thisname(__file__)}'
	usage += f'\n\t'
	usage += '\n'
	return indent_lines(usage, indentation)


def cases(flag: None):
	def default(pseudocode, commands, final):
		pseudocode[0] = p0 = f"${pseudocode[0]} = \\begin{{cases}}"
		convert_code(pseudocode, commands, print_function=lambda s: print(f"{s}{final if s != p0 else ''}"))

	pseudocode = get_code("Cases")
	commands = {
		".*": Transformer(r'(.*)', '£')
	}
	if not len(pseudocode):
		return
	final = '\\\\'
	if not flag:
		default(pseudocode, commands, final)
	elif flag == '-tn':
		if len(pseudocode) != 2:
			default(pseudocode, commands, final)
		else:
			print("$T(n) = \\begin{cases}")
			a = (s for s in ('n\\le1', 'otherwise'))
			convert_code(pseudocode, commands, print_function=lambda s: print(f"{s} & {next(a)}{final}"))
	print('\\end{cases}$')


def algorithm() -> None:
	pseudocode = list()
	replacements = [
		('==', '$$'), ('!=', '\\neq'),
		('=', '\\gets '), ('$$', '='),
		('step', '\\textbf{ step}'),
		('read', '\\textbf{read}'),
		('of', '\\textbf{ of}'),
		(' and ', '$ \\AND $'),
		(' or ', '$ \\OR $'),
		('qmezzo', 'q \\gets \\floor*{\\frac{p+r}{2}}')
	]
	transform = lambda *args: Transformer(*args, replacements=replacements)
	commands = {
		# "state": 	t(r'state (.*)', '\\STATE $£$;', replacements=replacements),
		"if": transform(r'if (.*)', '\\IF{$£$}', '\\ENDIF'),
		"for": transform(r'for (.*) to (.*)', '\\FOR{$£$ \\TO $£$}', '\\ENDFOR'),
		"fordown": transform(r'for (.*) downto (.*)', '\\FOR{$£$ \\textbf{ downto } $£$}', '\\ENDFOR'),
		"forall": transform(r'forall (.*) of (.*)', '\\FORALL{£ of £}', '\\ENDFOR'),
		"repeat": transform(r'repeat', '\\REPEAT'),
		"until": transform(r'until (.*)', '\\UNTIL{£}'),
		"require": transform(r'require (.*)', '\\REQUIRE{£};'),
		"ensure": transform(r'ensure (.*)', '\\ENSURE{£};'),
		"function": transform(r'function ([a-zA-Z0-9]+)(.*)', '\\FUNCTION{£}{£}', '\\ENDFUNCTION'),
		"else": transform(r'else', '\\ELSE'),
		"elsif": transform(r'elsif (.*)', '\\ELSIF{$£$}'),
		"while": transform(r'while (.*)', '\\WHILE{$£$}', '\\ENDWHILE'),
		"endif": transform(r'endif', '\\ENDIF'),
		"endfor": transform(r'endfor', '\\ENDFOR'),
		"endwhile": transform(r'endwhile', '\\ENDWHILE'),
		"return": transform(r'return (.*)', '\\RETURN $£$;'),
		"print": transform(r'print (.*)', '\\PRINT £'),
		"xor": transform(r'(.*) xor (.*)', '£\\XOR£'),
		"true": transform(r'(.*) true (.*)', '£\\TRUE£'),
		"false": transform(r'(.*) false (.*)', '£\\FALSE£'),
		"algorithm": transform(r'alg (.*)', '%\\label{alg:}\n\\caption{£}\n\\begin{algorithmic}[1]',
							   '\\end{algorithmic}'),
		# NB: "state" deve essere in ultima posizione, inserisci altri comandi sopra questo punto
		"state": transform(r'(.*)', '\\STATE $£$;'),
	}

	if sys.stdin.isatty():
		pseudocode = get_code("Algorithm")
	else:
		pseudocode = [_ for _ in sys.stdin.read().split('\n') if _]
	if not len(pseudocode):
		return

	print('\\begin{algorithm}')
	convert_code(pseudocode, commands)
	print('\\end{algorithmic}\n\\end{algorithm}')


def addtoc(args: List[str]):
	string = ' '.join(args)
	feature("addcontentsline")
	# regex without escape braces r'\\([a-z]+)\*\{(.+)\}'
	match = re.match(r'\\([a-z]+)\*{(.+)}', string)
	if not match:
		e = "l'argomento passato non è l'intestazione di una sessione, " \
			"passare una stringa nella forma \\subsection*{my subsection}"
		raise R00(e)
	section_type, section_name = match.groups()
	print(f'\\addcontentsline{{toc}}{{{section_type}}}{{{section_name}}}\n')


def induzione():
	feature('induzione')
	print(
		"\\begin{enumerate}\n\\item\\textbf{Caso base}\\\\\n\\item\\textbf{Suppongo vero}\\\\"
		"\n\\item\\textbf{Passo induttivo}\\\\\n\\end{enumerate}")


def polynomial(args: List[str]) -> None:
	feature('polinomio')
	deg = 0
	coef = 'a'
	indet = 'x'
	if not len(args):
		raise A00("this function takes at least 1 argument (deg)")
	if len(args) >= 1:
		deg = int(args[0])
	if len(args) >= 2:
		coef = args[1]
	if len(args) == 3:
		indet = args[2]
	pol = ''
	for i in range(deg, -1, -1):
		pol += f'{coef}_{i}{indet if i else ""}{f"^{i}" if i > 1 else ""}{" + " if i else ""}'
	print(pol + '\n')


def array(args):
	feature('tabella array')
	if len(args):
		try:
			index = int(args[0])
		except ValueError:
			index = 0
	else:
		index = 0
	elements = input("Inserisci gli elementi dell'array separati da una virgola\n> ")
	elements = list(map(str.strip, elements.split(',')))
	res = '\\begin{center}\n'
	res += '\\begin{tabular}{|' + '|'.join(['c' for _ in elements]) + '|}\n\\hline\n'
	res += '&'.join(map(str, range(index, len(elements) + index))) + '\\\\\\hline\n'
	res += '&'.join(map(lambda s: f'\\textbf{{{s}}}' if s else '', elements)) + '\\\\\\hline\n'
	res += '\\end{tabular}\n'
	res += '\\end{center}'
	print(res)


def vector(args: List[str], /, headers=True):
	def dotted(char, escape, dot, format):
		format, final_repl = format.split(',')
		v = f"{char}_{{{format.replace('d', '1')}}} {escape} {char}_{{{format.replace('d', '2')}}} " \
			f"{escape} \\{dot} {escape} {char}_{{{format.replace('d', final_repl)}}}"
		print(v + '\\\\')

	def normal(char, escape, n, format):
		v = ''
		for i in range(int(n)):
			v += f"{char}_{{{format.replace('d', str(i + 1))}}} {escape if i != int(n) - 1 else ''}"
		v += '\\\\'
		print(v)

	def ifdotted(char, escape, dot, n, format):
		dotted(char, escape, dot, format) if n == 'dot' else normal(char, escape, n, format)

	if headers:
		feature('vettore')
	e = 'Il vettore deve avere 4 parametri: tipo (c,col,r,row), lettera, ' \
		'formato_pedice (d,dd,1d,dn, ecc...), lunghezza (int o "dot")'
	assert len(args) >= 4, e
	type, char, format, n = args
	e = f'Il vettore deve essere di tipo (c,col) o (r,row), non {type}'
	assert type in ('c', 'col', 'r', 'row'), e

	if headers:
		print(f'${char} = \\begin{{bmatrix}}')
	if type in ('c', 'col'):
		ifdotted(char, '\\\\', 'vdots', n, format)
	else:
		ifdotted(char, '&', 'dots', n, format)
	if headers:
		print('\\end{bmatrix}$\n')


def matrix(args: List[str], /, headers=True):
	feature('matrice')
	e = "La matrice deve avere 2 parametri: lettera, dimensione (nxm)"
	assert len(args) >= 2, e
	letter, dim = args
	n, m = dim.split('x')
	if headers:
		print(f"${letter.upper()} = \\begin{{bmatrix}}")
	try:
		n, m = int(n), int(m)
		for i in range(n):
			vector(['r', letter, f'{i + 1}d', m], headers=False)
	except ValueError:
		vector(['r', letter, f'1d,{m}', 'dot'], headers=False)
		vector(['r', letter, f'2d,{m}', 'dot'], headers=False)
		print('\\vdots & ' * 3 + '\\vdots\\\\')
		vector(['r', letter, f'{n}d,{m}', 'dot'], headers=False)

	if headers:
		print('\\end{bmatrix}$')


def boolean_function(
		args: List[str], *,
		center: bool = False,
		expression: bool = False,
		SOP: bool = False,
		POS: bool = False):
	"""Takes functions as arguments and return a latex table with the variables binary cases on the left
	and the functions values on the right.

	Example:
		latex -b "f(x,y,z): (x | y) and (x or y&z)" "s: x^y" "c: x&y"\n\n

		\\\\begin{tabular}{ccc|ccc}\n
		$x$&$y$&$z$&$f(x,y,z)$&$s$&$c$\\\\\\\\\\hline\n
		0&0&0&\\\\textcolor{red}{0}&\\\\textcolor{red}{0}&\\\\textcolor{red}{0}\\\\\\\\\n
		0&0&1&\\\\textcolor{red}{0}&\\\\textcolor{red}{0}&\\\\textcolor{red}{0}\\\\\\\\\n
		0&1&0&\\\\textcolor{red}{0}&\\\\textcolor{red}{1}&\\\\textcolor{red}{0}\\\\\\\\\n
		0&1&1&\\\\textcolor{red}{1}&\\\\textcolor{red}{1}&\\\\textcolor{red}{0}\\\\\\\\\n
		1&0&0&\\\\textcolor{red}{1}&\\\\textcolor{red}{1}&\\\\textcolor{red}{0}\\\\\\\\\n
		1&0&1&\\\\textcolor{red}{1}&\\\\textcolor{red}{1}&\\\\textcolor{red}{0}\\\\\\\\\n
		1&1&0&\\\\textcolor{red}{1}&\\\\textcolor{red}{0}&\\\\textcolor{red}{1}\\\\\\\\\n
		1&1&1&\\\\textcolor{red}{1}&\\\\textcolor{red}{0}&\\\\textcolor{red}{1}\\\\\\\\\n
		\\\\end{tabular}\n


	:param args: a list of functions
	:param center: a flag to tell if print the latex directive \begin{center} or not
	:param expression: a flag for testing, if True the program will return only the expression
	"""
	functions = {"__vars": set()}
	for function in args:
		if function.startswith('__order'):
			functions['__order'] = function.split('=')[1]
		else:
			name, body = map(str.strip, function.split(':', 1))
			if name in functions:
				raise ValueError(f"Every function must have a different name, there are two instances of {name}")

			functions[name] = {'body': body}

	operators = "and or if else int in not + - * / // & | != == < > <= >= ^ ' ( ) \\ ,".split(' ')
	# for i in range(6):
	# 	operators[i] = f' {operators[i]} '
	operators.append(' ')

	def joined(_list: list, char: str = ','):
		return char.join(_list)

	def from_order(order:str, variables:set) -> list:
		return [var for var in order if var in variables]

	for i, function in enumerate(functions):
		if not function.startswith('__'):
			body = functions[function]['body']
			for operator in operators:
				body = body.replace(operator, '')

			vars = {x for x in set(body) if x.isalpha()}
			functions['__vars'] |= vars
			functions[function]['vars'] = vars = sorted(vars) if not '__order' in functions \
				else from_order(functions['__order'], vars)

			body = functions[function]['body']
			functions[function]['body'] = f"def function{i}({joined(vars)}):\n" \
										  f"\ttry:\n" \
										  f"\t\treturn int({body})\n" \
										  f"\texcept ValueError:\n" \
										  f"\t\treturn '-'"

	functions['__vars'] = sorted(functions['__vars']) if not '__order' in functions else functions['__order']

	if expression:
		for function in functions:
			if function == '__vars':
				print(f'vars:\n\t{joined(functions["__vars"])}')
			elif not function.startswith('__'):
				print(function + ':')
				print('\tvars: ' + joined(functions[function]['vars']))
				print(functions[function]['body'])

		return
	command = ''

	for function_name, function in functions.items():
		if not function_name.startswith('__'):
			command += function['body'] + '\n'

	i = 0
	tab = '\t'
	variables = functions['__vars']
	function_list = [function for function in functions if not function.startswith('__')]

	for variable in variables:
		command += f"{tab * i}for {variable} in range(2):\n"
		i += 1

	command += f"{tab * i}values.append(f'{{{'}{'.join(variables)}}}"
	# {{function({joined})}}

	for i, function in enumerate(function_list):
		command += f"{{function{i+1}({joined(functions[function]['vars'])})}}"

	command += "')"

	values = []
	exec(command, {'values': values})
	values = map(list, values)

	var_len = len(variables)

	if SOP:
		# matrice dei dati con variabili e funzioni
		values = np.array(list(map(lambda a: np.array(list(map(lambda x: int(x) if x.isdigit() else np.nan, a))), values)))
		# matrice delle variabili
		var_matrix = values[:, :var_len]
		# debug(values)
		# debug(var_matrix)
		string = '\\begin{eqnarray*}\n'
		# per ogni funzione
		for i, function_name in enumerate(function_list):
			# function diventa il vettore dei dati della funzione
			function = values[:,var_len + i]

			# crea una stringa del tipo f(x,y,z)
			string += function_name + f'({joined(functions[function_name]["vars"])}) &=& '
			# per ciascun valore di function dove value rappresenta l'elemento values[var_len + i][j]
			for j, value in enumerate(function):
				if value == 1:
					for k, var in enumerate(functions[function_name]["vars"]):
						string += var if var_matrix[j, k] == 1 else var + "'"
					string += ' + '
			string = string[:-3]
			if i != len(function_list) - 1:
				string += '\\\\\n'
		string += '\n\\end{eqnarray*}'
		print(string)
		return

	result = ''
	if center:
		result += '\\begin{center}\n'
	result += f"\\begin{{tabular}}{{{'c' * len(variables)}|{'c' * len(function_list)}}}\n"
	result += f"${'$&$'.join([*variables, *function_list])}$\\\\\\hline\n"



	for value in values:
		for i, bit in enumerate(value):
			if i < var_len:
				result += f"{bit}&"
			else:
				result += f"\\textcolor{{red}}{{{bit}}}" if bit != '-' else '$-$'
				if i != len(value) - 1:
					result += '&'
				else:
					result += f"\\\\\n"
	result += '\\end{tabular}\n'
	if center:
		result += '\\end{center}\n'
	print(result)






# def boolean_function_legacy(
# 		args: List[str], *,
# 		center: bool = False,
# 		expression: bool = False):
# 	e = "La funzione deve avere almeno due parametri: almeno una variabile e almeno una funzione da applicare"
# 	if len(args) < 2:
# 		raise ValueError(e)
# 	variables, function = args
# 	joined = ','.join(variables)
#
# 	if expression:
# 		print(function)
# 		return
#
# 	function = f"def function({joined}):\n\ttry:\n\t\treturn int({function})\n\texcept ValueError:\n\t\treturn '-'"
# 	command = f'{function}\n'
# 	i = 0
# 	tab = '\t'
# 	for variable in variables:
# 		command += f"{tab * i}for {variable} in range(2):\n"
# 		i += 1
# 	command += f"{tab * i}values.append(f'{{{'}{'.join(variables)}}}{{function({joined})}}')"
# 	values = []
# 	exec(command, {'values': values})
# 	values = map(list, values)
#
# 	result = ''
# 	if center:
# 		result += '\\begin{center}\n'
# 	result += f"\\begin{{tabular}}{{{'c' * len(variables)}|c}}\n"
# 	result += f"${'$&$'.join(variables)}$&$f({joined})$\\\\\\hline\n"
# 	for *vars, value in values:
# 		result += f"{'&'.join(vars)}&"
# 		result += f"\\textcolor{{red}}{{{value}}}" if value != '-' else '$-$'
# 		result += f"\\\\\n"
# 	result += '\\end{tabular}\n'
# 	if center:
# 		result += '\\end{center}\n'
# 	print(result)

def mealy(center: bool = False):
	feature('Mealy table')
	n_s = int(input("Inserisci il numero di stati della macchina\n> "))
	table = []
	for i in range(n_s):
		table.append([])
		for j in range(2):
			s_o = input(f"Stato {c_red(f's_{i}')}, input {c_white(j)}: inserisci l'indice del prossimo stato e l'output "
						f"separati da uno spazio\n> ").strip()
			try:
				s_o = tuple(map(int, s_o.split(' ')))
				table[i].append(s_o)
			except Exception:
				input('Qualcosa è andato storto, riprova\n')
				j -= 1

	res = ''

	if center:
		res = '\\begin{center}\n'

	res += f'\\begin{{tabular}}{{|c|c|c|}}\n\\hline\n&\\textcolor{{gray}}{{0}}&\\textcolor{{gray}}{{1}}\\\\\\hline\n'

	for i, row in enumerate(table):
		res += f'\\textcolor{{red}}{{$s_{i}$}} & '
		for s_o in row:
			s, o = s_o
			res += f'$s_{s}$/\\textcolor{{teal}}{{{o}}} & '
		res = res[:-2] + '\\\\\\hline\n'

	res += '\\end{tabular}\n'

	if center:
		res += '\\end{center}\n'

	print(res)

def moore(center: bool = False):
	feature('Moore table')
	n_s = int(input("Inserisci il numero di stati della macchina\n> "))
	table = []
	for i in range(n_s):
		table.append([])
		try:
			s_o = input(f"Stato {c_red(f's_{i}')}: inserisci l'indice dei prossimi "
						f"due stati e l'output separati da uno spazio\n> ").strip()
			s_o = tuple(map(int, s_o.split(' ')))
			assert len(s_o) == 3
			table[i] = s_o
		except Exception as e:
			print(e)
			input('Qualcosa è andato storto, riprova\n')
			i -= 1

	res = ''

	if center:
		res = '\\begin{center}\n'

	res += f'\\begin{{tabular}}{{|c|c|c|c|}}\n\\hline\n&\\textcolor{{gray}}{{0}}&\\textcolor{{gray}}{{1}}&' \
		   f'\\textcolor{{teal}}{{U}}\\\\\\hline\n'

	for i, row in enumerate(table):
		res += f'\\textcolor{{red}}{{$s_{i}$}} & '
		for j, n in enumerate(row):
			if j != 2:
				res += f'$s_{n}$ & '
			else:
				res += f'\\textcolor{{teal}}{{{n}}}'
		res += '\\\\\\hline\n'

	res += '\\end{tabular}\n'

	if center:
		res += '\\end{center}\n'

	print(res)




def UnknownFlagError(flag: str) -> None:
	""" Solleva l'errore F01 del modulo pyerrors
	:raises pyerrors.UnknownFlagError
	"""
	raise F01(flag + usage(1))


def main(argv: List[str]) -> None:
	if len(argv) == 1:
		argv.append('')
	try:
		with Switch(argv[1]) as s:
			s.exit_case('--edit', edit)
			s.case('-i', usage)
			s.case('-a', algorithm)
			s.case('-ar', array, argv[2:])
			s.case('-c', cases, argv[2] if len(argv) > 2 else None)
			s.case('-m', matrix, argv[2:])
			s.case('-p', polynomial, argv[2:])
			s.case('-v', vector, argv[2:])
			s.case('-b', boolean_function, argv[2:])
			s.case('-bc', boolean_function, argv[2:], center=True)
			s.case('-be', boolean_function, argv[2:], expression=True)
			s.case('-bsop', boolean_function, argv[2:], SOP=True)
			s.case('-addtoc', addtoc, argv[2:])
			s.case('-induzione', induzione)
			s.case('-mealy', mealy)
			s.case('-mealyc', mealy, center=True)
			s.case('-moore', moore)
			s.case('-moorec', moore, center=True)
			s.default(UnknownFlagError, argv[1])
	except IndexError as e:
		print(e.with_traceback)
		raise F00(usage(1))
	except KeyboardInterrupt:
		print('\n\nEsecuzione terminata\n')


if __name__ == '__main__':
	main(sys.argv)
