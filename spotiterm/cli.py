from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

HELPFUL_TRACKS = [
  "Daft Punk - Around the World",
  "Tame Impala - Borderline",
  "The Weeknd - Blinding Lights",
  "ODESZA - A Moment Apart",
  "Tycho - Awake",
]


@dataclass(frozen=True)
class PlatformSupport:
  name: str
  open_command: str
  notes: tuple[str, ...]


def detect_platform(system: str | None = None) -> PlatformSupport:
  detected = (system or platform.system()).lower()

  if detected == "windows":
    return PlatformSupport(
      name="Windows",
      open_command="start",
      notes=(
        "Works in Windows Terminal, PowerShell, Command Prompt, and WSL.",
        "Install Python from winget, the Microsoft Store, or python.org.",
      ),
    )

  if detected == "darwin":
    return PlatformSupport(
      name="macOS",
      open_command="open",
      notes=("Works in Terminal.app, iTerm2, and other modern terminals.",),
    )

  if detected == "linux":
    distro = get_linux_distro()
    return PlatformSupport(
      name=f"Linux{f' ({distro})' if distro else ''}",
      open_command="xdg-open",
      notes=(
        "Arch: sudo pacman -S python xdg-utils",
        "Debian/Ubuntu: sudo apt install python3 xdg-utils",
        "Fedora: sudo dnf install python3 xdg-utils",
        "openSUSE: sudo zypper install python3 xdg-utils",
      ),
    )

  return PlatformSupport(
    name=platform.system() or "Unknown",
    open_command="manual browser open",
    notes=("Copy the printed Spotify URL into a browser if auto-open is unavailable.",),
  )


def get_linux_distro() -> str:
  try:
    with open("/etc/os-release", encoding="utf-8") as file:
      values = {}
      for line in file:
        if "=" not in line:
          continue
        key, value = line.rstrip().split("=", 1)
        values[key] = value.strip('"')
      return values.get("PRETTY_NAME") or values.get("NAME") or ""
  except OSError:
    return ""


def spotify_search_url(query: str) -> str:
  return "https://open.spotify.com/search/" + urlencode({"q": query})[2:]


def spotify_artist_url(artist_id: str) -> str:
  return f"https://open.spotify.com/artist/{artist_id}"


def open_url(url: str, opener: str | None = None) -> bool:
  system = platform.system().lower()
  command = opener or detect_platform().open_command

  try:
    if system == "windows" or command == "start":
      subprocess.Popen(["cmd", "/c", "start", "", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif command in {"open", "xdg-open"}:
      subprocess.Popen([command, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
      return False
    return True
  except OSError:
    return False


def print_banner() -> None:
  print(
    r"""
  ____             _   _ _____
 / ___| _ __   ___| |_(_)_   _|__ _ __ _ __ ___
 \___ \| '_ \ / _ \ __| | | |/ _ \ '__| '_ ` _ \
  ___) | |_) | (_) | |_| | | |  __/ |  | | | | | |
 |____/| .__/ \___/ \__|_| |_|\___|_|  |_| |_| |_|
       |_|
    """
  )


def print_recommendations(seed: str) -> None:
  print("\nRecommended terminal vibes:")
  offset = sum(ord(char) for char in seed) % len(HELPFUL_TRACKS)
  for index in range(5):
    track = HELPFUL_TRACKS[(offset + index) % len(HELPFUL_TRACKS)]
    print(f"  {index + 1}. {track}")


def fetch_spotify_status() -> str:
  request = Request("https://open.spotify.com", headers={"User-Agent": "spotiterm/0.1"})
  try:
    with urlopen(request, timeout=5) as response:
      return f"Spotify web reachable: HTTP {response.status}"
  except HTTPError as error:
    return f"Spotify web reachable with HTTP {error.code}"
  except (OSError, URLError) as error:
    return f"Spotify web check failed: {error}"


def run(args: Sequence[str] | None = None) -> int:
  parser = argparse.ArgumentParser(
    prog="spotiterm",
    description="A cross-platform terminal companion for opening Spotify searches fast.",
  )
  parser.add_argument("query", nargs="*", help="Song, artist, playlist, album, or mood to search")
  parser.add_argument("--artist-id", help="Open a Spotify artist URL by ID instead of searching")
  parser.add_argument("--no-open", action="store_true", help="Print the URL without opening a browser")
  parser.add_argument("--status", action="store_true", help="Check whether Spotify Web is reachable")
  parser.add_argument("--platform", action="store_true", help="Show detected OS/distro support details")
  parsed = parser.parse_args(args)

  print_banner()
  support = detect_platform()

  if parsed.platform:
    print(f"Detected: {support.name}")
    print(f"Browser opener: {support.open_command}")
    for note in support.notes:
      print(f"- {note}")
    return 0

  if parsed.status:
    print(fetch_spotify_status())
    return 0

  query = " ".join(parsed.query).strip()
  if parsed.artist_id:
    url = spotify_artist_url(parsed.artist_id.strip())
    label = f"artist:{parsed.artist_id.strip()}"
  else:
    label = query or "focus playlist"
    url = spotify_search_url(label)

  print(f"Detected: {support.name}")
  print_recommendations(label)
  print(f"\nSpotify URL: {url}")

  if parsed.no_open:
    print("Not opening browser because --no-open was set.")
    return 0

  opened = open_url(url)
  time.sleep(0.15)
  if opened:
    print("Opened Spotify in your default browser.")
    return 0

  print("Could not auto-open a browser. Copy the URL above instead.")
  return 1


def main() -> None:
  raise SystemExit(run())
