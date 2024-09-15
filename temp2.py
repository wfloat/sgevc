import os
import shutil

# Define emotion ranges
emotions = {
    "angry": (351, 370),
    "happy": (701, 720),
    "sad": (1051, 1070),
    "surprised": (1401, 1420)
}

# Define target directories
target_dirs = {
    "angry": "./Target/Angry",
    "happy": "./Target/Happy",
    "sad": "./Target/Sad",
    "surprised": "./Target/Surprise"
}

# Ensure directories exist
for dir_path in target_dirs.values():
    os.makedirs(dir_path, exist_ok=True)

# Process the input file
input_file = './filelists/chinese/ch_audio_text_val_ESD_all_fix.txt'  # Change this to the actual file path if needed
with open(input_file, 'r') as f:
    for line in f:
        # Split line to get the path and filename
        file_path = line.split('|')[0]
        # Extract the second number from the filename
        base_name = os.path.basename(file_path)
        file_number = int(base_name.split('_')[1].split('.')[0])

        # Determine the emotion based on the file number
        for emotion, (low, high) in emotions.items():
            if low <= file_number <= high:
                # Move or copy the file to the corresponding directory
                target_dir = target_dirs[emotion]
                target_path = os.path.join(target_dir, os.path.basename(file_path))
                
                # You can either copy or move the file. Uncomment the method you prefer.
                shutil.copy(f".{file_path}", target_path)  # Copies the file
                # shutil.move(file_path, target_path)  # Moves the file
                
                print(f"Copied {file_path} to {target_path}")
                break
