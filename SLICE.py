import csv
import os
import gui.gui_browse_t as gui_browse
import gui.gui_enterstring_t as gui_enterstring
import pyt.paths.create_folder as create_folder
import pyt.paths.copy_file as copy_file
import pyt.paths.delete_file as delete_file
import gui.gui_menu_t as gui_menu
import copyover

verbose=True

def slice_csv(input_csv, names_txt, output_path='OUTPUT'):
    # Extract the base name from the input CSV file
    base_name = os.path.splitext(os.path.basename(input_csv))[0]

    # Read the names from the text file
    # with open(names_txt, 'r') as names_file:
    #     names = [name.strip() for name in names_file.readlines()]

    with open(names_txt, 'r') as names_file:
        names = [name.strip() for name in names_file.readlines() if not name.startswith('>')] # exclude lines starting with the character '>'

    print("input_csv", input_csv)
    # exit()

    list_of_created_files = []

    # Read the input CSV file
    with open(input_csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Assuming first row is the header

        # print("names", names)

        # print(enumerate(csv_reader))
        # exit()
        # print()

        # For each row in the CSV file, create a new CSV file with one row
        for i, row in enumerate(csv_reader):
            try:
                name = names[i]
            except IndexError:
                print(f"Index {i} is out of range for the 'names' list.")
                continue  # Skip this iteration and move to the next one

            print("number [i]", i, "names[i]:", names[i])
            output_csv_name = f"{base_name}_{names[i]}.csv"
            with open(output_path+"/"+output_csv_name, 'w', newline='') as output_csv:
                csv_writer = csv.writer(output_csv)
                csv_writer.writerow(header)
                csv_writer.writerow(row)

            print(f"Created {output_csv_name}")
            list_of_created_files.append(output_csv_name)
    
    return list_of_created_files


def trim_path(path, middle_folder="INPUT/", alternative_folder="OUTPUT/"):
    # path = "/Users/artacho/Work/Dissertation/CODE/salta/slicefeatures/INPUT/exp5b_mpipe-L/exp5_crop-L_renamedcolsS16_ts.csv"
    parts = path.split(middle_folder)
    if len(parts) > 1:
        # before_input, after_input = parts[0], middle_folder + parts[1]
        before_folder, after_folder = parts[0], middle_folder + parts[1]
        # print("Before 'INPUT/':", before_input)
        # print("After 'INPUT/':", after_input)
        print(f"Before '{middle_folder}':", before_folder)
        print(f"After '{middle_folder}':", after_folder)
    else:
        parts = path.split(alternative_folder)
        if len(parts) > 1:
            before_folder, after_folder = parts[0], alternative_folder + parts[1]
            print(f"Before '{alternative_folder}':", before_folder)
            print(f"After '{alternative_folder}':", after_folder)
        else:
            print(f"The string does not contain '{middle_folder}' or '{alternative_folder}'.")
            return None, None
    
    return before_folder, after_folder
        # print("The string does not contain 'INPUT/'.")
    
    # return before_input, after_input

def figure_out_folder_path(path, verbose=verbose):
    print("input_folder_path", path)
    # exit()

    browse_path = gui_browse.main(params_title='Browse files', 
            params_initbrowser=path,           # params_initbrowser=input_folder_path,
            params_extensions='.csv',                       # E.g. '.csv'
            # size=(40,20)
            )
    
    # exit()
    if verbose:
        print("browse_path", browse_path)
    # exit()

    before_input, after_input = trim_path(browse_path, middle_folder="INPUT/")

    if verbose:
        print("before_input", before_input)
        print("after_input", after_input)

    directory_path = os.path.dirname(after_input)

    if verbose:
        print("Directory path:", directory_path)

    return directory_path, before_input, after_input


def path_string_beginning(file_path, verbose=verbose):

    if verbose:
        print("input_csv, file_path", file_path)
    
    # exit()
    # file_path = "INPUT/exp5_crop-L_renamedcolsS16_ts.csv"
    substring = file_path.split('_')[0].split('/')[-1]

    if verbose:
        print(substring)
    
    return substring

###############################################
# Set the path to the INPUT folder
input_folder_path = 'INPUT/'
output_folder_path = 'OUTPUT'

menu_choice_options = [input_folder_path, '../prepcsv/OUTPUT/']
menu_choice_gui = gui_menu.main(menu_choice_options, 
                                'choose one of the following options', 
                                'Listbox Example')

print("menu_choice_gui:", menu_choice_gui)
# exit()

########

directory_path, before_input, after_input = figure_out_folder_path(menu_choice_gui)

print("directory_path:", directory_path)
# exit()

input_folder_path = before_input+directory_path # AAB
print("input_folder_path", input_folder_path)


# create_folder.main(entered_string, local_folder = output_folder_path)

# Initialize variables to store the paths of the files
input_csv = None
names_txt = None

print("input_folder_path:", input_folder_path)
print("before_input:", before_input)
# exit()

# Loop through each file in the INPUT directory
for file in os.listdir(input_folder_path):
    # Check if the file is a CSV file
    if file.endswith('.csv'):
        input_csv = os.path.join(input_folder_path, file)
        print(f"Found CSV file: {input_csv}")
    
    # Check if the file is a TXT file
    elif file.endswith('.txt'):
        names_txt = os.path.join(input_folder_path, file)
        print(f"Found TXT file: {names_txt}")

# Check if both files were found
if input_csv and names_txt:
    print("Both files found.")
    list_of_files = slice_csv(input_csv, names_txt, output_path=output_folder_path)
else:
    print("One or both files are missing.")

# print("input_csv", input_csv)
# exit()

suggested_string = path_string_beginning(input_csv)

if verbose:
    print("suggested_string:", suggested_string)

# exit()
entered_string = gui_enterstring.main("text_explanation", "text_enter", "text_window", 
         font = ("Arial", 16), default_text=suggested_string+"_feat_?_SLICED", 
         verbose=verbose)

create_folder.main(entered_string, local_folder = output_folder_path)

for file in list_of_files:
    relative_path = output_folder_path+'/'+file
    print(relative_path)
    copy_file.main(relative_path, output_folder_path, entered_string)

    delete_file.main(relative_path)

### Copying over files to the /INPUT folder of 'MotionSegmentation''

if verbose:
    print("relative_path", relative_path, "output_folder_path", output_folder_path, "entered_string", entered_string)

copyover.main(entered_string)