import phonemize
import os

data_dir = "/data/DATA/ESD-wavs-22k/"
filelists_dir = "./filelists/english/"
en_speaker_ids = range(11, 21)
emotions = [
    {
        "name": "neutral",
        "range": [1, 350],
        "id": 0,
    },
    {
        "name": "angry",
        "range": [351, 700],
        "id": 1,
    },
    {
        "name": "happy",
        "range": [701, 1050],
        "id": 2,
    },
    {
        "name": "sad",
        "range": [1051, 1400],
        "id": 3,
    },
    {
        "name": "suprise",
        "range": [1401, 1750],
        "id": 4,
    },
]

# unwanted_characters = {",", ".", "?", "!"}
dic = {}


with open("./data/DATA/ESD_transcripts_en.txt", "r") as file:
    lines = file.readlines()


for line in lines:
    id, transcript = line.split("|")
    transcript = transcript.strip("\n")

    id = int(id)
    dic[id] = transcript

sorted_results_dict = dict(sorted(dic.items()))

train_all_path = os.path.join(filelists_dir, "en_audio_text_train_ESD_all_fix.txt")
train_3_path = os.path.join(filelists_dir, "en_audio_text_train_ESD_3_fix.txt")
train_30_path = os.path.join(filelists_dir, "en_audio_text_train_ESD_30_fix.txt")
val_all_path = os.path.join(filelists_dir, "en_audio_text_val_ESD_all_fix.txt")
test_all_path = os.path.join(filelists_dir, "en_audio_text_test_ESD_all_fix.txt")
val_range = range(1, 21)
test_range = range(21, 51)
train_labeled_1_percent = range(51, 54)
train_labeled_10_percent = range(51, 81)
with open(train_all_path, "w") as train_all, open(train_3_path, "w") as train_3, open(train_30_path, "w") as train_30, open(val_all_path, "w") as val_all, open(test_all_path, "w") as test_all:
    for i in en_speaker_ids:
        offset = 0
        for emotion in emotions:
            for key, value in sorted_results_dict.items():
                key_emotion = key + offset
                if key in val_range:
                    val_all.write(f"{data_dir}00{i}_{key_emotion:06d}.wav|{i - 1}|{emotion['id']}|{value}")
                    val_all.write("\n")
                elif key in test_range:
                    test_all.write(f"{data_dir}00{i}_{key_emotion:06d}.wav|{i - 1}|{emotion['id']}|{value}")
                    test_all.write("\n")
                else:
                    train_all.write(f"{data_dir}00{i}_{key_emotion:06d}.wav|{i - 1}|{emotion['id']}|{value}")
                    train_all.write("\n")
                    if key in train_labeled_1_percent:
                        train_3.write(f"{data_dir}00{i}_{key_emotion:06d}.wav|{i - 1}|{emotion['id']}|{value}")
                        train_3.write("\n")
                    else:
                        train_3.write(f"{data_dir}00{i}_{key_emotion:06d}.wav|{i - 1}|100000|{value}")
                        train_3.write("\n")
                    if key in train_labeled_10_percent:
                        train_30.write(f"{data_dir}00{i}_{key_emotion:06d}.wav|{i - 1}|{emotion['id']}|{value}")
                        train_30.write("\n")
                    else:
                        train_30.write(f"{data_dir}00{i}_{key_emotion:06d}.wav|{i - 1}|100000|{value}")
                        train_30.write("\n")
            offset += 350

def count_non_100000_percentage(file_path):
    total_rows = 0
    non_100000_rows = 0

    with open(file_path, 'r') as file:
        for line in file:
            total_rows += 1
            parts = line.strip().split('|')
            if len(parts) > 2 and parts[2] != '100000':
                non_100000_rows += 1

    if total_rows == 0:
        return 0  # To avoid division by zero

    non_100000_percentage = (non_100000_rows / total_rows) * 100
    return non_100000_percentage

# file_path = 'filelists/chinese/ch_audio_text_train_ESD_3_fix.txt'
# percentage = count_non_100000_percentage(file_path)
# print(f"Percentage of rows without 100000 in the third column: {percentage:.2f}%")