# randomly samples images from other datasets, copies them to Dataset

from fileinput import filename
import os
import random
import shutil

ROOT = "RawData/TennisBall"
TRAIN_PATH = os.path.join(ROOT, "train")
VAL_PATH = os.path.join(ROOT, "valid")
TEST_PATH = os.path.join(ROOT, "test")

def get_image_label_pairs(source_dir):
    image_path = os.path.join(source_dir, "images")
    label_path = os.path.join(source_dir, "labels")

    images = sorted([f for f in os.listdir(image_path) if f.endswith('.jpg')])
    labels = sorted([f for f in os.listdir(label_path) if f.endswith('.txt')])
    all_files = list(zip(images, labels))

    return all_files

def copy_files(sampled_files, source_dir, dest_dir):
    for image_file, label_file in sampled_files:
        src_path_image = os.path.join(source_dir, "images", image_file)
        dest_path_image = os.path.join(dest_dir, "images", image_file)
        shutil.copy2(src_path_image, dest_path_image)

        src_path_label = os.path.join(source_dir, "labels", label_file)
        dest_path_label = os.path.join(dest_dir, "labels", label_file)
        shutil.copy2(src_path_label, dest_path_label)

def copy_all_files(source_dir, dest_dir):
    all_files = get_image_label_pairs(source_dir)
    copy_files(all_files, source_dir, dest_dir)

def sample_roomba_images(source_dir, dest_dir, num_samples):
    # function specifically for weird roomba dataset with
    # some roomba some background
    all_files = get_image_label_pairs(source_dir)

    # separate roombas and background
    roomba_files = []
    background_files = []

    for image_file, label_file in all_files:
        with open(os.path.join(source_dir, "labels", label_file), 'r') as file:
            line = file.readline()
            if line: 
                roomba_files.append((image_file, label_file))
            else:
                background_files.append((image_file, label_file))

    random.shuffle(roomba_files)  # Randomize the order of roomba files
    random.shuffle(background_files)  # Randomize the order of background files

    # Sample an equal number of roombas and background images
    num_roombas = num_samples // 2
    num_background = num_samples - num_roombas

    sampled_roomba_files = roomba_files[:num_roombas]
    sampled_background_files = background_files[:num_background]

    copy_files(sampled_roomba_files, source_dir, os.path.join(dest_dir, "roomba"))
    copy_files(sampled_background_files, source_dir, os.path.join(dest_dir, "background"))


def sample_images(source_dir, dest_dir, num_samples):
    all_files = get_image_label_pairs(source_dir)

   
    random.shuffle(all_files)  # Randomize the order of puck files
    sampled_puck_files = all_files[:num_samples]

    copy_files(sampled_puck_files, source_dir, dest_dir)
    


if __name__ == "__main__":

    copy_all_files(TRAIN_PATH, "Dataset/train")
    copy_all_files(VAL_PATH, "Dataset/valid")
    copy_all_files(TEST_PATH, "Dataset/test")
    