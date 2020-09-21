from utils.pdfUtils import *
import argparse
from tqdm import tqdm
from DataGenerator import DataSetGenerator


def main(args):
	if args.extract_pdf:
		"""Extract PDF from all PDF files under the root Directory"""
		print("Extract Mode...")
		generator = DataSetGenerator(args)
		generator.generate()

	if args.copy_pdf:
		# copy all amharic pdf files from the root directory to output_dir
		print("Copy Mode...")
		all_files = explore_dir(args.root_dir)
		for file in tqdm(all_files):
			meta, content = read_pdf(file)
			if content != None or content != []:
				if os.path.exists(args.output_dir): 
					copy_file(file, args.output_dir)
				else:
					os.mkdir(args.output_dir)
					copy_file(file, args.output_dir)
				




if __name__ == "__main__":
	print('init')
	parser = argparse.ArgumentParser()      

	parser.add_argument("--extract_pdf", action='store_true', help="Whether to run training.")
	parser.add_argument("--copy_pdf", action='store_true', help="Whether to run training.")
	parser.add_argument("--root_dir", default=None, type=str)
	parser.add_argument("--output_dir", default='data', type=str)
	parser.add_argument("--output_encoding", default='utf-16', type=str)
	parser.add_argument("--text_split_param", default='sentence', type=str, help="Determines how we split the text [sentence|paragraph]")
	parser.add_argument("--reader_starting_index", default=1, type=int , help="Determines Where to start Reading PDF chunks")
	parser.add_argument("--reader_ending_index", default=-1, type=int , help="Determines Where to stop Reading PDF chunks")
	parser.add_argument("--reader_progress", default='progress.json', type=str)
	parser.add_argument("--progress_update_interval", default=3, type=int , help="Determines how to load the progress to progress.json")
	parser.add_argument("--max_pdf_size", default=-1, type=int, help="Maximum size of each PDF file size allowed. [-1 matches to any sizes] (bytes)")
	parser.add_argument("--max_output_size", default=100000000, type=int, help="Maximum size of each output file size. (bytes)")
	parser.add_argument("--chunk_size", default=5, type=int, help="Number of Sentence chunk Randomly distributed")
	parser.add_argument("--number_of_output_files", default=100, type=int, help="Maximum size of each output file size.")
	parser.add_argument("--total_parsed_data_size", default=10000000000, type=int, help="The Maximum parsed Data allowed in (bytes)")
	args = parser.parse_args()

	main(args)
