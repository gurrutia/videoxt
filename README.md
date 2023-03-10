<h1 align="center">
  <img src="https://user-images.githubusercontent.com/3451528/222875688-e8d60da9-0439-4996-936d-c75ffd47cb58.png" alt="videoxt" width="210"></a>
</h1>

[![PyPI](https://img.shields.io/pypi/v/videoxt)](https://pypi.org/project/videoxt) [![Downloads](https://static.pepy.tech/badge/videoxt)](https://pepy.tech/project/videoxt)

<p align="center">
  <b>videoxt</b> is a Python library and command-line tool that allows you to convert video frames to images, or create a GIF between two points in a video.<br/><br/>
  <a href="#installation">Installation</a> •
  <a href="#examples">Examples</a> •
  <a href="#options">Options</a> •
  <a href="#used-by">Used by</a>
</p>

<div align="center">
  <b>View demo on Vimeo:</b><br/>
  <a href="https://vimeo.com/804903665"><img src="https://i.vimeocdn.com/video/1625119839-dd58766e279a6ff55dc505a718c721da027467575bf25f844d909558cc7fa2f0-d_640" alt="videoxt demo" title="View videoxt demo on Vimeo"></a>
</div>


---

## Installation

```sh
pip install videoxt
```

or

```sh
git clone https://github.com/gurrutia/videoxt.git
```

---

## Examples

> **NOTE**: All command-line examples are run from the directory where the video is located. You can run the commands from any directory by specifying the full path to the video.
>
> **vxt** cli entry point will be deprecated in a future release, use **videoxt** instead.

**Example 1**: Extract all video frames.

```python
from videoxt.extractors import VideoToImages

vti = VideoToImages("C:/Users/gurrutia/Videos/video.mp4")

vti.extract_images()
```

Command-line equivalent:

```sh
videoxt images video.mp4
```

<img src="https://user-images.githubusercontent.com/3451528/222924597-da48b568-cf13-4117-b5bf-cdecf4e006ce.jpg" alt="videoxt_example_1" width="700"></a>

**Example 2**: Extract every `30th` frame from `50` seconds to the end of the video, save the images as `png`, resize the frames by `50%` and rotate the frames by `180` degrees.

```python
from videoxt.extractors import VideoToImages

vti = VideoToImages(
  "C:/Users/gurrutia/Videos/video.mp4",
  start_time=50,
  capture_rate=30,
  image_format="png",
  resize=0.5,
  rotate=180,
)

vti.extract_images()
```

Command-line equivalent:

```sh
videoxt images video.mp4 --start-time 50 --capture-rate 30 --image-format png --resize 0.5 --rotate 180
```

<img src="https://user-images.githubusercontent.com/3451528/222924619-f4e5b3d8-e743-476c-af86-da3b50b8b1a3.jpg" alt="videoxt_example_2" width="700"></a>

**Example 3**: Create a GIF between `01:10` and `01:12` of the video at 1/4 the video speed, and resize the GIF to 640x480.

```python
from videoxt.extractors import VideoToGIF

vtg = VideoToGIF(
  "C:/Users/gurrutia/Videos/video.mp4",
  start_time="01:10",
  stop_time="01:12",
  speed=.25,
  dimensions=(640, 480),
)

vtg.create_gif()
```

Command-line equivalent:

```sh
videoxt gif video.mp4 --start-time 01:10 --stop-time 01:12 --speed 0.25 --dimensions 640 480
```

<img src="https://user-images.githubusercontent.com/3451528/222924624-583b2ad2-b34c-4278-871b-094e13f83034.jpg" alt="videoxt_example_2" width="700"></a>

## Options

### General options

Argument&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Description
---|---
**`video_path`** | Path to the video file with the extension. **(Required)**<br/><br/>Example: `C:/Users/gurrutia/Videos/video.mp4`
**`--start-time`** | Specify the video extraction start time, in seconds or as a timestamp in the format `HH:MM:SS`, `H:MM:SS`, `MM:SS` or `M:SS`.<br/><br/>Example: `--start-time 1:30` or `--start-time 90`<br/><br/>Default: the start of the video.
**`--stop-time`** | Specify the video extraction stop time, in seconds or as a timestamp in the format `HH:MM:SS`, `H:MM:SS`, `MM:SS` or `M:SS`.<br/><br/>Example: `--stop-time 2:00` or `--stop-time 120`<br/><br/>Default: the end of the video.
**`--fps`** | Number of frames per second in the video file, overrides the video metadata frames per second. Use this option sparingly and only when the video metadata fps is incorrectly detected.<br/><br/>Example: `--fps 30`<br/><br/>Default: the video metadata fps.
**`--dimensions`** | Specify the media output dimensions as space-separated values.<br/><br/>Example: `--dimensions 1920 1080`<br/><br/>Default: the native video dimensions.
**`--resize`** | Resize the media output by a factor of *n*.<br/><br/>Example: `--resize 1.5` to increase the media output size by 50%<br/><br/>Default: `1.0`, no resize.
**`--rotate`** | Rotate the media output by 90, 180, or 270 degrees.<br/><br/>Valid rotate values: 0, 90, 180, 270<br/><br/>Example: `--rotate 270` to rotate the media counter-clockwise by 90 degrees.<br/><br/>Default: `0`, no rotation.
**`--output-dir`** | Directory to save the media output to.<br/><br/>Example: `--output-dir C:/Users/gurrutia/Videos/custom_folder`<br/><br/>Default for *images*: `same/directory/as/video/video_frames`<br/>Default for *gif*: `same/directory/as/video`.
**`--output-filename`** | Specify the file name of the media output.<br/><br/>Example for *images*: `--output-filname my_images`, which will name all the images as `my_images_*.jpg` where `*` is the frame number.<br/>Example for *gif*: `--output-filename my.gif`<br/><br/>Default for *images*: `video_filename_*.jpg`<br/>Default for *gif*: `video_filename.gif`
**`--monochrome`** | Convert the media output to monochrome (black and white).<br/><br/>Example: `--monochrome`.<br/><br/>Default: `False`
**`--quiet`** | Disable extraction details in terminal.<br/><br/>Example: `--quiet` to disable extraction details from being printed.<br/><br/>Default: `False`
**`--emoji`** | Enable emoji's in terminal. Added by special request 👍.<br/><br/>Example: `--emoji` to enable emoji's.<br/><br/>Default: `False`

### Image only options
Argument&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Description
---|---
**`---capture-rate`** | Capture every *nth* video frame.<br/><br/>Example: `--capture-rate 30` to every 30th frame.<br/><br/>Default: `1`, every frame.
**`--image-format`** | Specify the image format to save the frames as.<br/><br/>Valid image formats: bmp, dib, jpeg, jpg, png, tiff, tif, webp<br/><br/>Example: `--image-format png` or `--image-format .png`<br/><br/>Default: `jpg`
### GIF only options
Argument&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Description
---|---
**`--speed`** | Speed of the GIF animation.<br/><br/>Example: `--speed 0.5` to create a GIF at half the video speed.<br/><br/>Default: `1.0`, same speed as the video.
**`--bounce`** | Make GIF bounce forwards and backwards, boomerang style.<br/><br/>Example: `--bounce`<br/><br/>Default: `False`
---

## Used by

- **Grand St. Settlement** *(non-profit)* filmmaking instructors to gather film stills that aid in constructing lesson plans for their youth workshops. [Download workshop example here.](https://github.com/gurrutia/videoxt/files/10887456/GSS_Filmmaking_Fall_2022_Transfiguration_Schools_W1.pdf)
