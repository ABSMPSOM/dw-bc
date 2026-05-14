from pathlib import Path
import yt_dlp

DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)


def get_youtube_qualities(video_url):

    ydl_opts = {
        "quiet": True,
        "nocheckcertificate": True,
        "ignoreerrors": True,
        "no_warnings": True,
        "noplaylist": True
    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                video_url,
                download=False
            )

            if not info:
                return []

            formats = info.get("formats", [])

    except Exception as e:

        print("YOUTUBE QUALITY ERROR:")
        print(str(e))

        return []

    video_formats = [
        fmt for fmt in formats
        if fmt.get("height")
        and fmt.get("ext") == "mp4"
        and fmt.get("vcodec") != "none"
    ]

    unique_formats = {}

    for fmt in video_formats:

        height = fmt["height"]

        current = unique_formats.get(height)

        current_bitrate = (
            current.get("tbr") or 0
            if current else 0
        )

        new_bitrate = fmt.get("tbr") or 0

        if (
            current is None or
            new_bitrate > current_bitrate
        ):

            unique_formats[height] = fmt

    sorted_formats = sorted(
        unique_formats.items(),
        reverse=True
    )

    result = []

    for height, fmt in sorted_formats:

        result.append({
            "quality": f"{height}p",
            "format_id": fmt["format_id"],
            "ext": fmt.get("ext"),
            "fps": fmt.get("fps"),
            "filesize": fmt.get("filesize")
        })

    return result


def download_youtube_video(
    video_url,
    format_id
):

    ydl_opts = {
        "format": f"{format_id}+bestaudio",
        "merge_output_format": "mp4",
        "outtmpl": str(
            DOWNLOAD_DIR / "%(title)s.%(ext)s"
        ),
        "noplaylist": True,
        "quiet": True,
        "nocheckcertificate": True,
        "ignoreerrors": True,
        "no_warnings": True,
        "cookiefile": "cookies.txt"
    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                video_url,
                download=True
            )

            file_name = ydl.prepare_filename(info)

        return {
            "success": True,
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "saved_file": file_name
        }

    except Exception as e:

        print("DOWNLOAD ERROR:")
        print(str(e))

        return {
            "success": False,
            "error": str(e)
        }