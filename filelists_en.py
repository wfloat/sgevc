import phonemize
import os

data_dir = "/data/DATA/ESD-wavs-22k/"
filelists_dir = "/filelists/"
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


with open("./data/DATA/ESD-transcripts.txt", "r") as file:
    lines = file.readlines()


for line in lines:
    id, transcript = line.split("|")
    transcript = transcript.strip("\n")
    res = phonemize.enPhonemes(transcript)
    # print(id, res)
    flat_res = [item for sublist in res for item in sublist]
    # filtered_res = [' '.join(char for char in item if char not in unwanted_characters) for item in flat_res]
    filtered_list = [item for item in flat_res if item]
    res_str = "".join(filtered_list)

    id = int(id)
    dic[id] = res_str

sorted_results_dict = dict(sorted(dic.items()))

train_all_path = os.path.join(filelists_dir, "en_audio_text_train_ESD_all_fix.txt")
train_3_path = os.path.join(filelists_dir, "en_audio_text_train_ESD_3_fix.txt")
train_30_path = os.path.join(filelists_dir, "en_audio_text_train_ESD_30_fix.txt")
val_all_path = os.path.join(filelists_dir, "en_audio_text_val_ESD_all_fix.txt")
test_all_path = os.path.join(filelists_dir, "en_audio_text_test_ESD_all_fix.txt")
with open(train_all_path, "w") as train_all, open(train_3_path, "w") as train_3, open(train_30_path, "w") as train_30, open(val_all_path, "w") as val_all, open(test_all_path, "w") as test_all:
    for i in en_speaker_ids:
        offset = 0
        for emotion in emotions:
            for key, value in sorted_results_dict.items():
                key_emotion = key + offset
                file.write(f"{data_dir}00{i}_{key_emotion:06d}.wav|{i - 1}|{emotion['id']}|{value}")
                file.write("\n")
            offset += 350
