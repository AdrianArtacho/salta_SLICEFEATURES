import csv
import os
# from gui import gui_browse


def slice_csv(input_csv, names_txt):
    # Extract the base name from the input CSV file
    base_name = os.path.splitext(os.path.basename(input_csv))[0]

    # Read the names from the text file
    with open(names_txt, 'r') as names_file:
        names = [name.strip() for name in names_file.readlines()]

    # Read the input CSV file
    with open(input_csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Assuming first row is the header

        # For each row in the CSV file, create a new CSV file with one row
        for i, row in enumerate(csv_reader):
            output_csv_name = f"{base_name}_{names[i]}.csv"
            with open("OUTPUT/"+output_csv_name, 'w', newline='') as output_csv:
                csv_writer = csv.writer(output_csv)
                csv_writer.writerow(header)
                csv_writer.writerow(row)

            print(f"Created {output_csv_name}")

# Set the path to the INPUT folder
input_folder_path = 'INPUT/'

# Initialize variables to store the paths of the files
input_csv = None
names_txt = None

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
    slice_csv(input_csv, names_txt)
else:
    print("One or both files are missing.")





# Example usage
# input_csv = "INPUT/exp5b_celloS67_ts.csv"
# names_txt = "INPUT/exp5b_celloS68.txt"
# slice_csv(input_csv, names_txt)
