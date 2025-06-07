from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt

class EventPanel(QWidget):
    def __init__(self, events_by_year: dict, parent=None):
        super().__init__(parent)
        self.events_by_year = events_by_year
        self.events_by_year = {}
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
        self.label.setTextFormat(Qt.RichText)  # Поддержка HTML
        self.label.setStyleSheet("font-size: 13px;")
        self.label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

    def resizeEvent(self, event):
        self.label.setGeometry(10, 10, self.width() - 20, self.height() - 20)

    def update_event(self, year: int):
        event = self.events_by_year.get(year)
        if event:
            title = event.get("title", "")
            desc = event.get("description", "")
            formatted = f"<b>{title}</b><br><br>{desc}"
            self.label.setText(formatted)
        else:
            self.label.setText("Нет данных о событиях")

    def show_details_by_id(self, event_id):
        for year_events in self.events_by_year.values():
            for event in year_events:
                if event["id"] == event_id:
                    self.details_widget.setText(event["details"])
                    self.stack.setCurrentIndex(1)
                    return