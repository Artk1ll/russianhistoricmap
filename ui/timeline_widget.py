from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QHBoxLayout, QSpinBox, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal

class TimelineWidget(QWidget):
    yearChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.min_year = 862
        self.max_year = 2020

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            QWidget {
                background: transparent;
            }

            QSlider::groove:horizontal {
                height: 10px;
                background: rgba(100, 70, 30, 120);
                border-radius: 5px;
            }

            QSlider::handle:horizontal {
                background: #d2ab78;
                border: 2px solid #5c3a21;
                width: 20px;
                height: 20px;
                margin: -7px 0;
                border-radius: 10px;
            }

            QSpinBox {
                background: rgba(240, 222, 190, 200);
                color: #3e2f1c;
                font-weight: bold;
                border: 2px solid #a78a63;
                border-radius: 6px;
                padding: 6px;
                font-size: 16px;
            }

            QSpinBox::up-button, QSpinBox::down-button {
                width: 0px;
                height: 0px;
                border: none;
            }

            QLabel {
                color: #4a331e;
                font-weight: bold;
                font-size: 20px;
                padding: 4px;
            }
        """)

        # Слайдер растягиваемый
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(self.min_year)
        self.slider.setMaximum(self.max_year)
        self.slider.setTickInterval(50)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setFixedHeight(30)
        self.slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Поле ручного ввода (без стрелок)
        self.spin_box = QSpinBox()
        self.spin_box.setRange(self.min_year, self.max_year)
        self.spin_box.setFixedWidth(100)

        # Метка года (большая и выразительная)
        self.label = QLabel(f"Год: {self.min_year}")
        self.label.setFixedWidth(120)

        # Компоновка
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(20)
        layout.addWidget(self.label)
        layout.addWidget(self.slider)
        layout.addWidget(self.spin_box)
        self.setLayout(layout)

        # Синхронизация
        self.slider.valueChanged.connect(self.on_slider_changed)
        self.spin_box.valueChanged.connect(self.on_spinbox_changed)

    def on_slider_changed(self, value):
        self.label.setText(f"Год: {value}")
        self.spin_box.setValue(value)
        self.yearChanged.emit(value)

    def on_spinbox_changed(self, value):
        self.slider.setValue(value)

    def value(self):
        return self.slider.value()

    def set_value(self, year):
        self.slider.setValue(year)