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
    QTableWidgetItem, QHeaderView, QSystemTrayIcon, QMenu, QAction,
    QListWidgetItem
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

        # Gemini (Google AI)
        gemini_group = QGroupBox("🤖 Gemini (Google AI for scripts & images)")
        gem_layout = QVBoxLayout()

        gem_info = QLabel("✅ Uses your Google AI key (Gemini Pro) for scripts + image clips")
        gem_layout.addWidget(gem_info)

        gem_link_btn = QPushButton("Log in to Google / Open Gemini Console →")
        gem_link_btn.clicked.connect(lambda: webbrowser.open('https://makersuite.google.com/app/apikey'))
        gem_layout.addWidget(gem_link_btn)

        gem_token_btn = QPushButton("Open Google OAuth Playground (paste token) →")
        gem_token_btn.clicked.connect(lambda: webbrowser.open('https://developers.google.com/oauthplayground'))
        gem_layout.addWidget(gem_token_btn)

        gem_key_layout = QHBoxLayout()
        gem_key_layout.addWidget(QLabel("API Key:"))
        self.gemini_key = QLineEdit()
        self.gemini_key.setPlaceholderText("Paste your Gemini API key here")
        self.gemini_key.setText(self.settings.value('gemini_key', ''))
        gem_key_layout.addWidget(self.gemini_key)
        gem_layout.addLayout(gem_key_layout)

        gem_token_layout = QHBoxLayout()
        gem_token_layout.addWidget(QLabel("Access Token:"))
        self.gemini_token = QLineEdit()
        self.gemini_token.setPlaceholderText("Optional: paste OAuth access token (Bearer)")
        self.gemini_token.setText(self.settings.value('gemini_token', ''))
        gem_token_layout.addWidget(self.gemini_token)
        gem_layout.addLayout(gem_token_layout)

        gemini_group.setLayout(gem_layout)
        layout.addWidget(gemini_group)

        # OpenAI (scripts/images if enabled)
        openai_group = QGroupBox("🧠 OpenAI (API key or access token)")
        oa_layout = QVBoxLayout()

        oa_info = QLabel("Use your OpenAI key for scripts/images (key or access token).")
        oa_layout.addWidget(oa_info)

        oa_link_btn = QPushButton("Open OpenAI API Keys →")
        oa_link_btn.clicked.connect(lambda: webbrowser.open('https://platform.openai.com/account/api-keys'))
        oa_layout.addWidget(oa_link_btn)

        oa_token_btn = QPushButton("Open OpenAI Dashboard / Log in →")
        oa_token_btn.clicked.connect(lambda: webbrowser.open('https://platform.openai.com/'))
        oa_layout.addWidget(oa_token_btn)

        oa_key_layout = QHBoxLayout()
        oa_key_layout.addWidget(QLabel("API Key:"))
        self.openai_key = QLineEdit()
        self.openai_key.setPlaceholderText("Paste your OpenAI API key here")
        self.openai_key.setText(self.settings.value('openai_key', ''))
        oa_key_layout.addWidget(self.openai_key)
        oa_layout.addLayout(oa_key_layout)

        oa_token_layout = QHBoxLayout()
        oa_token_layout.addWidget(QLabel("Access Token:"))
        self.openai_token = QLineEdit()
        self.openai_token.setPlaceholderText("Optional: paste OpenAI access token (Bearer)")
        self.openai_token.setText(self.settings.value('openai_token', ''))
        oa_token_layout.addWidget(self.openai_token)
        oa_layout.addLayout(oa_token_layout)

        openai_group.setLayout(oa_layout)
        layout.addWidget(openai_group)
         
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

        # Launcher option
        self.create_launcher_checkbox = QCheckBox("Create Kali start-menu launcher")
        self.create_launcher_checkbox.setChecked(False)
        layout.addWidget(self.create_launcher_checkbox)
        
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
        
        if self.gemini_key.text():
            os.environ['GEMINI_API_KEY'] = self.gemini_key.text()
            self.settings.setValue('gemini_key', self.gemini_key.text())
        
        if self.gemini_token.text():
            os.environ['GEMINI_ACCESS_TOKEN'] = self.gemini_token.text()
            self.settings.setValue('gemini_token', self.gemini_token.text())

        if self.openai_key.text():
            os.environ['OPENAI_API_KEY'] = self.openai_key.text()
            self.settings.setValue('openai_key', self.openai_key.text())

        if self.openai_token.text():
            os.environ['OPENAI_ACCESS_TOKEN'] = self.openai_token.text()
            self.settings.setValue('openai_token', self.openai_token.text())
        
        # Save preferences
        self.settings.setValue('default_voice', self.voice_combo.currentData())
        self.settings.setValue('default_length', self.video_length.value())
        self.settings.setValue('default_style', self.style_combo.currentText().lower())
        self.settings.setValue('add_subtitles', self.add_subtitles.isChecked())
        self.settings.setValue('auto_save', self.auto_save.isChecked())
        self.settings.setValue('default_privacy', self.privacy_combo.currentText())
        self.settings.setValue('use_ollama', self.use_ollama.isChecked())
        self.settings.setValue('enable_youtube', self.enable_youtube.isChecked())
        self.settings.setValue('create_launcher', self.create_launcher_checkbox.isChecked())
        self.settings.setValue('setup_complete', True)

        if self.create_launcher_checkbox.isChecked():
            success, path_or_err = self.create_desktop_launcher()
            if success:
                QMessageBox.information(self, "Launcher created", f"Launcher added: {path_or_err}")
            else:
                QMessageBox.warning(self, "Launcher failed", f"Could not create launcher:\n{path_or_err}")
        
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


class SimpleDialog(QDialog):
    """Base dialog with OK/Close button"""
    def __init__(self, title, widget, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(600, 400)
        layout = QVBoxLayout()
        layout.addWidget(widget)
        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)
        self.setLayout(layout)


class ScriptEditorDialog(QDialog):
    """Lightweight script editor"""
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Script Editor")
        self.setMinimumSize(800, 500)
        layout = QVBoxLayout()
        self.editor = QTextEdit()
        self.editor.setPlainText(text)
        layout.addWidget(self.editor)
        btns = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)
        self.setLayout(layout)

    def get_text(self):
        return self.editor.toPlainText()


class BatchQueueDialog(QDialog):
    """Simple batch queue manager"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Batch Queue")
        self.setMinimumSize(700, 500)
        self.queue = []
        layout = QVBoxLayout()
        form = QHBoxLayout()
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Topic")
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(15, 300)
        self.duration_spin.setValue(60)
        form.addWidget(self.topic_input)
        form.addWidget(self.duration_spin)
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_item)
        form.addWidget(add_btn)
        layout.addLayout(form)
        self.list = QListWidget()
        layout.addWidget(self.list)
        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)
        self.setLayout(layout)

    def add_item(self):
        text = self.topic_input.text().strip()
        if not text:
            return
        item = f"{text} ({self.duration_spin.value()}s)"
        self.queue.append({'topic': text, 'duration': self.duration_spin.value()})
        self.list.addItem(item)
        self.topic_input.clear()

    def get_queue(self):
        return self.queue


class TemplateManagerDialog(QDialog):
    """Manage simple templates stored in settings"""
    def __init__(self, settings: QSettings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Templates")
        self.setMinimumSize(600, 400)
        layout = QVBoxLayout()
        self.list = QListWidget()
        layout.addWidget(self.list)
        form = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Template name")
        form.addWidget(self.name_input)
        save_btn = QPushButton("Save Current")
        save_btn.clicked.connect(self.save_template)
        form.addWidget(save_btn)
        load_btn = QPushButton("Load Selected")
        load_btn.clicked.connect(self.load_selected)
        form.addWidget(load_btn)
        layout.addLayout(form)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        self.setLayout(layout)
        self.refresh()

    def refresh(self):
        self.list.clear()
        templates = self.settings.value("templates", {})
        if not isinstance(templates, dict):
            templates = {}
        if templates:
            for name in templates.keys():
                self.list.addItem(name)

    def save_template(self):
        name = self.name_input.text().strip()
        if not name:
            return
        p = self.parent()
        if not p:
            return
        tpl = {
            'duration': p.duration_spin.value(),
            'voice': p.voice_combo.currentText(),
            'style': p.style_combo.currentText(),
            'subtitles': p.subtitles_check.isChecked()
        }
        templates = self.settings.value("templates", {})
        if not isinstance(templates, dict):
            templates = {}
        templates[name] = tpl
        self.settings.setValue("templates", templates)
        self.refresh()

    def load_selected(self):
        item = self.list.currentItem()
        if not item:
            return
        templates = self.settings.value("templates", {})
        if not isinstance(templates, dict):
            templates = {}
        tpl = templates.get(item.text(), {})
        p = self.parent()
        if p:
            p.duration_spin.setValue(tpl.get('duration', p.duration_spin.value()))
            p.voice_combo.setCurrentText(tpl.get('voice', p.voice_combo.currentText()))
            p.style_combo.setCurrentText(tpl.get('style', p.style_combo.currentText()))
            p.subtitles_check.setChecked(tpl.get('subtitles', p.subtitles_check.isChecked()))


class VoicePreviewDialog(QDialog):
    """Voice preview tester"""
    def __init__(self, voice_list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Voice Preview")
        self.setMinimumSize(500, 300)
        layout = QVBoxLayout()
        self.voice_combo = QComboBox()
        self.voice_combo.addItems(voice_list)
        layout.addWidget(self.voice_combo)
        self.text = QTextEdit()
        self.text.setPlainText("This is a sample preview.")
        layout.addWidget(self.text)
        preview_btn = QPushButton("Preview (simulated)")
        preview_btn.clicked.connect(self.preview)
        layout.addWidget(preview_btn)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        self.setLayout(layout)

    def preview(self):
        QMessageBox.information(self, "Preview", f"Would play voice '{self.voice_combo.currentText()}' with current text.")


class ThumbnailDialog(QDialog):
    """Thumbnail generator placeholder"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thumbnail Generator")
        self.setMinimumSize(500, 300)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Generate thumbnail from a selected frame or image.\n(Placeholder UI)"))
        choose_btn = QPushButton("Choose Image/Frame")
        choose_btn.clicked.connect(self.choose_image)
        layout.addWidget(choose_btn)
        save_btn = QPushButton("Save Thumbnail")
        save_btn.clicked.connect(self.save_thumb)
        layout.addWidget(save_btn)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        self.setLayout(layout)

    def choose_image(self):
        QFileDialog.getOpenFileName(self, "Select image", "", "Images (*.png *.jpg *.jpeg)")

    def save_thumb(self):
        QFileDialog.getSaveFileName(self, "Save thumbnail", "", "Images (*.png *.jpg)")


class AnalyticsDialog(QDialog):
    """Minimal analytics snapshot"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Analytics Dashboard")
        self.setMinimumSize(500, 300)
        layout = QVBoxLayout()
        stats = self.compute_stats()
        text = QTextEdit()
        text.setReadOnly(True)
        text.setPlainText(stats)
        layout.addWidget(text)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        self.setLayout(layout)

    def compute_stats(self):
        output_dir = Path("output")
        total_videos = 0
        voices = {}
        durations = []
        if output_dir.exists():
            for md in output_dir.glob("video_*/metadata.json"):
                try:
                    data = json.load(open(md))
                    total_videos += 1
                    voice = data.get("voice", "Unknown")
                    voices[voice] = voices.get(voice, 0) + 1
                    durations.append(data.get("duration", 0))
                except:
                    pass
        avg_duration = sum(durations)/len(durations) if durations else 0
        top_voice = max(voices.items(), key=lambda x: x[1])[0] if voices else "N/A"
        return (
            f"Total videos: {total_videos}\n"
            f"Average duration: {avg_duration:.1f}s\n"
            f"Most used voice: {top_voice}\n"
        )


class ImportExportDialog(QDialog):
    """Export/import settings"""
    def __init__(self, settings: QSettings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Import/Export Settings")
        self.setMinimumSize(400, 200)
        layout = QVBoxLayout()
        export_btn = QPushButton("Export Settings to JSON")
        export_btn.clicked.connect(self.export_settings)
        layout.addWidget(export_btn)
        import_btn = QPushButton("Import Settings from JSON")
        import_btn.clicked.connect(self.import_settings)
        layout.addWidget(import_btn)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        self.setLayout(layout)

    def export_settings(self):
        file, _ = QFileDialog.getSaveFileName(self, "Export settings", "", "JSON Files (*.json)")
        if file:
            data = {}
            for key in self.settings.allKeys():
                data[key] = self.settings.value(key)
            json.dump(data, open(file, "w"), indent=2)
            QMessageBox.information(self, "Exported", f"Settings saved to {file}")

    def import_settings(self):
        file, _ = QFileDialog.getOpenFileName(self, "Import settings", "", "JSON Files (*.json)")
        if file:
            try:
                data = json.load(open(file))
                for k, v in data.items():
                    self.settings.setValue(k, v)
                QMessageBox.information(self, "Imported", "Settings imported. Restart app to apply.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import: {e}")

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ultimate YouTube Video Generator")
        self.setMinimumSize(1200, 800)
        
        self.settings = QSettings('VideoGenerator', 'Settings')
        self.generator = None
        self.dark_mode = False
        self.setAcceptDrops(True)
        
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
        if self.settings.value('gemini_key'):
            os.environ['GEMINI_API_KEY'] = self.settings.value('gemini_key')
        if self.settings.value('gemini_token'):
            os.environ['GEMINI_ACCESS_TOKEN'] = self.settings.value('gemini_token')
        if self.settings.value('openai_key'):
            os.environ['OPENAI_API_KEY'] = self.settings.value('openai_key')
        if self.settings.value('openai_token'):
            os.environ['OPENAI_ACCESS_TOKEN'] = self.settings.value('openai_token')
    
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
        
        # Tools tab
        tabs.addTab(self.create_tools_tab(), "🧰 Tools")
        
        # Analytics tab
        tabs.addTab(self.create_analytics_tab(), "📊 Analytics")
        
        # Settings tab
        tabs.addTab(self.create_settings_tab(), "⚙️ Settings")
        
        # Help tab
        tabs.addTab(self.create_help_tab(), "❓ Help")
        
        main_layout.addWidget(tabs)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        self.setup_shortcuts()
        
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
        
        # Budget and cost estimation
        budget_group = QGroupBox("💰 Budget & Cost")
        budget_layout = QVBoxLayout()
        
        budget_row = QHBoxLayout()
        budget_row.addWidget(QLabel("Budget limit (per video):"))
        self.budget_combo = QComboBox()
        self.budget_combo.addItems([
            "Free only ($0)",
            "Up to $0.10",
            "Up to $0.50",
            "Up to $1.00",
            "Up to $5.00",
            "No limit"
        ])
        budget_row.addWidget(self.budget_combo)
        budget_row.addStretch()
        budget_layout.addLayout(budget_row)
        
        self.cost_label = QLabel("Estimated cost per video: $0.00")
        budget_layout.addWidget(self.cost_label)
        
        budget_group.setLayout(budget_layout)
        layout.addWidget(budget_group)
        
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
        
        # Cost estimate listeners
        self.duration_spin.valueChanged.connect(self.update_cost_estimate)
        self.voice_combo.currentTextChanged.connect(self.update_cost_estimate)
        self.budget_combo.currentTextChanged.connect(self.update_cost_estimate)
        self.upload_check.stateChanged.connect(self.update_cost_estimate)
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
        
        # Initial cost estimate
        QTimer.singleShot(0, self.update_cost_estimate)
        return tab
    
    def create_history_tab(self):
        """Create history tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(7)
        self.history_table.setHorizontalHeaderLabels(['Title', 'Created', 'Duration', 'Voice', 'Script Src', 'Video Srcs', 'Actions'])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.history_table)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_history)
        layout.addWidget(refresh_btn)
        
        tab.setLayout(layout)
        return tab
    
    def create_tools_tab(self):
        """Tools tab with quick actions"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        btns = [
            ("📝 Script Editor", self.open_script_editor),
            ("📋 Batch Queue", self.open_batch_queue),
            ("🎤 Voice Preview", self.open_voice_preview),
            ("🖼️ Thumbnail Generator", self.open_thumbnail_gen),
            ("📑 Templates", self.open_templates),
            ("📂 Import/Export Settings", self.open_import_export),
            ("🌙 Toggle Dark Mode", self.toggle_theme),
        ]
        for text, handler in btns:
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            layout.addWidget(btn)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_analytics_tab(self):
        """Analytics tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        info = QLabel("Basic analytics summary. Open dashboard for details.")
        layout.addWidget(info)
        open_btn = QPushButton("Open Analytics Dashboard")
        open_btn.clicked.connect(self.open_analytics)
        layout.addWidget(open_btn)
        layout.addStretch()
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

        # Gemini (Google AI)
        gem_layout = QHBoxLayout()
        gem_layout.addWidget(QLabel("Gemini (Google AI):"))
        self.gem_key_input = QLineEdit()
        self.gem_key_input.setEchoMode(QLineEdit.Password)
        self.gem_key_input.setText(self.settings.value('gemini_key', ''))
        gem_layout.addWidget(self.gem_key_input)
        gem_show = QPushButton("👁")
        gem_show.clicked.connect(lambda: self.toggle_password(self.gem_key_input))
        gem_layout.addWidget(gem_show)
        api_layout.addLayout(gem_layout)

        gem_token_layout = QHBoxLayout()
        gem_token_layout.addWidget(QLabel("Gemini Access Token:"))
        self.gem_token_input = QLineEdit()
        self.gem_token_input.setEchoMode(QLineEdit.Password)
        self.gem_token_input.setText(self.settings.value('gemini_token', ''))
        gem_token_layout.addWidget(self.gem_token_input)
        gem_token_show = QPushButton("👁")
        gem_token_show.clicked.connect(lambda: self.toggle_password(self.gem_token_input))
        gem_token_layout.addWidget(gem_token_show)
        api_layout.addLayout(gem_token_layout)

        # OpenAI
        oa_layout = QHBoxLayout()
        oa_layout.addWidget(QLabel("OpenAI API Key:"))
        self.oa_key_input = QLineEdit()
        self.oa_key_input.setEchoMode(QLineEdit.Password)
        self.oa_key_input.setText(self.settings.value('openai_key', ''))
        oa_layout.addWidget(self.oa_key_input)
        oa_show = QPushButton("👁")
        oa_show.clicked.connect(lambda: self.toggle_password(self.oa_key_input))
        oa_layout.addWidget(oa_show)
        api_layout.addLayout(oa_layout)

        oa_token_layout = QHBoxLayout()
        oa_token_layout.addWidget(QLabel("OpenAI Access Token:"))
        self.oa_token_input = QLineEdit()
        self.oa_token_input.setEchoMode(QLineEdit.Password)
        self.oa_token_input.setText(self.settings.value('openai_token', ''))
        oa_token_layout.addWidget(self.oa_token_input)
        oa_token_show = QPushButton("👁")
        oa_token_show.clicked.connect(lambda: self.toggle_password(self.oa_token_input))
        oa_token_layout.addWidget(oa_token_show)
        api_layout.addLayout(oa_token_layout)

        save_keys_btn = QPushButton("💾 Save API Keys")
        save_keys_btn.clicked.connect(self.save_api_keys)
        api_layout.addWidget(save_keys_btn)

        # Provider status
        status_group = QGroupBox("📡 Provider Status")
        status_layout = QVBoxLayout()
        self.provider_status_label = QLabel("Checking providers...")
        status_layout.addWidget(self.provider_status_label)
        status_btn = QPushButton("Refresh Provider Status")
        status_btn.clicked.connect(self.refresh_provider_status)
        status_layout.addWidget(status_btn)
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
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

    def refresh_provider_status(self):
        """Display quick provider status based on env/settings"""
        statuses = []
        if os.getenv('OPENAI_API_KEY') or os.getenv('OPENAI_ACCESS_TOKEN') or self.settings.value('openai_key'):
            statuses.append("✅ OpenAI")
        else:
            statuses.append("⚪ OpenAI (set key)")

        if os.getenv('GEMINI_API_KEY') or os.getenv('GEMINI_ACCESS_TOKEN') or self.settings.value('gemini_key'):
            statuses.append("✅ Gemini")
        else:
            statuses.append("⚪ Gemini (set key/token)")

        if os.getenv('ELEVENLABS_API_KEY') or self.settings.value('elevenlabs_key'):
            statuses.append("✅ ElevenLabs")
        else:
            statuses.append("⚪ ElevenLabs")

        # Ollama check
        try:
            import requests
            r = requests.get('http://localhost:11434/api/tags', timeout=1)
            statuses.append("✅ Ollama" if r.status_code == 200 else "⚪ Ollama")
        except Exception:
            statuses.append("⚪ Ollama")

        self.provider_status_label.setText(" | ".join(statuses))

    def create_desktop_launcher(self):
        """Create a .desktop launcher for Kali/Ubuntu start menu"""
        try:
            repo_dir = Path(__file__).resolve().parent
            start_menu = repo_dir / "start_menu.sh"
            if start_menu.exists():
                start_menu.chmod(start_menu.stat().st_mode | 0o111)

            desktop_dir = Path.home() / ".local/share/applications"
            desktop_dir.mkdir(parents=True, exist_ok=True)
            desktop_file = desktop_dir / "youtube_studio_generator.desktop"

            exec_cmd = f"/bin/bash -lc 'cd \"{repo_dir}\" && ./start_menu.sh'"
            desktop_file.write_text(
                "[Desktop Entry]\n"
                "Name=YouTube Studio Generator\n"
                "Comment=Launch CLI or GUI\n"
                f"Exec={exec_cmd}\n"
                "Icon=utilities-terminal\n"
                "Terminal=true\n"
                "Type=Application\n"
                "Categories=AudioVideo;Utility;\n"
            )

            return True, str(desktop_file)
        except Exception as e:
            return False, str(e)
    
    def save_api_keys(self):
        """Save API keys"""
        if self.el_key_input.text():
            self.settings.setValue('elevenlabs_key', self.el_key_input.text())
            os.environ['ELEVENLABS_API_KEY'] = self.el_key_input.text()
        
        if self.pex_key_input.text():
            self.settings.setValue('pexels_key', self.pex_key_input.text())
            os.environ['PEXELS_API_KEY'] = self.pex_key_input.text()

        if self.gem_key_input.text():
            self.settings.setValue('gemini_key', self.gem_key_input.text())
            os.environ['GEMINI_API_KEY'] = self.gem_key_input.text()

        if self.gem_token_input.text():
            self.settings.setValue('gemini_token', self.gem_token_input.text())
            os.environ['GEMINI_ACCESS_TOKEN'] = self.gem_token_input.text()

        if self.oa_key_input.text():
            self.settings.setValue('openai_key', self.oa_key_input.text())
            os.environ['OPENAI_API_KEY'] = self.oa_key_input.text()

        if self.oa_token_input.text():
            self.settings.setValue('openai_token', self.oa_token_input.text())
            os.environ['OPENAI_ACCESS_TOKEN'] = self.oa_token_input.text()
        
        QMessageBox.information(self, "Success", "API keys saved successfully!")
        self.refresh_provider_status()
    
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
        self.create_launcher_checkbox.setChecked(self.settings.value('create_launcher', False, type=bool))
        self.refresh_provider_status()
    
    def create_video(self):
        """Start video creation"""
        topic = self.topic_input.text().strip()
        
        if not topic:
            QMessageBox.warning(self, "Error", "Please enter a video topic!")
            return
        
        if not GENERATOR_AVAILABLE:
            QMessageBox.critical(self, "Error", "Video generator not available. Check installation.")
            return
        
        est = self.estimate_cost(self.duration_spin.value(), self.voice_combo.currentText(), self.upload_check.isChecked())
        budget_limit = self.get_budget_limit()
        if budget_limit is not None and est > budget_limit:
            reply = QMessageBox.question(
                self,
                "Budget Warning",
                f"Estimated cost ${est:.2f} exceeds your budget limit (${budget_limit:.2f}).\nContinue?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
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
        
    def get_budget_limit(self):
        """Return numeric budget limit or None for no limit"""
        text = self.budget_combo.currentText()
        if "Free only" in text:
            return 0.0
        if "Up to $" in text:
            try:
                val = float(text.split("$")[1])
                return val
            except:
                return None
        return None  # No limit
    
    def estimate_cost(self, duration_seconds, voice_name, upload):
        """
        Rough cost estimate:
        - Voice (premium): ~$0.03 per minute if ElevenLabs key present, else $0
        - Video stock: $0 (free providers)
        - Upload: $0
        """
        minutes = max(duration_seconds / 60.0, 0.25)
        has_el = bool(os.environ.get("ELEVENLABS_API_KEY"))
        voice_cost_per_min = 0.03 if has_el else 0.0
        voice_cost = voice_cost_per_min * minutes
        # keep future placeholders for other services
        total = voice_cost
        return round(total, 2)
    
    def update_cost_estimate(self):
        """Update cost estimate label"""
        est = self.estimate_cost(self.duration_spin.value(), self.voice_combo.currentText(), self.upload_check.isChecked())
        budget_limit = self.get_budget_limit()
        if budget_limit is None:
            budget_text = "Budget: No limit"
        else:
            budget_text = f"Budget: ${budget_limit:.2f} max"
        self.cost_label.setText(f"Estimated cost per video: ${est:.2f}  |  {budget_text}")
    
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
            meta_file = video_dir / "meta.json"
            chosen = metadata_file if metadata_file.exists() else meta_file if meta_file.exists() else None
            if chosen and chosen.exists():
                try:
                    with open(chosen) as f:
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
            
            script_src = meta.get('script_provider') or meta.get('tools', {}).get('script') or 'Unknown'
            videos_srcs = meta.get('video_sources') or meta.get('tools', {}).get('videos') or []
            videos_srcs_display = ", ".join(videos_srcs) if isinstance(videos_srcs, list) else str(videos_srcs)
            
            self.history_table.setItem(row, 4, QTableWidgetItem(str(script_src)))
            self.history_table.setItem(row, 5, QTableWidgetItem(videos_srcs_display))
            
            # Actions button
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            open_btn = QPushButton("📁 Open")
            open_btn.clicked.connect(lambda checked, d=video['dir']: self.open_video_folder(d))
            actions_layout.addWidget(open_btn)
            
            actions_widget.setLayout(actions_layout)
            self.history_table.setCellWidget(row, 6, actions_widget)
    
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
    
    def open_script_editor(self):
        """Open script editor with current topic as seed"""
        text = f"Title: {self.topic_input.text().strip()}\n\nWrite your script here..."
        dlg = ScriptEditorDialog(text, self)
        if dlg.exec_() == QDialog.Accepted:
            edited = dlg.get_text().splitlines()
            if edited:
                self.topic_input.setText(edited[0].replace("Title:", "").strip() or self.topic_input.text())
    
    def open_batch_queue(self):
        dlg = BatchQueueDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            queue = dlg.get_queue()
            if queue:
                QMessageBox.information(self, "Batch Queue", f"{len(queue)} items added to queue (placeholder).")
    
    def open_voice_preview(self):
        dlg = VoicePreviewDialog([self.voice_combo.itemText(i) for i in range(self.voice_combo.count())], self)
        dlg.exec_()
    
    def open_thumbnail_gen(self):
        dlg = ThumbnailDialog(self)
        dlg.exec_()
    
    def open_templates(self):
        dlg = TemplateManagerDialog(self.settings, self)
        dlg.exec_()
    
    def open_import_export(self):
        dlg = ImportExportDialog(self.settings, self)
        dlg.exec_()
    
    def open_analytics(self):
        dlg = AnalyticsDialog(self)
        dlg.exec_()
    
    def setup_shortcuts(self):
        shortcuts = [
            ("New Video", "Ctrl+N", lambda: self.topic_input.setFocus()),
            ("Create Video", "Ctrl+Return", self.create_video),
            ("Batch Queue", "Ctrl+B", self.open_batch_queue),
            ("Script Editor", "Ctrl+E", self.open_script_editor),
            ("Templates", "Ctrl+T", self.open_templates),
            ("History", "Ctrl+H", self.load_history),
            ("Settings", "Ctrl+,", lambda: None),
            ("Quit", "Ctrl+Q", self.close),
            ("Toggle Theme", "Ctrl+D", self.toggle_theme),
        ]
        for name, key, handler in shortcuts:
            act = QAction(name, self)
            act.setShortcut(key)
            act.triggered.connect(handler)
            self.addAction(act)
    
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
    
    def apply_theme(self):
        if self.dark_mode:
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(42, 42, 42))
            palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
            palette.setColor(QPalette.HighlightedText, Qt.black)
            QApplication.instance().setPalette(palette)
        else:
            QApplication.instance().setPalette(QApplication.style().standardPalette())
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() or event.mimeData().hasText():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                path = urls[0].toLocalFile()
                try:
                    text = Path(path).read_text().strip()
                    if text:
                        self.topic_input.setText(text.splitlines()[0])
                        self.log("Loaded topic from dropped file.")
                except Exception as e:
                    self.log(f"Could not read dropped file: {e}")
        elif event.mimeData().hasText():
            self.topic_input.setText(event.mimeData().text().strip())
            self.log("Loaded topic from dropped text.")


def main():
    if sys.platform.startswith("linux") and not os.environ.get("DISPLAY"):
        print("No DISPLAY found. GUI requires a desktop session. Use CLI mode or launch with X11/VNC.")
        sys.exit(1)

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
