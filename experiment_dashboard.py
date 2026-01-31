import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox,
    QStackedWidget, QScrollArea, QGridLayout, QFrame, QDialog,
    QDialogButtonBox, QTextEdit, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd


class ProfileSettingsDialog(QDialog):
    """Dialog for profile settings"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Profile Settings")
        self.setMinimumWidth(400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Name section
        name_label = QLabel("Name:")
        name_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        self.name_input.setText("John Doe")  # Default name
        
        # Email section
        email_label = QLabel("Email:")
        email_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setText("john.doe@example.com")  # Default email
        
        # Password section
        password_label = QLabel("Change Password:")
        password_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.old_password_input = QLineEdit()
        self.old_password_input.setPlaceholderText("Old password")
        self.old_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("New password")
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm new password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Delete profile section
        delete_label = QLabel("Danger Zone:")
        delete_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        delete_label.setStyleSheet("color: red;")
        
        self.delete_btn = QPushButton("Delete Profile")
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_profile)
        
        # Add widgets to layout
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addSpacing(10)
        
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        layout.addSpacing(10)
        
        layout.addWidget(password_label)
        layout.addWidget(self.old_password_input)
        layout.addWidget(self.new_password_input)
        layout.addWidget(self.confirm_password_input)
        layout.addSpacing(20)
        
        layout.addWidget(delete_label)
        layout.addWidget(self.delete_btn)
        layout.addSpacing(20)
        
        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.save_settings)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
    
    def save_settings(self):
        """Save profile settings"""
        # Validate password change
        if self.new_password_input.text():
            if self.new_password_input.text() != self.confirm_password_input.text():
                QMessageBox.warning(self, "Error", "Passwords do not match!")
                return
            if not self.old_password_input.text():
                QMessageBox.warning(self, "Error", "Please enter your old password!")
                return
        
        # Save settings (in a real app, you'd save to a database)
        QMessageBox.information(self, "Success", "Profile settings saved successfully!")
        self.accept()
    
    def delete_profile(self):
        """Delete user profile"""
        reply = QMessageBox.question(
            self,
            "Delete Profile",
            "Are you sure you want to delete your profile? This action cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Profile Deleted", "Your profile has been deleted.")
            self.accept()


class MatplotlibCanvas(FigureCanvas):
    """Matplotlib canvas for displaying graphs"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        
    def plot_data(self, x_data, y_data, title="Graph", xlabel="X", ylabel="Y", plot_type="line"):
        """Plot data on the canvas"""
        self.axes.clear()
        
        if plot_type == "line":
            self.axes.plot(x_data, y_data, marker='o', linestyle='-', linewidth=2)
        elif plot_type == "bar":
            self.axes.bar(x_data, y_data)
        elif plot_type == "scatter":
            self.axes.scatter(x_data, y_data, s=50, alpha=0.6)
        
        self.axes.set_title(title, fontsize=14, fontweight='bold')
        self.axes.set_xlabel(xlabel, fontsize=10)
        self.axes.set_ylabel(ylabel, fontsize=10)
        self.axes.grid(True, alpha=0.3)
        self.fig.tight_layout()
        self.draw()


class MainDashboard(QMainWindow):
    """Main Dashboard Application"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Application")
        self.setGeometry(100, 100, 1200, 700)
        
        # Data storage
        self.uploaded_data = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main UI"""
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Create main content area
        content_area = self.create_content_area()
        main_layout.addWidget(content_area, 1)
        
    def create_sidebar(self):
        """Create sidebar menu"""
        sidebar = QFrame()
        sidebar.setMaximumWidth(250)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
            }
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                padding: 15px;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:pressed {
                background-color: #1abc9c;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # App title
        title_label = QLabel("📊 Dashboard")
        title_label.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 20px;
            background-color: #1abc9c;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Menu buttons
        dashboard_btn = QPushButton("🏠 Dashboard")
        dashboard_btn.clicked.connect(lambda: self.switch_page(0))
        
        upload_btn = QPushButton("📁 Upload Files")
        upload_btn.clicked.connect(lambda: self.switch_page(1))
        
        graphs_btn = QPushButton("📈 Graphs")
        graphs_btn.clicked.connect(lambda: self.switch_page(2))
        
        profile_btn = QPushButton("👤 Profile Settings")
        profile_btn.clicked.connect(self.open_profile_settings)
        
        layout.addWidget(dashboard_btn)
        layout.addWidget(upload_btn)
        layout.addWidget(graphs_btn)
        layout.addWidget(profile_btn)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        # Footer
        footer_label = QLabel("v1.0.0")
        footer_label.setStyleSheet("color: #95a5a6; padding: 10px;")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer_label)
        
        return sidebar
    
    def create_content_area(self):
        """Create main content area with stacked pages"""
        self.stacked_widget = QStackedWidget()
        
        # Page 0: Dashboard overview
        dashboard_page = self.create_dashboard_page()
        self.stacked_widget.addWidget(dashboard_page)
        
        # Page 1: Upload files
        upload_page = self.create_upload_page()
        self.stacked_widget.addWidget(upload_page)
        
        # Page 2: Graphs
        graphs_page = self.create_graphs_page()
        self.stacked_widget.addWidget(graphs_page)
        
        return self.stacked_widget
    
    def create_dashboard_page(self):
        """Create dashboard overview page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = QLabel("Dashboard Overview")
        header.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        layout.addWidget(header)
        
        # Stats cards
        stats_layout = QGridLayout()
        stats_layout.setSpacing(20)
        
        # Create stat cards
        cards_data = [
            ("Total Users", "1,234", "#3498db"),
            ("Revenue", "$45,678", "#2ecc71"),
            ("Active Sessions", "89", "#e74c3c"),
            ("Growth Rate", "+12.5%", "#f39c12")
        ]
        
        for i, (title, value, color) in enumerate(cards_data):
            card = self.create_stat_card(title, value, color)
            stats_layout.addWidget(card, i // 2, i % 2)
        
        layout.addLayout(stats_layout)
        layout.addStretch()
        
        return page
    
    def create_stat_card(self, title, value, color):
        """Create a statistics card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        card.setMinimumHeight(120)
        
        card_layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 14px;")
        
        value_label = QLabel(value)
        value_label.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")
        
        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        card_layout.addStretch()
        
        return card
    
    def create_upload_page(self):
        """Create file upload page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = QLabel("Upload Files")
        header.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        layout.addWidget(header)
        
        # Upload section
        upload_frame = QFrame()
        upload_frame.setStyleSheet("""
            QFrame {
                background-color: #ecf0f1;
                border: 2px dashed #95a5a6;
                border-radius: 10px;
                padding: 40px;
            }
        """)
        
        upload_layout = QVBoxLayout(upload_frame)
        
        # Upload icon/text
        upload_label = QLabel("📤 Drop files here or click to browse")
        upload_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        upload_label.setFont(QFont("Arial", 16))
        upload_layout.addWidget(upload_label)
        
        # Upload buttons
        button_layout = QHBoxLayout()
        
        csv_btn = QPushButton("Upload CSV File")
        csv_btn.setStyleSheet(self.get_button_style("#3498db"))
        csv_btn.clicked.connect(lambda: self.upload_file("csv"))
        
        pdf_btn = QPushButton("Upload PDF File")
        pdf_btn.setStyleSheet(self.get_button_style("#e74c3c"))
        pdf_btn.clicked.connect(lambda: self.upload_file("pdf"))
        
        button_layout.addWidget(csv_btn)
        button_layout.addWidget(pdf_btn)
        upload_layout.addLayout(button_layout)
        
        layout.addWidget(upload_frame)
        
        # File info display
        self.file_info_label = QLabel("No file uploaded")
        self.file_info_label.setStyleSheet("padding: 20px; font-size: 14px;")
        layout.addWidget(self.file_info_label)
        
        # Data preview
        self.data_preview = QTextEdit()
        self.data_preview.setReadOnly(True)
        self.data_preview.setPlaceholderText("File preview will appear here...")
        layout.addWidget(self.data_preview)
        
        layout.addStretch()
        
        return page
    
    def create_graphs_page(self):
        """Create graphs display page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = QLabel("Data Visualization")
        header.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        layout.addWidget(header)
        
        # Control buttons
        control_layout = QHBoxLayout()
        
        line_btn = QPushButton("Line Chart")
        line_btn.setStyleSheet(self.get_button_style("#3498db"))
        line_btn.clicked.connect(lambda: self.plot_sample_data("line"))
        
        bar_btn = QPushButton("Bar Chart")
        bar_btn.setStyleSheet(self.get_button_style("#2ecc71"))
        bar_btn.clicked.connect(lambda: self.plot_sample_data("bar"))
        
        scatter_btn = QPushButton("Scatter Plot")
        scatter_btn.setStyleSheet(self.get_button_style("#e74c3c"))
        scatter_btn.clicked.connect(lambda: self.plot_sample_data("scatter"))
        
        control_layout.addWidget(line_btn)
        control_layout.addWidget(bar_btn)
        control_layout.addWidget(scatter_btn)
        control_layout.addStretch()
        
        layout.addLayout(control_layout)
        
        # Matplotlib canvas
        self.canvas = MatplotlibCanvas(self, width=10, height=6, dpi=100)
        layout.addWidget(self.canvas)
        
        # Instructions
        info_label = QLabel("Upload your data and click a chart type to visualize it")
        info_label.setStyleSheet("color: #7f8c8d; font-style: italic; padding: 10px;")
        layout.addWidget(info_label)
        
        return page
    
    def get_button_style(self, color):
        """Get button style with specified color"""
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
            }}
            QPushButton:pressed {{
                background-color: {color}aa;
            }}
        """
    
    def switch_page(self, index):
        """Switch to a different page"""
        self.stacked_widget.setCurrentIndex(index)
    
    def open_profile_settings(self):
        """Open profile settings dialog"""
        dialog = ProfileSettingsDialog(self)
        dialog.exec()
    
    def upload_file(self, file_type):
        """Upload CSV or PDF file"""
        if file_type == "csv":
            file_filter = "CSV Files (*.csv);;All Files (*)"
        else:
            file_filter = "PDF Files (*.pdf);;All Files (*)"
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            f"Select {file_type.upper()} File",
            "",
            file_filter
        )
        
        if file_path:
            try:
                if file_type == "csv":
                    # Read CSV file
                    self.uploaded_data = pd.read_csv(file_path)
                    preview = f"File: {file_path}\n\n"
                    preview += f"Shape: {self.uploaded_data.shape}\n"
                    preview += f"Columns: {list(self.uploaded_data.columns)}\n\n"
                    preview += "First 10 rows:\n"
                    preview += self.uploaded_data.head(10).to_string()
                    
                    self.data_preview.setPlainText(preview)
                    self.file_info_label.setText(f"✅ CSV file loaded: {file_path.split('/')[-1]}")
                    
                else:
                    # PDF handling (basic)
                    self.file_info_label.setText(f"✅ PDF file uploaded: {file_path.split('/')[-1]}")
                    self.data_preview.setPlainText(f"PDF file: {file_path}\n\nPDF parsing would require additional libraries like PyPDF2.")
                
                QMessageBox.information(self, "Success", f"{file_type.upper()} file uploaded successfully!")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")
    
    def plot_sample_data(self, plot_type):
        """Plot data on the canvas"""
        if self.uploaded_data is not None and not self.uploaded_data.empty:
            # Use actual uploaded data
            try:
                # Get first two numeric columns
                numeric_cols = self.uploaded_data.select_dtypes(include=['number']).columns
                if len(numeric_cols) >= 2:
                    x_data = self.uploaded_data[numeric_cols[0]].values
                    y_data = self.uploaded_data[numeric_cols[1]].values
                    xlabel = numeric_cols[0]
                    ylabel = numeric_cols[1]
                elif len(numeric_cols) == 1:
                    y_data = self.uploaded_data[numeric_cols[0]].values
                    x_data = list(range(len(y_data)))
                    xlabel = "Index"
                    ylabel = numeric_cols[0]
                else:
                    raise ValueError("No numeric columns found")
                
                self.canvas.plot_data(
                    x_data, y_data,
                    title=f"Data Visualization - {plot_type.capitalize()}",
                    xlabel=xlabel,
                    ylabel=ylabel,
                    plot_type=plot_type
                )
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not plot data: {str(e)}\nUsing sample data instead.")
                self.plot_sample_default(plot_type)
        else:
            # Use sample data
            self.plot_sample_default(plot_type)
    
    def plot_sample_default(self, plot_type):
        """Plot sample default data"""
        import numpy as np
        x_data = np.linspace(0, 10, 50)
        y_data = np.sin(x_data) * 10 + np.random.randn(50) * 2
        
        self.canvas.plot_data(
            x_data, y_data,
            title=f"Sample {plot_type.capitalize()} Chart",
            xlabel="X Axis",
            ylabel="Y Axis",
            plot_type=plot_type
        )


def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = MainDashboard()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()