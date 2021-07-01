"""A video playlist class."""

from .video_library import VideoLibrary


class Playlist(VideoLibrary):
    """A class used to represent a Playlist."""

    def __init__(self, playlist_name: str):
        self._name = playlist_name
        self._videos = {}
    
    @property
    def name(self) -> str:
        """Returns the name of a playlist."""
        return self._name
