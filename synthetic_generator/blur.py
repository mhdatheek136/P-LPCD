import cv2
from PIL import Image, ImageFilter, ImageDraw
import numpy as np
import random
import os

def simulate_dust_and_noise(input_image_path, output_image_path, scale_factor=0.1, dust_density=0.02, noise_factor=0.05, blur_radius=2, particle_size=1):
    # Open the image using OpenCV
    img = cv2.imread(input_image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {input_image_path}")

    # Convert the image to RGB for compatibility with PIL
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Step 1: Resize the image to simulate low resolution (scale_factor controls the downscale)
    new_width = int(img.shape[1] * scale_factor)
    new_height = int(img.shape[0] * scale_factor)
    img_resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Step 2: Add normal noise (grainy texture)
    noise = np.random.normal(0, noise_factor * 255, img_resized.shape).astype(np.uint8)
    img_noisy = np.clip(img_resized + noise, 0, 255).astype(np.uint8)

    # Step 3: Add dust particles (random small spots) using PIL
    img_noisy_pil = Image.fromarray(img_noisy)
    draw = ImageDraw.Draw(img_noisy_pil)
    num_dust_particles = int(dust_density * img_noisy_pil.width * img_noisy_pil.height)

    for _ in range(num_dust_particles):
        # Random position for dust spot
        x = random.randint(0, img_noisy_pil.width - 1)
        y = random.randint(0, img_noisy_pil.height - 1)

        # Random radius and intensity for the dust particle
        radius = random.randint(1, particle_size)  # Dust particle size
        intensity = random.randint(50, 150)  # Intensity of dust (light grayish)

        # Draw dust spots as circles
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=(intensity, intensity, intensity), outline=None)

    # Step 4: Apply Gaussian blur to the image and dust spots
    img_blurred = img_noisy_pil.filter(ImageFilter.GaussianBlur(blur_radius))

    # Step 5: Resize to 416 pixels width while maintaining aspect ratio using OpenCV
    img_blurred_cv = np.array(img_blurred)
    img_blurred_cv = cv2.cvtColor(img_blurred_cv, cv2.COLOR_RGB2BGR)  # Convert back to BGR for OpenCV
    aspect_ratio = img_blurred_cv.shape[0] / img_blurred_cv.shape[1]
    final_width = 416
    final_height = int(final_width * aspect_ratio)
    img_final = cv2.resize(img_blurred_cv, (final_width, final_height), interpolation=cv2.INTER_AREA)

    # Step 6: Save the resulting image
    cv2.imwrite(output_image_path, img_final)
    print(f"Image with dust and noise simulated saved to: {output_image_path}")

# Ensure the output directory exists
output_dir = "variations_t"
os.makedirs(output_dir, exist_ok=True)

# Input images
input_images = ["license_plate_bike_front.jpg", "license_plate_bike_back.jpg"]

# Variations
variations = [
    {"scale_factor": 0.2, "dust_density": 0.025, "noise_factor": 0.0025, "blur_radius": 1, "particle_size": 1},
]

# Generate all variations for each input image
for image_path in input_images:
    for i, params in enumerate(variations, start=1):
        output_image = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(image_path))[0]}_variation_{i}.jpg")
        simulate_dust_and_noise(
            input_image_path=image_path,
            output_image_path=output_image,
            **params
        )
