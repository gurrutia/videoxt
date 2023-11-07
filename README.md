<h1 align="center">
  <img src="https://user-images.githubusercontent.com/3451528/222875688-e8d60da9-0439-4996-936d-c75ffd47cb58.png" alt="videoxt" width="170"></a>
</h1>

[![PyPI](https://img.shields.io/pypi/v/videoxt)](https://pypi.org/project/videoxt) [![Downloads](https://static.pepy.tech/badge/videoxt)](https://pepy.tech/project/videoxt) ![tests](https://github.com/gurrutia/videoxt/actions/workflows/tox.yml/badge.svg)

**VideoXT** is a simple library and CLI tool for extracting audio, individual frames, short clips and GIFs from videos.

See the [documentation](https://gurrutia.github.io/videoxt) for more details.

---

## Installation

Available on <a href="https://pypi.org/project/videoxt/">pypi</a>.

```sh
pip install videoxt
```

---

## Usage

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

## Used By

* **Best Buy Teen Tech Center** at **Grand St. Settlement**, allowing filmmaking instructors to gather film stills that aid in constructing lesson plans for their youth workshops. [Download a workshop example here](https://github.com/gurrutia/videoxt/files/10887456/GSS_Filmmaking_Fall_2022_Transfiguration_Schools_W1.pdf).
