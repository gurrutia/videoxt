<h1 align="center">
  <img src="https://user-images.githubusercontent.com/3451528/222875688-e8d60da9-0439-4996-936d-c75ffd47cb58.png" alt="videoxt" width="170"></a>
</h1>

[![PyPI](https://img.shields.io/pypi/v/videoxt)](https://pypi.org/project/videoxt) [![Downloads](https://static.pepy.tech/badge/videoxt)](https://pepy.tech/project/videoxt)

<b>VideoXT</b> is a simple library and CLI tool for extracting audio, individual frames, short clips and GIFs from videos.

---

## Contents

* <a href="#basic-examples">Basic Examples</a><br/>
* <a href="#installation">Installation</a><br/>
* <a href="#command-line-usage">Command-line Usage</a><br/>
* <a href="#audio">*Audio*</a><br/>
* <a href="#frames">*Frames*</a><br/>
* <a href="#gif">*GIF*</a><br/>
* <a href="#clip">*Clip*</a><br/>
* <a href="#more-examples">More Examples</a><br/>
* <a href="#used-by">Used By</a>

---

## Basic Examples

From the command-line:
```sh
# extract audio from a video file (default: 'mp3')
$ videoxt audio MyVideo.mp4
{"video": {"filepath": "C:/Users/gurrutia/MyVideo.mp4", ...}, "start_time": 0, ...}
# Extracting audio...
{"success": true, ...}
$ ls
MyVideo.mp4  MyVideo.mp3
```

As a library:
```python
$ python
>>> import videoxt
>>> filepath = 'C:/Users/gurrutia/MyVideo.mp4'  # or <class 'pathlib.Path'>
>>> result = videoxt.extract_frames(filepath)  # or videoxt.extract('frames', filepath)
>>> result.destpath
pathlib.Path('C:/Users/gurrutia/MyVideo.mp4_frames')
>>> result.elapsed_time
3.14159265358979323
>>> len(list(result.destpath.glob('*.jpg'))) # default: 'jpg'
100  # number of frames extracted
>>> result.json()
{'success': True, ...}
```

---

## Installation

Available on <a href="https://pypi.org/project/videoxt/">pypi</a>.
```sh
pip install videoxt
```

---

## Command-line Usage

```sh
$ videoxt --help
usage: videoxt [-h] [--version] {audio,clip,frames,gif} ...

Extract audio, individual frames, short clips and GIFs from videos.

positional arguments:
  {audio,clip,frames,gif}
    audio               Extract audio from a video file.
    clip                Extract a short clip from a video file as 'mp4'.
    frames              Extract individual frames from a video and save them as images.
    gif                 Create a GIF from a video between two specified points.

options:
  -h, --help            show this help message and exit
  --version, -V         show program's version number and exit
```

### *Audio*

```sh
$ videoxt audio --help
usage: videoxt audio [-h] [--start-time] [--stop-time] [--destdir] [--filename] [--quiet] [--overwrite] [--fps] [--volume] [--normalize] [--speed] [--bounce] [--reverse]
                     [--audio-format]
                     filepath

positional arguments:
  filepath              Path to the video file with extension.

options:
  -h, --help            show this help message and exit
  --start-time , -s     Time to start extraction. Can be a number representing seconds or a timestamp (Ex: --start-time 0:45 or -s 45).
  --stop-time , -S      Time to stop extraction. Can be a number representing seconds or a timestamp (Ex: --stop-time 1:30 or -S 90).
  --destdir , -d        Specify the directory you want to save output to. If not provided, media is saved in the directory of the input video file.
  --filename , -fn      Set the name of the output media file(s), without the extension. If not provided, the video's filename is used.
  --quiet, -q           Disable extraction details from being printed to the console.
  --overwrite, -ov      Overwrite the output file(s) if they already exist.
  --fps , -f            Manually set the video's frames per second (FPS). Helpful if the FPS is not read accurately by OpenCV. Use with caution.
  --volume , -v         Increase or decrease the output audio volume by a factor of N.
  --normalize           Normalize the audio output to a maximum of 0dB.
  --speed , -sp         Increase or decrease the speed of the output by a factor of N.
  --bounce              Make the output bounce back-and-forth, boomerang style.
  --reverse             Reverse the output.
  --audio-format , -af
                        Set the extracted audio file format. Default is 'mp3'.
```

### *Frames*

```sh
$ videoxt frames --help
usage: videoxt frames [-h] [--start-time] [--stop-time] [--destdir] [--filename] [--quiet] [--overwrite] [--fps] [--dimensions] [--resize] [--rotate] [--monochrome]
                      [--image-format] [--capture-rate]
                      filepath

positional arguments:
  filepath              Path to the video file with extension.

options:
  -h, --help            show this help message and exit
  --start-time , -s     Time to start extraction. Can be a number representing seconds or a timestamp (Ex: --start-time 0:45 or -s 45).
  --stop-time , -S      Time to stop extraction. Can be a number representing seconds or a timestamp (Ex: --stop-time 1:30 or -S 90).
  --destdir , -d        Specify the directory you want to save output to. If not provided, media is saved in the directory of the input video file.
  --filename , -fn      Set the name of the output media file(s), without the extension. If not provided, the video's filename is used.
  --quiet, -q           Disable extraction details from being printed to the console.
  --overwrite, -ov      Overwrite the output file(s) if they already exist.
  --fps , -f            Manually set the video's frames per second (FPS). Helpful if the FPS is not read accurately by OpenCV. Use with caution.
  --dimensions , -dm    Resize the output to a specific width and height (Ex: -dm 1920x1080).
  --resize , -rs        Increase or decrease the dimensions of the output by a factor of N.
  --rotate , -rt        Rotate the output by 90, 180, or 270 degrees.
  --monochrome          Apply a black-and-white filter to the output.
  --image-format , -if
                        Set the image format to save the frames as. Default is 'jpg'.
  --capture-rate , -cr
                        Capture every Nth video frame. Default is 1, which captures every frame.
```

### *GIF*

```sh
$ videoxt gif --help
usage: videoxt gif [-h] [--start-time] [--stop-time] [--destdir] [--filename] [--quiet] [--overwrite] [--fps] [--dimensions] [--resize] [--rotate] [--monochrome] [--speed]
                   [--bounce] [--reverse]
                   filepath

positional arguments:
  filepath             Path to the video file with extension.

options:
  -h, --help           show this help message and exit
  --start-time , -s    Time to start extraction. Can be a number representing seconds or a timestamp (Ex: --start-time 0:45 or -s 45).
  --stop-time , -S     Time to stop extraction. Can be a number representing seconds or a timestamp (Ex: --stop-time 1:30 or -S 90).
  --destdir , -d       Specify the directory you want to save output to. If not provided, media is saved in the directory of the input video file.
  --filename , -fn     Set the name of the output media file(s), without the extension. If not provided, the video's filename is used.
  --quiet, -q          Disable extraction details from being printed to the console.
  --overwrite, -ov     Overwrite the output file(s) if they already exist.
  --fps , -f           Manually set the video's frames per second (FPS). Helpful if the FPS is not read accurately by OpenCV. Use with caution.
  --dimensions , -dm   Resize the output to a specific width and height (Ex: -dm 1920x1080).
  --resize , -rs       Increase or decrease the dimensions of the output by a factor of N.
  --rotate , -rt       Rotate the output by 90, 180, or 270 degrees.
  --monochrome         Apply a black-and-white filter to the output.
  --speed , -sp        Increase or decrease the speed of the output by a factor of N.
  --bounce             Make the output bounce back-and-forth, boomerang style.
  --reverse            Reverse the output.
```

### *Clip*

```sh
$ videoxt clip --help
usage: videoxt clip [-h] [--start-time] [--stop-time] [--destdir] [--filename] [--quiet] [--overwrite] [--fps] [--volume] [--normalize] [--dimensions] [--resize] [--rotate]
                    [--monochrome] [--speed] [--bounce] [--reverse]
                    filepath

positional arguments:
  filepath             Path to the video file with extension.

options:
  -h, --help           show this help message and exit
  --start-time , -s    Time to start extraction. Can be a number representing seconds or a timestamp (Ex: --start-time 0:45 or -s 45).
  --stop-time , -S     Time to stop extraction. Can be a number representing seconds or a timestamp (Ex: --stop-time 1:30 or -S 90).
  --destdir , -d       Specify the directory you want to save output to. If not provided, media is saved in the directory of the input video file.
  --filename , -fn     Set the name of the output media file(s), without the extension. If not provided, the video's filename is used.
  --quiet, -q          Disable extraction details from being printed to the console.
  --overwrite, -ov     Overwrite the output file(s) if they already exist.
  --fps , -f           Manually set the video's frames per second (FPS). Helpful if the FPS is not read accurately by OpenCV. Use with caution.
  --volume , -v        Increase or decrease the output audio volume by a factor of N.
  --normalize          Normalize the audio output to a maximum of 0dB.
  --dimensions , -dm   Resize the output to a specific width and height (Ex: -dm 1920x1080).
  --resize , -rs       Increase or decrease the dimensions of the output by a factor of N.
  --rotate , -rt       Rotate the output by 90, 180, or 270 degrees.
  --monochrome         Apply a black-and-white filter to the output.
  --speed , -sp        Increase or decrease the speed of the output by a factor of N.
  --bounce             Make the output bounce back-and-forth, boomerang style.
  --reverse            Reverse the output.
```

---

## More Examples

> **NOTE**: All command-line examples are run from the directory where the video is located. You can run the commands from any directory by specifying the full path to the video.

**Example 1**: Extract every 30th **frame** of a video, save the frames as `png` images, set the dimensions of the images to 800x600, apply a monochrome (black and white) filter to the images and print extraction details to the console.

```python
import videoxt as vxt
from pathlib import Path

result = vxt.extract_frames(
  Path('C:/Users/gurrutia/Videos/MyVideo.avi'),
  capture_rate=30,
  image_format='png',  # default: 'mp3'
  dimensions=(800, 600),
  monochrome=True,
  verbose=True
)
...
```

Command-line equivalent:

```sh
$ videoxt frames MyVideo.avi --capture-rate 30 --image-format png --dimensions 800x600 --monochrome
# or...
$ videoxt frames MyVideo.avi -cr 30 -if png --dm 800x600 --monochrome
```

---

**Example 2**: Extract and normalize the **audio** from a list of videos, save the audio as `wav` files to a directory named `to_sample` that exists in the same directory as the video file.

```python
import videoxt as vxt

filepaths = [
  'C:/Users/gurrutia/Videos/First.mp4',
  'C:/Users/gurrutia/Videos/Second.mp4',
  'C:/Users/gurrutia/Videos/Third.mp4',
]

for filepath in filepaths:
  result = vxt.extract_audio(
    filepath,
    audio_format='wav',
    destdir=filepath.parent / 'to_sample',  # directory must exist
    normalize=True
  )
  ...
```

Command-line equivalent (for a single video file):

```sh
$ videoxt audio First.mp4 --audio-format wav --destdir to_sample --normalize
# or...
$ videoxt audio First.mp4 -af wav -d to_sample --normalize
```

---

**Example 3**: Create a **gif** between 1:08 and 1:10 of a video, reduce its dimensions by 50%, decrease the gif speed by 25%, and add a bouncing effect.

```python
import videoxt as vxt

result = vxt.extract(
  method='gif',
  filepath='C:/Users/gurrutia/Videos/MyVideo.mp4',
  start_time='1:08',  # or 68.0
  stop_time='1:10',   # or 70.0
  resize=0.5,
  speed=0.75,
  bounce=True
)
...
```

Command-line equivalent:
```sh
$ videoxt gif MyVideo.mp4 --start-time 1:08 --stop-time 1:10 --resize 0.5 --speed 0.75 --bounce
# or...
$ videoxt gif MyVideo.mp4 -s 1:08 -S 1:10 -rs 0.5 -sp 0.75 --bounce
```

---

## Used By

* **Best Buy Teen Tech Center** at **Grand St. Settlement**, allowing filmmaking instructors to gather film stills that aid in constructing lesson plans for their youth workshops. [Download workshop example here](https://github.com/gurrutia/videoxt/files/10887456/GSS_Filmmaking_Fall_2022_Transfiguration_Schools_W1.pdf).
