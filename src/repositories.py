import sqlite3
from models import clients,washers,services,orders


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
        return [clients(*row) for row in rows]

    def insert(self, client):
        self.cursor.execute("""
        INSERT INTO clients (name, email, phone, reg_date, birth_date)
        VALUES (?, ?, ?, ?, ?)
        """, (client.name, client.email, client.phone, client.reg_date, client.birth_date))
        self.commit()

    def update(self, client):
        self.cursor.execute("""
        UPDATE clients
        SET name=?, email=?, phone=?, reg_date=?, birth_date=?
        WHERE id=?
        """, (client.name, client.email, client.phone, client.reg_Date, client.birth_date, client.id))
        self.commit()

    def delete(self, id):
        self.cursor.execute("DELETE FROM clients WHERE id=?", (id,))
        self.commit()


class WasherRepository(BaseRepository):
    def __init__(self, db_path):
        super().__init__(db_path)

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM washers")
        rows = self.cursor.fetchall()
        return [washers(*row) for row in rows]
    
    def insert(self, washers):
        self.cursor.execute("""
        INSERT INTO tours (name, email, phone, work_experience, birth_date, qualification)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (washers.name, washers.email, washers.phone, washers.work_experience, washers.birth_date, washers.qualification))
        self.commit()

    def update(self, washers):
        self.cursor.execute("""
        UPDATE washers
        SET name=?, email=?, phone=?, work_experience=?, birth_date=?, qualification=?
        WHERE id=?
        """, (washers.name, washers.email, washers.phone, washers.work_experience, washers.birth_date, washers.qualification, washers.id))
        self.commit()

    def delete(self, id):
        self.cursor.execute("DELETE FROM washers WHERE id=?", (id,))
        self.commit()


class ServiceRepository(BaseRepository):
    def __init__(self, db_path):
        super().__init__(db_path)

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM services")
        rows = self.cursor.fetchall()
        return [services(*row) for row in rows]

    def insert(self, services):
        self.cursor.execute("""
        INSERT INTO services (id, name, price, execution_time)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (services.id, services.name, services.price, services.execution_time))
        self.commit()

    def update(self, services):
        self.cursor.execute("""
        UPDATE services
        SET id=? name=?, price=?, execution_time=?,
        WHERE id=?
        """, (services.id, services.name, services.price, services.execution_time))
        self.commit()

    def delete(self, services_id):
        self.cursor.execute("DELETE FROM services WHERE id=?", (id,))
        self.commit()


class OrderRepository(BaseRepository):
    def __init__(self, db_path):
        super().__init__(db_path)

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM orders")
        rows = self.cursor.fetchall()
        return [orders(*row) for row in rows]

    def insert(self, orders):
        self.cursor.execute("""
        INSERT INTO orders (id, services, washer, status)
        VALUES (?, ?, ?, ?)
        """, (orders.id, orders.services, orders.washer, orders.status))
        self.commit()

    def update(self, orders):
        self.cursor.execute("""
        UPDATE orders
        SET id=?, services=?, washer=?, status=?
        WHERE id=?
        """, (orders.id, orders.services, orders.washer, orders.status, orders.id))
        self.commit()

    def delete(self, id):
        self.cursor.execute("DELETE FROM orders WHERE payment_d=?", (id,))
        self.commit()
