import os
import re
from os.path import *
from shutil import copyfile
from utils import get_parent_dir


class File:
	def __init__(self, name:str, path:str):
		self.name:str = name
		self.path:str = path
		self.ext:str = splitext(path)[1]

	def __str__(self):
		return f'File({self.name}, {self.path})'

	def __repr__(self):
		return str(self)

class Notes:
	def __init__(self, path:str):
		self.path:str = path
		self.parent:str = get_parent_dir(path)
		self.images:str = join(path, 'images')
		self.tex:File
		self.img_ext = []
		self.head:str

	def __get_tex(self) -> File:
		head, tail = split(self.path)
		tex_path = join(self.path, tail + '.tex')
		if exists(tex_path):
			return File(tail, tex_path)
		for file in os.listdir(self.path):
			if file.endswith('.tex'):
				return File(file[:-4], join(self.path, file))
		raise FileNotFoundError(f'Tex file missing in {self.path}')

	def __remove_multilines(self, text:str) -> str:
		text = text.strip()
		split_text = text.split('\n')
		for i in range(len(split_text) - 1, 0, -1):
			if not (split_text[i] or split_text[i - 1]):
				del split_text[i]
		return '\n'.join(split_text)

	def split(self):
		self.tex = self.__get_tex()
		with open(self.tex.path, 'r') as tex:
			text = tex.read()
		splitted = re.split(r'(\\section\{[\w$\s\'àèéìòù,.()\-_]+\})', text)
		sections = {}
		section = ''
		for i, line in enumerate(splitted):
			if not i:
				self.head = self.__remove_multilines(line)
			else:
				if i % 2:
					section = f'{(i+1)//2}. ' + re.search(r'\\section\{([\w$\s\'àèéìòù,.()\-_]+)\}', line).group(1)
					sections[section] = {'tex':line}
				else:
					sections[section]['body'] = self.__remove_multilines(line)
					images = re.findall(r'\\includegraphics\[scale=[.\d]+]{([\w\s_\',.\-^()]+)}', line)
					for i, image in enumerate(images):
						image_path = ''
						for ext in self.img_ext:
							path = join(self.images, image + ext)
							if exists(path):
								image_path = path
								break
						if not image_path:
							match = filter(lambda f: f.startswith(image + '.'), os.listdir(self.images))
							image_name, ext = splitext(next(match))
							self.img_ext.append(ext)
							image_path = join(self.images, image_name + ext)
						images[i] = File(image, image_path)

					sections[section]['images'] = images

		correction_dir = join(self.parent, f'Correzione [{self.tex.name}]')

		if not exists(correction_dir):
			os.mkdir(join(self.parent, f'Correzione [{self.tex.name}]'))

		for section, content in sections.items():
			try:
				section_dir = join(correction_dir, section)
				images_dir = join(section_dir, 'images')
				os.mkdir(section_dir)
				os.mkdir(images_dir)

				for image in content['images']:
					src = image.path
					dst = join(images_dir, image.name + image.ext)
					copyfile(src, dst)

				is_not_last = not content['body'].endswith('\\end{document}')
				with open(join(section_dir, section + '.tex'), 'w') as file:
					section = re.search(r'\d+\. ([\w\W]+)', section).group(1)
					# head = self.head.replace(
					# 	'\\fancyhead[L]{\\slshape\MakeUppercase{Appunti di algoritmi e strutture dati}}',
					# 	f'\\fancyhead[L]{{\\slshape\MakeUppercase{{Correzione di {section}}}}}'
					# )
					head = re.sub(
						r'\\fancyhead\[L\]\{\\slshape\\MakeUppercase\{[\w$\s\'àèéìòù,.()\-_]+\}\}',
						r'\\fancyhead[L]{\\slshape\\MakeUppercase{%s}}' % f'Correzione di {section}',
						self.head
					)
					body = f'{head}\n{content["tex"]}\n{content["body"]}'
					if is_not_last:
						body += '\n\\pagebreak\n\\end{document}'
					file.write(body)

			except FileExistsError as e:
				print(e)


	def join(self):
		dir_name = basename(self.path)
		if not dir_name.startswith('Correzione'):
			raise ValueError(f"{self.path} is not a correction directory")

		final_dir_name = re.search(r'Correzione \[([\w\s_\-]+)\]', dir_name).group(1)
		final_dir_path = join(self.parent, final_dir_name + ' [Corretto]')
		final_images_path = join(final_dir_path, 'images')
		for path in [final_dir_path, final_images_path]:
			if not exists(path):
				os.mkdir(path)


		sections = [directory for directory in os.listdir(self.path) if re.match(r'^\d+\.', directory)]
		sections = sorted(sections, key=lambda s: int(s.split('.')[0]))
		body:str = ''
		section_latex:str

		#print(sections)
		#return

		for i, section in enumerate(sections):
			with open(join(self.path, section, section + '.tex'), 'r') as tex_file:
				text = tex_file.read()
			if not i:
				self.head, section_latex, current_body = re.split(r'(\\section\{[\w$\s\'àèéìòù,.()\-_]+\})', text)
				header = re.search(r'\\Large\{\\textbf\{([\w$\s\'àèéìòù,.()\-_]+)\}\}', self.head).group(1)
				sub_re = r'\\fancyhead[L]{\\slshape\\MakeUppercase{%s}}' % header
				self.head = re.sub(
					r'\\fancyhead\[L\]\{\\slshape\\MakeUppercase\{Correzione di [\w$\s\'àèéìòù,.()\-_]+\}\}',
					sub_re,
					self.head
				)
				current_body = current_body.strip()
				body = '\n'.join([self.head, section_latex, current_body[:-14]]) # len(\end{document}) = 14
			else:
				_, section_latex, current_body = re.split(r'(\\section\{[\w$\s\'àèéìòù,.()\-_]+\})', text)
				current_body = current_body.strip()
				body += '\n'.join([section_latex, current_body[:-14]])

			section_path = join(self.path, section)
			images_path = join(section_path, 'images')
			for image in os.listdir(images_path):
				try:
					copyfile(join(images_path, image), join(final_images_path, image))
				except Exception as e:
					raise e

		body += '\\end{document}'

		with open(join(final_dir_path, final_dir_name + '.tex'), 'w') as tex_file:
			tex_file.write(body)