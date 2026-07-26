import concurrent.futures
import pathlib

import segja
from taka.audio import chunk_audio, download_audio

__all__ = ["download"]


def download_one(video_id: str, audios_path: pathlib.Path, proxies: list[str] | None, sample_rate: int, frames: int | None) -> None:
    audio_path = download_audio(video_id, audios_path, proxies)

    if audio_path is not None and frames is not None:
        chunk_audio(audio_path, frames, sample_rate)


def download(
    video_ids: list[str],
    audios_path: str | pathlib.Path,
    replace: bool = False,
    workers: int = 1,
    proxies: list[str] | None = None,
    sample_rate: int = 44100,
    frames: int | None = None,
) -> None:
    audios_path = pathlib.Path(audios_path)
    audios_path.mkdir(parents=True, exist_ok=replace)

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(download_one, video_id, audios_path, proxies, sample_rate, frames) for video_id in video_ids]

        for future in segja.progress(concurrent.futures.as_completed(futures), description="Downloading", total=len(futures)):
            future.result()
