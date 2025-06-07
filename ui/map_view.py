from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsPolygonItem, QGraphicsEllipseItem
from PyQt5.QtGui import QPixmap, QPolygonF, QPen, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QPointF, pyqtSignal
from shapely.geometry import Polygon
from shapely.ops import unary_union

class HoverablePolygonItem(QGraphicsPolygonItem):
    def __init__(self, polygon, normal_pen, hover_pen):
        super().__init__(polygon)
        self.normal_pen = normal_pen
        self.hover_pen = hover_pen
        self.setPen(self.normal_pen)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        self.setPen(self.hover_pen)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setPen(self.normal_pen)
        super().hoverLeaveEvent(event)

class MapView(QGraphicsView):
    markerClicked = pyqtSignal(str)
    def __init__(self, borders_by_year):
        super().__init__()

        self.raw_borders_by_year = borders_by_year
        self.original_size = (1920, 1080)

        self.points = []

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.setRenderHint(QPainter.Antialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)

        self.setStyleSheet("background-color: black; border: none;")
        self.bg_pixmap = QPixmap("assets/Airbrush-Image-Enhancer-1748799855806.jpeg")
        self.bg_item = QGraphicsPixmapItem(self.bg_pixmap)
        self.scene.addItem(self.bg_item)

        self.current_items = []
        self.current_year = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._resize_background()
        if self.current_year is not None:
            self.update_year(self.current_year)

    def _resize_background(self):
        view_size = self.viewport().size()
        if not self.bg_pixmap.isNull():
            scaled = self.bg_pixmap.scaled(
                view_size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )
            self.bg_item.setPixmap(scaled)
            self.bg_item.setPos(0, 0)
            self.scene.setSceneRect(0, 0, scaled.width(), scaled.height())

    def scale_coords(self, coords):
        orig_w, orig_h = self.original_size
        curr_w, curr_h = self.viewport().width(), self.viewport().height()
        scale_x = curr_w / orig_w
        scale_y = curr_h / orig_h
        return [[x * scale_x, y * scale_y] for x, y in coords]

    def draw_poly_outline(self, qpoly, main_color=Qt.black, outline_color=Qt.white, z=3):
        outline = QGraphicsPolygonItem(qpoly)
        outline.setPen(QPen(outline_color, 6))
        outline.setBrush(QBrush(Qt.NoBrush))
        outline.setZValue(z - 0.1)
        self.scene.addItem(outline)
        self.current_items.append(outline)

        hoverable = HoverablePolygonItem(
            qpoly,
            QPen(main_color, 2),
            QPen(QColor("orange"), 2, Qt.SolidLine)
        )
        hoverable.setBrush(QBrush(Qt.NoBrush))
        hoverable.setZValue(z)
        self.scene.addItem(hoverable)
        self.current_items.append(hoverable)

    def update_year(self, year):
        self.current_year = year
        for item in self.current_items:
            self.scene.removeItem(item)
        self.current_items.clear()

        past_polygons = []
        for y in sorted(self.raw_borders_by_year.keys()):
            if int(y) < int(year):
                for coords in self.raw_borders_by_year[y]:
                    if len(coords) < 3:
                        continue
                    poly = Polygon(self.scale_coords(coords))
                    if not poly.is_valid:
                        poly = poly.buffer(0)
                    if poly.is_valid and not poly.is_empty:
                        past_polygons.append(poly)
        past_union = unary_union(past_polygons) if past_polygons else None

        current_polygons = []
        for coords in self.raw_borders_by_year.get(year, []):
            if len(coords) < 3:
                continue
            poly = Polygon(self.scale_coords(coords))
            if not poly.is_valid:
                poly = poly.buffer(0)
            if poly.is_valid and not poly.is_empty:
                current_polygons.append(poly)
        current_union = unary_union(current_polygons) if current_polygons else None

        if past_union:
            for poly in past_union.geoms if hasattr(past_union, "geoms") else [past_union]:
                qpoly = QPolygonF([QPointF(x, y) for x, y in poly.exterior.coords])
                self.draw_poly_outline(qpoly, main_color=Qt.darkGray, outline_color=Qt.black, z=1)

        for poly in current_polygons:
            if past_union and not poly.difference(past_union).is_empty:
                diff = poly.difference(past_union)
                geometries = diff.geoms if hasattr(diff, "geoms") else [diff]
                for g in geometries:
                    if not isinstance(g, Polygon) or not g.is_valid or g.is_empty:
                        continue
                    qpoly = QPolygonF([QPointF(x, y) for x, y in g.exterior.coords])
                    item = QGraphicsPolygonItem(qpoly)
                    item.setPen(QPen(Qt.green, 2, Qt.DashLine))
                    item.setBrush(QBrush(Qt.green, Qt.Dense4Pattern))
                    item.setZValue(2.5)
                    self.scene.addItem(item)
                    self.current_items.append(item)

        if current_union:
            for poly in current_union.geoms if hasattr(current_union, "geoms") else [current_union]:
                qpoly = QPolygonF([QPointF(x, y) for x, y in poly.exterior.coords])
                self.draw_poly_outline(qpoly, main_color=Qt.black, outline_color=Qt.lightGray, z=3)

    def wheelEvent(self, event):
        # Отключить реакцию на колесо мыши (чтобы карта не прокручивалась)
        event.ignore()

    def show_points_for_year(self, year, points):
        self.clear_points()
        for point in points:
            if point["year"] == year:
                self.add_interest_point(point["coordinates"], point["id"])

    def clear_points(self):
        for item in self.points:
            self.scene.removeItem(item)
        self.points.clear()

    def add_interest_point(self, coordinates, event_id):
        x, y = self.scale_coords([coordinates])[0]
        radius = 8
        circle = QGraphicsEllipseItem(x - radius / 2, y - radius / 2, radius, radius)
        circle.setBrush(QBrush(Qt.red))
        circle.setPen(QPen(Qt.black))
        circle.setZValue(10)
        circle.setData(0, event_id)

        def mousePressEvent(event, eid=event_id):
            self.markerClicked.emit(eid)

        circle.mousePressEvent = mousePressEvent
        self.scene.addItem(circle)
        self.points.append(circle)