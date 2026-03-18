import sys
import os
import subprocess

def install_dependencies():
    """Check and install missing dependencies if possible"""
    required = {'PyQt6', 'numpy', 'scipy', 'soundfile', 'pyyaml'}
    # This is just a helper check, actual installation might require user permission
    # or pip running in environment.
    pass

def main():
    # Ensure src is in path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(base_dir, 'src')
    if src_dir not in sys.path:
        sys.path.append(src_dir)

    print("Starting Audio Morph Studio Pro...")
    
    try:
        from src.ui.main_window import MainWindow, QApplication
    except ImportError as e:
        print(f"Error importing UI components: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r requirements.txt")
        return

    app = QApplication(sys.argv)
    
    # Set App Icon if available
    # app.setWindowIcon(QIcon('resources/icon.png'))
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
