import sys
import re
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton,
                               QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget, QHBoxLayout)
from PySide6.QtCore import Qt
from controllers import ClientController, TourController, BookingController, PaymentController
from models import Client, Tour, Booking, Payment

"""
Нужны проверки на все типы (чтобы телефон обязательно был телефон и т.д.)
Наверное нужно сделать, чтобы некоторые типы можно было не вводить 
Возможно стоит сделать некоторые пункты по-умолчанию
Визуализация БД
Фильтрация
"""


def is_integer(text):
    integer_pattern = re.compile(r'^\d+$')
    return bool(integer_pattern.match(text))


def is_date(text):
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    return bool(date_pattern.match(text))


class TableManager(QWidget):
    def __init__(self, controller, columns, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.columns = columns
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Форма для добавления записи
        self.inputs = {}
        types_list = self.controller.get_attr_types()[1:]
        for i, column in enumerate(self.columns[1:]):
            label = QLabel(column)
            layout.addWidget(label)

            input_field = QLineEdit()
            input_field.setPlaceholderText(types_list[i] if types_list[i] != "DATE" else "DATE (YYYY-MM-DD)")
            layout.addWidget(input_field)
            self.inputs[column] = input_field

        add_button = QPushButton(f"Add {self.controller.table_name}")
        add_button.clicked.connect(self.add_record)
        layout.addWidget(add_button)

        # Таблица для отображения записей
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        layout.addWidget(self.table)

        # Кнопки для редактирования и удаления
        button_layout = QHBoxLayout()
        edit_button = QPushButton("Edit Selected")
        edit_button.clicked.connect(self.edit_record)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_record)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

        self.load_records()

    def add_record(self):
        values = [self.inputs[column].text() for column in self.columns[1:]]
        if all(values):
            if isinstance(self.controller, ClientController):
                client = Client(None, *values)
                self.controller.add_client(client)
            elif isinstance(self.controller, TourController):
                tour = Tour(None, *values)
                self.controller.add_tour(tour)
            elif isinstance(self.controller, BookingController):
                booking = Booking(None, *values)
                self.controller.add_booking(booking)
            elif isinstance(self.controller, PaymentController):
                payment = Payment(None, *values)
                self.controller.add_payment(payment)

            self.load_records()
            self.clear_inputs()
            QMessageBox.information(self, "Success", f"{self.table_name.capitalize()} added successfully!")
        else:
            QMessageBox.warning(self, "Error", "Please fill in all required fields.")

    def load_records(self):
        records = []
        if isinstance(self.controller, ClientController):
            records = self.controller.get_all_clients()
        elif isinstance(self.controller, TourController):
            records = self.controller.get_all_tours()
        elif isinstance(self.controller, BookingController):
            records = self.controller.get_all_bookings()
        elif isinstance(self.controller, PaymentController):
            records = self.controller.get_all_payments()

        self.table.setRowCount(len(records))
        for row, record in enumerate(records):
            for col, value in enumerate(record.__dict__.values()):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row, col, item)

    def clear_inputs(self):
        for input_field in self.inputs.values():
            input_field.clear()

    def edit_record(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a record to edit.")
            return

        values = []
        # types_list = get_attr_types(self.cursor, self.table_name)
        for col in range(self.table.columnCount()):
            item = self.table.item(selected_row, col)

            # if (types_list[col] == "INTEGER" and not is_integer(item.text())) or \
            #         (types_list[col] == "DATE" and not is_date(item.text())):
            #     QMessageBox.warning(self, "Error", "Incorrect type")
            #     self.load_records()
            #     return

            values.append(item.text())

        # Первый столбец - это идентификатор записи
        record_id = values[0]
        values = values[1:]

        if isinstance(self.controller, ClientController):
            client = Client(record_id, *values)
            self.controller.update_client(client)
        elif isinstance(self.controller, TourController):
            tour = Tour(record_id, *values)
            self.controller.update_tour(tour)
        elif isinstance(self.controller, BookingController):
            booking = Booking(record_id, *values)
            self.controller.update_booking(booking)
        elif isinstance(self.controller, PaymentController):
            payment = Payment(record_id, *values)
            self.controller.update_payment(payment)

        self.load_records()
        QMessageBox.information(self, "Success", f"{self.controller.table_name} updated successfully!")

    def delete_record(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a record to delete.")
            return

        record_id = self.table.item(selected_row, 0).text()

        if isinstance(self.controller, ClientController):
            self.controller.delete_client(record_id)
        elif isinstance(self.controller, TourController):
            self.controller.delete_tour(record_id)
        elif isinstance(self.controller, BookingController):
            self.controller.delete_booking(record_id)
        elif isinstance(self.controller, PaymentController):
            self.controller.delete_payment(record_id)

        admin_interface = self.window()
        if isinstance(admin_interface, AdminInterface):
            admin_interface.update_all_tables()
        QMessageBox.information(self, "Success", f"{self.controller.table_name} deleted successfully!")


class AdminInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Interface")
        self.setGeometry(100, 100, 800, 600)
        self.db_path = "TravelAgency.db"
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.init_tab("clients", ["client_id", "name", "email", "phone", "address", "date_of_birth"])
        self.init_tab("tours", ["tour_id", "title", "city_of_departure", "destination", "start_date",
                                "end_date", "price", "available_place"])
        self.init_tab("bookings",
                      ["booking_id", "client_id", "tour_id", "booking_date", "people_number", "total_price", "status"])
        self.init_tab("payments", ["payment_id", "booking_id", "payment_date", "amount", "payment_method"])

    def init_tab(self, tab_name, columns):
        tab = QWidget()
        self.tabs.addTab(tab, tab_name)
        layout = QVBoxLayout(tab)

        controller = None
        if tab_name == "clients":
            controller = ClientController(self.db_path)
        elif tab_name == "tours":
            controller = TourController(self.db_path)
        elif tab_name == "bookings":
            controller = BookingController(self.db_path)
        elif tab_name == "payments":
            controller = PaymentController(self.db_path)

        table_manager = TableManager(controller, columns)
        layout.addWidget(table_manager)

    def closeEvent(self, event):
        for index in range(self.tabs.count()):
            tab = self.tabs.widget(index)
            table_manager = tab.findChild(TableManager)
            if table_manager:
                table_manager.controller.repo.close()
        event.accept()

    def update_all_tables(self):
        for index in range(self.tabs.count()):
            tab = self.tabs.widget(index)
            table_manager = tab.findChild(TableManager)
            if table_manager:
                table_manager.load_records()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminInterface()
    window.show()
    sys.exit(app.exec())
