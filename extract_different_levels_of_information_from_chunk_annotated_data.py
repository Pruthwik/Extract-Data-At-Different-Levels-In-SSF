"""
Extract different levels of information from chunk annotated files in SSF format.
This code works both on file and folder level.
For POS: level=0
python extract_different_levels_of_information_from_chunk_annotated_data.py --input input_folder_path --output output_folder_path --level 0
For Morph: level=1
python extract_different_levels_of_information_from_chunk_annotated_data.py --input input_folder_path --output output_folder_path --level 1
For POS+Chunk: level=2
python extract_different_levels_of_information_from_chunk_annotated_data.py --input input_folder_path --output output_folder_path --level 2
"""
from argparse import ArgumentParser
from re import findall
from re import DOTALL
import os
from re import search


def read_text_from_file(file_path):
    """Read text from a file using a file path."""
    with open(file_path, 'r', encoding='utf-8') as file_read:
        return file_read.read().strip()


def find_sentences_from_ssf_text(text):
    """Find all the sentences from text annotated in SSF format."""
    sentence_pattern = '(<Sentence id=.*?>)\n(.*?)\n(</Sentence>)'
    return findall(sentence_pattern, text, DOTALL)


def write_lines_to_file(lines, file_path):
    """Write lines to a file."""
    with open(file_path, 'w', encoding='utf-8') as file_write:
        file_write.write('\n'.join(lines))


def extract_tokens_and_other_info_level_wise(sentence_lines, level=0):
    """Extract tokens and other info in SSF sentence according to level.."""
    token_with_features_level_wise = []
    token_addr = 1
    for index, line in enumerate(sentence_lines):
        line = line.strip()
        line_split = line.split('\t')
        if level == 2 and search('^\d+\t\(\(\t[A-Z]+\t', line):
            token_with_features_level_wise.append('\t'.join(line_split[: 3]))
        if search('^\d+\.\d+\t', line):
            if len(line_split) >= 4:
                addr, token, pos, morph = line.split('\t')[: 4]
            elif len(line_split) == 3:
                addr, token, pos = line.split('\t')
                morph = ''
            else:
                print("Incorrect Annotations at Token level", line)
                return None
            if level == 0:
                extracted_info = '\t'.join([str(token_addr), token, pos])
                token_addr += 1
            elif level == 1:
                extracted_info = '\t'.join([str(token_addr), token, pos, morph])
                token_addr += 1
            else:
                extracted_info = '\t'.join([addr, token, pos])
            token_with_features_level_wise.append(extracted_info)
        if level == 2 and line == '))':
            token_with_features_level_wise.append('\t))')
    return token_with_features_level_wise


def extract_information_level_wise_for_file(file_path, level=0):
    """Extract information according to level for a file."""
    text_from_file = read_text_from_file(file_path)
    ssf_sentences = find_sentences_from_ssf_text(text_from_file)
    updated_ssf_sentences = []
    for (header, sentence_text, footer) in ssf_sentences:
        sentence_lines = sentence_text.split('\n')
        token_with_features_level_wise = extract_tokens_and_other_info_level_wise(sentence_lines, level)
        if token_with_features_level_wise is None:
            print('Error in annotation for the sentence:', sentence_text)
        else:
            updated_ssf_sentence_text = '\n'.join(token_with_features_level_wise)
            updated_ssf_sentence = '\n'.join([header, updated_ssf_sentence_text, footer])
            updated_ssf_sentences.append(updated_ssf_sentence + '\n')
    return updated_ssf_sentences


def main():
    """Pass arguments and call functions here."""
    parser = ArgumentParser()
    parser.add_argument('--input', dest='inp', help='Enter the input folder.')
    parser.add_argument('--output', dest='out', help='Enter the output folder.')
    parser.add_argument('--level', dest='lvl', help='Enter the level for extraction: 0 for POS, 1 for POS+morph', type=int, choices=[0, 1, 2], default=0)
    args = parser.parse_args()
    if not os.path.isdir(args.inp):
        updated_ssf_sentences = extract_information_level_wise_for_file(args.inp, args.lvl)
        write_lines_to_file(updated_ssf_sentences, args.out)
    else:
        if not os.path.isdir(args.out):
            os.makedirs(args.out)
        for root, dirs, files in os.walk(args.inp):
            for fl in files:
                if '-mor-pos-chunk' in fl:
                    file_name = fl[: fl.find('-mor-pos-chunk')]
                elif '-pos-chunk-mor' in fl:
                    file_name = fl[: fl.find('-pos-chunk-mor')]
                else:
                    file_name = fl[: fl.rfind('.')]
                if args.lvl == 0:
                    output_file_name = file_name + '-pos.txt'
                elif args.lvl == 1:
                    output_file_name = file_name + '-mor.txt'
                else:
                    output_file_name = file_name + '-pos-chunk.txt'
                input_path = os.path.join(root, fl)
                updated_ssf_sentences = extract_information_level_wise_for_file(input_path, args.lvl)
                output_path = os.path.join(args.out, output_file_name)
                write_lines_to_file(updated_ssf_sentences, output_path)


if __name__ == '__main__':
    main()
