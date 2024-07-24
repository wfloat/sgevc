import zipfile
import os
import shutil

zip_file_path = 'Emotional Speech Dataset (ESD).zip'
extracted_dir = 'Emotion Speech Dataset'
destination_dir = 'data/DATA/ESD-wavs-22k'

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall()

for root, dirs, files in os.walk(extracted_dir):
    for file in files:
        if file.endswith('.wav'):
            file_path = os.path.join(root, file)
            shutil.copy(file_path, destination_dir)

shutil.rmtree('__MACOSX')
shutil.rmtree('Emotion Speech Dataset')

print(f"Completed extracting and copying of .wav files to {destination_dir}.")