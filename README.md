# SpotiTerm

A cool terminal Spotify companion that works on Windows, Arch Linux, Ubuntu/Debian, Fedora, openSUSE, other Linux distros, macOS, and WSL.

It searches Spotify from your terminal and opens the result in your default browser.

## Features

- Fast Spotify search from the terminal
- Opens links automatically on Windows, Linux, macOS, and WSL
- Linux distro hints for Arch, Debian/Ubuntu, Fedora, and openSUSE
- `--no-open` mode for servers, SSH sessions, CI, and headless terminals
- `--status` command to check whether Spotify Web is reachable
- Zero runtime dependencies beyond Python

## Install

### Windows

Install Python:

```powershell
winget install Python.Python.3.12
```

Then run:

```powershell
python -m pip install .
spotiterm "night drive"
```

### Arch Linux

```bash
sudo pacman -S python xdg-utils
python -m pip install .
spotiterm "arch linux coding playlist"
```

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install python3 python3-pip xdg-utils
python3 -m pip install .
spotiterm "lofi beats"
```

### Fedora

```bash
sudo dnf install python3 python3-pip xdg-utils
python3 -m pip install .
spotiterm "focus flow"
```

### openSUSE

```bash
sudo zypper install python3 python3-pip xdg-utils
python3 -m pip install .
spotiterm "synthwave"
```

### Any other Linux distro

Install Python 3.10+ and `xdg-utils` with your distro package manager, then:

```bash
python3 -m pip install .
spotiterm "terminal music"
```

## Usage

Search Spotify:

```bash
spotiterm "daft punk around the world"
```

Print a URL without opening the browser:

```bash
spotiterm --no-open "study playlist"
```

Open an artist by Spotify ID:

```bash
spotiterm --artist-id 4tZwfgrHOc3mvqYlEYSvVi
```

Show platform support info:

```bash
spotiterm --platform
```

Check Spotify Web reachability:

```bash
spotiterm --status
```

Run directly without installing:

```bash
python -m spotiterm "workout mix"
```

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
pytest
```

## Notes

This app does not require Spotify API keys. It opens public Spotify Web search URLs, so it works immediately.
