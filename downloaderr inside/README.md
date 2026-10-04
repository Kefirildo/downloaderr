<div align="center">

# downloaderr

**Tiny console menu on top of [yt-dlp](https://github.com/yt-dlp/yt-dlp).**
Video or audio from YouTube and thousands of other sites, no long commands.

![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Powered by](https://img.shields.io/badge/powered%20by-yt--dlp-red)

</div>

```text
==============================================================
  DOWNLOADERR  -  console downloader powered by yt-dlp
==============================================================
  yt-dlp : installed    ffmpeg : found
  Mode: video best
  Cookies: browser: firefox
  Speed: 2MB/s
--------------------------------------------------------------
  1. Download by link
  2. Download from a list file
  3. Cookies (browser / file)
  4. Settings
  5. Show available formats for a link
  8. Install / update yt-dlp
  0. Exit
```

## Why

- Runs locally: no sketchy "downloader" sites, no ads, no server-side throttling
- Cookies from your browser (Firefox by default) for age-gated and private videos
- Built-in speed limiter, so your home network stays usable
- Quality up to 2160p or audio only, playlists, EN / RU interface

## Quick start

```bash
python downloaderr.py
```

You need **Python 3.9+** and, ideally, **ffmpeg** (`winget install ffmpeg` / `brew install ffmpeg` / `sudo apt install ffmpeg`). yt-dlp is installed from the menu on first run.

Then just pick a number and paste a link. That's it.

## Good to know

| I want to... | Menu |
|---|---|
| Use my browser cookies (age gate, private videos) | `3` then `1` |
| Limit download speed (default 2 MB/s) | `4` then `10` |
| Switch language | `4` then `9` |
| Fix a download that suddenly broke | `8` (update yt-dlp) |

> Sign in or confirm the age prompt in your browser first, then close the browser (needed for Chrome/Edge, usually not for Firefox).

<details>
<summary>Troubleshooting</summary>

- **Fails right away:** update yt-dlp (`8`), sites change often.
- **Age prompt still blocks:** use browser cookies (`3`).
- **Low quality or no merged file:** install ffmpeg.
- **Chrome/Edge cookies fail on Windows:** close the browser completely, or use Firefox / an exported `cookies.txt`.

</details>

## Notes

DRM-protected content (Netflix, Disney+, paid platforms with encrypted streams) is not supported and this tool does not try to bypass DRM. For personal use with content you have the right to save; respect copyright and site terms. Not affiliated with yt-dlp.

<details>
<summary>По-русски</summary>

Лёгкая консольная обёртка над yt-dlp: меню с цифрами вместо длинных команд. Работает локально, без сайтов-посредников и рекламы. Куки из браузера (по умолчанию Firefox), лимит скорости, смена языка (`4` → `9`). Если загрузка не идёт, обнови yt-dlp (пункт `8`). Без обхода DRM.

</details>

## License

MIT
