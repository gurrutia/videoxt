"""Functions that display extraction details to the console."""
from textwrap import dedent

import videoxt.constants as C
import videoxt.requestors as R
from videoxt.video import Video


def video_str(video: Video) -> str:
    """String representation of a Video that gets printed to the console."""
    length_display = (
        f"{video.properties.length_timestamp} | "
        f"{video.properties.length_seconds} seconds"
    )
    return dedent(
        f"""
        {C.EMOJI_MAP['video']}
            filepath:           {video.filepath.resolve()}
            format:             {video.properties.suffix!r}
            length:             {length_display}
            fps:                {video.properties.fps}
            frame count:        {video.properties.frame_count}
            dimensions:         {video.properties.dimensions}"""
    )


def base_request_str(request: R.BaseRequest) -> str:
    """String representation of a BaseRequest that gets printed to the console."""
    start_time_display = (
        f"{request.time_range.start_timestamp} | "
        f"{request.time_range.start_second} seconds | "
        f"frame {request.time_range.start_frame}"
    )

    stop_time_display = (
        f"{request.time_range.stop_timestamp} | "
        f"{request.time_range.stop_second} seconds | "
        f"frame {request.time_range.stop_frame}"
    )

    return dedent(
        f"""
        {C.EMOJI_MAP['extraction']}
            start time:         {start_time_display}
            stop time:          {stop_time_display}
            fps:                {request.fps}"""
    )


def audio_request_str(request: R.AudioRequest) -> str:
    """String representation of an AudioRequest that gets printed to the console."""
    return dedent(
        f"""
        {C.EMOJI_MAP['audio']}
            filepath:           {request.filepath.resolve()}
            format:             {request.audio_format!r}
            volume:             {request.volume}
            speed:              {request.speed}
            bounce:             {request.bounce}
            reverse:            {request.reverse}
            normalize:          {request.normalize}
        """
    )


def clip_request_str(request: R.ClipRequest) -> str:
    """String representation of a ClipRequest that gets printed to the console."""
    return dedent(
        f"""
        {C.EMOJI_MAP['clip']}
            filepath:           {request.filepath.resolve()}
            resize:             {request.resize}
            rotate:             {request.rotate}
            speed:              {request.speed}
            monochrome:         {request.monochrome}
            reverse:            {request.reverse}
            bounce:             {request.bounce}
            dimensions:         {request.dimensions}
        {C.EMOJI_MAP['audio']}
            volume:             {request.volume}
            normalize:          {request.normalize}
        """
    )


def frames_request_str(request: R.FramesRequest) -> str:
    """String representation of a FramesRequest that gets printed to the console."""
    return dedent(
        f"""
        {C.EMOJI_MAP['frames']}
            destination:        {request.destdir.resolve()}
            filenames:          {f"{request.filename}_*.{request.image_format}"!r}
            format:             {request.image_format!r}
            images expected:    {request.images_expected}
            capture rate:       {request.capture_rate}
            resize:             {request.resize}
            rotate:             {request.rotate}
            monochrome:         {request.monochrome}
            dimensions:         {request.dimensions}
        """
    )


def gif_request_str(request: R.GifRequest) -> str:
    """String representation of a GifRequest that gets printed to the console."""
    return dedent(
        f"""
        {C.EMOJI_MAP['gif']}
            filepath:           {request.filepath.resolve()}
            resize:             {request.resize}
            rotate:             {request.rotate}
            speed:              {request.speed}
            monochrome:         {request.monochrome}
            reverse:            {request.reverse}
            bounce:             {request.bounce}
            dimensions:         {request.dimensions}
        """
    )
