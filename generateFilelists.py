import phonemize
import os

data_dir = "/data/DATA/ESD-transcripts/"
filename = 'en.txt'
#unwanted_characters = {",", ".", "?", "!"}
dic = {}

file_path = os.path.join("", filename)


with open('./data/DATA/ESD-transcripts.txt', 'r') as file:
    lines = file.readlines()


for line in lines:
    id, transcript = line.split("|")
    res = phonemize.enPhonemes(transcript)
    #print(id, res)
    flat_res = [item for sublist in res for item in sublist]
    #filtered_res = [' '.join(char for char in item if char not in unwanted_characters) for item in flat_res]
    filtered_list = [item for item in flat_res if item]
    res_str = "".join(filtered_list)

    dic[id] = res_str

sorted_results_dict = dict(sorted(dic.items()))

i = 1
with open(file_path, 'w') as file:
    while i < 11:
        for key, value in sorted_results_dict.items():
            if (i < 10):
                file.write(data_dir + f'000{i}' + '_' + key + '.wav|' + value)
                file.write('\n')
            else:
                file.write(data_dir + f'00{i}' + '_' + key + '.wav|' + value)
                file.write('\n')
        i += 1
