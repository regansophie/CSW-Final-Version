from pathlib import Path
import json

# This Python script searches the directories "homophonous-images" and "polysemous-images".
# It finds all the image files in these directories, and it collects the file paths in the file "image-data.json".
# Re-run this Python script every time the images are updated.

def main():
  # Collect data
  data = {
    "homophonous-words": processWordCollection("homophonous-images"),
    "polysemous-words": processWordCollection("polysemous-images"),
    "distractors": processDistractors()
  }
  
  # Print data to the file "image-data.json"
  f = open("image-data.json", "w")
  json.dump(data, f, indent=2)
   
def processWordCollection(dirName):
  # We assume that the directory has a very specific structure:
  # - It contains a collection of subdirectories, one for each word, and nothing else
  # - Each word directory contains two subdirectories, one for each meaning, and no other directories
  # - Each meaning directory contains a collection of files, each of which is either (a) a legitimate image or (b) a file with the name ".DS_Store"
  # Under these assumptions, this method returns a data structure containing all of the image file paths in this directory.
  
  p = Path(dirName)
  words = [w for w in p.iterdir() if w.parts[-1] != ".DS_Store"]
  meaningPairs = [[m for m in w.iterdir() if m.is_dir()] for w in words]
  return [[[x.as_posix() for x in m.iterdir() if x.parts[-1] != ".DS_Store"] for m in meaningPair] for meaningPair in meaningPairs]

def processDistractors():
    p = Path("distractors")
    distractor_folders = [d for d in p.iterdir() if d.is_dir() and d.name != ".DS_Store"]
    distractors = {}
    for folder in distractor_folders:
        images = [img.as_posix() for img in folder.iterdir() if img.is_file() and img.name != ".DS_Store"]
        distractors[folder.name] = images
    return distractors
  
if __name__ == "__main__":
  main()
