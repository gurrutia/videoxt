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
