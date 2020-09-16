import unittest
import argparse
from utils.pdfUtils import *
from DataGenerator import DataSetGenerator

class TestUtil(unittest.TestCase):

	def setUp(self):	
		self.root_dir = r"C:\Users\Abiy\Desktop"
		self.text_split_param = "sentence"
		self.test_pdf = r"C:\Users\Abiy\Desktop\Dagi\pdf_sample.pdf"

	def test_explore_dir(self):
		files_explored_correctly, max_size = True, 10000
		ext = '.pdf'
		files = explore_dir(self.root_dir, ext , max_size)
		for f in files:
			file_name, file_extension = os.path.splitext(f)
			if file_extension != ext:
				files_explored_correctly = False
			if max_size < os.path.getsize(f):
				files_explored_correctly = False
		self.assertEqual(files_explored_correctly, True, 'file explorer not working within given params')

class TestDataSetGeneratorClass(unittest.TestCase):

	def setUp(self):
		parser = argparse.ArgumentParser() 
		parser.add_argument("--extract_pdf", action='store_true', help="Whether to run training.")
		parser.add_argument("--root_dir", default=None, type=str)
		parser.add_argument("--output_dir", default='data', type=str)
		parser.add_argument("--text_split_param", default='sentence', type=str, help="Determines how we split the text [sentence|paragraph]")
		parser.add_argument("--reader_starting_index", default=10, type=int , help="Determines Where to start Reading PDF chunks")
		parser.add_argument("--reader_ending_index", default=-10, type=int , help="Determines Where to stop Reading PDF chunks")
		parser.add_argument("--reader_progress", default='progress.json', type=str)
		parser.add_argument("--progress_update_interval", default=3, type=int , help="Determines how to load the progress to progress.json")
		parser.add_argument("--max_pdf_size", default=-1, type=int, help="Maximum size of each PDF file size allowed. (MB)")
		parser.add_argument("--max_output_size", default=100, type=int, help="Maximum size of each output file size. (MB)")
		parser.add_argument("--chunk_size", default=5, type=int, help="Number of Sentence chunk Randomly distributed")
		parser.add_argument("--number_of_output_files", default=100, type=int, help="Maximum size of each output file size.")
		parser.add_argument("--total_parsed_data_size", default=100000, type=int, help="The Maximum parsed Data allowed in (MB)")
		
		self.test_pdf = r"C:\Users\Abiy\Desktop\Dagi\pdf_sample.pdf"
		self.args = parser.parse_args()

		self.generator = DataSetGenerator(self.args)
		
	def test_is_readable(self):
		self.generator.pdf_files[self.test_pdf] = self.args.reader_starting_index
		metadata, content = read_pdf(self.test_pdf)		
		parsed_data = split_by(content, self.args.text_split_param)	
		print('-------------data length------------')
		print(self.args.reader_ending_index % len(parsed_data))
		self.assertEqual(self.generator.is_readable(self.test_pdf, len(parsed_data)), True, 'Readablity incorrect..')

	# def test_generator_writer(self):

if __name__ == '__main__':
    unittest.main()