from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QFormLayout,
                               QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget, QHBoxLayout, QDialog)
from genius_interface import ScheduleManager


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


class UserAccountManager(QWidget):
    def __init__(self, client_controller, orders_controller, exit_func, parent=None):
        super().__init__(parent)

        self.client_id = -1
        self.client_controller = client_controller
        self.client_columns = client_controller.get_attr_names()

        self.order_controller = orders_controller
        self.orders_columns = orders_controller.get_attr_names()

        layout = QVBoxLayout(self)
        self.init_user_data_section(layout)
        self.init_orders_section(layout)
        self.init_change(layout)
        self.init_exit(layout, exit_func)
        self.load_records()

    def set_id(self, id):
        self.client_id = id
        self.load_records()

    def init_user_data_section(self, layout):
        # Лейбл для данных пользователя
        user_data_label = QLabel("User Data")
        layout.addWidget(user_data_label)

        # Таблица для данных пользователя
        self.user_data_table = QTableWidget()
        self.user_data_table.setColumnCount(self.client_controller.get_columns_count() - 3)
        self.user_data_table.setHorizontalHeaderLabels(self.client_controller.get_attr_names())
        layout.addWidget(self.user_data_table)

    def init_orders_section(self, layout):
        # Лейбл для заказов
        orders_label = QLabel("Orders")
        layout.addWidget(orders_label)

        # Таблица для заказов
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(self.order_controller.get_columns_count())
        self.orders_table.setHorizontalHeaderLabels(self.order_controller.get_attr_names())
        layout.addWidget(self.orders_table)

    def init_change(self, layout):
        # Кнопка для редактирования
        self.edit_button = QPushButton("Edit Selected")
        self.edit_button.clicked.connect(self.edit_record)
        layout.addWidget(self.edit_button)

    def init_exit(self, layout, exit_func):
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(exit_func)
        layout.addWidget(exit_button)

    def load_records(self):
        if self.client_id == -1:
            return
        user_record = self.client_controller.get_by_id(self.client_id)
        self.update_table(self.user_data_table, [user_record])

        orders_records = self.order_controller.get_by_client_id(self.client_id)
        self.update_table(self.orders_table, orders_records)

    def update_table(self, table, records):
        table.setRowCount(len(records))
        for row, record in enumerate(records):
            for col, value in enumerate(record.__dict__.values()):
                item = QTableWidgetItem(str(value))
                table.setItem(row, col, item)

    def edit_record(self):
        if self.user_data_table.hasFocus():
            selected_table = self.user_data_table
            controller = self.client_controller
        elif self.orders_table.hasFocus():
            selected_table = self.orders_table
            controller = self.order_controller
        else:
            QMessageBox.warning(self, "Error", "Please select a table to edit.")
            return

        selected_row = selected_table.currentRow()
        selected_col = selected_table.currentColumn()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a record to edit.")
            return
        if controller.validate_primary_key_cols(selected_col):
            QMessageBox.warning(self, "Error", "You selected a primary key")
            self.load_records()
            return

        values = [selected_table.item(selected_row, col).text() for col in range(selected_table.columnCount())]
        is_valid, error_text = controller.validate_record_types(values)
        if not is_valid:
            QMessageBox.warning(self, "Error", error_text)
            self.load_records()
            return

        model = controller.get_model(*values)
        controller.update(model)
        self.load_records()
        QMessageBox.information(self, "Success", f"{controller.table_name} updated successfully!")


class UserInterface(QMainWindow):
    def __init__(self, controllers, exit_func):
        super().__init__()
        self.setWindowTitle("Client Interface")
        self.setGeometry(100, 100, 800, 600)

        self.services_controller = controllers["services"]
        self.schedule_controller = controllers["schedule"]
        self.washers_controller = controllers["washers"]
        self.orders_controller = controllers["orders"]
        self.client_controller = controllers["clients"]

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        self.init_account(exit_func)
        self.init_services()
        self.init_washers()
        self.init_schedule()
        self.init_order()

        self.client_id = -1

    def init_account(self, exit_func):
        tab = QWidget()
        self.tabs.addTab(tab, "account")
        layout = QVBoxLayout(tab)

        self.account_manager = UserAccountManager(self.client_controller, self.orders_controller, exit_func)
        layout.addWidget(self.account_manager)

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
        self.services_input.setPlaceholderText("TEXT")
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
        self.account_manager.set_id(client_id)

    def make_order(self):
        values = ["1", str(self.client_id), self.services_input.text(), self.washer_input.text(), "awaiting",
                  self.day_input.text(), self.time_input.text()]
        is_valid, error_text = self.orders_controller.validate_record_types(values)
        if not is_valid:
            QMessageBox.warning(self, "Error", error_text)
            return

        order = self.orders_controller.get_model(None, *values[1:])
        self.orders_controller.add(order)
        schedule_record = self.schedule_controller.get_record_by_pk(self.day_input.text(), self.washer_input.text())
        setattr(schedule_record, "hour_" + self.time_input.text(), 1)
        self.schedule_controller.update(schedule_record)
        self.schedule_manager.load_records()
        self.account_manager.load_records()
        QMessageBox.information(self, "Success", "Order was accepted")

    def closeEvent(self, event):
        for controller in [self.services_controller, self.schedule_controller]:
            controller.repo.close()
        event.accept()
