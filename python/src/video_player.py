"""A video player class."""

import random
from .video_library import VideoLibrary
from .video_playlist import Playlist


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playlists = {}
        self._playing_video = None
        self._is_video_paused = False

    def number_of_videos(self):
        """Returns the number of videos."""
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        videos = self._video_library.get_all_videos()
        sorted_videos = sorted(videos, key=lambda video: video.title)
        print("Here's a list of all available videos:")
        for video in sorted_videos:
            tags = " ".join(video.tags)
            flag_reason = video.flag_reason
            flag_msg = ""
            if flag_reason != None:
                flag_msg = f"- FLAGGED (reason: {flag_reason or 'Not supplied'})"
            print(f"{video.title} ({video.video_id}) [{tags}] {flag_msg}")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        self._is_video_paused = False
        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot play video: Video does not exist")
        elif video.flag_reason != None:
            flag_msg = video.flag_reason or 'Not supplied'
            print(f"Cannot play video: Video is currently flagged (reason: {flag_msg})")
        elif self._playing_video == None:
            self._playing_video = video
            print(f"Playing video: {video.title}")
        else:
            print(f"Stopping video: {self._playing_video.title}")
            self._playing_video = video
            print(f"Playing video: {self._playing_video.title}")

    def stop_video(self):
        """Stops the current video."""
        video = self._playing_video
        if video == None:
            print("Cannot stop video: No video is currently playing")
        else:
            print(f"Stopping video: {video.title}")
            self._playing_video = None

    def play_random_video(self):
        """Plays a random video from the video library."""
        videos = self._video_library.get_all_videos()
        unflagged_videos = [vid for vid in videos if vid.flag_reason == None]
        if len(unflagged_videos) == 0:
            print("No videos available")
        else:
            rand_video = random.choice(unflagged_videos)
            self.play_video(rand_video.video_id)

    def pause_video(self):
        """Pauses the current video."""
        video = self._playing_video
        is_paused = self._is_video_paused
        if video == None:
            print("Cannot pause video: No video is currently playing")
        elif is_paused:
            print(f"Video already paused: {video.title}")
        else:
            self._is_video_paused = True
            print(f"Pausing video: {video.title}")

    def continue_video(self):
        """Resumes playing the current video."""
        video = self._playing_video
        is_paused = self._is_video_paused
        if video == None:
            print("Cannot continue video: No video is currently playing")
        elif is_paused:
            self._is_video_paused = False
            print(f"Continuing video: {video.title}")
        else:
            print(f"Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""
        video = self._playing_video
        if video == None:
            print("No video is currently playing")
        else:
            title = video.title
            video_id = video.video_id
            tags = " ".join(video.tags)
            play_status = "- PAUSED" if self._is_video_paused else ""
            print(f"Currently playing: {title} ({video_id}) [{tags}] {play_status}")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_id = playlist_name.upper()
        name_exists = self._playlists.get(playlist_id) != None
        if name_exists:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            playlist = Playlist(playlist_name)
            self._playlists[playlist_id] = playlist
            print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        video = self._video_library.get_video(video_id)
        playlist_id = playlist_name.upper()
        playlist = self._playlists.get(playlist_id)
        if playlist == None:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
        elif not video:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
        elif video.flag_reason != None:
            flag_msg = video.flag_reason or 'Not supplied'
            print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {flag_msg})")
        elif playlist.get_video(video.video_id):
            print(f"Cannot add video to {playlist_name}: Video already added")
        else:
            self._playlists[playlist_id]._videos[video_id] = video
            print(f"Added video to {playlist_name}: {video.title}")

    def show_all_playlists(self):
        """Display all playlists."""
        playlists = self._playlists
        if len(playlists) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            sorted_names = sorted(playlists.values(), key=lambda pl: pl.name)
            for playlist in sorted_names:
                playlist_size = len(playlist.get_all_videos())
                plural_suffix = "s" if playlist_size != 1 else ""
                print(f"  {playlist.name} ({playlist_size} video{plural_suffix})")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_id = playlist_name.upper()
        playlist = self._playlists.get(playlist_id)
        if playlist == None:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
        else:
            videos = playlist.get_all_videos()
            print(f"Showing playlist: {playlist_name}")
            if len(videos) < 1:
                print("No videos here yet")
            else:
                for video in videos:
                    tags = " ".join(video.tags)
                    flag_reason = video.flag_reason
                    flag_msg = ""
                    if flag_reason != None:
                        flag_msg = f"- FLAGGED (reason: {flag_reason or 'Not supplied'})"
                    print(f"  {video.title} ({video.video_id}) [{tags}] {flag_msg}")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist_id = playlist_name.upper()
        playlist = self._playlists.get(playlist_id)
        if playlist == None:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        elif video_id not in self._video_library._videos:
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
        else:
            video = playlist.get_video(video_id)
            if video == None:
                print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            else:
                del self._playlists[playlist_id]._videos[video_id]
                print(f"Removed video from {playlist_name}: {video.title}")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_id = playlist_name.upper()
        playlist = self._playlists.get(playlist_id)
        if playlist == None:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        else:
            self._playlists[playlist_id]._videos = {}
            print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_id = playlist_name.upper()
        playlist = self._playlists.get(playlist_id)
        if playlist == None:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        else:
            del self._playlists[playlist_id]
            print(f"Deleted playlist: {playlist_name}")

    def display_matched_videos(self, videos):
        """Display the videos matching the tag or the search term
            and ask for any of the matched video to be played.

        Args:
            videos: A list of `Video` objects
        """
        for i, video in enumerate(videos):
            tags = " ".join(video.tags)
            print(f"  {i+1}) {video.title} ({video.video_id}) [{tags}]")
        try:
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            number = int(input())
            if number in range(1, len(videos) + 1):
                video_to_play = videos[number-1]
                self.play_video(video_to_play.video_id)
        # If the user's input could not be converted into an integer.
        # For example, if the user inputted "Nope!".
        except ValueError:
            pass

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = self._video_library.get_all_videos()
        matched_videos = []
        for video in videos:
            if search_term.upper() in video.title.upper() and video.flag_reason == None:
                matched_videos.append(video)
        if len(matched_videos):
            print(f"Here are the results for {search_term}:")
            self.display_matched_videos(matched_videos)
        else:
            print(f"No search results for {search_term}")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        videos = self._video_library.get_all_videos()
        matched_videos = []
        for video in videos:
            tags = " ".join(video.tags)
            if video_tag.upper() in tags.upper() and video.flag_reason == None:
                matched_videos.append(video)
        if len(matched_videos):
            print(f"Here are the results for {video_tag}:")
            self.display_matched_videos(matched_videos)
        else:
            print(f"No search results for {video_tag}")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot flag video: Video does not exist")
        elif video.flag_reason != None:
            print("Cannot flag video: Video is already flagged")
        else:
            if self._playing_video == video:
                self.stop_video()
            self._video_library._videos[video_id]._flag_reason = flag_reason
            print(f"Successfully flagged video: {video.title} (reason: {flag_reason or 'Not supplied'})")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot remove flag from video: Video does not exist")
        elif video.flag_reason == None:
            print("Cannot remove flag from video: Video is not flagged")
        else:
            self._video_library._videos[video_id]._flag_reason = None
            print(f"Successfully removed flag from video: {video.title}")
