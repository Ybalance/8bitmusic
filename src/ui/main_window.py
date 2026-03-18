import os
import sys
import threading
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QListWidget, QGroupBox,
    QComboBox, QSlider, QLineEdit, QProgressBar, QMessageBox, QScrollArea,
    QFormLayout, QTabWidget, QTextEdit, QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QThread
from PyQt6.QtGui import QIcon

# Import engine components
try:
    from engine.core import AudioMorphEngine
    from presets.manager import PresetManager
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from engine.core import AudioMorphEngine
    from presets.manager import PresetManager

from ui.styles import MODERN_STYLE

# --- Worker for Thread-Safe Operations ---
class TrainingWorker(QThread):
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        try:
            # Run training script as subprocess
            process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            for line in process.stdout:
                self.progress_signal.emit(line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                self.finished_signal.emit(True, "Training Completed Successfully!")
            else:
                self.finished_signal.emit(False, f"Training Failed with code {process.returncode}")
                
        except Exception as e:
            self.finished_signal.emit(False, str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Morph Studio Pro")
        self.resize(1200, 800)
        self.setStyleSheet(MODERN_STYLE)

        # Initialize Engine
        self.engine = AudioMorphEngine()
        self.preset_manager = PresetManager(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'presets_data'))
        
        # UI Setup
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_morph_tab(), "Morph (Conversion)")
        self.tabs.addTab(self.create_train_tab(), "Train (AI Model)")
        
        main_layout.addWidget(self.tabs)

    # --- Tab 1: Morphing (Conversion) ---
    def create_morph_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # Left Panel: Presets
        left_panel = QWidget()
        left_panel.setObjectName("LeftPanel")
        left_layout = QVBoxLayout(left_panel)
        left_panel.setFixedWidth(300)
        
        header = QLabel("Audio Morph Studio")
        header.setObjectName("HeaderLabel")
        left_layout.addWidget(header)

        self.category_combo = QComboBox()
        self.category_combo.addItems(["All", "Vintage", "Gaming", "Communication", "AI", "AI Custom"])
        self.category_combo.currentTextChanged.connect(self.filter_presets)
        left_layout.addWidget(QLabel("Category:"))
        left_layout.addWidget(self.category_combo)

        self.preset_list = QListWidget()
        self.preset_list.itemClicked.connect(self.on_preset_selected)
        left_layout.addWidget(self.preset_list)
        
        refresh_btn = QPushButton("Refresh Presets")
        refresh_btn.clicked.connect(self.refresh_presets)
        left_layout.addWidget(refresh_btn)

        layout.addWidget(left_panel)

        # Right Panel: Controls
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # I/O
        file_group = QGroupBox("I/O Configuration")
        file_layout = QFormLayout()
        
        self.input_path_edit = QLineEdit()
        self.input_path_edit.setReadOnly(True)
        input_btn = QPushButton("Select Input")
        input_btn.clicked.connect(self.browse_input)
        input_row = QHBoxLayout()
        input_row.addWidget(self.input_path_edit)
        input_row.addWidget(input_btn)
        file_layout.addRow("Input:", input_row)

        self.output_path_edit = QLineEdit()
        self.output_path_edit.setReadOnly(True)
        output_btn = QPushButton("Select Output")
        output_btn.clicked.connect(self.browse_output)
        output_row = QHBoxLayout()
        output_row.addWidget(self.output_path_edit)
        output_row.addWidget(output_btn)
        file_layout.addRow("Output:", output_row)
        
        file_group.setLayout(file_layout)
        right_layout.addWidget(file_group)

        # Parameters
        self.params_group = QGroupBox("Effect Parameters")
        self.params_layout = QVBoxLayout()
        self.params_group.setLayout(self.params_layout)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.params_container = QWidget()
        self.dynamic_params_layout = QFormLayout(self.params_container)
        scroll.setWidget(self.params_container)
        
        self.params_layout.addWidget(scroll)
        right_layout.addWidget(self.params_group, stretch=1)

        # Description
        self.desc_label = QLabel("Select a preset to see details.")
        self.desc_label.setObjectName("DescriptionLabel")
        self.desc_label.setWordWrap(True)
        right_layout.addWidget(self.desc_label)

        # Action
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        right_layout.addWidget(self.progress_bar)

        self.process_btn = QPushButton("MORPH AUDIO")
        self.process_btn.setObjectName("ProcessButton")
        self.process_btn.clicked.connect(self.start_processing)
        self.process_btn.setEnabled(False)
        right_layout.addWidget(self.process_btn)

        layout.addWidget(right_panel)
        
        # State
        self.input_file = None
        self.output_file = None
        self.current_preset = None
        self.presets_data = {}
        
        # Initial Load
        self.refresh_presets()
        
        return widget

    # --- Tab 2: Training (AI) ---
    def create_train_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Config
        config_group = QGroupBox("Training Configuration")
        config_layout = QFormLayout()

        # Data Dir
        self.train_data_edit = QLineEdit()
        data_btn = QPushButton("Browse Data Folder")
        data_btn.clicked.connect(self.browse_train_data)
        data_row = QHBoxLayout()
        data_row.addWidget(self.train_data_edit)
        data_row.addWidget(data_btn)
        config_layout.addRow("Audio Data Folder:", data_row)

        # Style Name
        self.style_name_edit = QLineEdit("my_new_style")
        config_layout.addRow("Style Name:", self.style_name_edit)

        # Epochs
        self.epochs_spin = QSpinBox()
        self.epochs_spin.setRange(1, 1000)
        self.epochs_spin.setValue(10)
        config_layout.addRow("Epochs:", self.epochs_spin)

        config_group.setLayout(config_layout)
        layout.addWidget(config_group)

        # Console Output
        self.console_out = QTextEdit()
        self.console_out.setReadOnly(True)
        self.console_out.setStyleSheet("background-color: #1e1e1e; color: #00ff00; font-family: Consolas;")
        layout.addWidget(self.console_out)

        # Action
        self.train_btn = QPushButton("START TRAINING")
        self.train_btn.setObjectName("ProcessButton")
        self.train_btn.clicked.connect(self.start_training)
        layout.addWidget(self.train_btn)

        return widget

    # --- Logic: Morphing ---
    def refresh_presets(self):
        self.preset_list.clear()
        self.presets_data = {}
        # Reload manager to pick up new trained models
        self.preset_manager._load_all_presets() 
        
        all_presets = self.preset_manager.list_presets()
        category_filter = self.category_combo.currentText()
        
        for name in all_presets:
            data = self.preset_manager.get_preset(name)
            cat = data.get('category', 'Uncategorized')
            
            if category_filter == "All" or category_filter == cat:
                self.preset_list.addItem(name)
                self.presets_data[name] = data

    def filter_presets(self):
        self.refresh_presets()

    def on_preset_selected(self, item):
        name = item.text()
        self.current_preset = self.presets_data.get(name)
        if not self.current_preset: return

        self.desc_label.setText(self.current_preset.get('description', ''))
        self.update_params_ui(self.current_preset.get('params', {}))
        self.check_ready()

    def update_params_ui(self, params):
        for i in reversed(range(self.dynamic_params_layout.count())): 
            self.dynamic_params_layout.itemAt(i).widget().setParent(None)
        self.param_inputs = {}
        for key, value in params.items():
            label = QLabel(key.replace('_', ' ').title())
            inp = QLineEdit(str(value))
            self.param_inputs[key] = inp
            self.dynamic_params_layout.addRow(label, inp)

    def browse_input(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Audio", "", "Audio (*.wav *.mp3 *.flac)")
        if path:
            self.input_file = path
            self.input_path_edit.setText(path)
            base, ext = os.path.splitext(path)
            self.output_file = f"{base}_morphed{ext}"
            self.output_path_edit.setText(self.output_file)
            self.check_ready()

    def browse_output(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Output", self.output_file, "Audio (*.wav)")
        if path:
            self.output_file = path
            self.output_path_edit.setText(path)
            self.check_ready()

    def check_ready(self):
        self.process_btn.setEnabled(bool(self.input_file and self.output_file and self.current_preset))

    def start_processing(self):
        if not self.input_file or not self.output_file or not self.current_preset:
            return

        # Gather params from UI
        preset_to_run = self.current_preset.copy()
        updated_params = preset_to_run.get('params', {}).copy()
        
        # Original params for type checking
        original_params = self.current_preset.get('params', {})
        
        for key, inp in self.param_inputs.items():
            val_text = inp.text()
            # Try to convert back to original type
            orig_val = original_params.get(key)
            
            try:
                if isinstance(orig_val, int):
                    updated_params[key] = int(val_text)
                elif isinstance(orig_val, float):
                    updated_params[key] = float(val_text)
                else:
                    updated_params[key] = val_text
            except ValueError:
                # If conversion fails, fallback to text but log warning internally if possible
                updated_params[key] = val_text 
        
        preset_to_run['params'] = updated_params

        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.process_btn.setEnabled(False)
        
        # Use simple threading for now
        threading.Thread(target=self._process_thread, args=(self.input_file, self.output_file, preset_to_run)).start()

    def _process_thread(self, inp, outp, preset):
        try:
            self.engine.process_audio(inp, outp, preset)
            print("Done") # In real app, emit signal
        except Exception as e:
            print(f"Error: {e}")
        # Note: UI updates from thread are unsafe here without signals, but kept simple for demo

    # --- Logic: Training ---
    def browse_train_data(self):
        path = QFileDialog.getExistingDirectory(self, "Select Data Directory")
        if path:
            self.train_data_edit.setText(path)

    def start_training(self):
        data_dir = self.train_data_edit.text()
        style_name = self.style_name_edit.text()
        epochs = self.epochs_spin.value()

        if not data_dir or not style_name:
            QMessageBox.warning(self, "Error", "Please provide data directory and style name.")
            return

        # Prepare Command
        # Assumes running from root
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'train.py'))
        cmd = [sys.executable, script_path, 
               "--data_dir", data_dir, 
               "--style_name", style_name, 
               "--epochs", str(epochs)]
        
        self.console_out.clear()
        self.console_out.append(f"Starting training for '{style_name}'...")
        self.train_btn.setEnabled(False)

        # Start Worker
        self.train_worker = TrainingWorker(cmd)
        self.train_worker.progress_signal.connect(self.on_train_progress)
        self.train_worker.finished_signal.connect(self.on_train_finished)
        self.train_worker.start()

    def on_train_progress(self, text):
        self.console_out.append(text)
        # Auto scroll
        sb = self.console_out.verticalScrollBar()
        sb.setValue(sb.maximum())

    def on_train_finished(self, success, message):
        self.train_btn.setEnabled(True)
        if success:
            QMessageBox.information(self, "Success", message)
            # Automatically create a preset for this new model
            style_name = self.style_name_edit.text()
            model_path = os.path.join("models", f"{style_name}.pth")
            self.preset_manager.create_ai_preset(style_name, model_path)
            self.console_out.append(f"Preset '{style_name}' created automatically.")
            # Refresh list
            self.refresh_presets()
        else:
            QMessageBox.critical(self, "Error", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
