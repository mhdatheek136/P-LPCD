from PIL import Image, ImageDraw, ImageFont

# Mapping of characters to class numbers starting from 0
CHARACTER_CLASSES = {
    **{chr(i): i - 65 for i in range(65, 91)},  # A-Z -> 0-25
    **{str(i): i + 26 for i in range(0, 10)},   # 0-9 -> 26-35
}

def create_license_plate_bike_front(ler_text="LER", number_text="1234", city_text="PUNJAB", manufacture_year="20", single_text="A", label_file="label_bike_front.txt", output_file="license_plate_bike_front.jpg"):
    # Load the Eurostile font (replace with Sauerkrauto.ttf if necessary)
    eurostile_large = ImageFont.truetype("Sauerkrauto.ttf", 200)  # For "LER" and "1234"
    eurostile_medium = ImageFont.truetype("Sauerkrauto.ttf", 100)  # For "20"
    eurostile_small = ImageFont.truetype("Sauerkrauto.ttf", 75)  # For "20"
    punjab_font = ImageFont.truetype("arial.ttf", 25)  # For "PUNJAB"
    
    # Create a blank white image (outside the border)
    width, height = 1010, 185
    plate = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(plate)

    # List to store YOLO labels
    yolo_labels = []

    # Draw the green strip with padding of 5 pixels (white space before the green)
    green_color = (0, 177, 91)
    green_strip_width = 140
    horizontal_padding = 8  # Padding between green strip and the rest of the plate
    vertical_padding = 10  # Padding from the top and bottom
    draw.rectangle([horizontal_padding, vertical_padding, green_strip_width + horizontal_padding, height - vertical_padding], fill=green_color)

    # Add text for the city (default "PUNJAB")
    draw.text((30, 140), city_text, fill="black", font=punjab_font)

    # Add flower image (wheat graphic) while maintaining the aspect ratio
    flower_image = Image.open("flower.png")  # Replace with your file path
    flower_width, flower_height = flower_image.size

    # Resize the image while maintaining the aspect ratio
    flower_image = flower_image.resize((120, 120))

    # Paste the flower image onto the license plate
    plate.paste(flower_image, (20, 20), flower_image)  # Position the image on the plate

    # Add "LER-" (default "LER" with the hyphen) in the image, but skip in YOLO labels
    ler_text_with_hyphen = ler_text   # Ensure "LER-" always appears
    x_pos = 155
    for char in ler_text_with_hyphen:
        
        # Draw the character on the image
        draw.text((x_pos, -45), char, fill="black", font=eurostile_large)
        
        # Get the class ID based on the character
        class_id = CHARACTER_CLASSES.get(char.upper(), 0)  # Use uppercase for class mapping
        
        # Get bounding box of the character
        char_bbox = draw.textbbox((x_pos, -45), char, font=eurostile_large)
        # Normalize the bounding box coordinates and dimensions for YOLO
        x_center = (char_bbox[0] + char_bbox[2]) / 2 / width
        y_center = (char_bbox[1] + char_bbox[3]) / 2 / height
        char_width = 1.0 * (char_bbox[2] - char_bbox[0]) / width
        char_height = 1.05 * (char_bbox[3] - char_bbox[1]) / height
        
        # Store the YOLO label with class ID
        yolo_labels.append(f"{class_id} {x_center} {y_center} {char_width} {char_height}")
        
        x_pos += eurostile_large.getlength(char)  # Adjust -8 for tighter spacing

    # Add the manufacture year (e.g., "20") with correct class mapping
    x_pos = 900 # Position for the manufacture year "20"
    for char in manufacture_year:
        draw.text((x_pos, -5), char, fill="black", font=eurostile_small)
        # Get the class ID based on the character
        class_id = CHARACTER_CLASSES.get(char, 0)  # Use the character's class ID
        
        # Get bounding box for the year text
        year_bbox = draw.textbbox((x_pos, -5), char, font=eurostile_small)
        # Normalize the bounding box for YOLO
        x_center = (year_bbox[0] + year_bbox[2]) / 2 / width
        y_center = (year_bbox[1] + year_bbox[3]) / 2 / height
        char_width = 1.0 * (year_bbox[2] - year_bbox[0]) / width
        char_height = 1.05 * (year_bbox[3] - year_bbox[1]) / height
        yolo_labels.append(f"{class_id} {x_center} {y_center} {char_width} {char_height}")
        
        x_pos += eurostile_small.getlength(char)  # Adjust -8 for tighter spacing

    # Add the customizable number text (default "1234")
    x_pos = 480
    for char in number_text:
        draw.text((x_pos, -45), char, fill="black", font=eurostile_large)
        # Get bounding box for the number
        num_bbox = draw.textbbox((x_pos, -45), char, font=eurostile_large)
        # Normalize the bounding box for YOLO
        x_center = (num_bbox[0] + num_bbox[2]) / 2 / width
        y_center = (num_bbox[1] + num_bbox[3]) / 2 / height
        num_width = 1.0 * (num_bbox[2] - num_bbox[0]) / width
        num_height = 1.05 * (num_bbox[3] - num_bbox[1]) / height
        yolo_labels.append(f"{CHARACTER_CLASSES[char]} {x_center} {y_center} {num_width} {num_height}")
        
        x_pos += eurostile_large.getlength(char) # Adjust -8 for tighter spacing

    # Add the single text (e.g., "A") with correct class mapping
    x_pos = 920 # Position for the single text "A"
    for char in single_text:
        if char != " ":  # Skip if the character is a space
            draw.text((x_pos, 60), char, fill="black", font=eurostile_medium)
            # Get the class ID based on the character
            class_id = CHARACTER_CLASSES.get(char, 0)  # Use the character's class ID
            
            # Get bounding box for the year text
            year_bbox = draw.textbbox((x_pos, 60), char, font=eurostile_medium)
            # Normalize the bounding box for YOLO
            x_center = (year_bbox[0] + year_bbox[2]) / 2 / width
            y_center = (year_bbox[1] + year_bbox[3]) / 2 / height
            char_width = 1.0 * (year_bbox[2] - year_bbox[0]) / width
            char_height = 1.05 * (year_bbox[3] - year_bbox[1]) / height
            yolo_labels.append(f"{class_id} {x_center} {y_center} {char_width} {char_height}")
            
            x_pos += eurostile_small.getlength(char)   # Adjust -8 for tighter spacing`

    # Draw the black rounded border on top of everything
    border_thickness = 5
    radius = 20  # Radius for rounded corners
    draw.rounded_rectangle(
        [border_thickness, border_thickness, width - border_thickness, height - border_thickness],
        radius=radius,
        outline="black",
        width=border_thickness
    )

    # Resize the image to the new dimensions (462x389)
    new_width, new_height = 960, 320
    plate_resized = plate.resize((new_width, new_height))

    # Update YOLO labels for the new size
    yolo_labels_resized = []
    for label in yolo_labels:
        parts = label.split()
        class_id = parts[0]
        
        # Recalculate normalized values for resized image
        x_center = float(parts[1]) * new_width
        y_center = float(parts[2]) * new_height
        char_width = float(parts[3]) * new_width
        char_height = float(parts[4]) * new_height
        
        # Normalize again for new size
        x_center /= new_width
        y_center /= new_height
        char_width /= new_width
        char_height /= new_height

        yolo_labels_resized.append(f"{class_id} {x_center} {y_center} {char_width} {char_height}")

    # Save the resized license plate image
    plate_resized.save(output_file)

    # Save the YOLO labels to a file
    with open(label_file, "w") as f:
        for label in yolo_labels_resized:
            f.write(f"{label}\n")

def create_new_license_plate_bike_front(ler_text="LER", number_text="1234", city_text="PUNJAB", label_file="label_new_bike_front.txt", output_file="license_plate_new_bike_front.jpg"):
    # Load the Eurostile font (replace with Sauerkrauto.ttf if necessary)
    eurostile_large = ImageFont.truetype("Sauerkrauto.ttf", 130)  # For "LER" and "1234"
    eurostile_medium = ImageFont.truetype("Sauerkrauto.ttf", 100)  # For "20"
    eurostile_small = ImageFont.truetype("Sauerkrauto.ttf", 100)  # For "20"
    eurostile_xsmall = ImageFont.truetype("arial.ttf", 18) 
    punjab_font = ImageFont.truetype("Sauerkrauto.ttf", 48)  # For "PUNJAB"
    
    # Create a blank white image (outside the border)
    width, height = 555, 200
    plate = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(plate)

    # List to store YOLO labels
    yolo_labels = []


    offset = 0  # Adjust for thickness
    for dx in range(-offset, offset + 1):
        for dy in range(-offset, offset + 1):
            draw.text((458 + dx, 25 + dy), "ET&NC", fill="black", font=eurostile_xsmall)

    # Add text for the city (default "PUNJAB"), but skip if it's just spaces
    if city_text.strip():  
        start_x, start_y = 185, 6  # Starting position
        spacing = 6  # Adjust letter spacing here

        # Variables to calculate bounding box
        city_x_min = start_x
        city_x_max = start_x  # Will be updated dynamically

        # Manually draw each letter with spacing
        x = start_x
        for letter in city_text:
            draw.text((x, start_y), letter, fill="black", font=punjab_font)
            letter_width = punjab_font.getlength(letter)
            x += letter_width + spacing  # Move cursor by letter width + spacing
            city_x_max = x  # Update max X-coordinate

        # Get bounding box using textbbox() for height
        city_bbox = draw.textbbox((start_x, start_y), city_text, font=punjab_font)
        city_y_min = city_bbox[1]
        city_y_max = city_bbox[3]

        # **Increase height by 5%**
        city_height = (city_y_max - city_y_min) * 1.05  # Increase height by 5%
        city_y_min = city_y_min - ((city_height - (city_y_max - city_y_min)) / 2)  # Adjust top position
        city_y_max = city_y_max + ((city_height - (city_y_max - city_y_min)) / 2)  # Adjust bottom position

        # Normalize the bounding box for YOLO format
        x_center = (city_x_min + city_x_max) / 2 / width
        y_center = (city_y_min + city_y_max) / 2 / height
        city_width = (city_x_max - city_x_min) / width
        city_height = city_height / height  # Normalize new height

        # Store the YOLO label with class ID 36 (for "PUNJAB")
        yolo_labels.append(f"36 {x_center} {y_center} {city_width} {city_height}")



    # Add flower image (wheat graphic) while maintaining the aspect ratio
    logo_image = Image.open("logo_punjab.jpg")  # Replace with your file path
    logo_image = logo_image.convert("RGBA")  # Ensure it's in RGBA mode
    logo_width, logo_height = logo_image.size

    # Resize the image while maintaining the aspect ratio
    logo_image = logo_image.resize((80, 60))

    # Paste the flower image onto the license plate
    plate.paste(logo_image, (20, 10), logo_image)  # Position the image on the plate

    # Add "LER-" (default "LER" with the hyphen) in the image, but skip in YOLO labels
    ler_text_with_hyphen = ler_text   # Ensure "LER-" always appears
    x_pos = 30
    for char in ler_text_with_hyphen:
        
        # Draw the character on the image
        draw.text((x_pos, 35), char, fill="black", font=eurostile_large)
        
        # Get the class ID based on the character
        class_id = CHARACTER_CLASSES.get(char.upper(), 0)  # Use uppercase for class mapping
        
        # Get bounding box of the character
        char_bbox = draw.textbbox((x_pos, 35), char, font=eurostile_large)
        # Normalize the bounding box coordinates and dimensions for YOLO
        x_center = (char_bbox[0] + char_bbox[2]) / 2 / width
        y_center = (char_bbox[1] + char_bbox[3]) / 2 / height
        char_width = 1.0 * (char_bbox[2] - char_bbox[0]) / width
        char_height = 1.05 * (char_bbox[3] - char_bbox[1]) / height
        
        # Store the YOLO label with class ID
        yolo_labels.append(f"{class_id} {x_center} {y_center} {char_width} {char_height}")
        
        x_pos += eurostile_large.getlength(char) + 3 # Adjust -8 for tighter spacing


    # Add the customizable number text (default "1234")
    x_pos = 250
    for char in number_text:
        draw.text((x_pos, 35), char, fill="black", font=eurostile_large)
        # Get bounding box for the number
        num_bbox = draw.textbbox((x_pos, 35), char, font=eurostile_large)
        # Normalize the bounding box for YOLO
        x_center = (num_bbox[0] + num_bbox[2]) / 2 / width
        y_center = (num_bbox[1] + num_bbox[3]) / 2 / height
        num_width = 1.0 * (num_bbox[2] - num_bbox[0]) / width
        num_height = 1.05 * (num_bbox[3] - num_bbox[1]) / height
        yolo_labels.append(f"{CHARACTER_CLASSES[char]} {x_center} {y_center} {num_width} {num_height}")
        
        x_pos += eurostile_large.getlength(char) + 3 # Adjust -8 for tighter spacing


    # Draw the black rounded border on top of everything
    border_thickness = 8
    radius = 20  # Radius for rounded corners
    draw.rounded_rectangle(
        [border_thickness, border_thickness, width - border_thickness, height - border_thickness],
        radius=radius,
        outline="black",
        width=border_thickness
    )

    # Resize the image to the new dimensions (462x389)
    new_width, new_height = 328, 153
    plate_resized = plate.resize((new_width, new_height))

    # Update YOLO labels for the new size
    yolo_labels_resized = []
    for label in yolo_labels:
        parts = label.split()
        class_id = parts[0]
        
        # Recalculate normalized values for resized image
        x_center = float(parts[1]) * new_width
        y_center = float(parts[2]) * new_height
        char_width = float(parts[3]) * new_width
        char_height = float(parts[4]) * new_height
        
        # Normalize again for new size
        x_center /= new_width
        y_center /= new_height
        char_width /= new_width
        char_height /= new_height

        yolo_labels_resized.append(f"{class_id} {x_center} {y_center} {char_width} {char_height}")

    # Save the resized license plate image
    plate_resized.save(output_file)

    # Save the YOLO labels to a file
    with open(label_file, "w") as f:
        for label in yolo_labels_resized:
            f.write(f"{label}\n")

def create_new_license_plate_bike_back(ler_text="LER", number_text="1234", city_text="PUNJAB", label_file="label_new_bike_back.txt", output_file="license_plate_new_bike_back.jpg"):
    # Load the Eurostile font (replace with Sauerkrauto.ttf if necessary)
    eurostile_large = ImageFont.truetype("Sauerkrauto.ttf", 130)  # For "LER" and "1234"
    eurostile_medium = ImageFont.truetype("Sauerkrauto.ttf", 100)  # For "20"
    eurostile_small = ImageFont.truetype("Sauerkrauto.ttf", 100)  # For "20"
    eurostile_xsmall = ImageFont.truetype("arial.ttf", 22) 
    punjab_font = ImageFont.truetype("Sauerkrauto.ttf", 70)  # For "PUNJAB"
    
    # Create a blank white image (outside the border)
    width, height = 555, 250
    plate = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(plate)

    # List to store YOLO labels
    yolo_labels = []


    offset = 1  # Adjust for thickness
    for dx in range(-offset, offset + 1):
        for dy in range(-offset, offset + 1):
            draw.text((435 + dx, 75 + dy), "CET&NC", fill="black", font=eurostile_xsmall)

    # Add text for the city (default "PUNJAB"), but skip if it's just spaces
    if city_text.strip():  
        # Add text for the city (default "PUNJAB")
        city_text = "PUNJAB"
        start_x, start_y = 150, 5  # Starting position
        spacing = 6  # Adjust letter spacing here

        # Variables to calculate bounding box
        city_x_min = start_x
        city_x_max = start_x  # Will be updated dynamically

        # Manually draw each letter with spacing
        x = start_x
        for letter in city_text:
            draw.text((x, start_y), letter, fill="black", font=punjab_font)
            letter_width = punjab_font.getlength(letter)
            x += letter_width + spacing  # Move cursor by letter width + spacing
            city_x_max = x  # Update max X-coordinate

        # Get bounding box using textbbox() for height
        city_bbox = draw.textbbox((start_x, start_y), city_text, font=punjab_font)
        city_y_min = city_bbox[1]
        city_y_max = city_bbox[3]

        # **Increase height by 5%**
        city_height = (city_y_max - city_y_min) * 1.05  # Increase height by 5%
        city_y_min = city_y_min - ((city_height - (city_y_max - city_y_min)) / 2)  # Adjust top position
        city_y_max = city_y_max + ((city_height - (city_y_max - city_y_min)) / 2)  # Adjust bottom position

        # Normalize the bounding box for YOLO format
        x_center = (city_x_min + city_x_max) / 2 / width
        y_center = (city_y_min + city_y_max) / 2 / height
        city_width = (city_x_max - city_x_min) / width
        city_height = city_height / height  # Normalize new height

        # Store the YOLO label with class ID 36 (for "PUNJAB")
        yolo_labels.append(f"36 {x_center} {y_center} {city_width} {city_height}")


    # Add flower image (wheat graphic) while maintaining the aspect ratio
    logo_image = Image.open("logo_punjab.jpg")  # Replace with your file path
    logo_image = logo_image.convert("RGBA")  # Ensure it's in RGBA mode
    logo_width, logo_height = logo_image.size

    # Resize the image while maintaining the aspect ratio
    logo_image = logo_image.resize((100, 70))

    # Paste the flower image onto the license plate
    plate.paste(logo_image, (20, 50), logo_image)  # Position the image on the plate

    # Add "LER-" (default "LER" with the hyphen) in the image, but skip in YOLO labels
    ler_text_with_hyphen = ler_text   # Ensure "LER-" always appears
    x_pos = 30
    for char in ler_text_with_hyphen:
        
        # Draw the character on the image
        draw.text((x_pos, 80), char, fill="black", font=eurostile_large)
        
        # Get the class ID based on the character
        class_id = CHARACTER_CLASSES.get(char.upper(), 0)  # Use uppercase for class mapping
        
        # Get bounding box of the character
        char_bbox = draw.textbbox((x_pos, 80), char, font=eurostile_large)
        # Normalize the bounding box coordinates and dimensions for YOLO
        x_center = (char_bbox[0] + char_bbox[2]) / 2 / width
        y_center = (char_bbox[1] + char_bbox[3]) / 2 / height
        char_width = 1.0 * (char_bbox[2] - char_bbox[0]) / width
        char_height = 1.05 * (char_bbox[3] - char_bbox[1]) / height
        
        # Store the YOLO label with class ID
        yolo_labels.append(f"{class_id} {x_center} {y_center} {char_width} {char_height}")
        
        x_pos += eurostile_large.getlength(char) + 3 # Adjust -8 for tighter spacing


    # Add the customizable number text (default "1234")
    x_pos = 250
    for char in number_text:
        draw.text((x_pos, 80), char, fill="black", font=eurostile_large)
        # Get bounding box for the number
        num_bbox = draw.textbbox((x_pos, 80), char, font=eurostile_large)
        # Normalize the bounding box for YOLO
        x_center = (num_bbox[0] + num_bbox[2]) / 2 / width
        y_center = (num_bbox[1] + num_bbox[3]) / 2 / height
        num_width = 1.0 * (num_bbox[2] - num_bbox[0]) / width
        num_height = 1.05 * (num_bbox[3] - num_bbox[1]) / height
        yolo_labels.append(f"{CHARACTER_CLASSES[char]} {x_center} {y_center} {num_width} {num_height}")
        
        x_pos += eurostile_large.getlength(char) + 3 # Adjust -8 for tighter spacing


    # Draw the black rounded border on top of everything
    border_thickness = 8
    radius = 20  # Radius for rounded corners
    draw.rounded_rectangle(
        [border_thickness, border_thickness, width - border_thickness, height - border_thickness],
        radius=radius,
        outline="black",
        width=border_thickness
    )

    # Resize the image to the new dimensions (462x389)
    new_width, new_height = 415, 354
    plate_resized = plate.resize((new_width, new_height))

    # Update YOLO labels for the new size
    yolo_labels_resized = []
    for label in yolo_labels:
        parts = label.split()
        class_id = parts[0]
        
        # Recalculate normalized values for resized image
        x_center = float(parts[1]) * new_width
        y_center = float(parts[2]) * new_height
        char_width = float(parts[3]) * new_width
        char_height = float(parts[4]) * new_height
        
        # Normalize again for new size
        x_center /= new_width
        y_center /= new_height
        char_width /= new_width
        char_height /= new_height

        yolo_labels_resized.append(f"{class_id} {x_center} {y_center} {char_width} {char_height}")

    # Save the resized license plate image
    plate_resized.save(output_file)

    # Save the YOLO labels to a file
    with open(label_file, "w") as f:
        for label in yolo_labels_resized:
            f.write(f"{label}\n")

def create_license_plate_bike_back(ler_text="LER", number_text="1234", city_text="PUNJAB", manufacture_year="20", single_text="A", label_file="label_bike_back.txt", output_file="license_plate_bike_back.jpg"):
    # Load the Eurostile font (replace with Sauerkrauto.ttf if necessary)
    eurostile_large = ImageFont.truetype("Sauerkrauto.ttf", 150)  # For "LER" and "1234"
    eurostile_medium = ImageFont.truetype("Sauerkrauto.ttf", 100)  # For "20"
    eurostile_small = ImageFont.truetype("Sauerkrauto.ttf", 100)  # For "20"
    punjab_font = ImageFont.truetype("arial.ttf", 23)  # For "PUNJAB"
    
    # Create a blank white image (outside the border)
    width, height = 555, 288
    plate = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(plate)

    # List to store YOLO labels
    yolo_labels = []

    # Draw the green strip with padding of 5 pixels (white space before the green)
    green_color = (0, 177, 91)
    green_strip_width = 105
    horizontal_padding = 8  # Padding between green strip and the rest of the plate
    vertical_padding = 10  # Padding from the top and bottom
    draw.rectangle([horizontal_padding, vertical_padding, green_strip_width + horizontal_padding, height - vertical_padding], fill=green_color)

    # Add text for the city (default "PUNJAB")
    draw.text((18, 105), city_text, fill="black", font=punjab_font)

    # Add flower image (wheat graphic) while maintaining the aspect ratio
    flower_image = Image.open("flower.png")  # Replace with your file path
    flower_width, flower_height = flower_image.size

    # Resize the image while maintaining the aspect ratio
    flower_image = flower_image.resize((90, 80))

    # Paste the flower image onto the license plate
    plate.paste(flower_image, (20, 20), flower_image)  # Position the image on the plate

    # Add "LER-" (default "LER" with the hyphen) in the image, but skip in YOLO labels
    ler_text_with_hyphen = ler_text   # Ensure "LER-" always appears
    x_pos = 130
    for char in ler_text_with_hyphen:
        
        # Draw the character on the image
        draw.text((x_pos, -25), char, fill="black", font=eurostile_large)
        
        # Get the class ID based on the character
        class_id = CHARACTER_CLASSES.get(char.upper(), 0)  # Use uppercase for class mapping
        
        # Get bounding box of the character
        char_bbox = draw.textbbox((x_pos, -25), char, font=eurostile_large)
        # Normalize the bounding box coordinates and dimensions for YOLO
        x_center = (char_bbox[0] + char_bbox[2]) / 2 / width
        y_center = (char_bbox[1] + char_bbox[3]) / 2 / height
        char_width = 1.0 * (char_bbox[2] - char_bbox[0]) / width
        char_height = 1.05 * (char_bbox[3] - char_bbox[1]) / height
        
        # Store the YOLO label with class ID
        yolo_labels.append(f"{class_id} {x_center} {y_center} {char_width} {char_height}")
        
        x_pos += eurostile_large.getlength(char) + 6 # Adjust -8 for tighter spacing

    # Add the manufacture year (e.g., "20") with correct class mapping
    x_pos = 415 # Position for the manufacture year "20"
    for char in manufacture_year:
        draw.text((x_pos, 25), char, fill="black", font=eurostile_small)
        # Get the class ID based on the character
        class_id = CHARACTER_CLASSES.get(char, 0)  # Use the character's class ID
        
        # Get bounding box for the year text
        year_bbox = draw.textbbox((x_pos, 25), char, font=eurostile_small)
        # Normalize the bounding box for YOLO
        x_center = (year_bbox[0] + year_bbox[2]) / 2 / width
        y_center = (year_bbox[1] + year_bbox[3]) / 2 / height
        char_width = 1.0 * (year_bbox[2] - year_bbox[0]) / width
        char_height = 1.05 * (year_bbox[3] - year_bbox[1]) / height
        yolo_labels.append(f"{class_id} {x_center} {y_center} {char_width} {char_height}")
        
        x_pos += eurostile_small.getlength(char) + 5  # Adjust -8 for tighter spacing

    # Add the customizable number text (default "1234")
    x_pos = 130
    for char in number_text:
        draw.text((x_pos, 110), char, fill="black", font=eurostile_large)
        # Get bounding box for the number
        num_bbox = draw.textbbox((x_pos, 110), char, font=eurostile_large)
        # Normalize the bounding box for YOLO
        x_center = (num_bbox[0] + num_bbox[2]) / 2 / width
        y_center = (num_bbox[1] + num_bbox[3]) / 2 / height
        num_width = 1.0 * (num_bbox[2] - num_bbox[0]) / width
        num_height = 1.05 * (num_bbox[3] - num_bbox[1]) / height
        yolo_labels.append(f"{CHARACTER_CLASSES[char]} {x_center} {y_center} {num_width} {num_height}")
        
        x_pos += eurostile_large.getlength(char) + 6 # Adjust -8 for tighter spacing

    # Add the single text (e.g., "A") with correct class mapping
    x_pos = 470  # Position for the single text "A"
    for char in single_text:
        if char != " ":  # Skip if the character is a space
            draw.text((x_pos, 140), char, fill="black", font=eurostile_medium)
            # Get the class ID based on the character
            class_id = CHARACTER_CLASSES.get(char, 0)  # Use the character's class ID
            
            # Get bounding box for the year text
            year_bbox = draw.textbbox((x_pos, 140), char, font=eurostile_medium)
            # Normalize the bounding box for YOLO
            x_center = (year_bbox[0] + year_bbox[2]) / 2 / width
            y_center = (year_bbox[1] + year_bbox[3]) / 2 / height
            char_width = 1.0 * (year_bbox[2] - year_bbox[0]) / width
            char_height = 1.05 * (year_bbox[3] - year_bbox[1]) / height
            yolo_labels.append(f"{class_id} {x_center} {y_center} {char_width} {char_height}")
            
            x_pos += eurostile_small.getlength(char)   # Adjust -8 for tighter spacing

    # Draw the black rounded border on top of everything
    border_thickness = 5
    radius = 20  # Radius for rounded corners
    draw.rounded_rectangle(
        [border_thickness, border_thickness, width - border_thickness, height - border_thickness],
        radius=radius,
        outline="black",
        width=border_thickness
    )

    # Resize the image to the new dimensions (462x389)
    new_width, new_height = 462, 389
    plate_resized = plate.resize((new_width, new_height))

    # Update YOLO labels for the new size
    yolo_labels_resized = []
    for label in yolo_labels:
        parts = label.split()
        class_id = parts[0]
        
        # Recalculate normalized values for resized image
        x_center = float(parts[1]) * new_width
        y_center = float(parts[2]) * new_height
        char_width = float(parts[3]) * new_width
        char_height = float(parts[4]) * new_height
        
        # Normalize again for new size
        x_center /= new_width
        y_center /= new_height
        char_width /= new_width
        char_height /= new_height

        yolo_labels_resized.append(f"{class_id} {x_center} {y_center} {char_width} {char_height}")

    # Save the resized license plate image
    plate_resized.save(output_file)

    # Save the YOLO labels to a file
    with open(label_file, "w") as f:
        for label in yolo_labels_resized:
            f.write(f"{label}\n")

def create_license_plate_car_back(ler_text="LER", number_text="1234", city_text="PUNJAB", manufacture_year="20", single_text="A", label_file="label.txt", output_file="license_plate.jpg"):
    # Load the Eurostile font (replace with Sauerkrauto.ttf if necessary)
    eurostile_large = ImageFont.truetype("Sauerkrauto.ttf", 135)  # For "LER" and "1234"
    eurostile_medium = ImageFont.truetype("Sauerkrauto.ttf", 100)  # For "20"
    eurostile_small = ImageFont.truetype("Sauerkrauto.ttf", 80)  # For "20"
    punjab_font = ImageFont.truetype("arial.ttf", 28)  # For "PUNJAB"
    
    # Create a blank white image (outside the border)
    width, height = 555, 288
    plate = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(plate)

    # List to store YOLO labels
    yolo_labels = []

    # Draw the green strip with padding of 5 pixels (white space before the green)
    green_color = (0, 177, 91)
    green_strip_width = 130
    horizontal_padding = 8  # Padding between green strip and the rest of the plate
    vertical_padding = 10  # Padding from the top and bottom
    draw.rectangle([horizontal_padding, vertical_padding, green_strip_width + horizontal_padding, height - vertical_padding], fill=green_color)

    # Add text for the city (default "PUNJAB")
    draw.text((20, 220), city_text, fill="black", font=punjab_font)

    # Add flower image (wheat graphic) while maintaining the aspect ratio
    flower_image = Image.open("flower.png")  # Replace with your file path
    flower_width, flower_height = flower_image.size

    # Calculate the new size while maintaining the aspect ratio
    max_size = 180  # Maximum size for the image (width or height)
    if flower_width > flower_height:
        new_width = max_size
        new_height = int((new_width / flower_width) * flower_height)
    else:
        new_height = max_size
        new_width = int((new_height / flower_height) * flower_width)

    # Resize the image while maintaining the aspect ratio
    flower_image = flower_image.resize((new_width, new_height))

    # Paste the flower image onto the license plate
    plate.paste(flower_image, (25, 30), flower_image)  # Position the image on the plate

    # Add "LER-" (default "LER" with the hyphen) in the image, but skip in YOLO labels
    ler_text_with_hyphen = ler_text + " -"  # Ensure "LER-" always appears
    x_pos = 175
    for char in ler_text_with_hyphen:
        # Skip the hyphen from YOLO labels
        if char == "-" or char == " ":
            # Just draw the hyphen in the image
            draw.text((x_pos, -15), char, fill="black", font=eurostile_large)
            x_pos += eurostile_large.getlength(char) - 8  # Adjust -8 for tighter spacing
            continue
        
        # Draw the character on the image
        draw.text((x_pos, -15), char, fill="black", font=eurostile_large)
        
        # Get the class ID based on the character
        class_id = CHARACTER_CLASSES.get(char.upper(), 0)  # Use uppercase for class mapping
        
        # Get bounding box of the character
        char_bbox = draw.textbbox((x_pos, -15), char, font=eurostile_large)
        # Normalize the bounding box coordinates and dimensions for YOLO, increase by 5%
        x_center = (char_bbox[0] + char_bbox[2]) / 2 / width
        y_center = (char_bbox[1] + char_bbox[3]) / 2 / height
        char_width = 1.0 * (char_bbox[2] - char_bbox[0]) / width
        char_height = 1.05 * (char_bbox[3] - char_bbox[1]) / height
        
        # Store the YOLO label with class ID
        yolo_labels.append(f"{class_id} {x_center} {y_center} {char_width} {char_height}")
        
        x_pos += eurostile_large.getlength(char) - 8  # Adjust -8 for tighter spacing

    # Add the manufacture year (e.g., "20") with correct class mapping
    x_pos = 455  # Position for the manufacture year "20"
    for char in manufacture_year:
        draw.text((x_pos, 40), char, fill="black", font=eurostile_small)
        # Get the class ID based on the character
        class_id = CHARACTER_CLASSES.get(char, 0)  # Use the character's class ID
        
        # Get bounding box for the year text
        year_bbox = draw.textbbox((x_pos, 40), char, font=eurostile_small)
        # Normalize the bounding box for YOLO, increase by 5%
        x_center = (year_bbox[0] + year_bbox[2]) / 2 / width
        y_center = (year_bbox[1] + year_bbox[3]) / 2 / height
        char_width = 1.0 * (year_bbox[2] - year_bbox[0]) / width
        char_height = 1.05 * (year_bbox[3] - year_bbox[1]) / height
        yolo_labels.append(f"{class_id} {x_center} {y_center} {char_width} {char_height}")
        
        x_pos += eurostile_small.getlength(char) - 5  # Adjust -8 for tighter spacing

    # Add the customizable number text (default "1234")
    x_pos = 155
    for char in number_text:
        draw.text((x_pos, 110), char, fill="black", font=eurostile_large)
        # Get bounding box for the number
        num_bbox = draw.textbbox((x_pos, 110), char, font=eurostile_large)
        # Normalize the bounding box for YOLO, increase by 5%
        x_center = (num_bbox[0] + num_bbox[2]) / 2 / width
        y_center = (num_bbox[1] + num_bbox[3]) / 2 / height
        num_width = 1.0 * (num_bbox[2] - num_bbox[0]) / width
        num_height = 1.05 * (num_bbox[3] - num_bbox[1]) / height
        yolo_labels.append(f"{CHARACTER_CLASSES[char]} {x_center} {y_center} {num_width} {num_height}")
        
        x_pos += eurostile_large.getlength(char) - 8  # Adjust -8 for tighter spacing

    # Add the single text (e.g., "A") with correct class mapping
    x_pos = 455  # Position for the single text "A"
    for char in single_text:
        if char != " ":  # Skip if the character is a space
            # Draw the character using the medium-sized font
            draw.text((x_pos, 140), char, fill="black", font=eurostile_medium)
            
            # Get the class ID based on the character
            class_id = CHARACTER_CLASSES.get(char, 0)  # Use the character's class ID
            
            # Get bounding box for the single character
            char_bbox = draw.textbbox((x_pos, 140), char, font=eurostile_medium)
            
            # Normalize the bounding box for YOLO, increase by 5%
            x_center = (char_bbox[0] + char_bbox[2]) / 2 / width
            y_center = (char_bbox[1] + char_bbox[3]) / 2 / height
            char_width = 1.0 * (char_bbox[2] - char_bbox[0]) / width
            char_height = 1.05 * (char_bbox[3] - char_bbox[1]) / height
            
            # Store the YOLO label with class ID
            yolo_labels.append(f"{class_id} {x_center} {y_center} {char_width} {char_height}")
            
            # Adjust the x_pos for next character (if there's more than one)
            x_pos += eurostile_medium.getlength(char) - 5  # Adjust for tighter spacing


    # Draw the black rounded border on top of everything
    border_thickness = 5
    radius = 20  # Radius for rounded corners
    draw.rounded_rectangle(
        [border_thickness, border_thickness, width - border_thickness, height - border_thickness],
        radius=radius,
        outline="black",
        width=border_thickness
    )

    # Save the license plate image
    plate.save(output_file)

    # Save the YOLO labels to a file
    with open(label_file, "w") as f:
        for label in yolo_labels:
            f.write(f"{label}\n")

# Example usage:
# create_new_license_plate_bike_back(ler_text="LAR", number_text="2331", city_text=" ")
