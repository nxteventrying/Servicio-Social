import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import zscore
from sklearn.cluster import DBSCAN
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QPushButton
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Load your data
filename = "YO/FMLV031024/2024_10_03-11_58_51_RR.csv"
df = pd.read_csv(filename)

# Step 1: Calculate z-scores for the 'RtoR' data in df
df['z_scores'] = zscore(df['RtoR'])

# Define an outlier threshold (±3 standard deviations)
z_threshold = 3

# Step 2: Use IQR to define bounds
Q1 = df['RtoR'].quantile(0.25)
Q3 = df['RtoR'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
z_iqr_outliers = (df['z_scores'].abs() > z_threshold) | (df['RtoR'] < lower_bound) | (df['RtoR'] > upper_bound)


class DataAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('HRV Data Outlier Detection')
        
        # Main layout
        layout = QVBoxLayout()
        
        # Sliders layout
        sliders_layout = QVBoxLayout()
        
        # eps Slider
        self.eps_slider = QSlider(Qt.Horizontal)
        self.eps_slider.setMinimum(1)
        self.eps_slider.setMaximum(50)
        self.eps_slider.setValue(10)
        self.eps_slider.valueChanged.connect(self.update_plot)
        
        self.eps_label = QLabel(f'eps: {self.eps_slider.value()}')
        
        # min_samples Slider
        self.min_samples_slider = QSlider(Qt.Horizontal)
        self.min_samples_slider.setMinimum(1)
        self.min_samples_slider.setMaximum(50)
        self.min_samples_slider.setValue(5)
        self.min_samples_slider.valueChanged.connect(self.update_plot)
        
        self.min_samples_label = QLabel(f'min_samples: {self.min_samples_slider.value()}')
        
        # Horizontal Line 1 Slider
        self.hline1_slider = QSlider(Qt.Horizontal)
        self.hline1_slider.setMinimum(0)
        self.hline1_slider.setMaximum(1500)
        self.hline1_slider.setValue(200)
        self.hline1_slider.valueChanged.connect(self.update_plot)
        
        self.hline1_label = QLabel(f'H-Line 1: {self.hline1_slider.value()}')
        
        # Horizontal Line 2 Slider
        self.hline2_slider = QSlider(Qt.Horizontal)
        self.hline2_slider.setMinimum(0)
        self.hline2_slider.setMaximum(1500)
        self.hline2_slider.setValue(1000)
        self.hline2_slider.valueChanged.connect(self.update_plot)
        
        self.hline2_label = QLabel(f'H-Line 2: {self.hline2_slider.value()}')
        
        # Plot Area
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        
        # Add sliders to layout
        sliders_layout.addWidget(self.eps_label)
        sliders_layout.addWidget(self.eps_slider)
        
        sliders_layout.addWidget(self.min_samples_label)
        sliders_layout.addWidget(self.min_samples_slider)
        
        sliders_layout.addWidget(self.hline1_label)
        sliders_layout.addWidget(self.hline1_slider)
        
        sliders_layout.addWidget(self.hline2_label)
        sliders_layout.addWidget(self.hline2_slider)
        
        layout.addLayout(sliders_layout)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
        self.update_plot()
        
    def update_plot(self):
        eps = self.eps_slider.value()
        min_samples = self.min_samples_slider.value()
        hline1 = self.hline1_slider.value()
        hline2 = self.hline2_slider.value()
        
        # Update labels
        self.eps_label.setText(f'eps: {eps}')
        self.min_samples_label.setText(f'min_samples: {min_samples}')
        self.hline1_label.setText(f'H-Line 1: {hline1}')
        self.hline2_label.setText(f'H-Line 2: {hline2}')
        
        # Clear the previous plot
        self.ax.clear()
        
        # DBSCAN
        X = np.column_stack((np.arange(len(df['RtoR'])), df['RtoR']))
        db = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
        df['dbscan_labels'] = db.labels_
        dbscan_outliers = df['dbscan_labels'] == -1
        
        # Combine DBSCAN and z-score/IQR outliers
        df['combined_outliers'] = z_iqr_outliers | dbscan_outliers
        
        # Plotting
        self.ax.plot(df.index, df['RtoR'], label="Original Data", color="blue", alpha=0.6, marker='+', linestyle='')
        self.ax.scatter(df.index[df['combined_outliers']], df['RtoR'][df['combined_outliers']], 
                        color="red", label="Outliers", marker='o', linestyle='')
        
        self.ax.axhline(y=hline1, color='purple', linestyle='--', label=f'Horizontal Line 1 ({hline1})')
        self.ax.axhline(y=hline2, color='orange', linestyle='--', label=f'Horizontal Line 2 ({hline2})')
        
        # Plot settings
        self.ax.set_title("HRV Data Outlier Detection")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("RtoR Value")
        self.ax.set_ylim(0, 1500)
        self.ax.legend()
        
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DataAnalyzer()
    ex.show()
    sys.exit(app.exec_())
