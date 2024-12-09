import sys
from PySide6.QtWidgets import QApplication
from repositories import AuthRepository, ClientRepository, WasherRepository, ServiceRepository, OrderRepository,ScheduleRepository
from controllers import AuthController, ClientController, WasherController, ServiceController, OrderController, ScheduleController
from GeniusInterface import AdminInterface
from LoginRegister import LoginInterface
from user_interface import UserInterface


if __name__ == "__main__":
    db_path = "../databases/auto_washer.db"
    client_repo = ClientRepository(db_path)
    washer_repo = WasherRepository(db_path)
    service_repo = ServiceRepository(db_path)
    order_repo = OrderRepository(db_path)
    schedule_repo=ScheduleRepository(db_path)
    auth_repo=AuthRepository(db_path)

    admin_controllers = {
        "clients": ClientController(client_repo),
        "washers": WasherController(washer_repo),
        "services": ServiceController(service_repo),
        "orders": OrderController(order_repo),
        "schedule": ScheduleController(schedule_repo)
    }

    app = QApplication(sys.argv)
    login_window = LoginInterface(AuthController(auth_repo))
    admin_window=AdminInterface(admin_controllers)
    user_window=UserInterface(ServiceController(service_repo),ScheduleController(schedule_repo))
    login_window.set_windows(admin_window,user_window)
    login_window.show()
    sys.exit(app.exec())