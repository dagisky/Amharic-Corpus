import tika
from tika import parser
import tqdm
import re
import os

def explore_dir(path, ext='.pdf'):
	"""Takes Path to Directory and Explores pdf or other type of files
	Input (str): path to a directory
	Output (list): list of path to discovered files """
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
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
    parsed = parser.from_file(path)
    content = " ".join([c for c in re.split('\s|:',parsed["content"]) if not isEnglish(c)])
    return parsed["metadata"], content

