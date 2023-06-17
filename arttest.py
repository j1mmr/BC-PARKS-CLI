

from PIL import Image
from art import *
from colorama import init, Fore, Style
import numpy as np

# Initialize colorama
init(autoreset=True)

# Load the image
image = Image.open('/home/peter/Pictures/test.png')

# Resize the image to a desired width and height
width, height = 80, 40
image = image.resize((width, height))

# Convert the image to grayscale
image = image.convert('L')

# Convert the image to a numpy array
image_array = np.array(image)

# Define the character set for shading
char_set = [' ', '░', '▒', '▓', '█']

# Define the corresponding color set
color_set = [Fore.BLACK, Fore.BLUE, Fore.GREEN, Fore.YELLOW, Fore.WHITE]

# Adjust the length of color_set to match char_set
if len(color_set) < len(char_set):
    color_set += [Fore.WHITE] * (len(char_set) - len(color_set))
elif len(color_set) > len(char_set):
    color_set = color_set[:len(char_set)]

# Convert the image array to colored ASCII art
ascii_art = ''
for row in image_array:
    ascii_row = ''
    for pixel in row:
        char_index = pixel // 51  # Mapping pixel intensity to character set index
        ascii_row += f"{color_set[char_index]}{char_set[char_index]}"
    ascii_art += ascii_row + '\n'

# Print the colored ASCII art
print(ascii_art)
