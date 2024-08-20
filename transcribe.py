import os
import csv
import whisper
from glob import glob
from tqdm import tqdm

# Load the Whisper model
model = whisper.load_model("large")

# Get all files in the current directory that start with "0011_" and end with ".wav"
files = glob("./data/DATA/ESD-wavs-22k/0011_*.wav")

# Prepare the data for CSV
data = []

# Process each file
for file in tqdm(files):
    # Extract the file number from the filename
    file_number = file.split("_")[1].split(".")[0]
    file_number_int = int(file_number)
    if (file_number_int > 350):
        continue
    
    # Transcribe the audio file
    result = model.transcribe(file)
    transcription = result["text"]
    
    # Add the data to our list
    data.append([file_number, transcription])

# Write the data to a CSV file
with open("transcriptions.txt", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter="|")
    writer.writerow(["File Number", "Transcription"])  # Write header
    writer.writerows(data)

print("Transcription complete. Results saved in 'transcriptions.csv'.")