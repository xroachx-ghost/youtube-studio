#!/usr/bin/env python3
"""
Ultimate YouTube Video Generator - COMPLETE GUI
All features implemented except mobile app
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
import threading
import webbrowser
import subprocess
import shutil

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

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


class VideoPreviewDialog(QDialog):
    """Video preview dialog with player"""
    
    def __init__(self, video_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Preview: {Path(video_path).name}")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout()
        
        # Video widget
        self.video_widget = QVideoWidget()
        layout.addWidget(self.video_widget)
        
        # Media player
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player.setVideoOutput(self.video_widget)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(str(video_path))))
        
        # Controls
        controls = QHBoxLayout()
        
        self.play_btn = QPushButton("▶ Play")
        self.play_btn.clicked.connect(self.toggle_play)
        controls.addWidget(self.play_btn)
        
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.sliderMoved.connect(self.set_position)
        controls.addWidget(self.position_slider)
        
        self.time_label = QLabel("00:00 / 00:00")
        controls.addWidget(self.time_label)
        
        layout.addLayout(controls)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        open_btn = QPushButton("📁 Open Folder")
        open_btn.clicked.connect(lambda: self.open_folder(video_path))
        btn_layout.addWidget(open_btn)
        
        btn_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        # Connect player signals
        self.player.durationChanged.connect(self.duration_changed)
        self.player.positionChanged.connect(self.position_changed)
        self.player.stateChanged.connect(self.state_changed)
        
    def toggle_play(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()
    
    def state_changed(self, state):
        if state == QMediaPlayer.PlayingState:
            self.play_btn.setText("⏸ Pause")
        else:
            self.play_btn.setText("▶ Play")
    
    def duration_changed(self, duration):
        self.position_slider.setRange(0, duration)
        
    def position_changed(self, position):
        self.position_slider.setValue(position)
        self.update_time_label(position, self.player.duration())
        
    def set_position(self, position):
        self.player.setPosition(position)
        
    def update_time_label(self, position, duration):
        pos_time = self.format_time(position)
        dur_time = self.format_time(duration)
        self.time_label.setText(f"{pos_time} / {dur_time}")
        
    def format_time(self, ms):
        s = ms // 1000
        m = s // 60
        s = s % 60
        return f"{m:02d}:{s:02d}"
    
    def open_folder(self, video_path):
        folder = Path(video_path).parent
        if sys.platform == "win32":
            os.startfile(folder)
        elif sys.platform == "darwin":
            subprocess.run(["open", str(folder)])
        else:
            subprocess.run(["xdg-open", str(folder)])


class ScriptEditorDialog(QDialog):
    """Script editor with live preview"""
    
    def __init__(self, script_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Script Editor")
        self.setMinimumSize(900, 700)
        self.script_data = script_data
        
        layout = QVBoxLayout()
        
        # Title
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("Title:"))
        self.title_edit = QLineEdit(script_data.get('title', ''))
        title_layout.addWidget(self.title_edit)
        layout.addLayout(title_layout)
        
        # Sections editor
        sections_label = QLabel("<b>Video Sections:</b>")
        layout.addWidget(sections_label)
        
        self.sections_table = QTableWidget()
        self.sections_table.setColumnCount(3)
        self.sections_table.setHorizontalHeaderLabels(['Time', 'Narration', 'Visuals'])
        self.sections_table.horizontalHeader().setStretchLastSection(True)
        
        # Populate sections
        sections = script_data.get('sections', [])
        self.sections_table.setRowCount(len(sections))
        
        for i, section in enumerate(sections):
            self.sections_table.setItem(i, 0, QTableWidgetItem(section.get('time', '')))
            self.sections_table.setItem(i, 1, QTableWidgetItem(section.get('narration', '')))
            self.sections_table.setItem(i, 2, QTableWidgetItem(section.get('visuals', '')))
        
        layout.addWidget(self.sections_table)
        
        # Section controls
        section_btns = QHBoxLayout()
        
        add_btn = QPushButton("➕ Add Section")
        add_btn.clicked.connect(self.add_section)
        section_btns.addWidget(add_btn)
        
        remove_btn = QPushButton("➖ Remove Section")
        remove_btn.clicked.connect(self.remove_section)
        section_btns.addWidget(remove_btn)
        
        section_btns.addStretch()
        layout.addLayout(section_btns)
        
        # Keywords
        keywords_layout = QHBoxLayout()
        keywords_layout.addWidget(QLabel("Keywords:"))
        self.keywords_edit = QLineEdit(", ".join(script_data.get('keywords', [])))
        keywords_layout.addWidget(self.keywords_edit)
        layout.addLayout(keywords_layout)
        
        # Description
        layout.addWidget(QLabel("Description:"))
        self.description_edit = QTextEdit()
        self.description_edit.setPlainText(script_data.get('description', ''))
        self.description_edit.setMaximumHeight(100)
        layout.addWidget(self.description_edit)
        
        # Preview
        preview_group = QGroupBox("📄 Full Script Preview")
        preview_layout = QVBoxLayout()
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        preview_layout.addWidget(self.preview_text)
        
        refresh_btn = QPushButton("🔄 Refresh Preview")
        refresh_btn.clicked.connect(self.update_preview)
        preview_layout.addWidget(refresh_btn)
        
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Save & Use")
        save_btn.clicked.connect(self.accept)
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        self.update_preview()
        
    def add_section(self):
        row = self.sections_table.rowCount()
        self.sections_table.insertRow(row)
        self.sections_table.setItem(row, 0, QTableWidgetItem("0-10s"))
        self.sections_table.setItem(row, 1, QTableWidgetItem("New section narration"))
        self.sections_table.setItem(row, 2, QTableWidgetItem("visuals description"))
        
    def remove_section(self):
        current_row = self.sections_table.currentRow()
        if current_row >= 0:
            self.sections_table.removeRow(current_row)
            
    def update_preview(self):
        preview = f"<h2>{self.title_edit.text()}</h2>"
        preview += "<hr>"
        
        for i in range(self.sections_table.rowCount()):
            time_item = self.sections_table.item(i, 0)
            narration_item = self.sections_table.item(i, 1)
            
            if time_item and narration_item:
                preview += f"<p><b>[{time_item.text()}]</b><br>{narration_item.text()}</p>"
        
        self.preview_text.setHtml(preview)
        
    def get_script_data(self):
        """Get edited script data"""
        sections = []
        for i in range(self.sections_table.rowCount()):
            time_item = self.sections_table.item(i, 0)
            narration_item = self.sections_table.item(i, 1)
            visuals_item = self.sections_table.item(i, 2)
            
            if time_item and narration_item and visuals_item:
                sections.append({
                    'time': time_item.text(),
                    'narration': narration_item.text(),
                    'visuals': visuals_item.text()
                })
        
        keywords = [k.strip() for k in self.keywords_edit.text().split(',') if k.strip()]
        
        return {
            'title': self.title_edit.text(),
            'sections': sections,
            'keywords': keywords,
            'description': self.description_edit.toPlainText(),
            'hook': sections[0]['narration'] if sections else '',
            'cta': sections[-1]['narration'] if sections else ''
        }


class BatchQueueDialog(QDialog):
    """Batch video creation queue"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Batch Video Queue")
        self.setMinimumSize(800, 600)
        self.queue_items = []
        
        layout = QVBoxLayout()
        
        # Add items section
        add_group = QGroupBox("➕ Add to Queue")
        add_layout = QVBoxLayout()
        
        topic_layout = QHBoxLayout()
        topic_layout.addWidget(QLabel("Topic:"))
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Enter video topic...")
        topic_layout.addWidget(self.topic_input)
        add_layout.addLayout(topic_layout)
        
        settings_layout = QHBoxLayout()
        
        settings_layout.addWidget(QLabel("Duration:"))
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(15, 300)
        self.duration_spin.setValue(60)
        self.duration_spin.setSuffix("s")
        settings_layout.addWidget(self.duration_spin)
        
        settings_layout.addWidget(QLabel("Voice:"))
        self.voice_combo = QComboBox()
        self.voice_combo.addItems(["Rachel", "Adam", "Antoni", "Josh", "Bella"])
        settings_layout.addWidget(self.voice_combo)
        
        settings_layout.addStretch()
        add_layout.addLayout(settings_layout)
        
        add_btn = QPushButton("➕ Add to Queue")
        add_btn.clicked.connect(self.add_to_queue)
        add_layout.addWidget(add_btn)
        
        add_group.setLayout(add_layout)
        layout.addWidget(add_group)
        
        # Queue list
        queue_group = QGroupBox("📋 Queue")
        queue_layout = QVBoxLayout()
        
        self.queue_table = QTableWidget()
        self.queue_table.setColumnCount(4)
        self.queue_table.setHorizontalHeaderLabels(['Topic', 'Duration', 'Voice', 'Actions'])
        self.queue_table.horizontalHeader().setStretchLastSection(True)
        queue_layout.addWidget(self.queue_table)
        
        queue_btns = QHBoxLayout()
        
        remove_btn = QPushButton("🗑️ Remove Selected")
        remove_btn.clicked.connect(self.remove_selected)
        queue_btns.addWidget(remove_btn)
        
        clear_btn = QPushButton("🗑️ Clear All")
        clear_btn.clicked.connect(self.clear_queue)
        queue_btns.addWidget(clear_btn)
        
        queue_btns.addStretch()
        
        save_queue_btn = QPushButton("💾 Save Queue")
        save_queue_btn.clicked.connect(self.save_queue)
        queue_btns.addWidget(save_queue_btn)
        
        load_queue_btn = QPushButton("📂 Load Queue")
        load_queue_btn.clicked.connect(self.load_queue)
        queue_btns.addWidget(load_queue_btn)
        
        queue_layout.addLayout(queue_btns)
        
        queue_group.setLayout(queue_layout)
        layout.addWidget(queue_group)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("🎬 Start Processing Queue")
        self.start_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.start_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
    def add_to_queue(self):
        topic = self.topic_input.text().strip()
        if not topic:
            QMessageBox.warning(self, "Error", "Please enter a topic!")
            return
        
        item = {
            'topic': topic,
            'duration': self.duration_spin.value(),
            'voice': self.voice_combo.currentText()
        }
        
        self.queue_items.append(item)
        self.refresh_table()
        self.topic_input.clear()
        
    def refresh_table(self):
        self.queue_table.setRowCount(len(self.queue_items))
        
        for i, item in enumerate(self.queue_items):
            self.queue_table.setItem(i, 0, QTableWidgetItem(item['topic']))
            self.queue_table.setItem(i, 1, QTableWidgetItem(f"{item['duration']}s"))
            self.queue_table.setItem(i, 2, QTableWidgetItem(item['voice']))
            
            # Action button
            btn_widget = QWidget()
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(0, 0, 0, 0)
            
            up_btn = QPushButton("↑")
            up_btn.clicked.connect(lambda checked, idx=i: self.move_up(idx))
            btn_layout.addWidget(up_btn)
            
            down_btn = QPushButton("↓")
            down_btn.clicked.connect(lambda checked, idx=i: self.move_down(idx))
            btn_layout.addWidget(down_btn)
            
            btn_widget.setLayout(btn_layout)
            self.queue_table.setCellWidget(i, 3, btn_widget)
            
    def move_up(self, index):
        if index > 0:
            self.queue_items[index], self.queue_items[index-1] = self.queue_items[index-1], self.queue_items[index]
            self.refresh_table()
            
    def move_down(self, index):
        if index < len(self.queue_items) - 1:
            self.queue_items[index], self.queue_items[index+1] = self.queue_items[index+1], self.queue_items[index]
            self.refresh_table()
            
    def remove_selected(self):
        current_row = self.queue_table.currentRow()
        if current_row >= 0:
            self.queue_items.pop(current_row)
            self.refresh_table()
            
    def clear_queue(self):
        reply = QMessageBox.question(self, "Confirm", "Clear entire queue?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.queue_items.clear()
            self.refresh_table()
            
    def save_queue(self):
        file, _ = QFileDialog.getSaveFileName(self, "Save Queue", "", "JSON Files (*.json)")
        if file:
            with open(file, 'w') as f:
                json.dump(self.queue_items, f, indent=2)
            QMessageBox.information(self, "Success", "Queue saved!")
            
    def load_queue(self):
        file, _ = QFileDialog.getOpenFileName(self, "Load Queue", "", "JSON Files (*.json)")
        if file:
            with open(file, 'r') as f:
                self.queue_items = json.load(f)
            self.refresh_table()
            QMessageBox.information(self, "Success", f"Loaded {len(self.queue_items)} items!")
            
    def get_queue(self):
        return self.queue_items


class ThumbnailGeneratorDialog(QDialog):
    """Thumbnail generator"""
    
    def __init__(self, video_file, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thumbnail Generator")
        self.setMinimumSize(700, 500)
        self.video_file = video_file
        
        layout = QVBoxLayout()
        
        info = QLabel("<b>Generate a custom thumbnail for your video</b>")
        layout.addWidget(info)
        
        # Thumbnail preview
        self.preview_label = QLabel()
        self.preview_label.setMinimumSize(640, 360)
        self.preview_label.setScaledContents(True)
        self.preview_label.setStyleSheet("border: 2px solid #ccc;")
        layout.addWidget(self.preview_label)
        
        # Text overlay
        text_group = QGroupBox("Text Overlay")
        text_layout = QVBoxLayout()
        
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("Title:"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter thumbnail title...")
        self.title_input.textChanged.connect(self.update_preview)
        title_layout.addWidget(self.title_input)
        text_layout.addLayout(title_layout)
        
        subtitle_layout = QHBoxLayout()
        subtitle_layout.addWidget(QLabel("Subtitle:"))
        self.subtitle_input = QLineEdit()
        self.subtitle_input.setPlaceholderText("Optional subtitle...")
        self.subtitle_input.textChanged.connect(self.update_preview)
        subtitle_layout.addWidget(self.subtitle_input)
        text_layout.addLayout(subtitle_layout)
        
        text_group.setLayout(text_layout)
        layout.addWidget(text_group)
        
        # Options
        options_layout = QHBoxLayout()
        
        options_layout.addWidget(QLabel("Font Size:"))
        self.font_size = QSpinBox()
        self.font_size.setRange(20, 100)
        self.font_size.setValue(48)
        self.font_size.valueChanged.connect(self.update_preview)
        options_layout.addWidget(self.font_size)
        
        options_layout.addWidget(QLabel("Style:"))
        self.style_combo = QComboBox()
        self.style_combo.addItems(["Bold", "Shadow", "Outline"])
        self.style_combo.currentTextChanged.connect(self.update_preview)
        options_layout.addWidget(self.style_combo)
        
        options_layout.addStretch()
        layout.addLayout(options_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        extract_btn = QPushButton("🎬 Extract Frame from Video")
        extract_btn.clicked.connect(self.extract_frame)
        btn_layout.addWidget(extract_btn)
        
        save_btn = QPushButton("💾 Save Thumbnail")
        save_btn.clicked.connect(self.save_thumbnail)
        btn_layout.addWidget(save_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        self.extract_frame()
        
    def extract_frame(self):
        """Extract first frame from video"""
        try:
            output = Path(self.video_file).parent / "thumbnail_temp.jpg"
            subprocess.run([
                'ffmpeg', '-i', str(self.video_file),
                '-vf', 'scale=1280:720',
                '-vframes', '1',
                '-y', str(output)
            ], capture_output=True, check=True)
            
            pixmap = QPixmap(str(output))
            self.preview_label.setPixmap(pixmap)
            self.base_pixmap = pixmap
            self.update_preview()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to extract frame: {e}")
            
    def update_preview(self):
        """Update preview with text overlay"""
        if not hasattr(self, 'base_pixmap'):
            return
            
        pixmap = self.base_pixmap.copy()
        painter = QPainter(pixmap)
        
        # Setup font
        font = QFont('Arial', self.font_size.value(), QFont.Bold)
        painter.setFont(font)
        
        # Style
        style = self.style_combo.currentText()
        if style == "Shadow":
            painter.setPen(QPen(Qt.black, 3))
            painter.drawText(pixmap.rect(), Qt.AlignCenter, self.title_input.text())
            painter.setPen(Qt.white)
        elif style == "Outline":
            painter.setPen(QPen(Qt.black, 5))
            painter.drawText(pixmap.rect(), Qt.AlignCenter, self.title_input.text())
            painter.setPen(Qt.white)
        else:
            painter.setPen(Qt.white)
        
        # Draw title
        rect = pixmap.rect()
        rect.setHeight(rect.height() // 2)
        painter.drawText(rect, Qt.AlignCenter, self.title_input.text())
        
        # Draw subtitle
        if self.subtitle_input.text():
            font.setPointSize(self.font_size.value() // 2)
            painter.setFont(font)
            rect.moveTop(rect.height())
            painter.drawText(rect, Qt.AlignCenter, self.subtitle_input.text())
        
        painter.end()
        
        self.preview_label.setPixmap(pixmap)
        
    def save_thumbnail(self):
        """Save thumbnail"""
        file, _ = QFileDialog.getSaveFileName(
            self, "Save Thumbnail", 
            str(Path(self.video_file).parent / "thumbnail.jpg"),
            "Image Files (*.jpg *.png)"
        )
        
        if file:
            self.preview_label.pixmap().save(file)
            QMessageBox.information(self, "Success", f"Thumbnail saved to:\n{file}")


class VideoTemplateDialog(QDialog):
    """Video template manager"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Video Templates")
        self.setMinimumSize(600, 500)
        self.templates = self.load_templates()
        
        layout = QVBoxLayout()
        
        # Template list
        list_group = QGroupBox("📋 Saved Templates")
        list_layout = QVBoxLayout()
        
        self.template_list = QListWidget()
        self.template_list.itemDoubleClicked.connect(self.load_template)
        self.refresh_list()
        list_layout.addWidget(self.template_list)
        
        list_group.setLayout(list_layout)
        layout.addWidget(list_group)
        
        # Template details
        details_group = QGroupBox("📝 Template Details")
        details_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        details_layout.addRow("Name:", self.name_input)
        
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(15, 300)
        self.duration_spin.setValue(60)
        details_layout.addRow("Duration:", self.duration_spin)
        
        self.voice_combo = QComboBox()
        self.voice_combo.addItems(["Rachel", "Adam", "Antoni", "Josh", "Bella"])
        details_layout.addRow("Voice:", self.voice_combo)
        
        self.style_combo = QComboBox()
        self.style_combo.addItems(["Professional", "Casual", "Educational", "Entertaining"])
        details_layout.addRow("Style:", self.style_combo)
        
        details_group.setLayout(details_layout)
        layout.addWidget(details_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Save Template")
        save_btn.clicked.connect(self.save_template)
        btn_layout.addWidget(save_btn)
        
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.clicked.connect(self.delete_template)
        btn_layout.addWidget(delete_btn)
        
        btn_layout.addStretch()
        
        use_btn = QPushButton("✓ Use Template")
        use_btn.clicked.connect(self.accept)
        btn_layout.addWidget(use_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
    def load_templates(self):
        """Load saved templates"""
        templates_file = Path("templates.json")
        if templates_file.exists():
            with open(templates_file) as f:
                return json.load(f)
        return {}
        
    def save_templates(self):
        """Save templates to file"""
        with open("templates.json", 'w') as f:
            json.dump(self.templates, f, indent=2)
            
    def refresh_list(self):
        """Refresh template list"""
        self.template_list.clear()
        for name in self.templates.keys():
            self.template_list.addItem(name)
            
    def save_template(self):
        """Save current template"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Please enter a template name!")
            return
            
        self.templates[name] = {
            'duration': self.duration_spin.value(),
            'voice': self.voice_combo.currentText(),
            'style': self.style_combo.currentText()
        }
        
        self.save_templates()
        self.refresh_list()
        QMessageBox.information(self, "Success", f"Template '{name}' saved!")
        
    def load_template(self, item):
        """Load selected template"""
        name = item.text()
        if name in self.templates:
            template = self.templates[name]
            self.name_input.setText(name)
            self.duration_spin.setValue(template['duration'])
            self.voice_combo.setCurrentText(template['voice'])
            self.style_combo.setCurrentText(template['style'])
            
    def delete_template(self):
        """Delete selected template"""
        current = self.template_list.currentItem()
        if current:
            name = current.text()
            reply = QMessageBox.question(self, "Confirm", f"Delete template '{name}'?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                del self.templates[name]
                self.save_templates()
                self.refresh_list()
                
    def get_template(self):
        """Get current template settings"""
        return {
            'name': self.name_input.text(),
            'duration': self.duration_spin.value(),
            'voice': self.voice_combo.currentText(),
            'style': self.style_combo.currentText()
        }


# Continue in next file due to length...
