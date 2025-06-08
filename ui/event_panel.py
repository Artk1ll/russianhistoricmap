from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt

class EventPanel(QWidget):
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

        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.setTextFormat(Qt.RichText)
        self.label.setStyleSheet("font-size: 13px;")
        self.label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.label.linkActivated.connect(self.handle_link_clicked)

    def resizeEvent(self, event):
        self.label.setGeometry(10, 10, self.width() - 20, self.height() - 20)

    def update_event(self, year):
        if self.current_view_mode == "details":
            return  # Не перезаписываем подробности
        self.current_view_mode = "list"
        self.current_year = str(year)
        events = self.events_by_year.get(self.current_year, [])
        if not events:
            self.label.setText("Нет событий")
            return

        html = "<b>События:</b><br><br>"
        for event in events:
            html += f"• {event['title']}<br>{event['description']}<br><br>"
        self.label.setText(html)

    def show_details_by_id(self, event_id):
        for year, year_events in self.events_by_year.items():
            for event in year_events:
                if event.get("id") == event_id:
                    html = f"<b>{event['title']}</b><br><br>{event['details']}<br><br>"
                    html += "<a href='__back__'>← Назад</a>"
                    self.label.setText(html)
                    self.current_view_mode = "details"
                    self.current_year = year  # запоминаем для возврата
                    return

    def handle_link_clicked(self, link):
        if link == "__back__":
            self.current_view_mode = "list"
            self.update_event(self.current_year)
