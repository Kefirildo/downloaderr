Enter file contests here

its downloadrr
A tiny single-file console menu on top of yt-dlp. Download video or audio from YouTube and thousands of other sites without typing long commands.
It runs entirely on your machine: no third-party "downloader" website in the middle, no ads, no server-side throttling. Speed is whatever the source site and your connection allow, and you can cap it yourself.
Features
Numbered colorful console menu
Download by link, several links at once, or from a text file (one link per line)
Video quality up to 2160p, or audio only (mp3, m4a, opus, flac, wav)
Cookie import from your browser (Firefox by default; Chrome, Edge, Brave and others also supported) or from a `cookies.txt` file
Automatic age-confirmation cookie for sites that show an "are you 18?" prompt
Download speed limiter so you don't saturate your home network
Optional: whole playlists, embedded tags and thumbnails, skip already downloaded items
English / Russian interface (Settings, option 9)
One-click install / update of yt-dlp from the menu
Requirements
Python 3.9+
ffmpeg (recommended, needed to merge video and audio streams and to convert audio)
Windows: `winget install ffmpeg`
macOS: `brew install ffmpeg`
Linux: `sudo apt install ffmpeg`
yt-dlp (the script offers to install it on first run)

Pick an option by typing its number and pressing Enter. Settings are saved to `its_downloadrr_settings.json` next to the script.
Cookies (for age-gated, private or members-only videos)
Open the site in your browser, confirm the age prompt, log in if needed.
Close the browser (required for Chrome/Edge, usually not for Firefox).
In the menu: 3. Cookies -> 1. Use cookies from browser. Change the browser with option 2.
Speed limit
4. Settings -> 10. Speed limit. Values are in megaBYTES per second (`2M` is roughly 16 Mbit/s). Default is `2M`.
Troubleshooting
Download fails right away: update yt-dlp (main menu, option 8). Sites change often.
Age prompt still blocks: use browser cookies (see above).
Only low quality / no merged file: install ffmpeg.
Cookies from Chrome/Edge fail on Windows: close the browser completely, or use Firefox / an exported `cookies.txt`.
Disclaimer
For personal use with content you have the right to save. Respect copyright and the terms of the sites you use. You are responsible for how you use this tool. Not affiliated with yt-dlp.

---

По-русски
Лёгкая консольная обёртка над yt-dlp: меню с цифрами вместо длинных команд. Работает локально, без сайтов-посредников и рекламы.
Запуск очевидного файла .py
Что умеет: скачивание по ссылке или списком, выбор качества и режим «только аудио», импорт куки из браузера (по умолчанию Firefox), автоматическое подтверждение возраста, лимит скорости (по умолчанию 2 МБ/с), смена языка (Настройки, пункт 9), установка и обновление yt-dlp из меню.
Нужны Python 3.9+ и желательно ffmpeg. Если загрузка не идёт, сначала обнови yt-dlp (пункт 8 главного меню).
