import os

# Define the directory containing the stop words files
directory = '20211030 Test Assignment/StopWords/'

# List all text files in the directory
file_list = [file for file in os.listdir(directory) if file.endswith('.txt')]

# Create a new combined stop words file
combined_file_path = 'combined_stopwords.txt'

with open(combined_file_path, 'w') as combined_file:
    for file_name in file_list:
        file_path = os.path.join(directory, file_name)
        
        # Read the content of each file and append to the combined file
        with open(file_path, 'r') as file:
            content = file.read()
            combined_file.write(content)
            combined_file.write('\n')  # Add a new line between each file's content

print(f"Combined stop words saved to '{combined_file_path}'.")
