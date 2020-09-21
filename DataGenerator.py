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
		print('Initializing Output...')
		if os.path.exists(self.args.output_dir): 
			# self.output_files = explore_dir(os.path(self.args.output_dir), ext='.txt', max_size=self.args.max_output_size)
			for i in range(self.args.number_of_output_files):
					self.output_files.append(os.path.join(self.args.output_dir, str(i)+".txt"))
			assert self.output_files != [], "Output files not initialized: No output files have been found with "
		else:			
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

	def get_data_chunk(self, file, parsed_data_size):
		"""Return Chunk pdf data interval of the data to be randomly written on the output file
			Input:
				file (str): to enable  the code to check if the file exists in the initialized list of pdf files
							 and assert the progress
				Parsed_data_size (int): size of the parsed data
			Output:
				(start_index: end_index)
		"""
		assert file in  self.pdf_files, "Chunk data should be in initialized pdf documents"
		if self.pdf_files[file] + self.args.chunk_size < (self.args.reader_ending_index % parsed_data_size):
			return (self.pdf_files[file] , self.pdf_files[file]+self.args.chunk_size), self.args.chunk_size
		else:
			last_chunk = self.args.reader_ending_index % parsed_data_size
			return (self.pdf_files[file], self.pdf_files[file]+last_chunk), last_chunk


	def write_output(self, file, data):
		"""Write data to a file
			Input:
				file (str): path to output file
				data (list)"""
		mode = 'w+'
		if os.path.exists(file):
			mode = 'a+'
		with open(file, mode, encoding=self.args.output_encoding) as f:
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
		if not os.path.exists(file) or os.path.getsize(file) < self.args.max_output_size:
			self.write_output(file, data)
			is_block_written = True
			return is_block_written
		else:
			self.output_files.remove(file)
			is_block_written = self.write_randomized_output(data)
		return is_block_written


	def write_progress(self, filename, data):
		with open(filename, 'w+') as outfile:
			json.dump(data, outfile)
		outfile.close()


	def generate(self):
		"""Main Function to Generate Data form PDF files"""
		assert self.pdf_files != {}, "All Pdf Files have been explored"
		# itterate untill all data has been fully written [input can be ra]
		number_of_sentence_generated = 0
		for i, file  in tqdm(enumerate(list(self.pdf_files.keys()))):
			metadata, content = read_pdf(file)	
			if content == None:
				continue		
			parsed_data = split_by(content, self.args.text_split_param)

			while self.is_readable(file, len(parsed_data)):
				chunk, chunk_size = self.get_data_chunk(file, len(parsed_data))
				data = parsed_data[chunk[0]:chunk[1]]
				written = self.write_randomized_output(data)				
				self.pdf_files[file] += chunk_size
				if written:
					number_of_sentence_generated += chunk_size
			self.write_progress(self.args.reader_progress, self.pdf_files)
		print("{} sentences have been written".format(number_of_sentence_generated))
	


