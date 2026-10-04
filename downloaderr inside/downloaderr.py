#!/usr/bin/env python3
"""
downloaderr - lightweight console menu on top of yt-dlp.

Run:   python downloaderr.py
Needs: Python 3.9+, yt-dlp (the script offers to install it), ffmpeg (recommended).
Settings are stored in downloaderr_settings.json next to the script.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

APP_NAME = "DOWNLOADERR"

# ----------------------------------------------------------------------------
# Colors
# ----------------------------------------------------------------------------
os.system("")  # enables ANSI colors in cmd/PowerShell on Windows

C = {
    "r": "\033[91m", "g": "\033[92m", "y": "\033[93m",
    "b": "\033[94m", "m": "\033[95m", "c": "\033[96m",
    "w": "\033[97m", "d": "\033[90m", "0": "\033[0m",
}


def col(text, color):
    return f"{C[color]}{text}{C['0']}"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


# ----------------------------------------------------------------------------
# Translations
# ----------------------------------------------------------------------------
TR = {
    "en": {
        "subtitle": "console downloader powered by yt-dlp",
        "not_installed": "not installed", "found": "found", "missing": "missing",
        "on": "ON", "off": "OFF", "back": "Back", "enter": "Press Enter to return...",
        "enter_short": "Enter...",
        "mode_video": "video", "mode_audio": "audio only", "best": "best",
        "lbl_mode": "Mode", "lbl_cookies": "Cookies", "lbl_speed": "Speed",
        "lbl_age": "Age gate", "lbl_playlists": "Playlists", "lbl_folder": "Folder",
        "nolimit": "no limit",
        "ck_browser": "browser: {b}{p}", "ck_file": "file: {f}", "ck_notset": "not set",
        "ck_off": "not used", "default_profile": "default",
        "m_download": "Download by link", "m_batch": "Download from a list file",
        "m_cookies": "Cookies (browser / file)", "m_settings": "Settings",
        "m_formats": "Show available formats for a link",
        "m_update": "Install / update yt-dlp", "m_exit": "Exit",
        "paste_links": "Paste a link (or several separated by spaces). Empty = back.",
        "batch_prompt": "Path to a text file with links (one per line).",
        "file_not_found": "File not found.", "links_found": "Links found: {n}",
        "ytdlp_missing": "yt-dlp is not installed. Use the install/update option.",
        "ffmpeg_missing": "Warning: ffmpeg not found. High quality merging and audio conversion may fail.",
        "err_hint": "Download failed. Common causes: outdated yt-dlp (option 8), cookies needed (option 3), private or region-locked video.",
        "done": "Done: {ok} ok, {fail} failed.", "folder_line": "Folder: {f}",
        "interrupted": "Interrupted.",
        "installing": "Installing / updating yt-dlp...",
        "install_ok": "Done. yt-dlp version: {v}",
        "install_fail": "Could not install yt-dlp. Try manually: pip install -U yt-dlp",
        "ytdlp_nf": "yt-dlp not found.", "install_now": "Install now? [Y/n]: ",
        "yes_answers": ("", "y", "yes"),
        "ck_title": "COOKIE SETTINGS",
        "ck_1": "Use cookies from browser   (now: {b})",
        "ck_2": "Choose browser",
        "ck_3": "Browser profile (optional, now: {p})",
        "ck_4": "Use a cookies.txt file",
        "ck_5": "Disable cookies",
        "ck_hint": "Tip: open the site in your browser first, confirm the age prompt,\nlog in if needed, and close the browser (especially Chrome/Edge).",
        "ck_set": "Cookies will be taken from {b}.",
        "profile_prompt": "Profile name or path (empty = default):",
        "path_prompt": "Path to cookies.txt (Netscape format):",
        "s_title": "SETTINGS",
        "s_mode": "Mode: video / audio          (now: {v})",
        "s_quality": "Video quality                (now: {v})",
        "s_audio": "Audio format                 (now: {v})",
        "s_folder": "Download folder",
        "s_playlist": "Whole playlists              {v}",
        "s_age": "Age confirmation bypass      {v}",
        "s_meta": "Embed tags and thumbnail     {v}",
        "s_archive": "Skip already downloaded      {v}",
        "s_lang": "Language: English / Russian  (now: {v})",
        "s_rate": "Speed limit                  (now: {v})",
        "s_reset": "Reset settings",
        "choose_browser": "Browser:", "choose_quality": "Maximum video height:",
        "choose_audio": "Audio format:", "new_folder": "New folder:",
        "rate_title": "Download speed limit (MegaBYTES per second, not megabits):",
        "rate_custom": "Custom value (e.g. 750K or 3M)", "rate_off": "No limit",
        "rate_value": "Value: ", "rate_bad": "Invalid format. Examples: 500K, 2M.",
        "formats_prompt": "Link to list formats for:",
        "lang_name": "English",
    },
    "ru": {
        "subtitle": "консольный загрузчик на базе yt-dlp",
        "not_installed": "не установлен", "found": "есть", "missing": "нет",
        "on": "ВКЛ", "off": "ВЫКЛ", "back": "Назад", "enter": "Enter - вернуться в меню...",
        "enter_short": "Enter...",
        "mode_video": "видео", "mode_audio": "только аудио", "best": "лучшее",
        "lbl_mode": "Режим", "lbl_cookies": "Куки", "lbl_speed": "Скорость",
        "lbl_age": "Возраст", "lbl_playlists": "Плейлисты", "lbl_folder": "Папка",
        "nolimit": "без лимита",
        "ck_browser": "браузер: {b}{p}", "ck_file": "файл: {f}", "ck_notset": "не указан",
        "ck_off": "не используются", "default_profile": "по умолчанию",
        "m_download": "Скачать по ссылке", "m_batch": "Скачать списком из файла",
        "m_cookies": "Куки (браузер / файл)", "m_settings": "Настройки",
        "m_formats": "Показать доступные форматы ссылки",
        "m_update": "Установить/обновить yt-dlp", "m_exit": "Выход",
        "paste_links": "Вставь ссылку (или несколько через пробел). Пусто = назад.",
        "batch_prompt": "Путь к текстовому файлу со ссылками (по одной в строке).",
        "file_not_found": "Файл не найден.", "links_found": "Найдено ссылок: {n}",
        "ytdlp_missing": "yt-dlp не установлен. Выбери пункт установки/обновления.",
        "ffmpeg_missing": "Внимание: ffmpeg не найден. Высокое качество и конвертация аудио могут не работать.",
        "err_hint": "Ошибка загрузки. Частые причины: старая версия yt-dlp (пункт 8), нужны куки (пункт 3), видео приватное или недоступно в регионе.",
        "done": "Готово: {ok} успешно, {fail} с ошибкой.", "folder_line": "Папка: {f}",
        "interrupted": "Прервано.",
        "installing": "Установка/обновление yt-dlp...",
        "install_ok": "Готово. Версия yt-dlp: {v}",
        "install_fail": "Не получилось установить yt-dlp. Попробуй вручную: pip install -U yt-dlp",
        "ytdlp_nf": "yt-dlp не найден.", "install_now": "Установить сейчас? [Y/n]: ",
        "yes_answers": ("", "y", "д", "да"),
        "ck_title": "НАСТРОЙКА КУКИ",
        "ck_1": "Брать куки из браузера   (сейчас: {b})",
        "ck_2": "Выбрать браузер",
        "ck_3": "Профиль браузера (необязательно, сейчас: {p})",
        "ck_4": "Использовать файл cookies.txt",
        "ck_5": "Отключить куки",
        "ck_hint": "Подсказка: сначала зайди на сайт в браузере, нажми «Мне 18 лет»,\nпри необходимости войди в аккаунт и закрой браузер (особенно Chrome/Edge).",
        "ck_set": "Куки будут браться из {b}.",
        "profile_prompt": "Имя профиля или путь (пусто = по умолчанию):",
        "path_prompt": "Путь к cookies.txt (формат Netscape):",
        "s_title": "НАСТРОЙКИ",
        "s_mode": "Режим: видео / аудио         (сейчас: {v})",
        "s_quality": "Качество видео               (сейчас: {v})",
        "s_audio": "Формат аудио                 (сейчас: {v})",
        "s_folder": "Папка для загрузок",
        "s_playlist": "Плейлисты целиком            {v}",
        "s_age": "Обход подтверждения возраста {v}",
        "s_meta": "Вшивать теги и обложку       {v}",
        "s_archive": "Не качать повторно           {v}",
        "s_lang": "Язык: English / Русский      (сейчас: {v})",
        "s_rate": "Лимит скорости               (сейчас: {v})",
        "s_reset": "Сбросить настройки",
        "choose_browser": "Браузер:", "choose_quality": "Максимальная высота кадра:",
        "choose_audio": "Формат аудио:", "new_folder": "Новая папка:",
        "rate_title": "Лимит скорости загрузки (МБайт/с, а не Мбит/с):",
        "rate_custom": "Свое значение (например 750K или 3M)", "rate_off": "Без лимита",
        "rate_value": "Значение: ", "rate_bad": "Неверный формат. Примеры: 500K, 2M.",
        "formats_prompt": "Ссылка для просмотра доступных форматов:",
        "lang_name": "Русский",
    },
}

LANG = "en"


def t(key, **kw):
    v = TR.get(LANG, TR["en"]).get(key, TR["en"].get(key, key))
    return v.format(**kw) if kw and isinstance(v, str) else v


# ----------------------------------------------------------------------------
# Settings
# ----------------------------------------------------------------------------
SETTINGS_FILE = Path(__file__).with_name("downloaderr_settings.json")

DEFAULTS = {
    "lang": "en",                 # en / ru
    "output_dir": str(Path.home() / "Downloads" / "downloaderr"),
    "quality": "best",            # best / 2160 / 1440 / 1080 / 720 / 480 / 360
    "mode": "video",              # video / audio
    "audio_format": "mp3",        # mp3 / m4a / opus / flac / wav
    "rate_limit": "2M",           # 500K, 1M, 2M, 5M...  empty = no limit
    "playlist": False,            # download whole playlists
    "cookie_mode": "off",         # off / browser / file
    "browser": "firefox",         # firefox / chrome / edge / brave / ...
    "browser_profile": "",        # empty = default profile
    "cookie_file": "",            # path to cookies.txt
    "age_bypass": True,           # send age_verified=1 cookie on age-gated sites
    "embed_meta": True,           # embed tags / thumbnail
    "save_archive": False,        # skip already downloaded items
}

BROWSERS = ["firefox", "chrome", "edge", "brave", "opera", "vivaldi", "chromium", "safari"]
QUALITIES = ["best", "2160", "1440", "1080", "720", "480", "360"]
AUDIO_FORMATS = ["mp3", "m4a", "opus", "flac", "wav"]

# Sites that show an "are you 18?" prompt
AGE_GATE_HINTS = ("pornhub.", "xvideos.", "xhamster.", "redtube.", "youporn.", "spankbang.")


def load_settings():
    s = dict(DEFAULTS)
    if SETTINGS_FILE.exists():
        try:
            s.update(json.loads(SETTINGS_FILE.read_text(encoding="utf-8")))
        except Exception:
            pass
    return s


def save_settings(s):
    try:
        SETTINGS_FILE.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        print(col(f"Could not save settings: {e}", "r"))


def apply_lang(s):
    global LANG
    LANG = s.get("lang", "en") if s.get("lang") in TR else "en"


# ----------------------------------------------------------------------------
# yt-dlp / ffmpeg
# ----------------------------------------------------------------------------
def ytdlp_version():
    try:
        r = subprocess.run([sys.executable, "-m", "yt_dlp", "--version"],
                           capture_output=True, text=True, check=True)
        return r.stdout.strip()
    except Exception:
        return None


def ytdlp_available():
    return ytdlp_version() is not None


def install_or_update_ytdlp():
    print(col("\n" + t("installing"), "c"))
    cmd = [sys.executable, "-m", "pip", "install", "-U", "yt-dlp[default]"]
    r = subprocess.run(cmd)
    if r.returncode != 0:
        # some systems need this flag for "externally managed" Python
        subprocess.run(cmd + ["--break-system-packages"])
    v = ytdlp_version()
    print(col(t("install_ok", v=v), "g") if v else col(t("install_fail"), "r"))


def has_ffmpeg():
    return shutil.which("ffmpeg") is not None


def needs_age_cookie(url):
    u = url.lower()
    return any(h in u for h in AGE_GATE_HINTS)


def cookie_args(s, url=None):
    """Cookie-related yt-dlp arguments. Returns (args, cookies_used)."""
    if s["cookie_mode"] == "browser":
        spec = s["browser"] + (f":{s['browser_profile']}" if s["browser_profile"] else "")
        return ["--cookies-from-browser", spec], True
    if s["cookie_mode"] == "file" and s["cookie_file"]:
        return ["--cookies", s["cookie_file"]], True
    if s["age_bypass"] and url and needs_age_cookie(url):
        return ["--add-headers", "Cookie: age_verified=1"], False
    return [], False


def build_command(url, s):
    out_dir = Path(s["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [sys.executable, "-m", "yt_dlp", "--newline", "--no-colors", "--progress"]

    # Format
    if s["mode"] == "audio":
        cmd += ["-x", "--audio-format", s["audio_format"], "--audio-quality", "0"]
    else:
        if s["quality"] == "best":
            cmd += ["-f", "bv*+ba/b"]
        else:
            h = s["quality"]
            cmd += ["-f", f"bv*[height<={h}]+ba/b[height<={h}]/b"]
        cmd += ["--merge-output-format", "mp4"]

    # Speed limit
    if s.get("rate_limit"):
        cmd += ["--limit-rate", s["rate_limit"]]

    # Playlists
    cmd += ["--yes-playlist"] if s["playlist"] else ["--no-playlist"]

    # Cookies / age gate (the manual age cookie is skipped when browser cookies are used)
    cmd += cookie_args(s, url)[0]

    # Metadata
    if s["embed_meta"] and has_ffmpeg():
        cmd += ["--embed-metadata"]
        if s["mode"] == "audio":
            cmd += ["--embed-thumbnail"]

    if s["save_archive"]:
        cmd += ["--download-archive", str(out_dir / "archive.txt")]

    cmd += ["-o", str(out_dir / "%(title).150B [%(id)s].%(ext)s")]
    cmd += [url]
    return cmd


def run_download(urls, s):
    if not ytdlp_available():
        print(col(t("ytdlp_missing"), "r"))
        return
    if not has_ffmpeg():
        print(col(t("ffmpeg_missing"), "y"))

    ok, fail = 0, 0
    for i, url in enumerate(urls, 1):
        print(col(f"\n[{i}/{len(urls)}] {url}", "c"))
        try:
            r = subprocess.run(build_command(url, s))
        except KeyboardInterrupt:
            print(col("\n" + t("interrupted"), "y"))
            break
        if r.returncode == 0:
            ok += 1
        else:
            fail += 1
            print(col(t("err_hint"), "r"))
    print(col("\n" + t("done", ok=ok, fail=fail), "g" if not fail else "y"))
    print(col(t("folder_line", f=s["output_dir"]), "d"))


# ----------------------------------------------------------------------------
# UI
# ----------------------------------------------------------------------------
def onoff(v):
    return col(t("on"), "g") if v else col(t("off"), "r")


def cookie_status(s):
    if s["cookie_mode"] == "browser":
        p = f" ({s['browser_profile']})" if s["browser_profile"] else ""
        return col(t("ck_browser", b=s["browser"], p=p), "g")
    if s["cookie_mode"] == "file":
        return col(t("ck_file", f=s["cookie_file"] or t("ck_notset")), "g")
    return col(t("ck_off"), "d")


def mode_text(s):
    if s["mode"] == "audio":
        return f"{t('mode_audio')} ({s['audio_format']})"
    q = t("best") if s["quality"] == "best" else s["quality"] + "p"
    return f"{t('mode_video')} {q}"


def rate_text(s):
    return s["rate_limit"] + "B/s" if s.get("rate_limit") else t("nolimit")


def header(s):
    clear()
    v = ytdlp_version()
    ff = col(t("found"), "g") if has_ffmpeg() else col(t("missing"), "y")
    print(col("=" * 62, "c"))
    print("  " + col(APP_NAME, "w") + col("  -  " + t("subtitle"), "d"))
    print(col("=" * 62, "c"))
    print(f"  yt-dlp : {col(v, 'g') if v else col(t('not_installed'), 'r')}    ffmpeg : {ff}")
    print(f"  {t('lbl_mode')}: {col(mode_text(s), 'w')}")
    print(f"  {t('lbl_cookies')}: {cookie_status(s)}")
    print(f"  {t('lbl_speed')}: {col(rate_text(s), 'g' if s.get('rate_limit') else 'y')}")
    print(f"  {t('lbl_age')}: {onoff(s['age_bypass'])}    {t('lbl_playlists')}: {onoff(s['playlist'])}")
    print(f"  {t('lbl_folder')}: {col(s['output_dir'], 'd')}")
    print(col("-" * 62, "c"))


def item(num, text):
    print(f"  {col(str(num), 'c')}. {text}")


def choose(title, options, current=None):
    print(col(f"\n{title}", "y"))
    for i, o in enumerate(options, 1):
        item(i, o + (col(" <-", "g") if o == current else ""))
    item(0, t("back"))
    raw = input(col("\n> ", "m")).strip()
    if raw.isdigit() and 1 <= int(raw) <= len(options):
        return options[int(raw) - 1]
    return None


def pause(key="enter"):
    input(col(t(key), "d"))


def menu_download(s):
    print(col("\n" + t("paste_links"), "y"))
    raw = input(col("> ", "m")).strip()
    if raw:
        run_download(raw.split(), s)
        pause()


def menu_batch_file(s):
    print(col("\n" + t("batch_prompt"), "y"))
    p = input(col("> ", "m")).strip().strip('"')
    if not p:
        return
    f = Path(p)
    if not f.exists():
        print(col(t("file_not_found"), "r"))
        pause("enter_short")
        return
    urls = [l.strip() for l in f.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")]
    print(col(t("links_found", n=len(urls)), "c"))
    run_download(urls, s)
    pause()


def menu_cookies(s):
    while True:
        header(s)
        print(col("  " + t("ck_title"), "y"))
        item(1, t("ck_1", b=col(s["browser"], "w")))
        item(2, t("ck_2"))
        item(3, t("ck_3", p=col(s["browser_profile"] or t("default_profile"), "w")))
        item(4, t("ck_4"))
        item(5, t("ck_5"))
        item(0, t("back"))
        print(col("\n  " + t("ck_hint").replace("\n", "\n  "), "d"))
        ch = input(col("\n> ", "m")).strip()
        if ch == "1":
            s["cookie_mode"] = "browser"
            print(col(t("ck_set", b=s["browser"]), "g"))
            pause("enter_short")
        elif ch == "2":
            b = choose(t("choose_browser"), BROWSERS, s["browser"])
            if b:
                s["browser"] = b
                s["cookie_mode"] = "browser"
        elif ch == "3":
            print(col(t("profile_prompt"), "y"))
            s["browser_profile"] = input(col("> ", "m")).strip().strip('"')
        elif ch == "4":
            print(col(t("path_prompt"), "y"))
            p = input(col("> ", "m")).strip().strip('"')
            if p and Path(p).exists():
                s["cookie_file"] = p
                s["cookie_mode"] = "file"
            else:
                print(col(t("file_not_found"), "r"))
                pause("enter_short")
        elif ch == "5":
            s["cookie_mode"] = "off"
        elif ch == "0":
            return
        save_settings(s)


def menu_rate_limit(s):
    presets = [("500K  (~4 Mbit/s)", "500K"), ("1M    (~8 Mbit/s)", "1M"),
               ("2M    (~16 Mbit/s)", "2M"), ("5M    (~40 Mbit/s)", "5M"),
               ("10M   (~80 Mbit/s)", "10M")]
    print(col("\n" + t("rate_title"), "y"))
    for i, (label, _) in enumerate(presets, 1):
        item(i, label)
    item(6, t("rate_custom"))
    item(7, t("rate_off"))
    item(0, t("back"))
    ch = input(col("\n> ", "m")).strip()
    if ch.isdigit() and 1 <= int(ch) <= len(presets):
        s["rate_limit"] = presets[int(ch) - 1][1]
    elif ch == "6":
        v = input(col(t("rate_value"), "m")).strip().upper()
        if v and v[:-1].replace(".", "", 1).isdigit() and v[-1] in "KMG":
            s["rate_limit"] = v
        elif v.isdigit():
            s["rate_limit"] = v  # bytes per second
        else:
            print(col(t("rate_bad"), "r"))
            pause("enter_short")
    elif ch == "7":
        s["rate_limit"] = ""


def menu_settings(s):
    while True:
        header(s)
        print(col("  " + t("s_title"), "y"))
        item(1, t("s_mode", v=col(s["mode"], "w")))
        item(2, t("s_quality", v=col(s["quality"], "w")))
        item(3, t("s_audio", v=col(s["audio_format"], "w")))
        item(4, t("s_folder"))
        item(5, t("s_playlist", v=onoff(s["playlist"])))
        item(6, t("s_age", v=onoff(s["age_bypass"])))
        item(7, t("s_meta", v=onoff(s["embed_meta"])))
        item(8, t("s_archive", v=onoff(s["save_archive"])))
        item(9, t("s_lang", v=col(t("lang_name"), "w")))
        item(10, t("s_rate", v=col(rate_text(s), "w")))
        item(11, t("s_reset"))
        item(0, t("back"))
        ch = input(col("\n> ", "m")).strip()
        if ch == "1":
            s["mode"] = "audio" if s["mode"] == "video" else "video"
        elif ch == "2":
            q = choose(t("choose_quality"), QUALITIES, s["quality"])
            if q:
                s["quality"] = q
        elif ch == "3":
            a = choose(t("choose_audio"), AUDIO_FORMATS, s["audio_format"])
            if a:
                s["audio_format"] = a
        elif ch == "4":
            print(col(t("new_folder"), "y"))
            p = input(col("> ", "m")).strip().strip('"')
            if p:
                s["output_dir"] = p
        elif ch == "5":
            s["playlist"] = not s["playlist"]
        elif ch == "6":
            s["age_bypass"] = not s["age_bypass"]
        elif ch == "7":
            s["embed_meta"] = not s["embed_meta"]
        elif ch == "8":
            s["save_archive"] = not s["save_archive"]
        elif ch == "9":
            s["lang"] = "ru" if s.get("lang", "en") == "en" else "en"
            apply_lang(s)
        elif ch == "10":
            menu_rate_limit(s)
        elif ch == "11":
            s.clear()
            s.update(DEFAULTS)
            apply_lang(s)
        elif ch == "0":
            return
        save_settings(s)


def menu_formats(s):
    print(col("\n" + t("formats_prompt"), "y"))
    url = input(col("> ", "m")).strip()
    if not url:
        return
    subprocess.run([sys.executable, "-m", "yt_dlp", "-F", url] + cookie_args(s, url)[0])
    pause()


def main():
    s = load_settings()
    apply_lang(s)

    if not ytdlp_available():
        header(s)
        print(col(t("ytdlp_nf"), "y"))
        if input(t("install_now")).strip().lower() in t("yes_answers"):
            install_or_update_ytdlp()
            pause("enter_short")

    while True:
        header(s)
        item(1, t("m_download"))
        item(2, t("m_batch"))
        item(3, t("m_cookies"))
        item(4, t("m_settings"))
        item(5, t("m_formats"))
        item(8, t("m_update"))
        item(0, t("m_exit"))
        ch = input(col("\n> ", "m")).strip()

        if ch == "1":
            menu_download(s)
        elif ch == "2":
            menu_batch_file(s)
        elif ch == "3":
            menu_cookies(s)
        elif ch == "4":
            menu_settings(s)
        elif ch == "5":
            menu_formats(s)
        elif ch == "8":
            install_or_update_ytdlp()
            pause("enter_short")
        elif ch == "0":
            break

    save_settings(s)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
