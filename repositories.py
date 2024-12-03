import sqlite3
from models import Client, Tour, Booking, Payment


class BaseRepository:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('PRAGMA foreign_keys = ON')

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def get_attr_names(self, table_name):
        self.cursor.execute(f'PRAGMA table_info("{table_name}")')
        rows = self.cursor.fetchall()
        types_list = []
        for row in rows:
            types_list.append(row[1])
        return types_list

    def get_attr_types(self, table_name):
        self.cursor.execute(f'PRAGMA table_info("{table_name}")')
        rows = self.cursor.fetchall()
        types_list = []
        for row in rows:
            types_list.append(row[2])
        return types_list

    def filter_by(self, table_name, model_class, order_by=None, order_direction='ASC', **kwargs):
        query = f"SELECT * FROM {table_name} WHERE "
        conditions = []
        params = []
        for key, value in kwargs.items():
            conditions.append(f"{key}=?")
            params.append(value)
        query += " AND ".join(conditions)

        if order_by:
            query += f" ORDER BY {order_by} {order_direction}"

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        return [model_class(*row) for row in rows]


class ClientRepository(BaseRepository):
    def __init__(self, db_path):
        super().__init__(db_path)

    def get_all(self):
        self.cursor.execute("SELECT * FROM clients")
        rows = self.cursor.fetchall()
        return [Client(*row) for row in rows]

    def get_by_id(self, client_id):
        self.cursor.execute("SELECT * FROM clients WHERE client_id=?", (client_id,))
        row = self.cursor.fetchone()
        return Client(*row) if row else None

    def add(self, client):
        self.cursor.execute("""
        INSERT INTO clients (name, email, phone, address, date_of_birth)
        VALUES (?, ?, ?, ?, ?)
        """, (client.name, client.email, client.phone, client.address, client.date_of_birth))
        self.commit()

    def update(self, client):
        self.cursor.execute("""
        UPDATE clients
        SET name=?, email=?, phone=?, address=?, date_of_birth=?
        WHERE client_id=?
        """, (client.name, client.email, client.phone, client.address, client.date_of_birth, client.client_id))
        self.commit()

    def delete(self, client_id):
        self.cursor.execute("DELETE FROM clients WHERE client_id=?", (client_id,))
        self.commit()


class TourRepository(BaseRepository):
    def __init__(self, db_path):
        super().__init__(db_path)

    def get_all(self):
        self.cursor.execute("SELECT * FROM tours")
        rows = self.cursor.fetchall()
        return [Tour(*row) for row in rows]

    def get_by_id(self, tour_id):
        self.cursor.execute("SELECT * FROM tours WHERE tour_id=?", (tour_id,))
        row = self.cursor.fetchone()
        return Tour(*row) if row else None

    def add(self, tour):
        self.cursor.execute("""
        INSERT INTO tours (title, city_of_departure, destination, start_date, end_date, price, available_place)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (tour.title, tour.city_of_departure, tour.destination, tour.start_date, tour.end_date, tour.price, tour.available_place))
        self.commit()

    def update(self, tour):
        self.cursor.execute("""
        UPDATE tours
        SET title=?, city_of_departure=?, destination=?, start_date=?, end_date=?, price=?, available_place=?
        WHERE tour_id=?
        """, (tour.title, tour.city_of_departure, tour.destination, tour.start_date, tour.end_date, tour.price, tour.available_place, tour.tour_id))
        self.commit()

    def delete(self, tour_id):
        self.cursor.execute("DELETE FROM tours WHERE tour_id=?", (tour_id,))
        self.commit()


class BookingRepository(BaseRepository):
    def __init__(self, db_path):
        super().__init__(db_path)

    def get_all(self):
        self.cursor.execute("SELECT * FROM bookings")
        rows = self.cursor.fetchall()
        return [Booking(*row) for row in rows]

    def get_by_id(self, booking_id):
        self.cursor.execute("SELECT * FROM bookings WHERE booking_id=?", (booking_id,))
        row = self.cursor.fetchone()
        return Booking(*row) if row else None

    def get_price_by_tour_id(self, tour_id):
        self.cursor.execute("SELECT * FROM tours WHERE tour_id=?", (tour_id,))
        row = self.cursor.fetchone()
        column_names = [description[0] for description in self.cursor.description]
        row_dict = dict(zip(column_names, row))
        return row_dict.get('price')

    def get_clients_id_list(self):
        self.cursor.execute("SELECT client_id FROM clients")
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def get_tours_id_list(self):
        self.cursor.execute("SELECT tour_id FROM tours")
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def add(self, booking):
        self.cursor.execute("""
        INSERT INTO bookings (client_id, tour_id, booking_date, people_number, total_price, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (booking.client_id, booking.tour_id, booking.booking_date, booking.people_number, booking.total_price, booking.status))
        self.commit()

    def update(self, booking):
        self.cursor.execute("""
        UPDATE bookings
        SET client_id=?, tour_id=?, booking_date=?, people_number=?, total_price=?, status=?
        WHERE booking_id=?
        """, (booking.client_id, booking.tour_id, booking.booking_date, booking.people_number, booking.total_price, booking.status, booking.booking_id))
        self.commit()

    def delete(self, booking_id):
        self.cursor.execute("DELETE FROM bookings WHERE booking_id=?", (booking_id,))
        self.commit()


class PaymentRepository(BaseRepository):
    def __init__(self, db_path):
        super().__init__(db_path)

    def get_all(self):
        self.cursor.execute("SELECT * FROM payments")
        rows = self.cursor.fetchall()
        return [Payment(*row) for row in rows]

    def get_by_id(self, payment_id):
        self.cursor.execute("SELECT * FROM payments WHERE payment_id=?", (payment_id,))
        row = self.cursor.fetchone()
        return Payment(*row) if row else None

    def get_bookings_id_list(self):
        self.cursor.execute("SELECT booking_id FROM bookings")
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def add(self, payment):
        self.cursor.execute("""
        INSERT INTO payments (booking_id, payment_date, amount, payment_method)
        VALUES (?, ?, ?, ?)
        """, (payment.booking_id, payment.payment_date, payment.amount, payment.payment_method))
        self.commit()

    def update(self, payment):
        self.cursor.execute("""
        UPDATE payments
        SET booking_id=?, payment_date=?, amount=?, payment_method=?
        WHERE payment_id=?
        """, (payment.booking_id, payment.payment_date, payment.amount, payment.payment_method, payment.payment_id))
        self.commit()

    def delete(self, payment_id):
        self.cursor.execute("DELETE FROM payments WHERE payment_id=?", (payment_id,))
        self.commit()
