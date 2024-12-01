from repositories import ClientRepository, TourRepository, BookingRepository, PaymentRepository
from models import Client, Tour, Booking, Payment


class BaseController:
    def __init__(self, db_path, table_name, repo):
        self.db_path = db_path
        self.table_name = table_name
        self.repo = repo

    def get_attr_types(self):
        return self.repo.get_attr_types(self.table_name)


class ClientController(BaseController):
    def __init__(self, db_path):
        super().__init__(db_path, "clients", ClientRepository(db_path))

    def get_all_clients(self):
        return self.repo.get_all()

    def get_client_by_id(self, client_id):
        return self.repo.get_by_id(client_id)

    def add_client(self, client):
        self.repo.add(client)

    def update_client(self, client):
        self.repo.update(client)

    def delete_client(self, client_id):
        self.repo.delete(client_id)


class TourController(BaseController):
    def __init__(self, db_path):
        super().__init__(db_path, "tours", TourRepository(db_path))

    def get_all_tours(self):
        return self.repo.get_all()

    def get_tour_by_id(self, tour_id):
        return self.repo.get_by_id(tour_id)

    def add_tour(self, tour):
        self.repo.add(tour)

    def update_tour(self, tour):
        self.repo.update(tour)

    def delete_tour(self, tour_id):
        self.repo.delete(tour_id)


class BookingController(BaseController):
    def __init__(self, db_path):
        super().__init__(db_path, "bookings", BookingRepository(db_path))

    def get_all_bookings(self):
        return self.repo.get_all()

    def get_booking_by_id(self, booking_id):
        return self.repo.get_by_id(booking_id)

    def add_booking(self, booking):
        self.repo.add(booking)

    def update_booking(self, booking):
        self.repo.update(booking)

    def delete_booking(self, booking_id):
        self.repo.delete(booking_id)


class PaymentController(BaseController):
    def __init__(self, db_path):
        super().__init__(db_path, "payments", PaymentRepository(db_path))

    def get_all_payments(self):
        return self.repo.get_all()

    def get_payment_by_id(self, payment_id):
        return self.repo.get_by_id(payment_id)

    def add_payment(self, payment):
        self.repo.add(payment)

    def update_payment(self, payment):
        self.repo.update(payment)

    def delete_payment(self, payment_id):
        self.repo.delete(payment_id)
