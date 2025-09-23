import cv2
import numpy as np
import os
import glob
import random

def apply_random_motion_blur(image):
    """
    Apply random motion blur to an image (kernel size 0-30) while preserving content positions
    
    Args:
        image: Input image (numpy array)
    
    Returns:
        Blurred image (numpy array)
    """
    # Random kernel size between 1-29 (odd number), with 10% chance of no blur
    if random.random() < 0.5:
        return image  # 50% chance to keep original (kernel_size = 0 equivalent)
    
    kernel_size = random.choice(range(1, 30, 2))  # Odd numbers between 1-29
    
    # Random direction (horizontal or vertical - diagonal might distort characters)
    direction = random.choice(['horizontal', 'vertical'])
    
    # Create motion blur kernel
    kernel = np.zeros((kernel_size, kernel_size))
    center = kernel_size // 2
    
    if direction == 'horizontal':
        kernel[center, :] = np.ones(kernel_size)  # Horizontal line
    else:  # vertical
        kernel[:, center] = np.ones(kernel_size)  # Vertical line
    
    # Normalize kernel
    kernel /= kernel.sum()
    
    # Apply convolution
    return cv2.filter2D(image, -1, kernel)

# Paths setup
input_base_dir = r"E:\syn_data\Image_Generation\images_aug"
output_base_dir = r"E:\syn_data\Image_Generation\images_aug_blurred"  # New folder for blurred images

# Create output directory structure
os.makedirs(output_base_dir, exist_ok=True)
for folder in ['train', 'val']:
    os.makedirs(os.path.join(output_base_dir, folder), exist_ok=True)

# Process each subfolder
for folder in ['train', 'val']:
    input_folder = os.path.join(input_base_dir, folder)
    output_folder = os.path.join(output_base_dir, folder)
    
    # Get all images in current folder
    image_paths = glob.glob(os.path.join(input_folder, "*.jpg"))
    
    print(f"Processing {len(image_paths)} images in {folder} folder...")
    
    for image_path in image_paths:
        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            print(f"Warning: Could not read image {image_path}")
            continue
        
        # Apply random motion blur
        blurred_img = apply_random_motion_blur(img)
        
        # Save with same filename to maintain label correspondence
        output_path = os.path.join(output_folder, os.path.basename(image_path))
        cv2.imwrite(output_path, blurred_img)
        
    print(f"Finished processing {folder} folder")

print("\nSubtle motion blur augmentation complete!")