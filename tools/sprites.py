"""Validate Clawdy's atlas or export its original pixels to PNG frames and GIFs."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def load():
    config = json.loads((ROOT / "pet.json").read_text(encoding="utf-8"))
    path = ROOT / config["spritesheet"]
    with Image.open(path) as source:
        if source.mode != "RGBA":
            raise ValueError("Expected an RGBA atlas")
        atlas = source.copy()
    return config, path, atlas


def cell(atlas, row, column, spec):
    w, h = spec["cellWidth"], spec["cellHeight"]
    return atlas.crop((column*w, row*h, (column+1)*w, (row+1)*h))


def validate(config, path, atlas):
    spec = config["atlas"]
    if atlas.size != (spec["width"], spec["height"]):
        raise ValueError("Atlas dimensions do not match pet.json")
    if hashlib.sha256(path.read_bytes()).hexdigest() != config["sha256"]:
        raise ValueError("SHA-256 mismatch: modified or damaged asset")
    counts = {v["row"]: v["frames"] for v in config["animations"].values()}
    counts.update({r: 8 for r in config["look"]["rows"]})
    used = 0
    for row in range(spec["rows"]):
        for column in range(spec["columns"]):
            frame = cell(atlas, row, column, spec)
            bbox = frame.getchannel("A").getbbox()
            required = column < counts[row]
            if bool(bbox) != required:
                raise ValueError(f"Wrong occupancy: row={row}, column={column}")
            if required:
                used += 1
                if frame.getchannel("A").getextrema()[0] != 0:
                    raise ValueError(f"No transparent background: {row},{column}")
    print(f"PASS: {used} populated cells; 15 empty cells; dimensions, alpha and SHA-256 match")


def gif(frames, durations, destination):
    frames[0].save(destination, save_all=True, append_images=frames[1:],
                   duration=durations, loop=0, disposal=2, optimize=False)


def export(config, atlas, destination):
    destination.mkdir(parents=True, exist_ok=True)
    for name, state in config["animations"].items():
        directory = destination / name
        directory.mkdir(exist_ok=True)
        frames = [cell(atlas, state["row"], i, config["atlas"])
                  for i in range(state["frames"])]
        for i, frame in enumerate(frames):
            frame.save(directory / f"{i:02d}.png")
        gif(frames, state["durationsMs"], destination / f"{name}.gif")
    directory = destination / "look"
    directory.mkdir(exist_ok=True)
    frames = []
    for i, angle in enumerate(config["look"]["anglesDegrees"]):
        frame = cell(atlas, config["look"]["rows"][i//8], i % 8, config["atlas"])
        frame.save(directory / f"{angle:05.1f}.png")
        frames.append(frame)
    gif(frames, [150]*16, destination / "look-loop.gif")
    print(f"Exported 73 PNG frames and 10 GIFs to {destination.resolve()}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["validate", "export"])
    parser.add_argument("--output", type=Path, default=ROOT / "output")
    args = parser.parse_args()
    config, path, atlas = load()
    validate(config, path, atlas)
    if args.command == "export":
        export(config, atlas, args.output)


if __name__ == "__main__":
    main()
