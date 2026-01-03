#!/usr/bin/env python3
"""
Ultimate YouTube Video Generator - Full GUI
Complete guided setup + all features
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
import threading
import webbrowser

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QComboBox, QSpinBox,
    QCheckBox, QProgressBar, QTabWidget, QListWidget, QFileDialog,
    QMessageBox, QGroupBox, QScrollArea, QSplitter, QStatusBar,
    QDialog, QDialogButtonBox, QRadioButton, QButtonGroup, QTableWidget,
    QTableWidgetItem, QHeaderView, QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSettings
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette, QPixmap

# Import our video generator
try:
    from main_ultimate_free import UltimateFreeGenerator
    GENERATOR_AVAILABLE = True
except:
    GENERATOR_AVAILABLE = False

try:
    from youtube_uploader import YouTubeUploader
    YOUTUBE_AVAILABLE = True
except:
    YOUTUBE_AVAILABLE = False


class SetupWizard(QDialog):
    """Guided setup wizard for first-time users"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Setup Wizard - YouTube Video Generator")
        self.setMinimumSize(800, 600)
        self.current_page = 0
        self.settings = QSettings('VideoGenerator', 'Settings')
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Welcome to Ultimate YouTube Video Generator!")
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Pages container
        self.pages_widget = QWidget()
        self.pages_layout = QVBoxLayout()
        self.pages_widget.setLayout(self.pages_layout)
        
        layout.addWidget(self.pages_widget)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.back_btn = QPushButton("← Back")
        self.back_btn.clicked.connect(self.prev_page)
        self.next_btn = QPushButton("Next →")
        self.next_btn.clicked.connect(self.next_page)
        self.finish_btn = QPushButton("Finish ✓")
        self.finish_btn.clicked.connect(self.finish_setup)
        self.finish_btn.hide()
        
        nav_layout.addWidget(self.back_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_btn)
        nav_layout.addWidget(self.finish_btn)
        
        layout.addLayout(nav_layout)
        
        self.setLayout(layout)
        
        # Create all pages
        self.pages = [
            self.create_welcome_page(),
            self.create_api_keys_page(),
            self.create_voice_selection_page(),
            self.create_ollama_page(),
            self.create_youtube_page(),
            self.create_preferences_page(),
            self.create_complete_page()
        ]
        
        self.show_page(0)
        
    def create_welcome_page(self):
        """Welcome and overview page"""
        page = QWidget()
        layout = QVBoxLayout()
        
        welcome = QLabel("""
        <h2>Let's get you set up!</h2>
        <p>This wizard will help you configure everything you need to create
        professional YouTube videos for FREE.</p>
        
        <h3>What you'll set up:</h3>
        <ul>
            <li><b>Voice</b>: Ultra-realistic AI voices (ElevenLabs)</li>
            <li><b>Videos</b>: HD stock footage (Pexels, Pixabay)</li>
            <li><b>Scripts</b>: AI-generated content (Ollama)</li>
            <li><b>Upload</b>: Direct YouTube publishing</li>
        </ul>
        
        <p><b>Time required:</b> 10-15 minutes</p>
        <p><b>Cost:</b> $0.00 (all free APIs)</p>
        """)
        welcome.setWordWrap(True)
        layout.addWidget(welcome)
        
        layout.addStretch()
        page.setLayout(layout)
        return page
    
    def create_api_keys_page(self):
        """API keys configuration"""
        page = QWidget()
        layout = QVBoxLayout()
        
        intro = QLabel("""
        <h2>Step 1: API Keys (All Free!)</h2>
        <p>Get free API keys for the best quality. Click the links below to sign up.</p>
        """)
        intro.setWordWrap(True)
        layout.addWidget(intro)
        
        # ElevenLabs
        elevenlabs_group = QGroupBox("🎤 ElevenLabs Voice (CRITICAL - Makes voice sound human!)")
        el_layout = QVBoxLayout()
        
        el_info = QLabel("✅ FREE: 10,000 characters/month (≈15 videos)")
        el_layout.addWidget(el_info)
        
        el_link_btn = QPushButton("Open ElevenLabs Signup →")
        el_link_btn.clicked.connect(lambda: webbrowser.open('https://elevenlabs.io'))
        el_layout.addWidget(el_link_btn)
        
        el_key_layout = QHBoxLayout()
        el_key_layout.addWidget(QLabel("API Key:"))
        self.elevenlabs_key = QLineEdit()
        self.elevenlabs_key.setPlaceholderText("Paste your ElevenLabs API key here")
        el_key_layout.addWidget(self.elevenlabs_key)
        el_layout.addLayout(el_key_layout)
        
        elevenlabs_group.setLayout(el_layout)
        layout.addWidget(elevenlabs_group)
        
        # Pexels
        pexels_group = QGroupBox("📹 Pexels Videos (IMPORTANT - HD stock footage)")
        pex_layout = QVBoxLayout()
        
        pex_info = QLabel("✅ FREE: 200 requests/hour (unlimited daily)")
        pex_layout.addWidget(pex_info)
        
        pex_link_btn = QPushButton("Open Pexels API Signup →")
        pex_link_btn.clicked.connect(lambda: webbrowser.open('https://www.pexels.com/api/'))
        pex_layout.addWidget(pex_link_btn)
        
        pex_key_layout = QHBoxLayout()
        pex_key_layout.addWidget(QLabel("API Key:"))
        self.pexels_key = QLineEdit()
        self.pexels_key.setPlaceholderText("Paste your Pexels API key here")
        pex_key_layout.addWidget(self.pexels_key)
        pex_layout.addLayout(pex_key_layout)
        
        pexels_group.setLayout(pex_layout)
        layout.addWidget(pexels_group)
        
        # Pixabay (optional)
        pixabay_group = QGroupBox("📹 Pixabay Videos (Optional - Extra footage)")
        pix_layout = QVBoxLayout()
        
        pix_info = QLabel("✅ FREE: 5,000 requests/hour")
        pix_layout.addWidget(pix_info)
        
        pix_link_btn = QPushButton("Open Pixabay API Signup →")
        pix_link_btn.clicked.connect(lambda: webbrowser.open('https://pixabay.com/api/docs/'))
        pix_layout.addWidget(pix_link_btn)
        
        pix_key_layout = QHBoxLayout()
        pix_key_layout.addWidget(QLabel("API Key:"))
        self.pixabay_key = QLineEdit()
        self.pixabay_key.setPlaceholderText("Optional: Paste Pixabay key")
        pix_key_layout.addWidget(self.pixabay_key)
        pix_layout.addLayout(pix_key_layout)
        
        pixabay_group.setLayout(pix_layout)
        layout.addWidget(pixabay_group)
        
        layout.addStretch()
        page.setLayout(layout)
        return page
    
    def create_voice_selection_page(self):
        """Voice selection and testing"""
        page = QWidget()
        layout = QVBoxLayout()
        
        intro = QLabel("""
        <h2>Step 2: Choose Your Default Voice</h2>
        <p>All voices are FREE with ElevenLabs. Pick one that fits your content style.</p>
        """)
        intro.setWordWrap(True)
        layout.addWidget(intro)
        
        self.voice_combo = QComboBox()
        voices = [
            ("Rachel - Professional Female", "Rachel"),
            ("Adam - Deep Male Narrator", "Adam"),
            ("Antoni - Warm Male", "Antoni"),
            ("Josh - Energetic Male", "Josh"),
            ("Bella - Youthful Female", "Bella"),
            ("Domi - Strong Female", "Domi"),
            ("Elli - Young Female", "Elli"),
            ("Arnold - Mature Male", "Arnold"),
            ("Sam - Young Male", "Sam")
        ]
        
        for display, value in voices:
            self.voice_combo.addItem(display, value)
        
        layout.addWidget(QLabel("Default Voice:"))
        layout.addWidget(self.voice_combo)
        
        # Voice descriptions
        desc = QLabel("""
        <h3>Voice Recommendations:</h3>
        <ul>
            <li><b>Rachel</b>: Tech, tutorials, professional content</li>
            <li><b>Adam</b>: Documentary, serious topics</li>
            <li><b>Josh</b>: Gaming, entertainment, trending</li>
            <li><b>Bella</b>: Fashion, lifestyle, casual</li>
            <li><b>Antoni</b>: Storytelling, motivational</li>
        </ul>
        <p><i>You can change this anytime!</i></p>
        """)
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        layout.addStretch()
        page.setLayout(layout)
        return page
    
    def create_ollama_page(self):
        """Ollama setup for AI scripts"""
        page = QWidget()
        layout = QVBoxLayout()
        
        intro = QLabel("""
        <h2>Step 3: AI Script Generation (Optional)</h2>
        <p>Install Ollama for GPT-4 quality scripts. Skip if you want to use templates.</p>
        """)
        intro.setWordWrap(True)
        layout.addWidget(intro)
        
        self.use_ollama = QCheckBox("Use Ollama for AI-generated scripts")
        layout.addWidget(self.use_ollama)
        
        info = QLabel("""
        <h3>What is Ollama?</h3>
        <ul>
            <li>Local AI (like ChatGPT) that runs on your computer</li>
            <li>FREE and unlimited usage</li>
            <li>Creates engaging, viral-worthy scripts</li>
            <li>4GB download required</li>
        </ul>
        
        <h3>How to install:</h3>
        <ol>
            <li>Click the button below to download</li>
            <li>Install Ollama</li>
            <li>Run: <code>ollama pull llama2</code></li>
            <li>Run: <code>ollama serve</code></li>
        </ol>
        """)
        info.setWordWrap(True)
        layout.addWidget(info)
        
        ollama_btn = QPushButton("Download Ollama →")
        ollama_btn.clicked.connect(lambda: webbrowser.open('https://ollama.ai'))
        layout.addWidget(ollama_btn)
        
        layout.addStretch()
        page.setLayout(layout)
        return page
    
    def create_youtube_page(self):
        """YouTube upload configuration"""
        page = QWidget()
        layout = QVBoxLayout()
        
        intro = QLabel("""
        <h2>Step 4: YouTube Auto-Upload (Optional)</h2>
        <p>Set up automatic uploading to your YouTube channel.</p>
        """)
        intro.setWordWrap(True)
        layout.addWidget(intro)
        
        self.enable_youtube = QCheckBox("Enable YouTube auto-upload")
        layout.addWidget(self.enable_youtube)
        
        info = QLabel("""
        <h3>Setup Steps:</h3>
        <ol>
            <li>Go to <a href="https://console.cloud.google.com">Google Cloud Console</a></li>
            <li>Create a new project</li>
            <li>Enable YouTube Data API v3</li>
            <li>Create OAuth 2.0 credentials</li>
            <li>Download as client_secrets.json</li>
            <li>Click button below to select the file</li>
        </ol>
        
        <p><i>See YOUTUBE_SETUP.md for detailed guide (15 min)</i></p>
        """)
        info.setWordWrap(True)
        info.setOpenExternalLinks(True)
        layout.addWidget(info)
        
        self.youtube_file_btn = QPushButton("Select client_secrets.json")
        self.youtube_file_btn.clicked.connect(self.select_youtube_file)
        self.youtube_file_btn.setEnabled(False)
        layout.addWidget(self.youtube_file_btn)
        
        self.youtube_file_label = QLabel("No file selected")
        layout.addWidget(self.youtube_file_label)
        
        self.enable_youtube.stateChanged.connect(
            lambda: self.youtube_file_btn.setEnabled(self.enable_youtube.isChecked())
        )
        
        layout.addStretch()
        page.setLayout(layout)
        return page
    
    def select_youtube_file(self):
        """Select YouTube client secrets file"""
        file, _ = QFileDialog.getOpenFileName(
            self, "Select client_secrets.json", "", "JSON Files (*.json)"
        )
        if file:
            self.youtube_file_label.setText(f"Selected: {Path(file).name}")
            self.youtube_secrets_file = file
    
    def create_preferences_page(self):
        """General preferences"""
        page = QWidget()
        layout = QVBoxLayout()
        
        intro = QLabel("""
        <h2>Step 5: Preferences</h2>
        <p>Configure your default settings.</p>
        """)
        intro.setWordWrap(True)
        layout.addWidget(intro)
        
        # Default video length
        length_layout = QHBoxLayout()
        length_layout.addWidget(QLabel("Default video length:"))
        self.video_length = QSpinBox()
        self.video_length.setRange(15, 300)
        self.video_length.setValue(60)
        self.video_length.setSuffix(" seconds")
        length_layout.addWidget(self.video_length)
        length_layout.addStretch()
        layout.addLayout(length_layout)
        
        # Default style
        style_layout = QHBoxLayout()
        style_layout.addWidget(QLabel("Default content style:"))
        self.style_combo = QComboBox()
        self.style_combo.addItems(["Professional", "Casual", "Educational", "Entertaining"])
        style_layout.addWidget(self.style_combo)
        style_layout.addStretch()
        layout.addLayout(style_layout)
        
        # Subtitles
        self.add_subtitles = QCheckBox("Add subtitles by default")
        self.add_subtitles.setChecked(True)
        layout.addWidget(self.add_subtitles)
        
        # Auto-save
        self.auto_save = QCheckBox("Auto-save generated scripts")
        self.auto_save.setChecked(True)
        layout.addWidget(self.auto_save)
        
        # Default privacy
        privacy_layout = QHBoxLayout()
        privacy_layout.addWidget(QLabel("Default YouTube privacy:"))
        self.privacy_combo = QComboBox()
        self.privacy_combo.addItems(["public", "unlisted", "private"])
        self.privacy_combo.setCurrentText("unlisted")
        privacy_layout.addWidget(self.privacy_combo)
        privacy_layout.addStretch()
        layout.addLayout(privacy_layout)
        
        layout.addStretch()
        page.setLayout(layout)
        return page
    
    def create_complete_page(self):
        """Setup complete page"""
        page = QWidget()
        layout = QVBoxLayout()
        
        complete = QLabel("""
        <h2>✅ Setup Complete!</h2>
        <p>You're all set to create amazing YouTube videos!</p>
        
        <h3>What happens next:</h3>
        <ul>
            <li>Your settings will be saved</li>
            <li>The main app will open</li>
            <li>You can create your first video right away!</li>
        </ul>
        
        <p><b>Remember:</b> You can change any of these settings later in Preferences.</p>
        
        <h3>Quick Tips:</h3>
        <ul>
            <li>Start with unlisted videos to test</li>
            <li>The ElevenLabs voice makes the BIGGEST difference</li>
            <li>Be specific with video topics for best results</li>
            <li>Create 2-3 variations and pick the best one</li>
        </ul>
        """)
        complete.setWordWrap(True)
        layout.addWidget(complete)
        
        layout.addStretch()
        page.setLayout(layout)
        return page
    
    def show_page(self, index):
        """Show specific page"""
        # Hide all pages
        for page in self.pages:
            page.hide()
        
        # Show current page
        self.pages_layout.addWidget(self.pages[index])
        self.pages[index].show()
        
        # Update buttons
        self.back_btn.setEnabled(index > 0)
        
        if index == len(self.pages) - 1:
            self.next_btn.hide()
            self.finish_btn.show()
        else:
            self.next_btn.show()
            self.finish_btn.hide()
        
        self.current_page = index
    
    def next_page(self):
        """Go to next page"""
        if self.current_page < len(self.pages) - 1:
            self.show_page(self.current_page + 1)
    
    def prev_page(self):
        """Go to previous page"""
        if self.current_page > 0:
            self.show_page(self.current_page - 1)
    
    def finish_setup(self):
        """Save settings and finish"""
        # Save API keys
        if self.elevenlabs_key.text():
            os.environ['ELEVENLABS_API_KEY'] = self.elevenlabs_key.text()
            self.settings.setValue('elevenlabs_key', self.elevenlabs_key.text())
        
        if self.pexels_key.text():
            os.environ['PEXELS_API_KEY'] = self.pexels_key.text()
            self.settings.setValue('pexels_key', self.pexels_key.text())
        
        if self.pixabay_key.text():
            os.environ['PIXABAY_API_KEY'] = self.pixabay_key.text()
            self.settings.setValue('pixabay_key', self.pixabay_key.text())
        
        # Save preferences
        self.settings.setValue('default_voice', self.voice_combo.currentData())
        self.settings.setValue('default_length', self.video_length.value())
        self.settings.setValue('default_style', self.style_combo.currentText().lower())
        self.settings.setValue('add_subtitles', self.add_subtitles.isChecked())
        self.settings.setValue('auto_save', self.auto_save.isChecked())
        self.settings.setValue('default_privacy', self.privacy_combo.currentText())
        self.settings.setValue('use_ollama', self.use_ollama.isChecked())
        self.settings.setValue('enable_youtube', self.enable_youtube.isChecked())
        self.settings.setValue('setup_complete', True)
        
        self.accept()


class VideoCreationThread(QThread):
    """Thread for video creation to avoid blocking UI"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, generator, topic, duration, voice, upload, privacy):
        super().__init__()
        self.generator = generator
        self.topic = topic
        self.duration = duration
        self.voice = voice
        self.upload = upload
        self.privacy = privacy
    
    def run(self):
        try:
            self.progress.emit("Starting video creation...")
            result = self.generator.create_and_upload_video(
                topic=self.topic,
                duration=self.duration,
                voice=self.voice,
                upload=self.upload,
                privacy=self.privacy
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ultimate YouTube Video Generator")
        self.setMinimumSize(1200, 800)
        
        self.settings = QSettings('VideoGenerator', 'Settings')
        self.generator = None
        
        # Check if setup is needed
        if not self.settings.value('setup_complete', False):
            wizard = SetupWizard(self)
            if wizard.exec_() != QDialog.Accepted:
                sys.exit(0)
        
        # Load API keys from settings
        self.load_api_keys()
        
        # Initialize generator
        if GENERATOR_AVAILABLE:
            self.generator = UltimateFreeGenerator()
        
        self.init_ui()
        self.load_settings()
        
    def load_api_keys(self):
        """Load API keys from settings"""
        if self.settings.value('elevenlabs_key'):
            os.environ['ELEVENLABS_API_KEY'] = self.settings.value('elevenlabs_key')
        if self.settings.value('pexels_key'):
            os.environ['PEXELS_API_KEY'] = self.settings.value('pexels_key')
        if self.settings.value('pixabay_key'):
            os.environ['PIXABAY_API_KEY'] = self.settings.value('pixabay_key')
    
    def init_ui(self):
        """Initialize UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Tab widget
        tabs = QTabWidget()
        
        # Create Video tab
        tabs.addTab(self.create_video_tab(), "🎬 Create Video")
        
        # History tab
        tabs.addTab(self.create_history_tab(), "📁 History")
        
        # Settings tab
        tabs.addTab(self.create_settings_tab(), "⚙️ Settings")
        
        # Help tab
        tabs.addTab(self.create_help_tab(), "❓ Help")
        
        main_layout.addWidget(tabs)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def create_video_tab(self):
        """Create video creation tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Topic input
        topic_group = QGroupBox("🎯 Video Topic")
        topic_layout = QVBoxLayout()
        
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Enter your video topic (e.g., '10 Python Tips for Beginners in 2025')")
        self.topic_input.setFont(QFont('Arial', 12))
        topic_layout.addWidget(self.topic_input)
        
        tips = QLabel("<i>💡 Tip: Be specific! '10 Python Pandas Tips for Data Science' > 'Python'</i>")
        topic_layout.addWidget(tips)
        
        topic_group.setLayout(topic_layout)
        layout.addWidget(topic_group)
        
        # Options
        options_splitter = QSplitter(Qt.Horizontal)
        
        # Left column - Video settings
        left_group = QGroupBox("📹 Video Settings")
        left_layout = QVBoxLayout()
        
        # Duration
        dur_layout = QHBoxLayout()
        dur_layout.addWidget(QLabel("Duration:"))
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(15, 300)
        self.duration_spin.setValue(60)
        self.duration_spin.setSuffix(" seconds")
        dur_layout.addWidget(self.duration_spin)
        dur_layout.addStretch()
        left_layout.addLayout(dur_layout)
        
        # Voice
        voice_layout = QHBoxLayout()
        voice_layout.addWidget(QLabel("Voice:"))
        self.voice_combo = QComboBox()
        voices = ["Rachel", "Adam", "Antoni", "Josh", "Bella", "Domi", "Elli", "Arnold", "Sam"]
        self.voice_combo.addItems(voices)
        voice_layout.addWidget(self.voice_combo)
        voice_layout.addStretch()
        left_layout.addLayout(voice_layout)
        
        # Style
        style_layout = QHBoxLayout()
        style_layout.addWidget(QLabel("Style:"))
        self.style_combo = QComboBox()
        self.style_combo.addItems(["Professional", "Casual", "Educational", "Entertaining"])
        style_layout.addWidget(self.style_combo)
        style_layout.addStretch()
        left_layout.addLayout(style_layout)
        
        # Subtitles
        self.subtitles_check = QCheckBox("Add subtitles")
        self.subtitles_check.setChecked(True)
        left_layout.addWidget(self.subtitles_check)
        
        left_layout.addStretch()
        left_group.setLayout(left_layout)
        options_splitter.addWidget(left_group)
        
        # Right column - Upload settings
        right_group = QGroupBox("📤 Upload Settings")
        right_layout = QVBoxLayout()
        
        self.upload_check = QCheckBox("Upload to YouTube")
        self.upload_check.setChecked(False)
        right_layout.addWidget(self.upload_check)
        
        privacy_layout = QHBoxLayout()
        privacy_layout.addWidget(QLabel("Privacy:"))
        self.privacy_combo = QComboBox()
        self.privacy_combo.addItems(["public", "unlisted", "private"])
        self.privacy_combo.setCurrentText("unlisted")
        privacy_layout.addWidget(self.privacy_combo)
        privacy_layout.addStretch()
        right_layout.addLayout(privacy_layout)
        
        self.privacy_combo.setEnabled(False)
        self.upload_check.stateChanged.connect(
            lambda: self.privacy_combo.setEnabled(self.upload_check.isChecked())
        )
        
        right_layout.addStretch()
        right_group.setLayout(right_layout)
        options_splitter.addWidget(right_group)
        
        layout.addWidget(options_splitter)
        
        # Create button
        self.create_btn = QPushButton("🎬 CREATE VIDEO")
        self.create_btn.setFont(QFont('Arial', 14, QFont.Bold))
        self.create_btn.setMinimumHeight(50)
        self.create_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.create_btn.clicked.connect(self.create_video)
        layout.addWidget(self.create_btn)
        
        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        # Log output
        log_group = QGroupBox("📝 Progress Log")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        log_layout.addWidget(self.log_text)
        
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        tab.setLayout(layout)
        return tab
    
    def create_history_tab(self):
        """Create history tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(['Title', 'Created', 'Duration', 'Voice', 'Actions'])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.history_table)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_history)
        layout.addWidget(refresh_btn)
        
        tab.setLayout(layout)
        return tab
    
    def create_settings_tab(self):
        """Create settings tab"""
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        layout = QVBoxLayout()
        
        # API Keys section
        api_group = QGroupBox("🔑 API Keys")
        api_layout = QVBoxLayout()
        
        # ElevenLabs
        el_layout = QHBoxLayout()
        el_layout.addWidget(QLabel("ElevenLabs:"))
        self.el_key_input = QLineEdit()
        self.el_key_input.setEchoMode(QLineEdit.Password)
        self.el_key_input.setText(self.settings.value('elevenlabs_key', ''))
        el_layout.addWidget(self.el_key_input)
        el_show = QPushButton("👁")
        el_show.clicked.connect(lambda: self.toggle_password(self.el_key_input))
        el_layout.addWidget(el_show)
        api_layout.addLayout(el_layout)
        
        # Pexels
        pex_layout = QHBoxLayout()
        pex_layout.addWidget(QLabel("Pexels:"))
        self.pex_key_input = QLineEdit()
        self.pex_key_input.setEchoMode(QLineEdit.Password)
        self.pex_key_input.setText(self.settings.value('pexels_key', ''))
        pex_layout.addWidget(self.pex_key_input)
        pex_show = QPushButton("👁")
        pex_show.clicked.connect(lambda: self.toggle_password(self.pex_key_input))
        pex_layout.addWidget(pex_show)
        api_layout.addLayout(pex_layout)
        
        save_keys_btn = QPushButton("💾 Save API Keys")
        save_keys_btn.clicked.connect(self.save_api_keys)
        api_layout.addWidget(save_keys_btn)
        
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        # Default settings
        defaults_group = QGroupBox("⚙️ Default Settings")
        defaults_layout = QVBoxLayout()
        
        # Add default settings controls here
        
        defaults_group.setLayout(defaults_layout)
        layout.addWidget(defaults_group)
        
        # Run setup wizard again
        wizard_btn = QPushButton("🔄 Run Setup Wizard Again")
        wizard_btn.clicked.connect(self.run_setup_wizard)
        layout.addWidget(wizard_btn)
        
        layout.addStretch()
        scroll_widget.setLayout(layout)
        scroll.setWidget(scroll_widget)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        tab.setLayout(main_layout)
        return tab
    
    def create_help_tab(self):
        """Create help tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setHtml("""
        <h2>🎬 Quick Start Guide</h2>
        
        <h3>1. Enter Your Topic</h3>
        <p>Be specific! "10 Python Tips for Data Science" works better than just "Python"</p>
        
        <h3>2. Configure Settings</h3>
        <ul>
            <li><b>Duration</b>: 60 seconds is optimal for YouTube</li>
            <li><b>Voice</b>: Pick one that fits your content style</li>
            <li><b>Style</b>: Match your channel's tone</li>
        </ul>
        
        <h3>3. Click Create</h3>
        <p>The process takes 3-5 minutes depending on video length</p>
        
        <h3>4. Review & Upload</h3>
        <p>Check the video, then upload manually or use auto-upload</p>
        
        <h2>�� Voice Guide</h2>
        <ul>
            <li><b>Rachel</b>: Tech, tutorials, professional</li>
            <li><b>Adam</b>: Documentary, serious topics</li>
            <li><b>Josh</b>: Gaming, entertainment</li>
            <li><b>Bella</b>: Fashion, lifestyle</li>
        </ul>
        
        <h2>💡 Pro Tips</h2>
        <ul>
            <li>Start with "unlisted" privacy to test</li>
            <li>Create 2-3 versions of same topic</li>
            <li>ElevenLabs voice = biggest quality boost</li>
            <li>Upload 1-2 videos/day consistently</li>
        </ul>
        
        <h2>📚 Documentation</h2>
        <p>Check the README files in the installation folder for detailed guides.</p>
        """)
        
        layout.addWidget(help_text)
        tab.setLayout(layout)
        return tab
    
    def toggle_password(self, line_edit):
        """Toggle password visibility"""
        if line_edit.echoMode() == QLineEdit.Password:
            line_edit.setEchoMode(QLineEdit.Normal)
        else:
            line_edit.setEchoMode(QLineEdit.Password)
    
    def save_api_keys(self):
        """Save API keys"""
        if self.el_key_input.text():
            self.settings.setValue('elevenlabs_key', self.el_key_input.text())
            os.environ['ELEVENLABS_API_KEY'] = self.el_key_input.text()
        
        if self.pex_key_input.text():
            self.settings.setValue('pexels_key', self.pex_key_input.text())
            os.environ['PEXELS_API_KEY'] = self.pex_key_input.text()
        
        QMessageBox.information(self, "Success", "API keys saved successfully!")
    
    def run_setup_wizard(self):
        """Run setup wizard again"""
        wizard = SetupWizard(self)
        wizard.exec_()
        self.load_api_keys()
    
    def load_settings(self):
        """Load saved settings"""
        self.voice_combo.setCurrentText(self.settings.value('default_voice', 'Rachel'))
        self.duration_spin.setValue(int(self.settings.value('default_length', 60)))
        self.style_combo.setCurrentText(self.settings.value('default_style', 'professional').title())
        self.subtitles_check.setChecked(self.settings.value('add_subtitles', True, type=bool))
        self.privacy_combo.setCurrentText(self.settings.value('default_privacy', 'unlisted'))
    
    def create_video(self):
        """Start video creation"""
        topic = self.topic_input.text().strip()
        
        if not topic:
            QMessageBox.warning(self, "Error", "Please enter a video topic!")
            return
        
        if not GENERATOR_AVAILABLE:
            QMessageBox.critical(self, "Error", "Video generator not available. Check installation.")
            return
        
        # Disable create button
        self.create_btn.setEnabled(False)
        self.progress_bar.show()
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.log_text.clear()
        self.log("Starting video creation...")
        
        # Create thread
        self.thread = VideoCreationThread(
            self.generator,
            topic,
            self.duration_spin.value(),
            self.voice_combo.currentText(),
            self.upload_check.isChecked(),
            self.privacy_combo.currentText()
        )
        
        self.thread.progress.connect(self.log)
        self.thread.finished.connect(self.on_video_created)
        self.thread.error.connect(self.on_error)
        self.thread.start()
    
    def log(self, message):
        """Add message to log"""
        self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        self.status_bar.showMessage(message)
    
    def on_video_created(self, result):
        """Handle video creation completion"""
        self.progress_bar.hide()
        self.create_btn.setEnabled(True)
        
        video_file = result.get('video_file')
        youtube_url = result.get('youtube_url')
        
        msg = f"✅ Video created successfully!\n\nFile: {video_file}"
        if youtube_url:
            msg += f"\n\nYouTube URL: {youtube_url}"
        
        QMessageBox.information(self, "Success", msg)
        self.log("✅ Video creation complete!")
        
        # Reload history
        self.load_history()
    
    def on_error(self, error):
        """Handle error"""
        self.progress_bar.hide()
        self.create_btn.setEnabled(True)
        
        QMessageBox.critical(self, "Error", f"Video creation failed:\n\n{error}")
        self.log(f"❌ Error: {error}")
    
    def load_history(self):
        """Load video history"""
        self.history_table.setRowCount(0)
        
        output_dir = Path("output")
        if not output_dir.exists():
            return
        
        videos = []
        for video_dir in output_dir.glob("video_*"):
            metadata_file = video_dir / "metadata.json"
            if metadata_file.exists():
                try:
                    with open(metadata_file) as f:
                        metadata = json.load(f)
                    
                    videos.append({
                        'dir': video_dir,
                        'metadata': metadata
                    })
                except:
                    pass
        
        # Sort by created date
        videos.sort(key=lambda x: x['metadata'].get('created', ''), reverse=True)
        
        # Add to table
        for video in videos:
            meta = video['metadata']
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)
            
            self.history_table.setItem(row, 0, QTableWidgetItem(meta.get('title', 'Unknown')))
            self.history_table.setItem(row, 1, QTableWidgetItem(meta.get('created', '')))
            self.history_table.setItem(row, 2, QTableWidgetItem(f"{meta.get('duration', 0)}s"))
            self.history_table.setItem(row, 3, QTableWidgetItem(meta.get('voice', 'Unknown')))
            
            # Actions button
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            open_btn = QPushButton("📁 Open")
            open_btn.clicked.connect(lambda checked, d=video['dir']: self.open_video_folder(d))
            actions_layout.addWidget(open_btn)
            
            actions_widget.setLayout(actions_layout)
            self.history_table.setCellWidget(row, 4, actions_widget)
    
    def open_video_folder(self, folder):
        """Open video folder in file manager"""
        import subprocess
        import platform
        
        system = platform.system()
        if system == "Windows":
            os.startfile(folder)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", str(folder)])
        else:  # Linux
            subprocess.run(["xdg-open", str(folder)])


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Ultimate YouTube Video Generator")
    app.setOrganizationName("VideoGenerator")
    
    # Set style
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
