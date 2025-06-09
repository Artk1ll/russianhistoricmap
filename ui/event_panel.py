from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal

class EventPanel(QWidget):
    year_selected = pyqtSignal(int)  # сигнал для ползунка и карты

    def __init__(self, events_by_year, parent=None):
        super().__init__(parent)
        self.events_by_year = events_by_year
        self.current_view_mode = "list"
        self.current_year = None

        self.setFixedWidth(300)
        self.setStyleSheet("""
            background-color: rgba(30, 30, 30, 200);
            border: 1px solid #666;
            border-radius: 8px;
            padding: 10px;
            color: white;
        """)

        # Поисковое поле
        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText("Поиск по событиям...")
        self.search_field.setStyleSheet("background-color: #222; color: white; padding: 4px; border-radius: 4px;")
        self.search_field.textChanged.connect(self.on_search)
        self.search_field.returnPressed.connect(self.on_search_enter)

        # Результаты поиска
        self.search_results = QListWidget(self)
        self.search_results.setStyleSheet("background-color: #222; color: white; border-radius: 4px;")
        self.search_results.itemClicked.connect(self.on_result_clicked)
        self.search_results.hide()

        # Основной виджет с событиями
        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.setTextFormat(Qt.RichText)
        self.label.setStyleSheet("font-size: 13px;")
        self.label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.label.linkActivated.connect(self.handle_link_clicked)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        margin = 10
        total_height = self.height()
        total_width = self.width()

        # Высоты отдельных элементов
        search_height = 30
        results_height = 100
        label_height = total_height - (margin * 3 + search_height + results_height)

        # Поле поиска
        self.search_field.setGeometry(
            margin, margin,
            total_width - 2 * margin,
            search_height
        )

        # Список результатов поиска
        self.search_results.setGeometry(
            margin,
            margin + search_height + margin,
            total_width - 2 * margin,
            results_height
        )

        # Метка с событиями
        self.label.setGeometry(
            margin,
            margin + search_height + margin + results_height + margin,
            total_width - 2 * margin,
            label_height
        )

    def update_event(self, year):
        if self.current_view_mode == "details":
            return
        self.current_view_mode = "list"
        self.current_year = str(year)
        events = self.events_by_year.get(self.current_year, [])
        if not events:
            self.label.setText("Нет событий")
            return

        html = "<b>События:</b><br><br>"
        for event in events:
            html += f"• {event['title']}<br>{event['description']}<br><br>"
        print("[DEBUG] HTML:", html)
        self.label.setText(html)

    def show_details_by_id(self, event_id):
        for year, year_events in self.events_by_year.items():
            for event in year_events:
                if event.get("id") == event_id:
                    html = f"<b>{event['title']}</b><br><br>{event['details']}<br><br>"
                    html += "<a href='__back__'>← Назад</a>"
                    self.label.setText(html)
                    self.current_view_mode = "details"
                    self.current_year = year
                    return

    def handle_link_clicked(self, link):
        if link == "__back__":
            self.current_view_mode = "list"
            self.update_event(self.current_year)

    def on_search(self, text):
        self.search_results.clear()
        query = text.lower().strip()
        if not query:
            self.search_results.hide()
            return

        found = 0
        for year, events in self.events_by_year.items():
            for event in events:
                tags = event.get("tags", [])
                if any(query in tag.lower() for tag in tags):
                    item = QListWidgetItem(f"{year} — {event['title']}")
                    item.setData(Qt.UserRole, int(year))
                    self.search_results.addItem(item)
                    found += 1

        self.search_results.setVisible(found > 0)

    def on_result_clicked(self, item):
        year = item.data(Qt.UserRole)
        self.year_selected.emit(year)  # передаём сигнал в ползунок и карту
        self.search_results.hide()
        self.search_field.clear()

    def on_search_enter(self):
        text = self.search_field.text()
        self.on_search(text)
