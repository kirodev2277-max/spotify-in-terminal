from spotiterm.cli import detect_platform, spotify_artist_url, spotify_search_url


def test_spotify_search_url_encodes_query():
  assert spotify_search_url("lo fi beats") == "https://open.spotify.com/search/lo+fi+beats"


def test_spotify_artist_url_uses_id():
  assert spotify_artist_url("123") == "https://open.spotify.com/artist/123"


def test_detect_platform_windows():
  support = detect_platform("Windows")
  assert support.name == "Windows"
  assert support.open_command == "start"


def test_detect_platform_arch_is_linux():
  support = detect_platform("Linux")
  assert support.open_command == "xdg-open"
  assert "Arch:" in support.notes[0]
