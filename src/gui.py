import os
import customtkinter as ctk
from tkinter import filedialog
from src.downloader import VideoDownloader


class DownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Config
        self.title("Universal Video Downloader")
        self.geometry("620x420")
        self.resizable(False, False)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Application State
        self.download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        self.current_downloader = None

        self._build_ui()

    def _build_ui(self):
        # Title Label
        title_label = ctk.CTkLabel(
            self, text="Media Video Downloader", font=ctk.CTkFont(size=22, weight="bold")
        )
        title_label.pack(pady=(20, 15))

        # URL Frame
        url_frame = ctk.CTkFrame(self, fg_color="transparent")
        url_frame.pack(fill="x", padx=30, pady=5)

        self.url_entry = ctk.CTkEntry(
            url_frame, placeholder_text="Paste video URL here...", width=560, height=38
        )
        self.url_entry.pack()

        # Quality Selection & Directory Frame
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.pack(fill="x", padx=30, pady=10)

        # Quality Dropdown
        quality_label = ctk.CTkLabel(options_frame, text="Quality:", font=ctk.CTkFont(size=13, weight="bold"))
        quality_label.pack(side="left", padx=(0, 5))

        self.quality_option = ctk.CTkOptionMenu(
            options_frame,
            values=["Best Quality", "1080p", "720p", "480p", "360p"],
            width=150
        )
        self.quality_option.pack(side="left", padx=(0, 20))

        # Browse Directory Button
        browse_btn = ctk.CTkButton(
            options_frame, text="Change Folder", width=120, command=self._browse_directory
        )
        browse_btn.pack(side="right")

        # Destination Label
        self.dir_label = ctk.CTkLabel(
            self, text=f"Save location: {self.download_dir}", anchor="w", text_color="gray"
        )
        self.dir_label.pack(fill="x", padx=30, pady=(0, 10))

        # Buttons Frame (Video, Audio, Cancel)
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=30, pady=10)

        self.download_video_btn = ctk.CTkButton(
            buttons_frame,
            text="Download Video",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            width=180,
            command=lambda: self._start_download(is_audio_only=False),
        )
        self.download_video_btn.pack(side="left", padx=(0, 10))

        self.download_audio_btn = ctk.CTkButton(
            buttons_frame,
            text="Download Audio",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2B8A3E",
            hover_color="#217A32",
            height=38,
            width=180,
            command=lambda: self._start_download(is_audio_only=True),
        )
        self.download_audio_btn.pack(side="left", padx=(0, 10))

        self.cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#D32F2F",
            hover_color="#B71C1C",
            height=38,
            width=160,
            state="disabled",
            command=self._cancel_download,
        )
        self.cancel_btn.pack(side="right")

        # Progress Indicator & Status Bar
        self.progress_bar = ctk.CTkProgressBar(self, width=560)
        self.progress_bar.pack(pady=(10, 5))
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(
            self, text="Ready", font=ctk.CTkFont(size=12), text_color="gray"
        )
        self.status_label.pack(pady=(0, 15))

    def _browse_directory(self):
        selected_dir = filedialog.askdirectory(initialdir=self.download_dir)
        if selected_dir:
            self.download_dir = selected_dir
            self.dir_label.configure(text=f"Save location: {self.download_dir}")

    def _update_progress(self, percent: float, status_text: str):
        self.after(0, lambda: self.progress_bar.set(percent))
        self.after(0, lambda: self.status_label.configure(text=status_text, text_color="white"))

    def _download_complete(self, success: bool, message: str):
        def update_ui():
            self.download_video_btn.configure(state="normal")
            self.download_audio_btn.configure(state="normal")
            self.cancel_btn.configure(state="disabled")
            
            if success:
                color = "#4CAF50"
                self.progress_bar.set(1.0)
            else:
                color = "#FF5252"
                self.progress_bar.set(0)

            self.status_label.configure(text=message, text_color=color)
            self.current_downloader = None

        self.after(0, update_ui)

    def _start_download(self, is_audio_only: bool = False):
        url = self.url_entry.get().strip()

        if not url:
            self.status_label.configure(text="Please enter a valid video URL.", text_color="#FF5252")
            return

        selected_quality = "Audio Only (MP3)" if is_audio_only else self.quality_option.get()

        self.download_video_btn.configure(state="disabled")
        self.download_audio_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        
        self.progress_bar.set(0)
        self.status_label.configure(text="Initializing download...", text_color="white")

        self.current_downloader = VideoDownloader(progress_callback=self._update_progress)
        self.current_downloader.download(
            url=url,
            output_dir=self.download_dir,
            quality=selected_quality,
            completion_callback=self._download_complete,
        )

    def _cancel_download(self):
        if self.current_downloader:
            self.status_label.configure(text="Cancelling download...", text_color="#FFC107")
            self.current_downloader.cancel()