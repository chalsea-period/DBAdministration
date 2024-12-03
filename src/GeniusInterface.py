import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton,
                               QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget, QHBoxLayout, QDialog)
from PySide6.QtCore import Qt
from controllers import ClientController, TourController, BookingController, PaymentController
from models import Client, Tour, Booking, Payment


class FilterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Filter")
        self.setGeometry(500, 300, 250, 200)
        self.layout = QVBoxLayout(self)

        self.condition_label = QLabel("Filter value (default=None)")
        self.layout.addWidget(self.condition_label)
        self.condition_input = QLineEdit(self)
        self.condition_input.setPlaceholderText(">Value_with_type_of_selected_attribute")
        self.layout.addWidget(self.condition_input)

        self.order_label = QLabel("Order attributes (default=selected)")
        self.layout.addWidget(self.order_label)
        self.order_input = QLineEdit(self)
        self.order_input.setPlaceholderText("attribute_name")
        self.layout.addWidget(self.order_input)

        self.direction_label = QLabel("Order direction (default=ascended)")
        self.layout.addWidget(self.direction_label)
        self.direction_input = QLineEdit(self)
        self.direction_input.setPlaceholderText("ASC|DESC")
        self.layout.addWidget(self.direction_input)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

    def get_filter_value(self):
        return self.condition_input.text()

    def get_direction_value(self):
        return self.direction_input.text()

    def get_attribute_value(self):
        return self.order_input.text()


class TableManager(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.columns = controller.get_attr_names()
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
        self.table.setColumnCount(self.controller.get_columns_count())
        self.table.setHorizontalHeaderLabels(self.controller.get_attr_names())
        self.table.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
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
        valids = [not self.controller.is_invalid_type(value, col, ids=False) for col, value in enumerate(["0"] + values)][1:]
        if all(valids):
            if isinstance(self.controller, ClientController):
                client = Client(None, *values)
                self.controller.add_client(client)
            elif isinstance(self.controller, TourController):
                tour = Tour(None, *values)
                self.controller.add_tour(tour)
            elif isinstance(self.controller, BookingController):
                booking = Booking(None, *values)
                if booking.total_price != self.controller.total_price_counting(booking):
                    QMessageBox.warning(self, "Error", "Wrong total price.")
                    return
                self.controller.add_booking(booking)
            elif isinstance(self.controller, PaymentController):
                payment = Payment(None, *values)
                self.controller.add_payment(payment)

            self.load_records()
            self.clear_inputs()
            QMessageBox.information(self, "Success", f"{self.controller.table_name} added successfully!")
        else:
            QMessageBox.warning(self, "Error", "Wrong input data.")

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

    def on_header_clicked(self, index):
        dialog = FilterDialog(self)
        if dialog.exec() == QDialog.Accepted:
            filter_value = dialog.get_filter_value()
            direction_value = dialog.get_direction_value()
            attribute_value = dialog.get_attribute_value()
            self.filter_records(self.columns[index], filter_value, direction_value, attribute_value)

    def filter_records(self, column, value, direction, attribute):
        records = []
        kwargs = {column: value} if value else {}
        if not attribute:
            attribute = column
        if not self.controller.validate_filter(value, attribute, direction):
            QMessageBox.warning(self, "Error", "Incorrect input")
            return

        if isinstance(self.controller, ClientController):
            records = self.controller.filter_clients(order_by=attribute, order_direction=direction, **kwargs)
        elif isinstance(self.controller, TourController):
            records = self.controller.filter_tours(order_by=attribute, order_direction=direction, **kwargs)
        elif isinstance(self.controller, BookingController):
            records = self.controller.filter_bookings(order_by=attribute, order_direction=direction, **kwargs)
        elif isinstance(self.controller, PaymentController):
            records = self.controller.filter_payments(order_by=attribute, order_direction=direction, **kwargs)

        self.table.setRowCount(len(records))
        for row, record in enumerate(records):
            for col, value in enumerate(record.__dict__.values()):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row, col, item)

    def edit_record(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a record to edit.")
            return

        values = []
        for col in range(self.table.columnCount()):
            item = self.table.item(selected_row, col)
            if self.controller.is_invalid_type(item.text(), col):
                QMessageBox.warning(self, "Error", "Incorrect type")
                self.load_records()
                return
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
    def __init__(self, db_path):
        super().__init__()
        self.setWindowTitle("Admin Interface")
        self.setGeometry(100, 100, 800, 600)
        self.db_path = db_path
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.init_tab("clients")
        self.init_tab("tours")
        self.init_tab("bookings")
        self.init_tab("payments")

    def init_tab(self, tab_name):
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

        table_manager = TableManager(controller)
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
    window = AdminInterface("../databases/TravelAgency.db")
    window.show()
    sys.exit(app.exec())
