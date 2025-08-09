import os
from PIL import Image
import shutil
from typing import List, Tuple

def pack_4bpp_tile_big_endian(tile_pixels, tile_size=10):
    """Converts a 10x10 tile of pixel indices into 50 bytes of 4bpp data."""
    byte_data = bytearray()
    for y in range(tile_size):
        row = tile_pixels[y]
        for x in range(0, tile_size, 2):
            high_nibble = row[x]
            low_nibble = row[x+1]
            byte = (high_nibble << 4) | low_nibble
            byte_data.append(byte)
    return byte_data

def hex_string_to_bytes(hex_string: str) -> bytes:
    """Converts a hexadecimal string to bytes."""
    hex_values = hex_string.split()
    return bytes(int(hex_val, 16) for hex_val in hex_values)

def apply_hex_modifications(rom_path: str, modifications: List[Tuple[int, int, str]]) -> bool:
    """
    Applies the specified hexadecimal modifications to the ROM.
    
    Args:
        rom_path: Path to the ROM file
        modifications: List of tuples (start_offset, end_offset, hex_data)
    
    Returns:
        True if modifications were successful, False otherwise
    """
    print("\n--- Applying Hexadecimal Modifications ---")
    
    try:
        with open(rom_path, 'r+b') as file:
            for i, (start_offset, end_offset, hex_data) in enumerate(modifications, 1):
                # Convert hex string to bytes
                new_bytes = hex_string_to_bytes(hex_data)
                expected_length = end_offset - start_offset + 1
                
                # Verify that the length matches
                if len(new_bytes) != expected_length:
                    print(f"Warning in modification {i}: "
                          f"Expected length {expected_length}, "
                          f"but {len(new_bytes)} bytes were provided")
                
                # Seek to the offset and write the new bytes
                file.seek(start_offset)
                file.write(new_bytes)
                
                print(f"Modification {i} completed: "
                      f"Offset 0x{start_offset:X} - 0x{end_offset:X} "
                      f"({len(new_bytes)} bytes)")
        
        print("All hexadecimal modifications completed successfully.")
        return True
        
    except Exception as e:
        print(f"Error applying hexadecimal modifications: {e}")
        return False

def insert_font(rom_path, font_image_path, start_offset, end_offset, max_tiles=180):
    """Reads a font sheet image and writes exactly 4100 bytes (82 tiles) into the ROM."""
    try:
        img = Image.open(font_image_path)
    except FileNotFoundError:
        print(f"Error: Font image '{font_image_path}' not found.")
        print("Make sure you have edited and saved your 'Font.png' file.")
        return False

    print(f"Reading pixel data from '{font_image_path}'...")
    
    num_tiles_x = img.width // tile_size
    num_tiles_y = img.height // tile_size
    total_tiles = min(max_tiles, num_tiles_x * num_tiles_y)  # Limit to 82 tiles
    
    full_font_data = bytearray()
    
    for i in range(total_tiles):
        tile_x = (i % num_tiles_x) * tile_size
        tile_y = (i // num_tiles_x) * tile_size
        
        current_tile_pixels = []
        for ty in range(tile_size):
            row = []
            for tx in range(tile_size):
                pixel_index = img.getpixel((tile_x + tx, tile_y + ty))
                row.append(pixel_index)
            current_tile_pixels.append(row)
            
        packed_tile = pack_4bpp_tile_big_endian(current_tile_pixels, tile_size)
        full_font_data.extend(packed_tile)

    # --- Safety Check ---
    expected_size = end_offset - start_offset  # Should be 4100 bytes
    if len(full_font_data) != expected_size:
        print("\n--- WARNING! ---")
        print(f"The generated font data size ({len(full_font_data)} bytes) does not match the")
        print(f"expected ROM space ({expected_size} bytes).")
        print("There might be an error in the tile count or script logic.")
        print("Aborting to prevent ROM corruption.")
        return False
        
    print(f"Font data successfully packed ({len(full_font_data)} bytes).")
    
    # --- Writing to ROM ---
    try:
        print(f"Opening ROM '{rom_path}' for writing...")
        with open(rom_path, 'r+b') as f:
            f.seek(start_offset)
            f.write(full_font_data)
        print(f"Successfully wrote 9000 bytes of font data to offset 0x{start_offset:X}.")
        print("\nFont insertion complete!")
        return True
        
    except FileNotFoundError:
        print(f"Error: ROM file '{rom_path}' not found.")
        return False
    except Exception as e:
        print(f"An error occurred while writing to the ROM: {e}")
        return False

def read_widths_from_file(file_path: str) -> str:
    """Reads decimal values from a text file and converts them to a space-separated hexadecimal string."""
    try:
        with open(file_path, 'r') as f:
            # Read lines, strip whitespace, and split into values
            decimal_values = []
            for line in f:
                # Remove leading/trailing whitespace and split by spaces
                values = line.strip().split()
                # Convert each value to an integer and validate range (0-10)
                for val in values:
                    try:
                        num = int(val)
                        if 0 <= num <= 10:
                            decimal_values.append(num)
                        else:
                            print(f"Warning: Value '{val}' in {file_path} is out of range (0-10). Skipping.")
                    except ValueError:
                        print(f"Warning: Invalid decimal value '{val}' in {file_path}. Skipping.")
            
            # Convert decimal values to two-digit hexadecimal (e.g., 10 -> "0a")
            hex_values = [f"{num:02x}" for num in decimal_values]
            
            # Verify the number of values matches the expected length (180 bytes)
            expected_length = 180  # Based on offset range (16979203 - 16979024 + 1)
            if len(hex_values) != expected_length:
                print(f"Error: Expected {expected_length} values in {file_path}, but found {len(hex_values)}.")
                return ""
            
            # Join the hex values with spaces to match the format expected by hex_string_to_bytes
            return " ".join(hex_values)
    except FileNotFoundError:
        print(f"Error: Widths file '{file_path}' not found.")
        return ""
    except Exception as e:
        print(f"Error reading Widths file '{file_path}': {e}")
        return ""

# --- CONFIGURATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
rom_path = os.path.join(script_dir, 'Insert', 'TPL.gba')
font_image_to_insert = 'Font.png'
start_offset = 0x58b400
end_offset = 0x58D728  # Updated to 0x5892cc + 4100 bytes for 82 tiles
tile_size = 10

# Read decimal data from Widths.txt and convert to hex
widths_file_path = os.path.join(script_dir, 'Widths.txt')
widths_hex_data = read_widths_from_file(widths_file_path)
if not widths_hex_data:
    print("Failed to read or process Widths.txt. Aborting.")
    input("Press Enter to exit...")
    exit()

# Define the hexadecimal modifications
hex_modifications = [
    # (start_offset, end_offset, hex_data)
    (112760, 112760, "B3"),
    (112784, 112785, "56 FF"),
    (112908, 112909, "56 FF"),
    (112912, 112914, "50 14 03"),
    (113117, 113119, "20 70 47"),
    (16979024, 16979203, widths_hex_data)  # Use data from Widths.txt
]

# --- EXECUTION ---
print("--- Riviera Font Inserter with Hexadecimal Modifications ---")

backup_path = rom_path + '.bak'
print(f"Creating a backup of your ROM at '{backup_path}'...")
try:
    shutil.copy(rom_path, backup_path)
    print("Backup successful.")
except FileNotFoundError:
    print(f"Could not find ROM at '{rom_path}' to create a backup.")
    input("Press Enter to exit...")
    exit()
except Exception as e:
    print(f"Could not create backup. Error: {e}")
    input("Press Enter to exit...")
    exit()

# Show information about the modifications that will be applied
print(f"\nScheduled hexadecimal modifications: {len(hex_modifications)}")
for i, (start, end, _) in enumerate(hex_modifications, 1):
    length = end - start + 1
    print(f"  {i}) 0x{start:X} - 0x{end:X} ({length} bytes)")

print("\nThe process will include:")
print("1. Font insertion from Font.png")
print("2. Application of hexadecimal modifications")

# Request confirmation
response = input("\nDo you want to continue with the complete process? (y/N): ").lower()
if response not in ['y', 'yes', 's', 'sí', 'si']:
    print("Process cancelled by user.")
    input("Press Enter to exit...")
    exit()

# Execute font insertion
print("\n--- Starting Font Insertion ---")
font_success = insert_font(rom_path, font_image_to_insert, start_offset, end_offset)

if font_success:
    print("\n✅ Font insertion completed successfully.")
    
    # Apply hexadecimal modifications
    hex_success = apply_hex_modifications(rom_path, hex_modifications)
    
    if hex_success:
        print("\n✅ All operations completed successfully!")
        print("The ROM has been modified with:")
        print("- New font inserted")
        print("- Hexadecimal modifications applied")
    else:
        print("\n⚠️ The font was inserted correctly, but there were problems with the hexadecimal modifications.")
else:
    print("\n❌ Font insertion failed. Hexadecimal modifications will not be applied.")

input("Press Enter to exit...")
