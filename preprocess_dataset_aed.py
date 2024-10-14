import zipfile
import os
import shutil
import subprocess

zip_file_path = "Azure Emotion Dataset (AED) v0.zip"
extracted_dir = "out"
destination_dir = "data/DATA/AED-wavs-22k"
NUM_DATA = 450
names = ["Aria", "Davis", "Guy", "Jane", "Jason", "Jenny", "Nancy", "Sara", "Tony"]
emotions = [
    {
        "name": "default",
        "shift": 0,
        "id": 0,
    },
    {
        "name": "cheerful",
        "shift": NUM_DATA,
        "id": 1,
    },
    {
        "name": "sad",
        "shift": NUM_DATA * 2,
        "id": 2,
    },
    {
        "name": "angry",
        "shift": NUM_DATA * 3,
        "id": 3,
    },
    {
        "name": "excited",
        "shift": NUM_DATA * 4,
        "id": 4,
    },
]

# if os.path.exists(destination_dir):
#     shutil.rmtree(destination_dir)
# os.makedirs(destination_dir)

# print(f"Unzipping {zip_file_path}...")
# with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
#     zip_ref.extractall()

print(
    f"Converting .wav files to 22kHz sample rate and copying them to {destination_dir}..."
)
for root, dirs, files in os.walk(extracted_dir):
    for file in files:
        if file.endswith(".wav"):
            file_path = os.path.join(root, file)
            _, name, emotion, _ = file_path.split("/")
            name_index = names.index(name)
            matching_emotion = next(
                (item for item in emotions if item["name"] == emotion), None
            )
            file_number = int(file.replace(".wav", ""))
            file_number_shifted = file_number + matching_emotion["shift"]
            new_file_path = os.path.join(
                destination_dir, f"{name_index:04d}_{file_number_shifted:06d}.wav"
            )
            cmd = (
                'sox "'
                + file_path
                + '" -b 16 -e signed-integer -r 22050 '
                + new_file_path
            )
            subprocess.call(cmd, shell=True)

print(f"Cleaning up...")
shutil.rmtree(extracted_dir)

print(f"Completed extracting and copying of .wav files to {destination_dir}.")
