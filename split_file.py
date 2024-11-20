import os
import sys
import re

# AWS Premier titan can output max 3,072 tokens
# 1 token = 4.6 ch
# to play it safe I am going to decrease the max to 3000 and decrease the conversion to 1 t = 3 ch
# 3 ch * 3000 tokens = 9000 characters

def split_file(max_character_count=370):
    """
    Splits a large file into smaller files with a specified number of lines.

    :param input_file_path: The path to the input file.
    :param lines_per_file: The number of lines each smaller file should contain.
    :return: A list of output file paths where the smaller files are saved.
    """
    if len(sys.argv) < 2:
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_file.txt')
        # print("Error: No file path provided.")
        # sys.exit(1)  # Exit if no argument is provided
    else:
        # The first argument passed after the script name is the file path
        input_file = sys.argv[1]
    
    output_file_names = []
    file_counter = 1
    code_blocks = []
    char_counter = 0
    in_block = False
    block = ""
    output_file_code = [] # ^END\s?([A-Za-z]+)?[^(LOOP)|(IF)];$
    
    # begin_regex = re.compile(r'^\s*(BEGIN)', re.IGNORECASE)
    # procedure_regex = re.compile(r'^\s*(PROCEDURE)', re.IGNORECASE)
    # function_regex = re.compile(r'^\s*(FUNCTION)', re.IGNORECASE)
    
    block_start_pattern = re.compile(r'^\s*(BEGIN|PROCEDURE|FUNCTION|PACKAGE|DROP|CREATE|REPLACE|WRT)', re.IGNORECASE)
    # block_end_pattern = re.compile(r'^END\s?([A-Za-z]+)?[^(LOOP)|(IF)];$')
    block_end_pattern = re.compile(r'^\/$|^END(?!(\sLOOP|\sIF|\;|\sCASE|\sKingAdj|\sPieceAdjust|\sSetP|\sInitialize)).*$')
    # Open the large PL/SQL file and read its contents
    with open(input_file, 'r', encoding='iso-8859-1', errors='ignore') as infile:
        lines = infile.readlines()

    print("Number of lines " + str(len(lines)))
    # Loop through the lines of the file to process them
    for idx, line in enumerate(lines):
        # print(line)
        print(block_start_pattern.match(line))
        if block_start_pattern.match(line):
            in_block = True
        
        if in_block:
            block += line
        
        if block_end_pattern.match(line):
            print("Entered Block End Pattern Statement")
            in_block = False # set in block variable back to false
            code_blocks.append(block) # append current block to file list
            block = "" # reset block string
    
    for block in code_blocks:
        # if we are not in the middle of a block and the next block of code makes our character count more than our limit
        if len(block) + char_counter > max_character_count:
            print("\nInside write to file")
            # write to the file and do not include the current line
            output_file_path = os.path.join('.', f"{os.path.basename(input_file)}_part_{file_counter}.txt")
            with open(output_file_path, 'w', encoding='iso-8859-1') as outfile:
                outfile.writelines(output_file_code)
            output_file_names.append(output_file_path)
            file_counter += 1
            output_file_code = [] # reset the file output code
            char_counter = 0 # reset the character counter
        
        output_file_code.append(block)
        char_counter += len(block)
    
    # if we have looped through all of the lines but there are unwritten lines left in the list
    if len(output_file_code) != 0:
        output_file_path = os.path.join('.', f"{os.path.basename(input_file)}_part_{file_counter}.txt")
        with open(output_file_path, 'w', encoding='iso-8859-1') as outfile:
            outfile.writelines(output_file_code)
        output_file_names.append(output_file_path)    

    print("output_files: ", output_file_names)
    return output_file_names

if __name__ == "__main__":
    split_file()
