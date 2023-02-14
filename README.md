# Extract-Data-At-Different-Levels
## Extract different levels of information from chunk annotated files in SSF format.
This code works both on file and folder level.
## For POS: level=0
python extract_different_levels_of_information_from_chunk_annotated_data.py --input input_folder_path --output output_folder_path --level 0
## For Morph: level=1
python extract_different_levels_of_information_from_chunk_annotated_data.py --input input_folder_path --output output_folder_path --level 1
## For POS+Chunk: level=2
python extract_different_levels_of_information_from_chunk_annotated_data.py --input input_folder_path --output output_folder_path --level 2

