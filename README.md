# taka

A fast YouTube audio downloader.

## Installation

```sh
uv add git+https://github.com/fairygaze/taka
```

## Usage

```py
import taka

# Download audios to ./audios.

taka.download(
    video_ids=[...], 
    audios_path="audios",
)

# Download audios to ./audios in 10s chunks.

taka.download(
    video_ids=[...], 
    audios_path="audios", 
    sample_rate=44100, 
    frames=44100 * 10,
)

# Download audios to ./audios with multiple workers.

taka.download(
    video_ids=[...], 
    audios_path="audios",
    workers=4,
)

# Download audios to ./audios with multiple workers and proxies.

taka.download(
    video_ids=[...], 
    audios_path="audios",
    workers=4,
    proxies=[...],  # Each written as, scheme://user:pass@host:port.
)
```
