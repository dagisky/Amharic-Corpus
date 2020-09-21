from tika import parser
import tqdm
import re
import os
import shutil
from shutil import copyfile

def explore_dir(path, ext='.pdf', max_size=None):
	"""Takes Path to Directory and Explores pdf or other type of files
	Input (str): path to a directory
	Output (list): list of path to discovered files """
	files = []
	for (dirpath, dirnames, filenames) in os.walk(path):
		if max_size:
			filenames = [os.path.join(dirpath, f) for f in filenames if os.path.splitext(f)[-1].lower() == ext and os.path.getsize(os.path.join(dirpath, f)) <= max_size]
		else:
			filenames = [os.path.join(dirpath, f) for f in filenames if os.path.splitext(f)[-1].lower() == ext]
		files.extend(filenames)
	return files


def isEnglish(s):
	"""Takes a token and checks if the input token is english or other language
		Input (str): input token
		output (bool): true if english else false"""
	try:
		s.encode(encoding='utf-8').decode('ascii')
	except UnicodeDecodeError:
		return bool(re.findall('[A-Za-z]', s))
	else:
		return True

def read_pdf(filename):
	"""Read a PDF file and return Metadata and Content of the input pdf file
	Input: (str) path to pdf file
	Output:
		metadata,
		content (str): content of the pdf file"""    
	filename = r"{}".format(filename)
	parsed = parser.from_file(filename)
	if parsed["content"] != None:
		content = " ".join([c for c in re.split('\s|:', parsed["content"]) if not isEnglish(c)])
		return parsed["metadata"], content
	else: 
		return parsed["metadata"], None



def split_by(data, param="sentence"):
	"""Split String by paragraph or Sentence
		Input:		
			data (str): textual data to split
			param (str): [sentence|paragraph]
		Output (list): list of sentence or paragraph"""
	if param == "sentence":
		return [p.strip()+"፡፡" for p in re.split('፡፡|\n+|።', data, flags=re.DOTALL)]               
	else:
		return [s.strip() for s in re.split('\n+', data, flags=re.DOTALL)]




def copy_file(filename, output_dir):
	"""Coppy all amharic files"""
	# copyfile(filename, output_dir)
	shutil.copy2(filename, output_dir)	