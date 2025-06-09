from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from ui.timeline_widget import TimelineWidget
from ui.map_view import MapView
from ui.event_panel import EventPanel
from data.loader import load_borders, load_events, load_points_of_interest

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Историческая карта России")
        self.setGeometry(100, 100, 1280, 800)

        # Загрузка данных
        self.borders_by_year = load_borders()
        self.events_by_year = load_events()
        self.points_of_interest = load_points_of_interest()

        # Центральный виджет и layout
        self.central = QWidget()
        self.setCentralWidget(self.central)
        layout = QVBoxLayout(self.central)
        layout.setContentsMargins(0, 0, 0, 0)

        # Карта
        self.map_view = MapView(self.borders_by_year)
        layout.addWidget(self.map_view)

        # Таймлайн
        self.timeline = TimelineWidget(self.map_view)
        self.timeline.setFixedHeight(60)
        self.timeline.setFixedWidth(800)
        self.timeline.show()

        # Панель событий
        self.event_panel = EventPanel(self.events_by_year, self)
        self.event_panel.setFixedWidth(300)
        self.event_panel.setFixedHeight(350)
        self.event_panel.show()

        # Сигналы
        self.timeline.yearChanged.connect(self.update_year_view)
        self.map_view.markerClicked.connect(self.on_marker_clicked)

        # 🔽 Добавленные сигналы для поиска
        self.event_panel.year_selected.connect(self.timeline.set_value)
        self.event_panel.year_selected.connect(self.update_year_view)

        # Первоначальный год
        self.current_year = self.timeline.value()
        self.update_year_view(self.current_year)

        self.reposition_widgets()
        self.event_panel.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.reposition_widgets()

    def reposition_widgets(self):
        map_rect = self.map_view.viewport().geometry()
        x = map_rect.x() + (map_rect.width() - self.timeline.width()) // 2
        y = map_rect.y() + map_rect.height() - self.timeline.height() - 20
        self.timeline.move(x, y)

        ep_x = self.width() - self.event_panel.width() - 20
        ep_y = self.height() - self.event_panel.height() - 40
        self.event_panel.move(ep_x, ep_y)

    def update_year_view(self, year):
        self.current_year = year
        self.map_view.update_year(year)
        self.map_view.show_points_for_year(year, self.points_of_interest)
        self.event_panel.update_event(year)  # только список, не детали

    def on_marker_clicked(self, event_id: str):
        print(f"[DEBUG] Marker clicked: {event_id}")
        self.event_panel.show_details_by_id(event_id)
