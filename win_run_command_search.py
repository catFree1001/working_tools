# %%
import os
import re
import colorama
from colorama import Fore, Style

FILE_NAME = "win_run_command.txt"

colorama.init()
# %%
# Get the path of the current script
script_path = os.path.abspath(__file__)

# Get the directory containing the script
script_directory = os.path.dirname(script_path)

# Construct the path to the text file
text_file_path = os.path.join(script_directory, FILE_NAME)

# %%
with open(text_file_path,"r") as file:
    r = file.read().splitlines()
    exe = [i.split("\t")[0] for i in r]
    print("commands :")
    for i in r:
        print(i)
    print("\n")

# %%
def colorful_text(word, text):
    matches = re.finditer(word, text, re.IGNORECASE)
    colored_text = ""
    prev_end = 0
    for match in matches:
        start = match.start()
        end = match.end()
        colored_text += text[prev_end:start] + f"{Fore.RED}{text[start:end]}{Style.RESET_ALL}"
        prev_end = end
    colored_text += text[prev_end:]
    return colored_text


# %%
while(True):
    word = input('If exit(), Press Enter \nfind text : ')
    word = word.strip()

    if word in exe:
        # word = word[2:] #remove "r " prefix
        print(word)
        os.system(f"start {word}")
        
    
    elif word == "":
        break
    
    else:
        for i in r:
            t = colorful_text(word,i)
            t1, *t2 = t.split("\t")
            print(t1)
            print("\t\t",*t2)
        # print("\n")
        
    
    print("\n")

# %%
