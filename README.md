# E-Paper Converter

A Python tool to convert images for the WaveShare PhotoPainter (B) 7-color e-paper display (RP2350 based).

This project has been packaged as a `uv` tool for easy installation and use.

## Installation

If you have [uv](https://github.com/astral-sh/uv) installed, you can run this tool without installing it:

```bash
uv run --with epaper-converter epaper-convert <path-to-image>
```

Or install it globally:

```bash
uv tool install .
```

## Usage

```bash
epaper-convert <input_path> [--dir landscape|portrait] [--mode scale|cut] [-r]
```

- `input_path`: Path to an image file or a directory of images.
- `--dir`: Force orientation (landscape or portrait). Default is auto-detected.
- `--mode`:
    - `scale`: Fit-to-fill and crop (default).
    - `cut`: Fit-to-box and pad with white.
- `-r`, `--recursive`: Recurse into subdirectories when `input_path` is a directory.

The output will be saved as a BMP file in the same directory as the input image, with `_scale_output.bmp` or `_cut_output.bmp` appended to the filename.

## Technical Details

- Targets standard 7.3 inch e-paper resolution (800x480 for landscape, 480x800 for portrait).
- Uses the 7-color e-paper palette (Black, White, Yellow, Red, Blue, Green).
- Employs Floyd-Steinberg dithering for color quantization.

## Source Information

This tool is a restatement of the official WaveShare conversion process.
See: [WaveShare Wiki - PhotoPainter (B)](https://www.waveshare.com/wiki/PhotoPainter_(B))

Original source: [PhotoPainter_B GitHub](https://github.com/waveshareteam/PhotoPainter_B.git)
