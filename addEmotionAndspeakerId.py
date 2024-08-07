import os
file_path = os.path.join("filelists", "en_audio_text_train_ESD.txt")


with open('./en.txt', 'r') as file:
    lines = file.readlines()

i = 1
id = 10
emotion_num = 1

with open(file_path, 'w') as file:

    for line in lines:
        file.write(line[:42] + f"|{id}|{emotion_num - 1}" + line[42:])

        if i % 70 == 0:
            emotion_num += 1
        if i % 350 == 0:
            id += 1
        if emotion_num == 6:
            emotion_num = 1
        i+=1
