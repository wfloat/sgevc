import zipfile
import os
import shutil
import subprocess

zip_file_path = 'Emotional Speech Dataset (ESD).zip'
extracted_dir = 'Emotion Speech Dataset'
destination_dir = 'data/DATA/ESD-wavs-22k'

shutil.rmtree(destination_dir)
os.makedirs(destination_dir)

print(f"Unzipping {zip_file_path}...")
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall()

print(f"Converting .wav files to 22kHz sample rate and copying them to {destination_dir}...")
for root, dirs, files in os.walk(extracted_dir):
    for file in files:
        if file.endswith('.wav'):
            file_path = os.path.join(root, file)
            new_file_path = os.path.join(destination_dir, file)
            cmd = 'sox "' + file_path +'" -b 16 -e signed-integer -r 22050 ' + new_file_path
            subprocess.call(cmd,shell=True)

print(f"Cleaning up...")
shutil.rmtree('__MACOSX')
shutil.rmtree(extracted_dir)

print(f"Completed extracting and copying of .wav files to {destination_dir}.")
