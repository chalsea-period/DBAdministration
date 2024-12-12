from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton,
                               QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget, QHBoxLayout, QDialog)


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
        layout = QVBoxLayout(self)
        self.init_add(layout)
        self.init_table(layout)
        self.init_change(layout)
        self.load_records()

    def init_add(self, layout):
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

    def init_table(self, layout):
        # Таблица для отображения записей
        self.table = QTableWidget()
        self.table.setColumnCount(self.controller.get_columns_count())
        self.table.setHorizontalHeaderLabels(self.controller.get_attr_names())
        self.table.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
        layout.addWidget(self.table)

    def init_change(self, layout):
        # Кнопки для редактирования и удаления
        button_layout = QHBoxLayout()
        edit_button = QPushButton("Edit Selected")
        edit_button.clicked.connect(self.edit_record)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_record)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

    def add_record(self):
        values = [self.inputs[column].text() for column in self.columns[1:]]
        is_valid, error_text = self.controller.validate_record_types(values)
        if not is_valid:
            QMessageBox.warning(self, "Error", error_text)
            return

        model = self.controller.get_model(None, *values)
        self.controller.add(model)
        self.load_records()
        self.clear_inputs()
        QMessageBox.information(self, "Success", f"{self.controller.table_name} added successfully!")

    def load_records(self):
        records = self.controller.get_all()
        self.update_table(records)

    def update_table(self, records):
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
        kwargs = {column: value} if value else {}
        if not attribute:
            attribute = column
        if not self.controller.validate_filter(value, attribute, direction):
            QMessageBox.warning(self, "Error", "Incorrect input")
            return

        records = self.controller.filter(order_by=attribute, order_direction=direction, **kwargs)
        self.update_table(records)
        QMessageBox.information(self, "Success", f"{self.controller.table_name} filtered successfully!")

    def edit_record(self):
        selected_row = self.table.currentRow()
        selected_col = self.table.currentColumn()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a record to edit.")
            return
        if self.controller.validate_primary_key_cols(selected_col):
            QMessageBox.warning(self, "Error", "You selected a primary key")
            self.load_records()
            return

        values = [self.table.item(selected_row, col).text() for col in range(self.table.columnCount())]
        is_valid, error_text = self.controller.validate_record_types(values)
        if not is_valid:
            QMessageBox.warning(self, "Error", error_text)
            self.load_records()
            return

        model = self.controller.get_model(*values)
        self.controller.update(model)
        self.load_records()
        QMessageBox.information(self, "Success", f"{self.controller.table_name} updated successfully!")

    def delete_record(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a record to delete.")
            return

        record_id = self.table.item(selected_row, 0).text()
        self.controller.delete(record_id)

        admin_interface = self.window()
        if isinstance(admin_interface, AdminInterface):
            admin_interface.load_all_tables()
        QMessageBox.information(self, "Success", f"{self.controller.table_name} deleted successfully!")


class ClientManager(TableManager):
    def __init__(self, controller, parent=None):
        super().__init__(controller, parent)

    def init_add(self, layout):
        return

    def add_record(self):
        return

    def init_table(self, layout):
        # Таблица для отображения записей
        self.table = QTableWidget()
        self.table.setColumnCount(self.controller.get_columns_count()-3)
        self.table.setHorizontalHeaderLabels(self.controller.get_attr_names())
        self.table.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
        layout.addWidget(self.table)

    def update_table(self, records):
        self.table.setRowCount(len(records))
        for row, record in enumerate(records):
            for col, value in enumerate(record.__dict__.values()):
                if col < 6:
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(row, col, item)


class ScheduleManager(TableManager):
    def __init__(self, controller, parent=None):
        super().__init__(controller, parent)

    def init_add(self, layout):
        washer_label = QLabel("washer_id")
        layout.addWidget(washer_label)
        self.washer_input = QLineEdit()
        self.washer_input.setPlaceholderText("INTEGER")
        layout.addWidget(self.washer_input)

        filter_washer_button = QPushButton("Choose washer")
        filter_washer_button.clicked.connect(self.filter_by_washer)
        layout.addWidget(filter_washer_button)

        washer_button = QPushButton(f"Add {self.controller.table_name}")
        washer_button.clicked.connect(self.add_record)
        layout.addWidget(washer_button)

    def add_record(self):
        washer_id = self.washer_input.text()
        is_valid, error_text = self.controller.validate_record_types([washer_id])
        if not is_valid:
            QMessageBox.warning(self, "Error", error_text)
            return

        model = self.controller.get_model(None, washer_id)
        self.controller.add(model)
        self.load_records()
        self.clear_inputs()
        QMessageBox.information(self, "Success", f"{self.controller.table_name} added successfully!")

    def clear_inputs(self):
        self.washer_input.clear()

    def filter_by_washer(self):
        washer_id = self.washer_input.text()
        self.filter_records("washer_id", "=" + washer_id, "", "")


class AccountManager(QWidget):
    def __init__(self, controller, exit_func, parent=None):
        super().__init__(parent)

        self.client_id = -1
        self.controller = controller
        self.columns = controller.get_attr_names()

        layout = QVBoxLayout(self)
        self.init_table(layout)
        self.init_change(layout)
        self.init_exit(layout, exit_func)
        self.load_records()

    def set_id(self, id):
        self.client_id = id
        self.load_records()

    def init_change(self, layout):
        # Кнопка для редактирования
        edit_button = QPushButton("Edit Selected")
        edit_button.clicked.connect(self.edit_record)
        layout.addWidget(edit_button)

    def init_exit(self, layout, exit_func):
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(exit_func)
        layout.addWidget(exit_button)

    def init_table(self, layout):
        self.table = QTableWidget()
        self.table.setColumnCount(self.controller.get_columns_count()-3)
        self.table.setHorizontalHeaderLabels(self.controller.get_attr_names())
        layout.addWidget(self.table)

    def load_records(self):
        if self.client_id == -1:
            return
        record = self.controller.get_by_id(self.client_id)
        self.update_table([record])

    def update_table(self, records):
        self.table.setRowCount(len(records))
        for row, record in enumerate(records):
            for col, value in enumerate(record.__dict__.values()):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row, col, item)

    def edit_record(self):
        selected_row = self.table.currentRow()
        selected_col = self.table.currentColumn()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a record to edit.")
            return
        if self.controller.validate_primary_key_cols(selected_col):
            QMessageBox.warning(self, "Error", "You selected a primary key")
            self.load_records()
            return

        values = [self.table.item(selected_row, col).text() for col in range(self.table.columnCount())]
        is_valid, error_text = self.controller.validate_record_types(values)
        if not is_valid:
            QMessageBox.warning(self, "Error", error_text)
            self.load_records()
            return

        model = self.controller.get_model(*values)
        self.controller.update(model)
        self.load_records()
        QMessageBox.information(self, "Success", f"{self.controller.table_name} updated successfully!")


class AdminInterface(QMainWindow):
    def __init__(self, controllers, exit_func):
        super().__init__()
        self.setWindowTitle("Admin Interface")
        self.setGeometry(100, 100, 800, 600)
        self.controllers = controllers

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.exit_func = exit_func
        self.init_tab("account", controllers["clients"])
        for table_name, controller in self.controllers.items():
            self.init_tab(table_name, controller)

        self.client_id = -1

    def set_id(self, id):
        self.client_id = id
        self.account_manager.set_id(id)

    def init_tab(self, tab_name, controller):
        tab = QWidget()
        self.tabs.addTab(tab, tab_name)
        layout = QVBoxLayout(tab)

        if tab_name == "account":
            self.account_manager = AccountManager(controller, self.exit_func)
            layout.addWidget(self.account_manager)
            return
        if tab_name == "clients":
            client_manager = ClientManager(controller)
            layout.addWidget(client_manager)
            return
        if tab_name == "schedule":
            schedule_manager = ScheduleManager(controller)
            layout.addWidget(schedule_manager)
            return

        table_manager = TableManager(controller)
        layout.addWidget(table_manager)

    def closeEvent(self, event):
        for controller in self.controllers.values():
            controller.repo.close()
        event.accept()

    def load_all_tables(self):
        for index in range(self.tabs.count()):
            tab = self.tabs.widget(index)
            table_manager = tab.findChild(TableManager)
            if table_manager:
                table_manager.load_records()
