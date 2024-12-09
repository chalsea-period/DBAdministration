from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit,QFormLayout,
                               QTabWidget,QPushButton)
from PySide6.QtCore import Qt


class LoginInterface(QMainWindow):
    def __init__(self):
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

        self.create_login_fields(self.tab1,"Login")
        self.create_login_fields(self.tab2,"Register")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.central_widget.setLayout(main_layout)

    def create_login_fields(self, tab,btn_name):
        grid_layout = QFormLayout()

        login_label = QLabel("Логин:")
        

        self.login_edit = QLineEdit()
        self.login_edit.setFixedWidth(200)
        

        grid_layout.addWidget(login_label)
        grid_layout.addWidget(self.login_edit)

        password_label = QLabel("Пароль:")
        

        self.password_edit = QLineEdit()
        self.password_edit.setFixedWidth(200)
        
        self.password_edit.setEchoMode(QLineEdit.Password)
       
        grid_layout.addWidget(password_label)
        grid_layout.addWidget(self.password_edit)

        button = QPushButton(btn_name)
        if btn_name=="Login":
            button.clicked.connect(self.login)
        else:
            button.clicked.connect(self.register)
        grid_layout.addWidget(button)



        tab.setLayout(grid_layout)

    def login(self):
        pass
    
    def register(self):
        pass
