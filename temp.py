import os
import shutil
from data_utils import TextAudioSpeakerEmotionLoader
from utils import HParams
import json

# Define emotion ranges
NUM_DATA = 450

emotions = {
    "default": (0, NUM_DATA - 1),
    "cheerful": (NUM_DATA, 2 * NUM_DATA - 1),
    "sad": (2 * NUM_DATA, 3 * NUM_DATA - 1),
    "angry": (3 * NUM_DATA, 4 * NUM_DATA - 1),
    "excited": (4 * NUM_DATA, 5 * NUM_DATA - 1),
}

# Define target directories for each emotion
target_dirs = {
    "default": "./Source/Default",
    "cheerful": "./Target/Cheerful",
    "sad": "./Target/Sad",
    "angry": "./Target/Angry",
    "excited": "./Target/Excited",
}

# Ensure directories exist
for dir_path in target_dirs.values():
    os.makedirs(dir_path, exist_ok=True)


# Helper function to load HParams configuration
def get_hparams(config_path="./configs/base.json", model_name=None, init=True):
    if model_name is None:
        raise ValueError("Model name must be provided")

    model_dir = os.path.join("./logs", model_name)

    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    config_save_path = os.path.join(model_dir, "config.json")
    if init:
        with open(config_path, "r") as f:
            data = f.read()
        with open(config_save_path, "w") as f:
            f.write(data)
    else:
        with open(config_save_path, "r") as f:
            data = f.read()

    config = json.loads(data)

    hparams = HParams(**config)
    hparams.model_dir = model_dir
    return hparams


# Load hparams and dataset
hps = get_hparams(
    config_path="./configs/AED_base_en.json",
    model_name="AED_english_semi_3_gamma_1.0_alpha_0.2",
)
eval_dataset = TextAudioSpeakerEmotionLoader(hps.data.validation_files, hps.data)

# Process the input file
input_file = "./filelists/aed/en_audio_text_val_AED_all_fix.txt"  # Adjust to your actual file path if different
with open(input_file, "r") as f:
    lines = f.readlines()

# Process each line in the file
for line in lines:
    # Split line to get the path and filename
    file_path = line.split("|")[0].strip()
    # Extract the second number from the filename
    base_name = os.path.basename(file_path)
    file_number = int(base_name.split("_")[1].split(".")[0])

    # Determine the emotion based on the file number
    for emotion, (low, high) in emotions.items():
        if low <= file_number <= high:
            # Move or copy the file to the corresponding directory
            target_dir = target_dirs[emotion]
            target_path = os.path.join(target_dir, os.path.basename(file_path))

            # Copy the audio file to the target directory
            shutil.copy(f".{file_path}", target_path)

            # Generate and save the corresponding .spec file
            eval_dataset.get_audio(target_path)

            print(f"Copied {file_path} to {target_path} and generated the .spec file")
            break

print("All matching files processed successfully.")
