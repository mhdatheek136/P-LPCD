from PIL import Image, ImageFilter, ImageDraw
import numpy as np
import random
import os
import cv2

def simulate_dust_and_noise_pillow(input_image_path, output_image_path, scale_factor=0.1, dust_density=0.02, noise_factor=0.05, blur_radius=1, particle_size=1):
    # Open the image
    with Image.open(input_image_path) as img:
        # Step 1: Resize the image to simulate low resolution (scale_factor controls the downscale)
        new_width = int(img.width * scale_factor)
        new_height = int(img.height * scale_factor)
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Step 2: Add normal noise (grainy texture)
        img_array = np.array(img_resized)
        noise = np.random.normal(0, noise_factor * 255, img_array.shape).astype(np.uint8)
        img_array = np.clip(img_array + noise, 0, 255)  # Add noise and clip to valid range
        img_noisy = Image.fromarray(img_array)

        # Step 3: Add dust particles (random small spots)
        draw = ImageDraw.Draw(img_noisy)

        num_dust_particles = int(dust_density * img_noisy.width * img_noisy.height)

        for _ in range(num_dust_particles):
            # Random position for dust spot
            x = random.randint(0, img_noisy.width - 1)
            y = random.randint(0, img_noisy.height - 1)

            # Random radius and intensity for the dust particle
            radius = random.randint(1, particle_size)  # Dust particle size
            intensity = random.randint(50, 150)  # Intensity of dust (light grayish)

            # Draw dust spots as circles
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=(intensity, intensity, intensity), outline=None)

        # Step 4: Apply Gaussian blur to the image and dust spots
        img_blurred = img_noisy.filter(ImageFilter.GaussianBlur(blur_radius))

        # Step 5: Resize to 416 pixels width while maintaining aspect ratio
        aspect_ratio = img_blurred.height / img_blurred.width
        final_width = 416
        final_height = int(final_width * aspect_ratio)
        img_final = img_blurred.resize((final_width, final_height), Image.Resampling.LANCZOS)

        # Step 6: Save the resulting image with dust and noise
        img_final.save(output_image_path)
        print(f"Image with dust and noise simulated saved to: {output_image_path}")

def simulate_dust_and_noise_cv2(input_image_path, output_image_path, scale_factor=0.1, dust_density=0.02, noise_factor=0.05, blur_radius=1, particle_size=1):
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

    # Step 6: Save the resulting image with dust and noise
    cv2.imwrite(output_image_path, img_final)
    print(f"Image with dust and noise simulated saved to: {output_image_path}")

# Ensure the output directory exists
output_dir = "variations"
os.makedirs(output_dir, exist_ok=True)

# Input image paths
# input_image_front = 'license_plate_bike_front.jpg'
# input_image_back = 'license_plate_bike_back.jpg'

# Variations
variations_pillow = [
    {"scale_factor": 0.1, "dust_density": 0.002, "noise_factor": 0.002, "blur_radius": 1, "particle_size": 1},
    {"scale_factor": 0.1, "dust_density": 0.001, "noise_factor": 0.001, "blur_radius": 1, "particle_size": 1},
    {"scale_factor": 0.13, "dust_density": 0.0025, "noise_factor": 0.002, "blur_radius": 1, "particle_size": 2},
    {"scale_factor": 0.15, "dust_density": 0.0025, "noise_factor": 0.002, "blur_radius": 1, "particle_size": 2},
    {"scale_factor": 0.2, "dust_density": 0.0025, "noise_factor": 0.0025, "blur_radius": 1, "particle_size": 3},
    {"scale_factor": 0.3, "dust_density": 0.0025, "noise_factor": 0.0025, "blur_radius": 1, "particle_size": 3},
    {"scale_factor": 0.4, "dust_density": 0.0025, "noise_factor": 0.0035, "blur_radius": 1, "particle_size": 5},
    {"scale_factor": 0.5, "dust_density": 0.0035, "noise_factor": 0.0035, "blur_radius": 1, "particle_size": 6},
    {"scale_factor": 0.8, "dust_density": 0.0035, "noise_factor": 0.0045, "blur_radius": 3, "particle_size": 6},
    {"scale_factor": 1, "dust_density": 0.001, "noise_factor": 0.001, "blur_radius": 3, "particle_size": 6},
    {"scale_factor": 1, "dust_density": 0.005, "noise_factor": 0.005, "blur_radius": 2, "particle_size": 6},
    {"scale_factor": 1, "dust_density": 0.0001, "noise_factor": 0.002, "blur_radius": 2, "particle_size": 6},
]

# Variations
variations_cv2 = [
    {"scale_factor": 0.12, "dust_density": 0.002, "noise_factor": 0.002, "blur_radius": 1, "particle_size": 1},
    {"scale_factor": 0.12, "dust_density": 0.001, "noise_factor": 0.001, "blur_radius": 1, "particle_size": 1},
    {"scale_factor": 0.1, "dust_density": 0.0025, "noise_factor": 0.002, "blur_radius": 0.7, "particle_size": 1},
    {"scale_factor": 0.12, "dust_density": 0.02, "noise_factor": 0.001, "blur_radius": 1, "particle_size": 1},
    {"scale_factor": 0.135, "dust_density": 0.025, "noise_factor": 0.0025, "blur_radius": 1, "particle_size": 1},
    {"scale_factor": 0.2, "dust_density": 0.025, "noise_factor": 0.0025, "blur_radius": 1, "particle_size": 1},
]

# # Generate all variations for both front and back images using Pillow
# for i, params in enumerate(variations_pillow, start=1):
#     output_image_front = os.path.join(output_dir, f"variation_front_{i}.jpg")
#     output_image_back = os.path.join(output_dir, f"variation_back_{i}.jpg")

#     # Apply variations to the front image using Pillow
#     simulate_dust_and_noise_pillow(
#         input_image_path=input_image_front,
#         output_image_path=output_image_front,
#         **params
#     )

#     # Apply variations to the back image using Pillow
#     simulate_dust_and_noise_pillow(
#         input_image_path=input_image_back,
#         output_image_path=output_image_back,
#         **params
#     )

# # Generate all variations for both front and back images using OpenCV
# for i, params in enumerate(variations_cv2, start=i):
#     output_image_front = os.path.join(output_dir, f"variation_front_{i}.jpg")
#     output_image_back = os.path.join(output_dir, f"variation_back_{i}.jpg")

#     # Apply variations to the front image using OpenCV
#     simulate_dust_and_noise_cv2(
#         input_image_path=input_image_front,
#         output_image_path=output_image_front,
#         **params
#     )

#     # Apply variations to the back image using OpenCV
#     simulate_dust_and_noise_cv2(
#         input_image_path=input_image_back,
#         output_image_path=output_image_back,
#         **params
#     )
