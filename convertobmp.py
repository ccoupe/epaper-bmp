#!/usr/bin/env python3
# encoding: utf-8

import argparse
import sys
from pathlib import Path
from PIL import Image, ImageOps

# Constants for e-paper palette (specific to 7-color e-paper displays)
EPAPER_PALETTE = (
    0, 0, 0,        # 0: Black
    255, 255, 255,  # 1: White
    255, 255, 0,    # 2: Yellow
    255, 0, 0,      # 3: Red
    0, 0, 0,        # 4: Black (Extra)
    0, 0, 255,      # 5: Blue
    0, 255, 0       # 6: Green
) + (0, 0, 0) * 249

def convert_image(input_path: Path, direction: str = None, mode: str = 'scale', dither_algorithm: int = Image.Dither.FLOYDSTEINBERG):
    """
    Converts a single image file to a BMP suitable for e-paper display.
    
    Args:
        input_path: Path to the input image file.
        direction: Forced orientation ('landscape' or 'portrait'). If None, auto-detected.
        mode: Scaling mode ('scale' for fit-to-fill/crop, 'cut' for fit-to-box/pad).
        dither_algorithm: Dithering algorithm to use during quantization.
    """
    try:
        with Image.open(input_path) as img:
            # Convert to RGB to ensure consistency
            img = img.convert('RGB')
            width, height = img.size

            # Determine target dimensions (standard 7.3 inch e-paper resolution)
            if direction == 'landscape':
                target_width, target_height = 800, 480
            elif direction == 'portrait':
                target_width, target_height = 480, 800
            else:
                # Auto-determine based on original aspect ratio
                if width > height:
                    target_width, target_height = 800, 480
                else:
                    target_width, target_height = 480, 800

            if mode == 'scale':
                # Fit to fill: scales image so it covers the target area, then crops the overflow
                output_image = ImageOps.fit(img, (target_width, target_height), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
            elif mode == 'cut':
                # Fit to box: scales image to fit inside the target area, then pads with white
                output_image = ImageOps.pad(img, size=(target_width, target_height), color=(255, 255, 255), centering=(0.5, 0.5))
            else:
                raise ValueError(f"Unknown mode: {mode}")

            # Create palette image for quantization
            pal_image = Image.new("P", (1, 1))
            pal_image.putpalette(EPAPER_PALETTE)

            # Quantize and convert back to RGB for saving as BMP
            quantized_image = output_image.quantize(dither=dither_algorithm, palette=pal_image).convert('RGB')

            # Save output image in the same directory as input
            output_filename = input_path.with_name(f"{input_path.stem}_{mode}_output.bmp")
            quantized_image.save(output_filename)
            print(f"Successfully converted {input_path} to {output_filename}")
            return True
    except Exception as e:
        print(f"Error processing {input_path}: {e}", file=sys.stderr)
        return False

def process_path(path: Path, recursive: bool, direction: str, mode: str, dither: int):
    """Processes a file or directory recursively for images."""
    if path.is_file():
        if path.suffix.lower() in ('.jpg', '.jpeg', '.png'):
            convert_image(path, direction, mode, dither)
    elif path.is_dir():
        pattern = '**/*' if recursive else '*'
        # Sort files to have consistent processing order
        for p in sorted(path.glob(pattern)):
            if p.is_file() and p.suffix.lower() in ('.jpg', '.jpeg', '.png'):
                convert_image(p, direction, mode, dither)
    else:
        print(f"Error: Path '{path}' does not exist or is not a valid file/directory.", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description='Process images for e-paper display (7-color/6c BMP conversion).')
    parser.add_argument('path', type=str, help='Input image file or directory')
    parser.add_argument('--dir', choices=['landscape', 'portrait'], help='Force image orientation (landscape or portrait)')
    parser.add_argument('--mode', choices=['scale', 'cut'], default='scale', 
                        help="'scale' for Fit-to-Fill/Crop (default), 'cut' for Fit-to-Box/Pad")
    parser.add_argument('--dither', type=int, choices=[Image.Dither.NONE, Image.Dither.FLOYDSTEINBERG], 
                        default=Image.Dither.FLOYDSTEINBERG, help='Dithering algorithm: NONE(0) or FLOYDSTEINBERG(3) (default)')
    parser.add_argument('-r', '--recursive', action='store_true', help='Recurse into directories')

    args = parser.parse_args()

    input_path = Path(args.path)
    process_path(input_path, args.recursive, args.dir, args.mode, args.dither)

if __name__ == "__main__":
    main()
