from PIL import Image, ImageDraw, ImageFont

def create_license_plate(ler_text="LER", number_text="1234", city_text="PUNJAB", manufacture_year="20"):
    # Load the Eurostile font (replace with Sauerkrauto.ttf if necessary)
    eurostile_large = ImageFont.truetype("Sauerkrauto.ttf", 135)  # For "LER" and "1234"
    eurostile_small = ImageFont.truetype("Sauerkrauto.ttf", 80)  # For "20"
    punjab_font = ImageFont.truetype("arial.ttf", 28)  # For "PUNJAB"
    year_font = ImageFont.truetype("arial.ttf", 28)  # For manufacture year text

    # Create a blank white image (outside the border)
    width, height = 555, 288
    plate = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(plate)

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

    # Add "LER-" (default "LER" with the hyphen)
    ler_text_with_hyphen = ler_text + " -"  # Ensure "LER-" always appears
    x_pos = 168
    for char in ler_text_with_hyphen:
        draw.text((x_pos, -15), char, fill="black", font=eurostile_large)
        x_pos += eurostile_large.getsize(char)[0] - 8  # Adjust -8 for tighter spacing

    # Add the manufacture year (e.g., "20")
    draw.text((450, 40), manufacture_year, fill="black", font=eurostile_small)  # Custom year

    # Add the customizable number text (default "1234")
    x_pos = 155
    for char in number_text:
        draw.text((x_pos, 110), char, fill="black", font=eurostile_large)
        x_pos += eurostile_large.getsize(char)[0] - 8  # Adjust -8 for tighter spacing

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
    plate.save("license_plate.png")

# Example usage:
create_license_plate(ler_text="LDR", number_text="1234", city_text="PUNJAB", manufacture_year="20")
