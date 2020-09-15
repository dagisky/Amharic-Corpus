
from utils.pdfUtils import *


tika.initVM()

def main(args):
	if args.extract_pdf:
		"""Extract PDF from all PDF files under the root Directory"""



if __name__ == "__main__":
        parser = argparse.ArgumentParser()      
        
        parser.add_argument("--extract_pdf", action='store_true', help="Whether to run training.")
        parser.add_argument("--root_dir", default=None, type=str)
        parser.add_argument("--output_dir", default='data', type=str)
        parser.add_argument("--text_split_param", default='sentence', type=str, help="Determines how we split the text [sentence|paragraph]")
        parser.add_argument("--reader_starting_index", default=10, type=int , help="Determines Where to start Reading PDF chunks")
        parser.add_argument("--reader_ending_index", default=-10, type=int , help="Determines Where to stop Reading PDF chunks")
        parser.add_argument("--reader_progress", default='progress.json', type=str)
        parser.add_argument("--max_pdf_size", default=10, type=int, help="Maximum size of each PDF file size allowed. (MB)")
        parser.add_argument("--max_output_size", default=100, type=int, help="Maximum size of each output file size. (MB)")
        parser.add_argument("--sentence_chunk_size", default=10, type=int, help="Number of Sentence chunk Randomly distributed")
        parser.add_argument("--number_of_output_files", default=100, type=int, help="Maximum size of each output file size.")
        parser.add_argument("--total_parsed_data_size", default=100000, type=int, help="The Maximum parsed Data allowed in (MB)")
        args = parser.parse_args()

        main(args)
