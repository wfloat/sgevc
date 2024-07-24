import zipfile
import os
import shutil
# from scipy.io.wavfile import write
import subprocess

zip_file_path = 'Emotional Speech Dataset (ESD).zip'
extracted_dir = 'Emotion Speech Dataset'
destination_dir = 'data/DATA/ESD-wavs-22k'

shutil.rmtree(destination_dir)
os.makedirs(destination_dir)

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall()

for root, dirs, files in os.walk(extracted_dir):
    for file in files:
        if file.endswith('.wav'):
            file_path = os.path.join(root, file)
            new_file_path = os.path.join(destination_dir, file)
            cmd = 'sox "' + file_path +'" -b 16 -e signed-integer -r 22050 ' + new_file_path 
            subprocess.call(cmd,shell=True)
            # write(new_file_path, 22050, audio_vc.astype(np.int16))
            # shutil.copy(file_path, destination_dir)

shutil.rmtree('__MACOSX')
shutil.rmtree('Emotion Speech Dataset')

print(f"Completed extracting and copying of .wav files to {destination_dir}.")

# import zipfile
# import os
# import shutil
# import librosa
# import soundfile
# from tqdm import tqdm

# zip_file_path = 'Emotional Speech Dataset (ESD).zip'
# extracted_dir = 'Emotion Speech Dataset'
# destination_dir = 'data/DATA/ESD-wavs-22k'

# with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#     zip_ref.extractall()

# for root, dirs, files in tqdm(os.walk(extracted_dir)):
#     for file in files:
#         if file.endswith('.wav'):
#             file_path = os.path.join(root, file)
#             audio, sr = librosa.load(file_path, sr=16000)
#             resampled_audio = librosa.resample(audio, orig_sr=sr, target_sr=22050)
#             new_file_path = os.path.join(destination_dir, file)
#             soundfile.write(new_file_path, resampled_audio, 22050)
#             # shutil.copy(file_path, destination_dir)

# shutil.rmtree('__MACOSX')
# shutil.rmtree('Emotion Speech Dataset')

# print(f"Completed extracting and copying of .wav files to {destination_dir}.")