from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from ui.timeline_widget import TimelineWidget
from ui.map_view import MapView
from ui.event_panel import EventPanel
from data.loader import load_borders, load_events

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Историческая карта России")
        self.setGeometry(100, 100, 1280, 800)

        self.borders_by_year = load_borders()
        self.events_by_year = load_events()

        self.central = QWidget()
        self.setCentralWidget(self.central)

        layout = QVBoxLayout(self.central)
        layout.setContentsMargins(0, 0, 0, 0)

        self.map_view = MapView(self.borders_by_year)
        layout.addWidget(self.map_view)

        # Таймлайн
        self.timeline = TimelineWidget(self.map_view)
        self.timeline.setFixedHeight(60)
        self.timeline.setFixedWidth(800)
        self.timeline.show()

        self.timeline.yearChanged.connect(self.map_view.update_year)

        # Панель событий
        self.event_panel = EventPanel(self.events_by_year, self)
        self.event_panel.setFixedWidth(300)
        self.event_panel.setFixedHeight(160)
        self.event_panel.show()

        # Связь таймлайна с панелью событий
        self.timeline.yearChanged.connect(self.event_panel.update_event)

        # Первичная отрисовка
        current_year = self.timeline.value()
        self.map_view.update_year(current_year)
        self.event_panel.update_event(current_year)

        self.reposition_widgets()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.reposition_widgets()

    def reposition_widgets(self):
        # Центрирование таймлайна внизу
        map_rect = self.map_view.viewport().geometry()
        x = map_rect.x() + (map_rect.width() - self.timeline.width()) // 2
        y = map_rect.y() + map_rect.height() - self.timeline.height() - 20
        self.timeline.move(x, y)

        # Панель событий в правом нижнем углу
        ep_x = self.width() - self.event_panel.width() - 20
        ep_y = self.height() - self.event_panel.height() - 40
        self.event_panel.move(ep_x, ep_y)
