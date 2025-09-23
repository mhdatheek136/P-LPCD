import os
import shutil
import random
from aug_noise import simulate_dust_and_noise_pillow, simulate_dust_and_noise_cv2

# Folder paths
image_base_dir = r"E:\syn_data\Image_Generation\images"
label_base_dir = r"E:\syn_data\Image_Generation\labels"
augmented_image_dir = r"E:\syn_data\Image_Generation\images_aug"
augmented_label_dir = r"E:\syn_data\Image_Generation\labels_aug"

# Ensure the output directories exist
os.makedirs(augmented_image_dir, exist_ok=True)
os.makedirs(augmented_label_dir, exist_ok=True)

# Subfolders for train, val, and test
subfolders = ['train', 'val']

# Variations - combine both sets
combined_variations = [
    {"type": "pillow", "params": {"scale_factor": 0.1, "dust_density": 0.002, "noise_factor": 0.002, "blur_radius": 1, "particle_size": 1}},
    {"type": "pillow", "params": {"scale_factor": 0.1, "dust_density": 0.001, "noise_factor": 0.001, "blur_radius": 1, "particle_size": 1}},
    {"type": "pillow", "params": {"scale_factor": 0.13, "dust_density": 0.0025, "noise_factor": 0.002, "blur_radius": 1, "particle_size": 2}},
    {"type": "pillow", "params": {"scale_factor": 0.15, "dust_density": 0.0025, "noise_factor": 0.002, "blur_radius": 1, "particle_size": 2}},
    {"type": "pillow", "params": {"scale_factor": 0.2, "dust_density": 0.0025, "noise_factor": 0.0025, "blur_radius": 1, "particle_size": 3}},
    {"type": "pillow", "params": {"scale_factor": 0.3, "dust_density": 0.0025, "noise_factor": 0.0025, "blur_radius": 1, "particle_size": 3}},
    {"type": "pillow", "params": {"scale_factor": 0.4, "dust_density": 0.0025, "noise_factor": 0.0035, "blur_radius": 1, "particle_size": 5}},
    {"type": "pillow", "params": {"scale_factor": 0.5, "dust_density": 0.0035, "noise_factor": 0.0035, "blur_radius": 1, "particle_size": 6}},
    {"type": "pillow", "params": {"scale_factor": 0.8, "dust_density": 0.0035, "noise_factor": 0.0045, "blur_radius": 3, "particle_size": 6}},
    {"type": "pillow", "params": {"scale_factor": 1, "dust_density": 0.001, "noise_factor": 0.001, "blur_radius": 3, "particle_size": 6}},
    {"type": "pillow", "params": {"scale_factor": 1, "dust_density": 0.005, "noise_factor": 0.005, "blur_radius": 2, "particle_size": 6}},
    {"type": "pillow", "params": {"scale_factor": 1, "dust_density": 0.0001, "noise_factor": 0.002, "blur_radius": 2, "particle_size": 6}},
    {"type": "cv2", "params": {"scale_factor": 0.12, "dust_density": 0.002, "noise_factor": 0.002, "blur_radius": 1, "particle_size": 1}},
    {"type": "cv2", "params": {"scale_factor": 0.12, "dust_density": 0.001, "noise_factor": 0.001, "blur_radius": 1, "particle_size": 1}},
    {"type": "cv2", "params": {"scale_factor": 0.1, "dust_density": 0.0025, "noise_factor": 0.002, "blur_radius": 0.7, "particle_size": 1}},
    {"type": "cv2", "params": {"scale_factor": 0.12, "dust_density": 0.02, "noise_factor": 0.001, "blur_radius": 1, "particle_size": 1}},
    {"type": "cv2", "params": {"scale_factor": 0.135, "dust_density": 0.025, "noise_factor": 0.0025, "blur_radius": 1, "particle_size": 1}},
    {"type": "cv2", "params": {"scale_factor": 0.2, "dust_density": 0.025, "noise_factor": 0.0025, "blur_radius": 1, "particle_size": 1}},
]

def apply_single_variation_per_image():
    """Apply exactly one random variation per original image"""
    for subfolder in subfolders:
        # Paths for the current subfolder
        image_dir = os.path.join(image_base_dir, subfolder)
        label_dir = os.path.join(label_base_dir, subfolder)

        augmented_image_subfolder = os.path.join(augmented_image_dir, subfolder)
        augmented_label_subfolder = os.path.join(augmented_label_dir, subfolder)

        os.makedirs(augmented_image_subfolder, exist_ok=True)
        os.makedirs(augmented_label_subfolder, exist_ok=True)

        # Get the total number of images in the subfolder
        images = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
        total_images = len(images)
        print(f"Processing {total_images} images in {subfolder}...")

        # Loop through all the images in the subfolder
        for idx, image_file in enumerate(images, start=1):
            base_name = os.path.splitext(image_file)[0]  # Get base name
            
            # Path for the corresponding label file
            label_file = os.path.join(label_dir, f"{base_name}.txt")
            
            if not os.path.exists(label_file):
                print(f"Warning: Missing label for {image_file}")
                continue

            # Select a RANDOM variation for this image
            variation = random.choice(combined_variations)
            
            # Generate new filenames (keep original name since we're replacing)
            new_image_name = f"{base_name}.jpg"
            new_label_name = f"{base_name}.txt"
            
            # Apply the selected variation
            if variation["type"] == "pillow":
                simulate_dust_and_noise_pillow(
                    input_image_path=os.path.join(image_dir, image_file),
                    output_image_path=os.path.join(augmented_image_subfolder, new_image_name),
                    **variation["params"]
                )
            else:  # cv2
                simulate_dust_and_noise_cv2(
                    input_image_path=os.path.join(image_dir, image_file),
                    output_image_path=os.path.join(augmented_image_subfolder, new_image_name),
                    **variation["params"]
                )
            
            # Copy the label to the augmented label directory (unchanged)
            new_label_path = os.path.join(augmented_label_subfolder, new_label_name)
            shutil.copy(label_file, new_label_path)

            # Display progress
            if idx % 100 == 0 or idx == total_images:
                print(f"[{idx}/{total_images}] Processed image: {image_file}")

        print(f"Completed processing {subfolder}.\n")

# Run the function
apply_single_variation_per_image()