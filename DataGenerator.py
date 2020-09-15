import tika
from utils.pdfUtils import *
import random

class DataSetGenerator(object):
	"""docstring for DataSetGenerator"""
	def __init__(self, args):
		super(DataSetGenerator, self).__init__()
		self.args = args
		self.pdf_files = dict()
		self.output_files = list()

		self.load_pdf_files()
		self.init_outputs()
		tika.initVM()

	def load_pdf_files(self):

		if os.path.exists(self.args.reader_progress):
			self.pdf_files = json.load(self.args.reader_progress) 	
		else:
			files = explore_dir(self.args.root_dir, max_size=self.args.max_pdf_size)
			start_indices = [self.starting_index for _ in range(len(files))]
			self.pdf_files = dict(zip(files, start_indices))

	def init_outputs(self):

		if os.path.exists(self.args.output_dir): 
			self.output_files = explore_dir(self.args.output_dir, ext='.txt', max_size=self.args.max_output_size)
		else:
			try:  
				os.mkdir(self.args.output_dir)  
				for i in range(self.args.number_of_output_files):
					self.output_files.append(os.path.join(self.args.output_dir, str(i)+".txt"))
			except OSError as error:  
				print(error)

	def is_readable(self, file, parsed_length): #index = index % len(l)
		if self.args.reader_starting_index < parsed_length and \
		(parsed_length-self.args.reader_starting_index) > abs(self.args.reader_ending_index) and \
		self.pdf_files[file] < self.args.reader_ending_index % parsed_length:
			return True
		else:
			return False

	def write_output(file, data):
		with open(file, 'w+', encoding='utf-8') as f:
			for d in data:
				f.write(d+"\n")
		f.close()

	def write_randomized_output(self, data):
		assert self.output_files != [], "All dataset Files have been completed"
		file = random.choice(self.output_files)
		written = False
		if os.path.getsize(file) < self.max_output_size:
			self.write_output(file, data)
			written = True
			return written
		else:
			self.output_files.remove(file)
			written = self.write_randomized_output(data)
		return written



	def generate(self):

		assert self.pdf_files != {}, "All Pdf Files have been explored"
		# itterate untill all data has been fully written [input can be ra]
		file = random.choice(self.pdf_files.keys())		
		metadata, content = read_pdf(random.choice(numberList))
		parsed_data = split_by(content, self.args.text_split_param)

		while self.is_readable(file, len(parsed_data)):
			if self.pdf_files[file] + self.args.chunk_size < self.args.reader_ending_index % len(parsed_data)
				data = parsed_data[self.pdf_files[file]:self.args.chunk_size]
				self.write_randomized_output(data)
				self.pdf_files[file] += self.args.chunk_size
			else:
				last_chunk = self.args.reader_ending_index % len(parsed_data)
				data = parsed_data[self.pdf_files[file]:last_chunk]
				self.write_randomized_output(data)
				del self.pdf_files[file] # += last_chunk [remove item from dictionary]

		


