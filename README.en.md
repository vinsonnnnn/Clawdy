# Clawdy · Your Pixel Companion

[简体中文](README.md) | **English**

A warm orange pixel companion inspired by the Claude Code aesthetic. Clawdy keeps you company while you code or wait for a task to finish, with blinking, waving, jumping, and thoughtful little gestures.

**Nine animation states · Mouse gaze tracking in sixteen directions · Transparent sprite sheet · Ready to adopt and reuse**

![Clawdy animation preview](assets/previews/Clawdy.gif)

## Copy Clawdy into your ChatGPT

### Option 1: Open the adoption link (recommended)

**[Adopt Clawdy →](https://chatgpt.com/s/sharepet_6acdf49f9adc8191be520acad84372b8)**

1. Open the sharing link and sign in to your own ChatGPT account.
2. In a ChatGPT Work environment that supports Pets, follow the sharing page instructions to add Clawdy to your pet list.
3. Select Clawdy as your active companion. If adoption has already activated it, you can skip this step.

Adoption creates your own copy in your account and does not change the author's active companion. Your account and interface must support Pets; downloading this GitHub project alone does not enable ChatGPT features.

If your assistant has access to Pets tools, you can also copy and send this prompt:

```text
Please adopt this animated ChatGPT pet and set it as my active companion:
https://chatgpt.com/s/sharepet_6acdf49f9adc8191be520acad84372b8
```

### Option 2: Download the assets for your own project

Select **Code → Download ZIP** on GitHub, or clone the repository:

```bash
git clone https://github.com/vinsonnnnn/Clawdy.git
cd Clawdy
```

- [Final transparent PNG sprite sheet](assets/clawdy-v2.png): all 73 frames, for players that support this layout.
- [Machine-readable pet.json configuration](pet.json): animation rows, frame counts, timings, and gaze directions.
- [GIF animation preview](assets/previews/Clawdy.gif) / [MP4 preview](assets/previews/Clawdy.mp4).
- [Individual animation GIFs](assets/previews/): useful for project pages, documentation, and messages.

Use the adoption link when adding Clawdy to ChatGPT. The sprite sheet is an image asset; the GitHub ZIP, GIFs, and `pet.json` are not universal one-click ChatGPT installers.

## Nine animations

Clawdy uses movement to respond to interactions and poses to express task states. **Blinking is part of the idle animation, and thinking is represented by the `running` state.** Here, `running` means processing a task; movement uses `running-right` and `running-left`.

| Animation | State | Frames | What you will see |
| --- | --- | ---: | --- |
| Idle and blinking | `idle` | 6 | Gentle breathing, subtle bobbing, and blinking |
| Move right | `running-right` | 8 | Eyes looking right and alternating steps |
| Move left | `running-left` | 8 | The corresponding leftward walking cycle |
| Wave | `waving` | 4 | A little paw rises to greet you, then returns to rest |
| Jump | `jumping` | 5 | Crouch, takeoff, peak, descent, and landing |
| Encounter a problem | `failed` | 8 | A lowered body, drooping paws, and flattened eyes |
| Wait | `waiting` | 6 | A slight expectant lean while awaiting input or confirmation |
| Think and process | `running` | 6 | A paw moves beside the face or in front of the body in a focused pose |
| Review results | `review` | 6 | Scanning eyes and a gentle tilt, as if checking the output |

The host application decides which animations to trigger. The included demo lets you select all nine states manually.

![Selected animation stills](assets/previews/motion-stills.png)

## Mouse gaze tracking in sixteen directions

Clawdy includes **16 gaze poses** around a full circle, spaced 22.5° apart. In screen coordinates, up is 0°, followed clockwise by right at 90°, down at 180°, and left at 270°.

The eyes move together as solid black rectangles while the body stays mostly front-facing and the feet remain anchored. As the pointer moves around Clawdy, the player selects the frame matching its direction relative to the pet's center. Moving near the center returns Clawdy to idle; the demo uses a dead zone with a radius of 24 CSS pixels.

![Sixteen-direction gaze loop](assets/previews/look-loop.gif)

These are discrete generated poses reviewed by hand, rather than real-time 3D head turns. Some near-vertical directions have subtle horizontal differences. The gaze poses are slightly narrower than the idle pose, with the same character design and stable foot placement.

## Local interactive preview

Open [`demo/index.html`](demo/index.html) in your browser to switch animations, adjust the display size, and move the pointer over the preview area to try sixteen-direction gaze tracking. The page uses no third-party libraries and makes no external network requests.

Alternatively, start a local static server:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000/demo/`. GitHub's file viewer does not run HTML directly; download the project to open the demo locally, or deploy it as a static page yourself.

## Assets and layout

| Property | Value |
| --- | --- |
| Format | PNG with an alpha channel |
| Version | v2 sprite sheet layout |
| Sheet dimensions | 1536 × 2288 pixels |
| Grid | 8 columns × 11 rows |
| Cell dimensions | 192 × 208 pixels |
| Standard animations | First 9 rows, 57 frames total |
| Gaze poses | Last 2 rows, 16 frames total |
| Total populated frames | 73 |
| Empty cells | 15, fully transparent |

Each row's populated frames start at the left. Do not play every row as an eight-frame animation, or the transparent empty cells will appear in playback.

```text
assets/clawdy-v2.png      Final transparent sprite sheet
assets/previews/          Nine animations, full preview, and gaze loop
pet.json                 States, timings, directions, and checksum
demo/index.html          Interactive player with no dependencies
docs/SPRITE_SPEC.md       Layout and integration notes (Chinese)
docs/QUALITY.md           Validation results and known limits (Chinese)
tools/sprites.py         Validation, frame extraction, and GIF export
LICENSE                  MIT license
```

See the [animation contact sheet](docs/contact-sheet-final.png) for the full frame layout and the [direction inspection sheet](docs/direction-qa.png) for the sixteen gaze poses.

## Extract frames and generate GIFs

Use Python 3.10 or later:

```bash
python -m pip install -r requirements.txt
python tools/sprites.py validate
python tools/sprites.py export --output output
```

`validate` checks dimensions, the alpha channel, populated cells, empty cells, and the SHA-256 checksum. It verifies asset integrity and does not replace host application import checks or manual animation review.

`export` reads `pet.json`, extracts the animation frames and sixteen gaze frames, and exports looping GIFs with the original timings. To integrate Clawdy into a website, desktop widget, or game, render the corresponding regions of the sprite sheet. Detailed formulas and timings are in [SPRITE_SPEC.md](docs/SPRITE_SPEC.md) (Chinese); `pet.json` provides the machine-readable values.

## Creation and reuse

Clawdy was created with generative image tools and assembled into a sprite sheet after transparency processing, frame extraction, alignment, animation previews, and direction review. This project contains the final assets and lightweight demo/export code. The underlying image generation service and ChatGPT Pets backend are not included.

You are welcome to fork, download, modify, and use Clawdy in your own projects. The code and image assets that the author is entitled to license are released under the [MIT License](LICENSE); retain the license notice when redistributing them. Rights to names and trademarks such as Claude, Claude Code, and ChatGPT are outside the scope of this license.

This is an independent community project inspired by Claude Code's pixel character, with no official affiliation, sponsorship, or endorsement from Anthropic or OpenAI.

If you enjoy this little companion, give the repository a star and share your own variation.
