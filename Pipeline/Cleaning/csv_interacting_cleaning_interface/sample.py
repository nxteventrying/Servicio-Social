from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtCore import Qt
import pandas as pd
import matplotlib.pyplot as plt

class FileDropper(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Plotter")
        self.setGeometry(100, 100, 800, 600)

        # Enable drag-and-drop for the main widget
        self.setAcceptDrops(True)

        self.label = QLabel("Drop your CSV file here or click to select", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("border: 2px dashed gray;")
        self.label.setFixedSize(600, 100)
        self.label.mousePressEvent = self.select_file

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        # Accept drag events with file URLs
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # Handle dropped files
        file_path = event.mimeData().urls()[0].toLocalFile()
        if file_path.endswith('.csv'):
            self.plot_csv(file_path)
        else:
            self.label.setText("Please drop a valid CSV file")

    def select_file(self, event):
        # Open file dialog to select a CSV file
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.plot_csv(file_path)

    def plot_csv(self, file_path):
        try:
            # Read the CSV file
            data = pd.read_csv(file_path, header=None)

            # Determine x and y columns
            if data.shape[1] == 2:
                x = data.iloc[:, 0]
                y = data.iloc[:, 1]
            elif data.shape[1] == 1:
                x = range(len(data))
                y = data.iloc[:, 0]
            else:
                raise ValueError("CSV must have 1 or 2 columns")

            # Plot the data
            plt.figure(figsize=(8, 6))
            plt.plot(x, y, marker='o', linestyle='-', color='b')
            plt.title("CSV Plot")
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.show()
        except Exception as e:
            self.label.setText(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication([])
    window = FileDropper()
    window.show()
    app.exec_()
