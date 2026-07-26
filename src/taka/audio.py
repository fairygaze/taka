import pathlib
import subprocess

import segja
import yt_dlp

__all__ = ["chunk_audio", "download_audio"]


def download_audio(video_id: str, audios_path: pathlib.Path, proxies: list[str] | None) -> pathlib.Path | None:
    for proxy in proxies or [None]:
        try:
            with yt_dlp.YoutubeDL(
                {
                    "format": "bestaudio/best",
                    "outtmpl": str(audios_path / "%(id)s.%(ext)s"),
                    "quiet": True,
                    "no_warnings": True,
                    "proxy": proxy,
                }
            ) as youtube:
                info = youtube.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=True)
                assert info is not None
                return pathlib.Path(youtube.prepare_filename(info))

        except Exception:  # noqa: BLE001
            segja.warning(f"Failed to download {video_id}.")
            continue


def chunk_audio(audio_path: pathlib.Path, frames: int, sample_rate: int) -> None:
    assert audio_path.exists()

    chunk_path = audio_path.with_name(f"{audio_path.stem}-%d{audio_path.suffix}")

    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(audio_path),
            "-c",
            "copy",
            "-f",
            "segment",
            "-segment_time",
            str(frames / sample_rate),
            "-reset_timestamps",
            "1",
            str(chunk_path),
        ],
        check=True,
    )

    audio_path.unlink()
