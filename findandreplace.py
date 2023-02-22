import os

folder_path = 'C:\\Users\\Alex\\Downloads\\snakes'  # Replace with the path to your folder

find_tedel = input('Enter the tedel to find: ')
replace_tedel = input('Enter the tedel to replace it with: ')

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.py'):  # Only process Python files
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                file_contents = f.read()
            file_contents = file_contents.replace(find_tedel, replace_tedel)
            with open(file_path, 'w') as f:
                f.write(file_contents)
