"""Functions that display extraction details to the console."""
from textwrap import dedent

import videoxt.constants as C
from videoxt.extractors import AudioRequest
from videoxt.extractors import BaseRequest
from videoxt.extractors import ClipRequest
from videoxt.extractors import FramesRequest
from videoxt.extractors import GifRequest
from videoxt.extractors import Video


def video_str(video: Video) -> str:
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


def base_request_str(request: BaseRequest) -> str:
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
            fps:                {request.fps}
            destination dir:    {request.destdir.resolve()}"""  # type: ignore
    )


def audio_request_str(request: AudioRequest) -> str:
    return dedent(
        f"""
        {C.EMOJI_MAP['audio']}
            filename:           {request.filepath.name!r}
            format:             {request.audio_format!r}
            volume:             {request.volume}
            speed:              {request.speed}
            bounce:             {request.bounce}
            reverse:            {request.reverse}
            normalize:          {request.normalize}
        """
    )


def clip_request_str(request: ClipRequest) -> str:
    return dedent(
        f"""
        {C.EMOJI_MAP['clip']}
            filename:           {request.filepath.name!r}
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


def frames_request_str(request: FramesRequest) -> str:
    return dedent(
        f"""
        {C.EMOJI_MAP['frames']}
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


def gif_request_str(request: GifRequest) -> str:
    return dedent(
        f"""
        {C.EMOJI_MAP['gif']}
            filename:           {request.filepath.name!r}
            resize:             {request.resize}
            rotate:             {request.rotate}
            speed:              {request.speed}
            monochrome:         {request.monochrome}
            reverse:            {request.reverse}
            bounce:             {request.bounce}
            dimensions:         {request.dimensions}
        """
    )