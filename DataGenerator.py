from utils.pdfUtils import *
import random
from tqdm import tqdm
import json
import tika
from tika import parser
import sys

class DataSetGenerator(object):
	"""docstring for DataSetGenerator"""
	def __init__(self, args):
		super(DataSetGenerator, self).__init__()
		self.args = args
		self.pdf_files = dict()
		self.output_files = list()
		tika.initVM()
		if args.extract_pdf:
			self.load_pdf_files()
			self.init_outputs()
		


	def load_pdf_files(self):
		'''Loads all PDF files from given root directory or if progress file'''
		if os.path.exists(self.args.reader_progress):
			print('Loading input files from pre-process progress file...')
			with open(self.args.reader_progress, 'r') as j:
				self.pdf_files = json.load(j)
			# self.pdf_files = json.load(self.args.reader_progress) 	
		else:
			print('Exploring for PDF files...')
			if self.args.max_pdf_size != -1:
				files = explore_dir(self.args.root_dir, max_size=self.args.max_pdf_size)
			else: 
				files = explore_dir(self.args.root_dir)
			if files == []:
				sys.exit("NO PDF found with the given parameters...")  
			start_indices = [self.args.reader_starting_index for _ in range(len(files))]
			self.pdf_files = dict(zip(files, start_indices))			
			with open(self.args.reader_progress, 'w+') as outfile:
				json.dump(self.pdf_files, outfile)



	def init_outputs(self):
		"""Initialize Output Files"""
		if os.path.exists(self.args.output_dir): 
			print('Loading Output files...')
			self.output_files = explore_dir(self.args.output_dir, ext='.txt', max_size=self.args.max_output_size)
		else:
			print('Initializing Output...')
			try:  
				os.mkdir(self.args.output_dir)  
				for i in range(self.args.number_of_output_files):
					self.output_files.append(os.path.join(self.args.output_dir, str(i)+".txt"))
			except OSError as error:  
				print(error)


	def is_readable(self, file, parsed_length): 
		"""Check if the given pdf file is within the given read parameters
			Input:
				file (str): path to the read file
				parsed_lenght (int): length of the parsed data based on sentence or paragraph"""
		if self.args.reader_starting_index < parsed_length and self.pdf_files[file] < self.args.reader_ending_index % parsed_length:
			return True
		else:
			return False


	def write_output(file, data):
		"""Write data to a file
			Input:
				file (str): path to output file
				data (list)"""
		with open(file, 'a+', encoding='utf-8') as f:
			for d in data:
				f.write(d+"\n")
		f.close()



	def write_randomized_output(self, data):
		"""Save the given section of data to randomized output depending on the size of the output data
		   The size of single output file should not exceed specific size
				Input (list): list of sentences
				Output (bool): returns true if file is successfuly written to document"""
		assert self.output_files != [], "All dataset Files have been completed"
		file = random.choice(self.output_files)
		is_block_written = False
		if not os.path.exists(file) or os.path.getsize(file) < self.max_output_size:
			self.write_output(file, data)
			is_block_written = True
			return is_block_written
		else:
			self.output_files.remove(file)
			is_block_written = self.write_randomized_output(data)
		return is_block_written



	def generate(self):
		"""Main Function to Generate Data form PDF files"""
		assert self.pdf_files != {}, "All Pdf Files have been explored"
		# itterate untill all data has been fully written [input can be ra]

		for i, file  in tqdm(enumerate(list(self.pdf_files.keys()))):
			# print('... reading {}'.format(file))	
			metadata, content = read_pdf(file)	
			if content == None:
				continue		
			parsed_data = split_by(content, self.args.text_split_param)

			while self.is_readable(file, len(parsed_data)):
				if self.pdf_files[file] + self.args.chunk_size < (self.args.reader_ending_index % len(parsed_data)):
					data = parsed_data[self.pdf_files[file]:self.args.chunk_size]
					print('--------------writing data--------------')
					print(file)
					print(len(data))
					print(data)
					self.write_randomized_output(data)
					self.pdf_files[file] += self.args.chunk_size
				else:
					last_chunk = self.args.reader_ending_index % len(parsed_data)
					data = parsed_data[self.pdf_files[file]:last_chunk]
					self.write_randomized_output(data)
					# del self.pdf_files[file] # += last_chunk [remove item from dictionary]
			if i % self.args.progress_update_interval:
				with open(self.args.reader_progress, 'w+') as outfile:
					json.dump(self.pdf_files, outfile)
		


