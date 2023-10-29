<h1 align="center">
  <img src="https://user-images.githubusercontent.com/3451528/222875688-e8d60da9-0439-4996-936d-c75ffd47cb58.png" alt="videoxt" width="200"></a>
</h1>

[![PyPI](https://img.shields.io/pypi/v/videoxt)](https://pypi.org/project/videoxt) [![Downloads](https://static.pepy.tech/badge/videoxt)](https://pepy.tech/project/videoxt)

<b>VideoXT</b> is a simple library and CLI tool for extracting audio, individual frames, short clips and GIFs from videos.


[![demo](https://user-images.githubusercontent.com/3451528/229325416-30faad6c-725f-4783-9a9f-1b83245810ec.jpg)](https://user-images.githubusercontent.com/3451528/229325422-0da43958-34b0-438e-9049-73a98a7924d7.mp4)

## Contents

* <a href="#installation">Installation</a><br/>
* <a href="#examples">Examples</a><br/>
* <a href="#command-line-usage">Command-line usage</a><br/>
* <a href="#frames">*frames* usage</a><br/>
* <a href="#gif">*gif* usage</a><br/>
* <a href="#audio">*audio* usage</a><br/>
* <a href="#clip">*clip* usage</a><br/>
* <a href="#used-by">Used by</a>

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

**Example 1**: Extract every `30th` **frame** of a video, save the frames as `png` images, set the dimensions of the images to `800x600`, apply a `monochrome` (black and white) filter to the images and print extraction details to the console.

```python
import videoxt

videoxt.extract_frames(
  'C:/Users/gurrutia/Videos/video.avi',  # pathlib.Path also works
  capture_rate=30,
  image_format='png',  # default is 'jpg'
  dimensions=(800, 600),
  monochrome=True,
  verbose=True,
)
```

Command-line equivalent:

```sh
>> videoxt frames video.avi --capture-rate 30 --image-format png --dimensions 800 600 --monochrome
or
>> videoxt frames video.avi -cr 30 -if png --dm 800 600 --monochrome
```

Extraction details printed to console:

![example1](https://user-images.githubusercontent.com/3451528/229313078-10b2ccc5-b643-4d2b-acdc-e75dcd7346fd.jpg)

**Example 2**: Extract and `normalize` the **audio** from a list of video filepaths, save the audio as `wav` files in a directory named `to_sample` that exists in the same directory as the video file.

```python
from pathlib import Path
import videoxt

filepaths = [
  Path('C:/Users/gurrutia/Videos/video.mp4'),
  Path('C:/Users/gurrutia/Videos/video2.mp4'),
  Path('C:/Users/gurrutia/Videos/video3.mp4'),
]

for filepath in filepaths:
  videoxt.extract_audio(
    filepath,
    audio_format='wav',  # default is 'mp3'
    destdir=filepath.parent / 'to_sample',  # directory must exist
    normalize=True,
  )
```

Command-line equivalent (for a single video file):

```sh
>> videoxt audio video.mp4 --audio-format wav --destdir to_sample --normalize
or
>> videoxt audio video.mp4 -af wav -d to_sample --normalize
```

**Example 3**: Create a **subclip** between `1:08` and `1:10` of the video, `resize` the subclip up by `25%`, slow the `speed` of subclip down by `75%`, `reverse` the subclip, and `normalize` the subclip audio. *Only `mp4` output is supported*.

```python
from pathlib import Path
import videoxt

videoxt.extract_clip(
  Path('C:/Users/gurrutia/Videos/video.mp4'),
  start_time='1:08',  # or 68.0
  stop_time=70,  # or '1:10'
  resize=1.25,
  speed=0.25,
  normalize=True,
)
```

Command-line equivalent:

```sh
>> videoxt clip video.mp4 --start-time 1:08 --stop-time 70 --resize 1.25 --speed 0.25 --normalize
or
>> videoxt clip video.mp4 -s 1:08 -S 70 -rs 1.25 -sp 0.25 --normalize
```

---

## Command-line usage

```sh
>> videoxt --help
usage: videoxt [-h] [--version] {audio,clip,frames,gif} ...

Extract audio, clips, frames and create gifs from a video.

positional arguments:
  {audio,clip,frames,gif}
    audio               Extract audio from video.
    clip                Extract a clip of a video file. Only supports 'mp4' output.
    frames              Extract individual frames from a video and save them as images.
    gif                 Create a GIF between two points in a video.

options:
  -h, --help            show this help message and exit
  --version, -V         show program's version number and exit
```

### *frames*

```sh
>> videoxt frames --help
usage: videoxt frames [-h] [--start-time] [--stop-time] [--fps] [--destdir] [--filename] [--quiet] [--dimensions ]
                      [--resize] [--rotate] [--monochrome] [--image-format] [--capture-rate]
                      filepath

positional arguments:
  filepath              Path to the video file with extension.

options:
  -h, --help            show this help message and exit
  --start-time , -s     Time to start extraction. Can be a number representing seconds or a timestamp (Ex: --start-
                        time 0:45 or -s 45).
  --stop-time , -S      Time to stop extraction. Can be a number representing seconds or a timestamp (Ex: --stop-time
                        1:30 or -S 90).
  --fps , -f            Manually set the frames per second (FPS). Helpful if the FPS is not read accurately.
  --destdir , -d        Specify the directory you want to save the media to. If not provided, media is saved in the
                        video directory.
  --filename , -fn      Set the name of the output media file(s), without the extension. If not provided, the video
                        filename is used.
  --quiet, -q           Disable extraction details from being printed to the console.
  --dimensions  , -dm
                        Resize the output to a specific width and height (Ex: --dm 1920 1080).
  --resize , -rs        Increase or decrease the dimensions of the output by a factor of N.
  --rotate , -rt        Rotate the output by 90, 180, or 270 degrees.
  --monochrome          Apply a black and white filter to the output.
  --image-format , -if
                        Set the image format to save the frames as. Default is 'jpg'.
  --capture-rate , -cr
                        Capture every Nth video frame. Default is 1, which captures every frame.
```

### *gif*

```sh
>> videoxt gif --help
usage: videoxt gif [-h] [--start-time] [--stop-time] [--fps] [--destdir] [--filename] [--quiet] [--dimensions ]
                   [--resize] [--rotate] [--monochrome] [--speed] [--bounce] [--reverse]
                   filepath

positional arguments:
  filepath              Path to the video file with extension.

options:
  -h, --help            show this help message and exit
  --start-time , -s     Time to start extraction. Can be a number representing seconds or a timestamp (Ex: --start-
                        time 0:45 or -s 45).
  --stop-time , -S      Time to stop extraction. Can be a number representing seconds or a timestamp (Ex: --stop-time
                        1:30 or -S 90).
  --fps , -f            Manually set the frames per second (FPS). Helpful if the FPS is not read accurately.
  --destdir , -d        Specify the directory you want to save the media to. If not provided, media is saved in the
                        video directory.
  --filename , -fn      Set the name of the output media file(s), without the extension. If not provided, the video
                        filename is used.
  --quiet, -q           Disable extraction details from being printed to the console.
  --dimensions  , -dm
                        Resize the output to a specific width and height (Ex: --dm 1920 1080).
  --resize , -rs        Increase or decrease the dimensions of the output by a factor of N.
  --rotate , -rt        Rotate the output by 90, 180, or 270 degrees.
  --monochrome          Apply a black and white filter to the output.
  --speed , -sp         Increase or decrease the speed of the output by a factor of N.
  --bounce              Make the output bounce back-and-forth, boomerang style.
  --reverse             Reverse the output.
```

### *audio*

```sh
>> videoxt audio --help
usage: videoxt audio [-h] [--start-time] [--stop-time] [--fps] [--destdir] [--filename] [--quiet] [--volume]
                     [--normalize] [--audio-format]
                     filepath

positional arguments:
  filepath              Path to the video file with extension.

options:
  -h, --help            show this help message and exit
  --start-time , -s     Time to start extraction. Can be a number representing seconds or a timestamp (Ex: --start-
                        time 0:45 or -s 45).
  --stop-time , -S      Time to stop extraction. Can be a number representing seconds or a timestamp (Ex: --stop-time
                        1:30 or -S 90).
  --fps , -f            Manually set the frames per second (FPS). Helpful if the FPS is not read accurately.
  --destdir , -d        Specify the directory you want to save the media to. If not provided, media is saved in the
                        video directory.
  --filename , -fn      Set the name of the output media file(s), without the extension. If not provided, the video
                        filename is used.
  --quiet, -q           Disable extraction details from being printed to the console.
  --volume , -v         Increase or decrease the output audio volume by a factor of N.
  --normalize           Normalize the audio output to a maximum of 0dB.
  --audio-format , -af
                        Set the audio format to as. Default is 'mp3'.
```

### *clip*

```sh
>> videoxt clip --help
usage: videoxt clip [-h] [--start-time] [--stop-time] [--fps] [--destdir] [--filename] [--quiet] [--volume]
                    [--normalize] [--dimensions ] [--resize] [--rotate] [--monochrome] [--speed] [--bounce]
                    [--reverse]
                    filepath

positional arguments:
  filepath              Path to the video file with extension.

options:
  -h, --help            show this help message and exit
  --start-time , -s     Time to start extraction. Can be a number representing seconds or a timestamp (Ex: --start-
                        time 0:45 or -s 45).
  --stop-time , -S      Time to stop extraction. Can be a number representing seconds or a timestamp (Ex: --stop-time
                        1:30 or -S 90).
  --fps , -f            Manually set the frames per second (FPS). Helpful if the FPS is not read accurately.
  --destdir , -d        Specify the directory you want to save the media to. If not provided, media is saved in the
                        video directory.
  --filename , -fn      Set the name of the output media file(s), without the extension. If not provided, the video
                        filename is used.
  --quiet, -q           Disable extraction details from being printed to the console.
  --volume , -v         Increase or decrease the output audio volume by a factor of N.
  --normalize           Normalize the audio output to a maximum of 0dB.
  --dimensions  , -dm
                        Resize the output to a specific width and height (Ex: --dm 1920 1080).
  --resize , -rs        Increase or decrease the dimensions of the output by a factor of N.
  --rotate , -rt        Rotate the output by 90, 180, or 270 degrees.
  --monochrome          Apply a black and white filter to the output.
  --speed , -sp         Increase or decrease the speed of the output by a factor of N.
  --bounce              Make the output bounce back-and-forth, boomerang style.
  --reverse             Reverse the output.
```

---

## Used by

* **Best Buy Teen Tech Center** at **Grand St. Settlement**, allowing filmmaking instructors to gather film stills that aid in constructing lesson plans for their youth workshops. [Download workshop example here.](https://github.com/gurrutia/videoxt/files/10887456/GSS_Filmmaking_Fall_2022_Transfiguration_Schools_W1.pdf)
