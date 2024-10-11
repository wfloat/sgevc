import phonemize
import os

data_dir = "/data/DATA/AED-wavs-22k/"
filelists_dir = "./filelists/aed/"
en_speaker_ids = range(0, 9)

dic = {}
with open("./data/DATA/AED_transcripts_en.txt", "r") as file:
    lines = file.readlines()
for i, line in enumerate(lines):
    transcript = line.strip("\n")
    dic[i] = transcript
sorted_results_dict = dict(sorted(dic.items()))

NUM_DATA = len(dic)
VAL_PCT = 0.057
TEST_PCT = 0.086
TRAIN_PCT = 0.857

num_val = int(NUM_DATA * VAL_PCT)
num_test = int(NUM_DATA * TEST_PCT)
num_train = NUM_DATA - num_val - num_test

val_range = range(0, num_val)
test_range = range(num_val, num_val + num_test)
train_range = range(num_val + num_test, NUM_DATA)

TRAIN_LABELED_1_PCT = 0.01
TRAIN_LABELED_10_PCT = 0.10
num_train_labeled_1_percent = int(num_train * TRAIN_LABELED_1_PCT)
num_train_labeled_10_percent = int(num_train * TRAIN_LABELED_10_PCT)
train_labeled_1_percent = range(
    num_val + num_test, num_val + num_test + num_train_labeled_1_percent
)
train_labeled_10_percent = range(
    num_val + num_test, num_val + num_test + num_train_labeled_10_percent
)


emotions = [
    {
        "name": "default",
        "range": [0, NUM_DATA - 1],
        "id": 0,
    },
    {
        "name": "cheerful",
        "range": [NUM_DATA, 2 * NUM_DATA - 1],
        "id": 1,
    },
    {
        "name": "sad",
        "range": [2 * NUM_DATA, 3 * NUM_DATA - 1],
        "id": 2,
    },
    {
        "name": "angry",
        "range": [3 * NUM_DATA, 4 * NUM_DATA - 1],
        "id": 3,
    },
    {
        "name": "excited",
        "range": [4 * NUM_DATA, 5 * NUM_DATA - 1],
        "id": 4,
    },
]

# unwanted_characters = {",", ".", "?", "!"}

train_all_path = os.path.join(filelists_dir, "en_audio_text_train_AED_all_fix.txt")
train_3_path = os.path.join(filelists_dir, "en_audio_text_train_AED_3_fix.txt")
train_30_path = os.path.join(filelists_dir, "en_audio_text_train_AED_30_fix.txt")
val_all_path = os.path.join(filelists_dir, "en_audio_text_val_AED_all_fix.txt")
test_all_path = os.path.join(filelists_dir, "en_audio_text_test_AED_all_fix.txt")
with open(train_all_path, "w") as train_all, open(train_3_path, "w") as train_3, open(
    train_30_path, "w"
) as train_30, open(val_all_path, "w") as val_all, open(test_all_path, "w") as test_all:
    for i in en_speaker_ids:
        offset = 0
        for emotion in emotions:
            for key, value in sorted_results_dict.items():
                key_emotion = key + offset
                if key in val_range:
                    val_all.write(
                        f"{data_dir}000{i}_{key_emotion:06d}.wav|{i}|{emotion['id']}|{value}"
                    )
                    val_all.write("\n")
                elif key in test_range:
                    test_all.write(
                        f"{data_dir}000{i}_{key_emotion:06d}.wav|{i}|{emotion['id']}|{value}"
                    )
                    test_all.write("\n")
                else:
                    train_all.write(
                        f"{data_dir}000{i}_{key_emotion:06d}.wav|{i}|{emotion['id']}|{value}"
                    )
                    train_all.write("\n")
                    if key in train_labeled_1_percent:
                        train_3.write(
                            f"{data_dir}000{i}_{key_emotion:06d}.wav|{i}|{emotion['id']}|{value}"
                        )
                        train_3.write("\n")
                    else:
                        train_3.write(
                            f"{data_dir}000{i}_{key_emotion:06d}.wav|{i}|100000|{value}"
                        )
                        train_3.write("\n")
                    if key in train_labeled_10_percent:
                        train_30.write(
                            f"{data_dir}000{i}_{key_emotion:06d}.wav|{i}|{emotion['id']}|{value}"
                        )
                        train_30.write("\n")
                    else:
                        train_30.write(
                            f"{data_dir}000{i}_{key_emotion:06d}.wav|{i}|100000|{value}"
                        )
                        train_30.write("\n")
            offset += 350


def count_non_100000_percentage(file_path):
    total_rows = 0
    non_100000_rows = 0

    with open(file_path, "r") as file:
        for line in file:
            total_rows += 1
            parts = line.strip().split("|")
            if len(parts) > 2 and parts[2] != "100000":
                non_100000_rows += 1

    if total_rows == 0:
        return 0  # To avoid division by zero

    non_100000_percentage = (non_100000_rows / total_rows) * 100
    return non_100000_percentage


# file_path = 'filelists/chinese/ch_audio_text_train_ESD_3_fix.txt'
# percentage = count_non_100000_percentage(file_path)
# print(f"Percentage of rows without 100000 in the third column: {percentage:.2f}%")
