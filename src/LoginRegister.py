from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QFormLayout,
                               QTabWidget, QPushButton, QMessageBox)


class LoginInterface(QMainWindow):
    def __init__(self, auth_controller):
        super().__init__()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Login Interface")
        self.setGeometry(100, 100, 800, 600)
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab1, "Login")
        self.tabs.addTab(self.tab2, "Register")

        self.login_edit_login = QLineEdit()
        self.password_edit_login = QLineEdit()
        self.login_edit_register = QLineEdit()
        self.password_edit_register = QLineEdit()

        self.create_login_fields(self.tab1, "Login", self.login_edit_login, self.password_edit_login)
        self.create_login_fields(self.tab2, "Register", self.login_edit_register, self.password_edit_register)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.central_widget.setLayout(main_layout)

        self.auth_controller = auth_controller

    def set_windows(self, admin, user):
        self.admin_window = admin
        self.user_window = user

    def create_login_fields(self, tab, btn_name, login_edit, password_edit):
        grid_layout = QFormLayout()

        login_label = QLabel("Логин:")
        grid_layout.addWidget(login_label)
        grid_layout.addWidget(login_edit)

        password_label = QLabel("Пароль:")
        password_edit.setEchoMode(QLineEdit.Password)
        grid_layout.addWidget(password_label)
        grid_layout.addWidget(password_edit)

        button = QPushButton(btn_name)
        if btn_name == "Login":
            button.clicked.connect(self.login)
        else:
            button.clicked.connect(self.register)
        grid_layout.addWidget(button)

        tab.setLayout(grid_layout)

    def login(self):
        login = self.login_edit_login.text()
        password = self.password_edit_login.text()
        if self.auth_controller.check_valid_user(login, password):
            if self.auth_controller.check_if_admin(login):
                self.hide()
                self.admin_window.show()
            else:
                self.hide()
                client_id = self.auth_controller.get_client_id(login)
                self.user_window.set_client_id(client_id)
                self.user_window.show()
        else:
            QMessageBox.warning(self, "Error", "User is not valid")

    def register(self):
        login = self.login_edit_register.text()
        password = self.password_edit_register.text()
        if self.auth_controller.check_valid_user(login, password):
            QMessageBox.warning(self, "Error", "User is exists")
            return
        self.auth_controller.register_user(login, password)

    def closeEvent(self, event):
        self.auth_controller.repo.close()
        event.accept()
