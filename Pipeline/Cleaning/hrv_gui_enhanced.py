import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import zscore
from sklearn.cluster import DBSCAN
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout,
    QPushButton, QFileDialog, QMainWindow
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class DataAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.df = None

    def initUI(self):
        self.setWindowTitle('HRV Data Outlier Detection')
        self.setGeometry(100, 100, 1200, 800)
        self.setAcceptDrops(True)
        
        # Main widget and layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)

        # Sliders layout
        sliders_layout = QVBoxLayout()

        # eps Slider
        self.eps_slider = self.create_slider(1, 50, 10, "eps")
        sliders_layout.addLayout(self.eps_slider['layout'])

        # min_samples Slider
        self.min_samples_slider = self.create_slider(1, 50, 5, "min_samples")
        sliders_layout.addLayout(self.min_samples_slider['layout'])

        # Horizontal Line 1 Slider
        self.hline1_slider = self.create_slider(0, 1500, 200, "H-Line 1")
        sliders_layout.addLayout(self.hline1_slider['layout'])

        # Horizontal Line 2 Slider
        self.hline2_slider = self.create_slider(0, 1500, 1000, "H-Line 2")
        sliders_layout.addLayout(self.hline2_slider['layout'])

        # Vertical Line 1 Slider
        self.vline1_slider = self.create_slider(0, 500, 100, "V-Line 1")
        sliders_layout.addLayout(self.vline1_slider['layout'])

        # Vertical Line 2 Slider
        self.vline2_slider = self.create_slider(0, 500, 300, "V-Line 2")
        sliders_layout.addLayout(self.vline2_slider['layout'])

        # Plot Area
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        layout.addLayout(sliders_layout)

        # Save Button
        self.save_button = QPushButton("Save Cleaned Data")
        self.save_button.clicked.connect(self.save_cleaned_data)
        layout.addWidget(self.save_button)

        self.update_plot()

    def create_slider(self, min_val, max_val, default, label):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default)
        slider.valueChanged.connect(self.update_plot)
        label_widget = QLabel(f'{label}: {slider.value()}')
        layout = QHBoxLayout()
        layout.addWidget(label_widget)
        layout.addWidget(slider)
        return {'slider': slider, 'label': label_widget, 'layout': layout}
        
    def update_plot(self):
        if self.df is None:
            return

        eps = self.eps_slider['slider'].value()
        min_samples = self.min_samples_slider['slider'].value()
        hline1 = self.hline1_slider['slider'].value()
        hline2 = self.hline2_slider['slider'].value()
        vline1 = self.vline1_slider['slider'].value()
        vline2 = self.vline2_slider['slider'].value()

        # Update labels
        self.eps_slider['label'].setText(f'eps: {eps}')
        self.min_samples_slider['label'].setText(f'min_samples: {min_samples}')
        self.hline1_slider['label'].setText(f'H-Line 1: {hline1}')
        self.hline2_slider['label'].setText(f'H-Line 2: {hline2}')
        self.vline1_slider['label'].setText(f'V-Line 1: {vline1}')
        self.vline2_slider['label'].setText(f'V-Line 2: {vline2}')

        # Clear the previous plot
        self.ax.clear()

        # Step 1: Calculate z-scores
        self.df['z_scores'] = zscore(self.df['RtoR'])

        # Step 2: DBSCAN
        X = np.column_stack((np.arange(len(self.df['RtoR'])), self.df['RtoR']))
        db = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
        self.df['dbscan_labels'] = db.labels_
        dbscan_outliers = self.df['dbscan_labels'] == -1

        # Step 3: Combine outliers
        Q1 = self.df['RtoR'].quantile(0.25)
        Q3 = self.df['RtoR'].quantile(0.75)
        IQR = Q3 - Q1
        z_iqr_outliers = (self.df['z_scores'].abs() > 3) | (self.df['RtoR'] < Q1 - 1.5 * IQR) | (self.df['RtoR'] > Q3 + 1.5 * IQR)
        self.df['combined_outliers'] = z_iqr_outliers | dbscan_outliers

        # Plot data
        self.ax.plot(self.df.index, self.df['RtoR'], label="Original Data", color="blue", alpha=0.6, marker='+', linestyle='')
        self.ax.scatter(self.df.index[self.df['combined_outliers']], self.df['RtoR'][self.df['combined_outliers']], 
                        color="red", label="Outliers", marker='o', linestyle='')

        # Add lines
        self.ax.axhline(y=hline1, color='purple', linestyle='--')
        self.ax.axhline(y=hline2, color='orange', linestyle='--')
        self.ax.axvline(x=vline1, color='gray', linestyle='--')
        self.ax.axvline(x=vline2, color='brown', linestyle='--')
        self.ax.axvspan(vline1, vline2, color='yellow', alpha=0.1)

        self.canvas.draw()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            filename = url.toLocalFile()
            if filename.endswith('.csv'):
                self.load_data(filename)
                break

    def load_data(self, filename):
        self.df = pd.read_csv(filename)
        self.vline1_slider['slider'].setMaximum(len(self.df) - 1)
        self.vline2_slider['slider'].setMaximum(len(self.df) - 1)
        self.update_plot()

    def save_cleaned_data(self):
        if self.df is not None:
            cleaned_df = self.df[~self.df['combined_outliers']]
            cleaned_df.to_csv("cleaned_data.csv", index=False)
            print("Cleaned data saved as 'cleaned_data.csv'.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataAnalyzer()
    window.show()
    sys.exit(app.exec_())
