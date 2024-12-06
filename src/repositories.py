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

    def __get_condition(self, **kwargs):
        query = " WHERE "
        conditions = []
        params = []
        for key, value in kwargs.items():
            sign = value[0]
            conditions.append(f"{key}{sign}?")
            params.append(value[1:])
        query += " AND ".join(conditions)
        return query, params

    def __get_order_by_part_query(self, order_by, order_direction):
        query = " ORDER BY "
        order = [attr.strip() for attr in order_by.split(',')]
        direction = [forward.strip() for forward in order_direction.split(',')]
        for i in range(len(order)):
            query += order[i] + " " + direction[i]
            if i != len(order) - 1:
                query += ", "
        return query

    def filter_by(self, table_name, model_class, order_by, order_direction, **kwargs):
        query = f"SELECT * FROM {table_name}"
        params = None
        if kwargs:
            cond_query, params = self.__get_condition(**kwargs)
            query += cond_query

        if order_by:
            query += self.__get_order_by_part_query(order_by, order_direction)

        print(query)
        self.cursor.execute(query, params if params else ())
        rows = self.cursor.fetchall()
        return [model_class(*row) for row in rows]


class ClientRepository(BaseRepository):
    def __init__(self, db_path):
        super().__init__(db_path)

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM clients")
        rows = self.cursor.fetchall()
        return [Client(*row) for row in rows]

    def fetch_by_id(self, client_id):
        self.cursor.execute("SELECT * FROM clients WHERE client_id=?", (client_id,))
        row = self.cursor.fetchone()
        return Client(*row) if row else None

    def insert(self, client):
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

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM tours")
        rows = self.cursor.fetchall()
        return [Tour(*row) for row in rows]

    def fetch_by_id(self, tour_id):
        self.cursor.execute("SELECT * FROM tours WHERE tour_id=?", (tour_id,))
        row = self.cursor.fetchone()
        return Tour(*row) if row else None

    def insert(self, tour):
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

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM bookings")
        rows = self.cursor.fetchall()
        return [Booking(*row) for row in rows]

    def fetch_by_id(self, booking_id):
        self.cursor.execute("SELECT * FROM bookings WHERE booking_id=?", (booking_id,))
        row = self.cursor.fetchone()
        return Booking(*row) if row else None

    def fetch_price_by_tour_id(self, tour_id):
        self.cursor.execute("SELECT * FROM tours WHERE tour_id=?", (tour_id,))
        row = self.cursor.fetchone()
        column_names = [description[0] for description in self.cursor.description]
        row_dict = dict(zip(column_names, row))
        return row_dict.get('price')

    def fetch_available_places_by_tour_id(self, tour_id):
        self.cursor.execute("SELECT * FROM tours WHERE tour_id=?", (tour_id,))
        row = self.cursor.fetchone()
        column_names = [description[0] for description in self.cursor.description]
        row_dict = dict(zip(column_names, row))
        return row_dict.get('available_place')

    def fetch_occupied_places_by_tour_id(self, tour_id):
        self.cursor.execute("""
        SELECT tour_id, SUM(people_number) AS occupied_count FROM bookings
        WHERE status = 'confirmed' OR status = 'pending'
        GROUP BY tour_id
        HAVING tour_id=?
        """, (tour_id,))
        row = self.cursor.fetchone()
        return row[1]

    def fetch_clients_id_list(self):
        self.cursor.execute("SELECT client_id FROM clients")
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def fetch_tours_id_list(self):
        self.cursor.execute("SELECT tour_id FROM tours")
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def insert(self, booking):
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

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM payments")
        rows = self.cursor.fetchall()
        return [Payment(*row) for row in rows]

    def fetch_by_id(self, payment_id):
        self.cursor.execute("SELECT * FROM payments WHERE payment_id=?", (payment_id,))
        row = self.cursor.fetchone()
        return Payment(*row) if row else None

    def fetch_bookings_id_list(self):
        self.cursor.execute("SELECT booking_id FROM bookings")
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def fetch_total_price_by_booking_id(self, booking_id):
        self.cursor.execute("SELECT total_price FROM bookings WHERE booking_id=?", (booking_id,))
        rows = self.cursor.fetchall()
        return rows[0][0]

    def insert(self, payment):
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
