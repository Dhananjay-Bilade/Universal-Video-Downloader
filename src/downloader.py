import os
import re
import threading
from typing import Callable, Optional
import yt_dlp


class VideoDownloader:
    def __init__(self, progress_callback: Optional[Callable[[float, str], None]] = None):
        self.progress_callback = progress_callback
        self.is_cancelled = False

    def cancel(self):
        """Download request ko cancel karne ke liye flag set karta hai."""
        self.is_cancelled = True

    def _clean_ansi(self, text: str) -> str:
        ansi_regex = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_regex.sub('', text)

    def _progress_hook(self, d: dict):
        if self.is_cancelled:
            # yt-dlp execution ko cancel karne ke liye exception raise karenge
            raise Exception("Download cancelled by user.")

        if not self.progress_callback:
            return

        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded_bytes = d.get('downloaded_bytes', 0)

            percent = (downloaded_bytes / total_bytes) if total_bytes > 0 else 0.0
            
            speed = self._clean_ansi(d.get('_speed_str', 'N/A')).strip()
            eta = self._clean_ansi(d.get('_eta_str', 'N/A')).strip()

            status_msg = f"Downloading: {percent * 100:.1f}%   |   Speed: {speed}   |   ETA: {eta}"
            self.progress_callback(percent, status_msg)

        elif d['status'] == 'finished':
            self.progress_callback(1.0, "Processing & Merging media streams...")

    def _get_format_spec(self, quality: str) -> dict:
        quality_map = {
            "Best Quality": {"format": "bestvideo+bestaudio/best"},
            "1080p": {"format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]"},
            "720p": {"format": "bestvideo[height<=720]+bestaudio/best[height<=720]"},
            "480p": {"format": "bestvideo[height<=480]+bestaudio/best[height<=480]"},
            "360p": {"format": "bestvideo[height<=360]+bestaudio/best[height<=360]"},
            "Audio Only (MP3)": {
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }]
            }
        }
        return quality_map.get(quality, {"format": "bestvideo+bestaudio/best"})

    def download(self, url: str, output_dir: str, quality: str, completion_callback: Callable[[bool, str], None]):
        self.is_cancelled = False

        def run():
            output_template = os.path.join(output_dir, "%(title)s.%(ext)s")
            format_opts = self._get_format_spec(quality)
            
            ydl_opts = {
                'outtmpl': output_template,
                'merge_output_format': 'mp4',
                'noplaylist': True,
                'nocolor': True,
                'progress_hooks': [self._progress_hook],
                'quiet': True,
                **format_opts
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                if not self.is_cancelled:
                    completion_callback(True, "Download finished successfully!")
            except Exception as err:
                if self.is_cancelled or "cancelled" in str(err).lower():
                    completion_callback(False, "Download cancelled by user.")
                else:
                    completion_callback(False, f"Error: {str(err)}")

        threading.Thread(target=run, daemon=True).start()