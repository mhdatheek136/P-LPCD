import random
import os
import string
import shutil

# Existing structure
base_dir = 'images_old'
label_dir = 'labels_old'
for folder in ['train', 'val']:
    os.makedirs(f'{base_dir}/{folder}', exist_ok=True)
    os.makedirs(f'{label_dir}/{folder}', exist_ok=True)

# New folders (without subdirectories)
os.makedirs('images', exist_ok=True)
os.makedirs('labels', exist_ok=True)

# Functions to generate license plates (assuming these are imported)
from label_img import create_license_plate_bike_front, create_license_plate_bike_back

# Helper function to randomly generate letters and digits
def random_string(length, char_set):
    return ''.join(random.choices(char_set, k=length))

# Function to generate the front and back license plates with random and balanced distribution
def generate_license_plates(num_front, num_back):
    front_count = 1
    back_count = 1

    # Character sets for generating license plate components
    letters = string.ascii_uppercase  # 'A' to 'Z'
    digits = string.digits  # '0' to '9'
    city = "PUNJAB"

    # Create a list to store image and label paths
    front_images = []
    back_images = []

    # Generate 5000 front plates
    for i in range(num_front):
        # Format the image and label number with leading zeros
        count_str = f"{front_count:06d}"

        # Randomly generate ler_text (3 letters)
        ler_text = random_string(3, letters)

        # 50% probability for 3-digit, 50% for 4-digit
        number_length = random.choices([3, 4], weights=[1, 1])[0]
        number_text = random_string(number_length, digits)

        # Randomly generate manufacture year (2 digits)
        manufacture_year = random_string(2, digits)

        # Randomly generate single_text (50% chance of letter or space)
        single_text = random.choice([random.choice(letters), " "])

        # Generate the front plate and corresponding label
        label_file = f"labels/lp_front_{count_str}.txt"
        output_file = f"images/lp_front_{count_str}.jpg"
        create_license_plate_bike_front(
            ler_text=ler_text, number_text=number_text, city_text=city, 
            manufacture_year=manufacture_year, single_text=single_text, 
            label_file=label_file, 
            output_file=output_file
        )

        # Add front plate to list
        front_images.append((label_file, output_file))
        front_count += 1

    # Generate 5000 back plates
    for i in range(num_back):
        # Format the image and label number with leading zeros
        count_str = f"{back_count:06d}"

        # Randomly generate ler_text (3 letters)
        ler_text = random_string(3, letters)

        # 50% probability for 3-digit, 50% for 4-digit
        number_length = random.choices([3, 4], weights=[1, 1])[0]
        number_text = random_string(number_length, digits)


        # Randomly generate manufacture year (2 digits)
        manufacture_year = random_string(2, digits)

        # Randomly generate single_text (50% chance of letter or space)
        single_text = random.choice([random.choice(letters), " "])

        # Generate the back plate and corresponding label
        label_file = f"labels/lp_back_{count_str}.txt"
        output_file = f"images/lp_back_{count_str}.jpg"
        create_license_plate_bike_back(
            ler_text=ler_text, number_text=number_text, city_text=city, 
            manufacture_year=manufacture_year, single_text=single_text, 
            label_file=label_file, 
            output_file=output_file
        )

        # Add back plate to list
        back_images.append((label_file, output_file))
        back_count += 1

    # Combine the front and back plate lists
    all_images = front_images + back_images

    # Shuffle the combined list
    random.shuffle(all_images)

    # Split into train (70%), val (15%), test (15%)
    total_images = len(all_images)
    train_size = int(0.8 * total_images)
    val_size = int(0.20 * total_images)
    test_size = total_images - train_size - val_size

    # Function to move files to respective directories
    def move_files(file_list, folder_name):
        for label_file, img_file in file_list:
            # Move image file
            shutil.move(img_file, f'{base_dir}/{folder_name}/{os.path.basename(img_file)}')
            # Move label file
            shutil.move(label_file, f'{label_dir}/{folder_name}/{os.path.basename(label_file)}')

    # Move the files into their respective folders
    move_files(all_images[:train_size], 'train')
    move_files(all_images[train_size:train_size + val_size], 'val')
    move_files(all_images[train_size + val_size:], 'test')

    print(f"Generated {num_front} front plates and {num_back} back plates.")
    print(f"Files moved to train (70%), val (15%), test (15%).")

# Call the function to generate 5000 front and 5000 back plates
generate_license_plates(10000, 10000)
