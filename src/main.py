import sys
from PySide6.QtWidgets import QApplication
from repositories import ClientRepository, TourRepository, BookingRepository, PaymentRepository
from controllers import ClientController, TourController, BookingController, PaymentController
from GeniusInterface import AdminInterface


if __name__ == "__main__":
    db_path = "../databases/auto_washer.db"
    client_repo = ClientRepository(db_path)
    tour_repo = TourRepository(db_path)
    booking_repo = BookingRepository(db_path)
    payment_repo = PaymentRepository(db_path)

    my_controllers = {
        "clients": ClientController(client_repo),
        "tours": TourController(tour_repo),
        "bookings": BookingController(booking_repo),
        "payments": PaymentController(payment_repo)
    }

    app = QApplication(sys.argv)
    window = AdminInterface(my_controllers)
    window.show()
    sys.exit(app.exec())