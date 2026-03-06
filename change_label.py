# Change label number in puck datasets to 1. 0 is roomba, 1 is puck.
import os
ROOT = "Dataset/"
TRAIN_PATH = os.path.join(ROOT, "train", "labels")
VAL_PATH = os.path.join(ROOT, "valid", "labels")
TEST_PATH = os.path.join(ROOT, "test", "labels")

def change_label(dataset_path):
    for filename in os.listdir(dataset_path):
        with open(os.path.join(dataset_path, filename), 'r') as file:
            line = file.readline()
        
        with open(os.path.join(dataset_path, filename), 'w') as file:
            if line.startswith("0 "):
                file.write(line.replace("0 ", "1 ", 1))
            else:
                file.write(line)
def clear_label(dataset_path):
    for filename in os.listdir(dataset_path):
        with open(os.path.join(dataset_path, filename), 'w') as file:
            file.write("")

if __name__ == "__main__":
    clear_label(TRAIN_PATH)
    clear_label(VAL_PATH)
    clear_label(TEST_PATH)