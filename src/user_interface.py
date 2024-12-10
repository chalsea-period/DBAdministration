from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QFormLayout,
                               QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget, QHBoxLayout, QDialog)
from GeniusInterface import ScheduleManager
from models import orders


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
    def __init__(self, controllers):
        super().__init__()
        self.setWindowTitle("Client Interface")
        self.setGeometry(100, 100, 800, 600)

        self.services_controller = controllers["services"]
        self.schedule_controller = controllers["schedule"]
        self.washers_controller = controllers["washers"]
        self.orders_controller = controllers["orders"]

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        self.init_services()
        self.init_washers()
        self.init_schedule()
        self.init_order()

        self.client_id = -1

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

    def init_washers(self):
        tab = QWidget()
        self.tabs.addTab(tab, "washers")
        layout = QVBoxLayout(tab)

        # Таблица для отображения записей
        self.table = QTableWidget()
        self.table.setColumnCount(self.washers_controller.get_columns_count())
        self.table.setHorizontalHeaderLabels(self.washers_controller.get_attr_names())
        # Делаем таблицу неизменяемой
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        records = self.washers_controller.get_all()
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

        self.schedule_manager = UserScheduleManager(self.schedule_controller)
        layout.addWidget(self.schedule_manager)

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

        self.day_input = QLineEdit(self)
        self.day_input.setPlaceholderText("DATE (YYYY-MM-DD)")
        layout.addRow("work_day", self.day_input)

        self.time_input = QLineEdit(self)
        self.time_input.setPlaceholderText("8am-6pm")
        layout.addRow("Time", self.time_input)

        add_button = QPushButton(f"Make order")
        add_button.clicked.connect(self.make_order)
        layout.addWidget(add_button)

    def set_client_id(self, client_id):
        self.client_id = client_id

    def make_order(self):
        values = ["1", str(self.client_id), self.services_input.text(), self.washer_input.text(), "awaiting",
                  self.day_input.text(), self.time_input.text()]
        is_valid, error_text = self.orders_controller.validate_record_types(values)
        if not is_valid:
            QMessageBox.warning(self, "Error", error_text)
            return

        order = orders(None, *values[1:])
        self.orders_controller.add(order)
        schedule_record = self.schedule_controller.get_record_by_pk(self.day_input.text(), self.washer_input.text())
        setattr(schedule_record, "hour_" + self.time_input.text(), 1)
        self.schedule_controller.update(schedule_record)
        self.schedule_manager.load_records()
        QMessageBox.information(self, "Success", "Order was accepted")

    def closeEvent(self, event):
        for controller in [self.services_controller, self.schedule_controller]:
            controller.repo.close()
        event.accept()
