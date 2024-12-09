from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QFormLayout,
                               QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget, QHBoxLayout, QDialog)
from PySide6.QtCore import Qt
import sys
from PySide6.QtWidgets import QApplication
from GeniusInterface import ScheduleManager
from repositories import ClientRepository, WasherRepository, ServiceRepository, OrderRepository,ScheduleRepository
from controllers import ClientController, WasherController, ServiceController, OrderController, ScheduleController


class UserScheduleManager(ScheduleManager):
    def __init__(self, controller, parent=None):
        super().__init__(controller, parent)

    def init_table(self, layout):
        # Таблица для отображения записей
        self.table = QTableWidget()
        self.table.setColumnCount(self.controller.get_columns_count())
        self.table.setHorizontalHeaderLabels(self.controller.get_attr_names())
        # self.table.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
        # Делаем таблицу неизменяемой
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

    def init_change(self, layout):
        return

    def edit_record(self):
        return

    def delete_record(self):
        return

    def on_header_clicked(self, index):
        return


class UserInterface(QMainWindow):
    def __init__(self, services_controller, schedule_controller):
        super().__init__()
        self.setWindowTitle("Client Interface")
        self.setGeometry(100, 100, 800, 600)

        self.services_controller = services_controller
        self.schedule_controller = schedule_controller

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        self.init_services()
        self.init_schedule()
        self.init_order()

    def init_services(self):
        tab = QWidget()
        self.tabs.addTab(tab, "services")
        layout = QVBoxLayout(tab)

        # Таблица для отображения записей
        self.table = QTableWidget()
        self.table.setColumnCount(self.services_controller.get_columns_count())
        self.table.setHorizontalHeaderLabels(self.services_controller.get_attr_names())
        # Делаем таблицу неизменяемой
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        records = self.services_controller.get_all()
        self.table.setRowCount(len(records))
        for row, record in enumerate(records):
            for col, value in enumerate(record.__dict__.values()):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row, col, item)

        layout.addWidget(self.table)

    def init_schedule(self):
        tab = QWidget()
        self.tabs.addTab(tab, "schedule")
        layout = QVBoxLayout(tab)

        schedule_manager = UserScheduleManager(self.schedule_controller)
        layout.addWidget(schedule_manager)

    def init_order(self):
        tab = QWidget()
        self.tabs.addTab(tab, "make_order")
        layout = QFormLayout(tab)

        self.services_input = QLineEdit(self)
        self.services_input.setPlaceholderText("")
        layout.addRow("services", self.services_input)

        self.washer_input = QLineEdit(self)
        self.washer_input.setPlaceholderText("INTEGER")
        layout.addRow("washer_id", self.washer_input)

        self.time_input = QLineEdit(self)
        self.time_input.setPlaceholderText("8am-6pm")
        layout.addRow("Time", self.time_input)

        add_button = QPushButton(f"Make order")
        add_button.clicked.connect(self.make_order)
        layout.addWidget(add_button)

    def make_order(self):
        pass


if __name__ == '__main__':
    db_path = "../databases/auto_washer.db"
    service_repo = ServiceRepository(db_path)
    schedule_repo = ScheduleRepository(db_path)

    service_controller = ServiceController(service_repo)
    schedule_controller = ScheduleController(schedule_repo)

    app = QApplication(sys.argv)
    window = UserInterface(service_controller, schedule_controller)
    window.show()
    sys.exit(app.exec())
