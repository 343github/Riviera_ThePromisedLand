import os
from PIL import Image

def read_4bpp_tile_big_endian(data, offset, tile_size=10):
    tile = []
    for y in range(tile_size):
        row = []
        for x in range(0, tile_size, 2):
            byte = data[offset]
            offset += 1
            high_nibble = byte >> 4
            low_nibble = byte & 0xF
            row.extend([high_nibble, low_nibble])
        tile.append(row)
    return tile

def gba_color_to_rgb(color):
    r = (color & 0x1F) << 3
    g = ((color >> 5) & 0x1F) << 3
    b = ((color >> 10) & 0x1F) << 3
    return (r, g, b)

def create_image_from_tiles(tiles, tile_size=10):
    width = 16 * tile_size
    height = (len(tiles) // 16 + (1 if len(tiles) % 16 else 0)) * tile_size
    img = Image.new('P', (width, height))
    
    # Palette
    gba_palette = [
        0x0000, 0x6318, 0x318C, 0x0000, 0x0000, 0x318C, 0x7FFF, 0x0000,
        0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000
    ]
    
    palette = [color for gba_color in gba_palette for color in gba_color_to_rgb(gba_color)]
    img.putpalette(palette)
    for i, tile in enumerate(tiles):
        x = (i % 16) * tile_size
        y = (i // 16) * tile_size
        for ty, row in enumerate(tile):
            for tx, pixel in enumerate(row):
                img.putpixel((x + tx, y + ty), pixel)
    return img

def create_spaced_image(image_path, tile_size=10, spacing=5):
    original_image = Image.open(image_path)
    num_tiles_x = original_image.width // tile_size
    num_tiles_y = original_image.height // tile_size
    new_width = num_tiles_x * (tile_size + spacing) - spacing
    new_height = num_tiles_y * (tile_size + spacing) - spacing
    new_image = Image.new("RGB", (new_width, new_height), (0, 0, 0))
    for y in range(num_tiles_y):
        for x in range(num_tiles_x):
            tile = original_image.crop((x * tile_size, y * tile_size, 
                                        (x + 1) * tile_size, (y + 1) * tile_size))
            new_x = x * (tile_size + spacing)
            new_y = y * (tile_size + spacing)
            new_image.paste(tile, (new_x, new_y))
    spaced_image_path = image_path.replace('.png', '_spaced.png')
    new_image.save(spaced_image_path)
    print(f"Image saved as {spaced_image_path}")

def extract_and_save(file_path, start_offset, end_offset, output_image):
    with open(file_path, 'rb') as f:
        f.seek(start_offset)
        data = f.read(end_offset - start_offset)
    
    tiles = []
    for i in range(0, len(data), 50):
        tiles.append(read_4bpp_tile_big_endian(data, i))
    img = create_image_from_tiles(tiles)
    img.save(output_image)
    
    create_spaced_image(output_image)

# Rutas y offsets
script_dir = os.path.dirname(os.path.abspath(__file__))
tpl_path = os.path.join(script_dir, 'Insert', 'TPL.gba')
offsets = [
    (0x5892cc, 0x5a290c, 'Font.png')
]

# Extraer y guardar las imágenes
for start, end, img_name in offsets:
    extract_and_save(tpl_path, start, end, img_name)

print("Extraction completed")
