import os

def print_outcome(outcome:str):
    txt_filename = 'debug_outcome.txt'
    txt_file_path = os.path.join("app", txt_filename)
    if not os.path.exists(txt_file_path):
        os.makedirs(txt_file_path)
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(outcome)
    print("Written into debug_outcome")