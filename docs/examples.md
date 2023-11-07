## Basic Examples

From the command-line:

```sh
# extract audio from a video file (default: 'mp3')
$ videoxt audio MyVideo.mp4
{"video": {"filepath": "C:/Users/gurrutia/MyVideo.mp4", ...}, "start_time": 0, ...}
# extracting audio...
{"success": true, ...}
$ ls
MyVideo.mp4  MyVideo.mp3
```

As a library:

```python
$ python
>>> # extract all frames from a video file (default: 'jpg')
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

> **NOTE**: All command-line examples are run from the directory where the video is located. You can run the commands from any directory by specifying the full path to the video.

## Frames: Extract every 30th frame...

Extract every 30th **frame** of a video, save the frames as `png` images, set the dimensions of the images to 800x600, apply a monochrome (black and white) filter to the images and print extraction details to the console.

```python
import videoxt
from pathlib import Path

result = videoxt.extract_frames(
  Path('C:/Users/gurrutia/Videos/MyVideo.avi'),
  capture_rate=30,
  image_format='png',  # default: 'mp3'
  dimensions=(800, 600),
  monochrome=True,
  verbose=True
)
...
```

### CLI equivalent

```sh
$ videoxt frames MyVideo.avi --capture-rate 30 --image-format png --dimensions 800x600 --monochrome
# or...
$ videoxt frames MyVideo.avi -cr 30 -if png --dm 800x600 --monochrome
```

---

## Audio: Extract from a list of videos...

Extract and normalize the **audio** from a list of videos, save the audio as `wav` files to a directory named `to_sample` that exists in the same directory as the video file.

```python
import videoxt

filepaths = [
  'C:/Users/gurrutia/Videos/First.mp4',
  'C:/Users/gurrutia/Videos/Second.mp4',
  'C:/Users/gurrutia/Videos/Third.mp4',
]

for filepath in filepaths:
    result = videoxt.extract_audio(
        filepath,
        audio_format='wav',
        destdir=filepath.parent / 'to_sample',  # directory must exist
        normalize=True
    )
    ...
```

### CLI equivalent

```sh
$ videoxt audio First.mp4 --audio-format wav --destdir to_sample --normalize
# or...
$ videoxt audio First.mp4 -af wav -d to_sample --normalize
```

---

## GIF: Create a gif between...

Create a **gif** 1:08 and 1:10 of a video, reduce its dimensions by 50%, decrease the gif speed by 25%, and add a bouncing effect.

```python
import videoxt

result = videoxt.extract_gif(
    'C:/Users/gurrutia/Videos/MyVideo.mp4',
    start_time='1:08',  # or 68.0
    stop_time='1:10',   # or 70.0
    resize=0.5,
    speed=0.75,
    bounce=True
)
...
```

### CLI equivalent

```sh
$ videoxt gif MyVideo.mp4 --start-time 1:08 --stop-time 1:10 --resize 0.5 --speed 0.75 --bounce
# or...
$ videoxt gif MyVideo.mp4 -s 1:08 -S 1:10 -rs 0.5 -sp 0.75 --bounce
```

---

## Clip: Create a clip of the initial 5 seconds...

Create a **clip** of the initial 5 seconds of a video, rotate the clip 180 degrees, and save the file as `MyVideoRotated.mp4`.

```python
import videoxt

result = videoxt.extract_clip(
  filepath='C:/Users/gurrutia/Videos/MyVideo.mp4',
  stop_time=5,   # or '0:05'
  rotate=180,
  filename='MyVideoRotated'  # default extension: 'mp4'
)
result.destpath # pathlib.Path('C:/Users/gurrutia/Videos/MyVideoRotated.mp4')
...
```

### CLI equivalent

```sh
$ videoxt clip MyVideo.mp4 --stop-time 5 --rotate 180 --filename MyVideoRotated
# or...
$ videoxt clip MyVideo.mp4 -S 5 -rt 180 -fn MyVideoRotated
```
