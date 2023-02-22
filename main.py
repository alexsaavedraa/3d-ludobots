import os



folder_path = 'C:\\Users\\Alex\\Downloads\\snakes'  # Replace with the path to your folder

for root, dirs, files in os.walk(folder_path):
     for file in files:
          if 'body' in file:  # Only process files that contain "body" in their filename
               file_path = os.path.join(root, file)
               os.remove(file_path)


for i in range(6):
     os.system("python snakegen.py " + str(i))


for root, dirs, files in os.walk(folder_path):
     for file in files:
          if 'body' in file:  # Only process files that contain "body" in their filename
               file_path = os.path.join(root, file)
               os.remove(file_path)
