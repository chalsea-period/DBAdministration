import sqlite3
import bcrypt
from models import *


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

    def get_primary_keys(self, table_name):
        self.cursor.execute(f"""
            SELECT name
            FROM pragma_table_info("{table_name}")
            WHERE pk > 0
        """)
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

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
        return [Clients(*row) for row in rows]

    def fetch_by_id(self, client_id):
        self.cursor.execute("SELECT * FROM clients WHERE id=?", (client_id,))
        row = self.cursor.fetchone()
        return Clients(*row) if row else None

    def hash_password(self, password):
        if isinstance(password, str):
            password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        return hashed

    def insert(self, client):
        hashed_password = self.hash_password(client.password)
        self.cursor.execute("""
        INSERT INTO clients (name, email, phone, reg_date, birth_date, admin, login, password_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (client.name, client.email, client.phone, client.reg_date, client.birth_date, client.admin, client.login, hashed_password))
        self.commit()

    def update(self, client):
        self.cursor.execute("""
        UPDATE clients
        SET name=?, email=?, phone=?, reg_date=?, birth_date=?, admin=?, login=?, password_hash=?
        WHERE id=?
        """, (client.name, client.email, client.phone, client.reg_date, client.birth_date, client.admin, client.login, client.password, client.id))
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
        return [Washers(*row) for row in rows]
    
    def insert(self, washers):
        self.cursor.execute("""
        INSERT INTO washers (name, email, phone, work_experience, birth_date, qualification)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (washers.name, washers.email, washers.phone, washers.work_experience, washers.birth_date,
              washers.qualification))
        self.commit()

    def update(self, washers):
        self.cursor.execute("""
        UPDATE washers
        SET name=?, email=?, phone=?, work_experience=?, birth_date=?, qualification=?
        WHERE id=?
        """, (washers.name, washers.email, washers.phone, washers.work_experience, washers.birth_date,
              washers.qualification, washers.id))
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
        return [Services(*row) for row in rows]

    def insert(self, service):
        self.cursor.execute("""
        INSERT INTO services (name, price, execution_time)
        VALUES (?, ?, ?)
        """, (service.name, service.price, service.execution_time))
        self.commit()

    def update(self, services):
        self.cursor.execute("""
        UPDATE services
        SET name=?, price=?, execution_time=?
        WHERE id=?
        """, (services.name, services.price, services.execution_time, services.id))
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
        return [Orders(*row) for row in rows]

    def fetch_by_client_id(self, client_id):
        self.cursor.execute("SELECT * FROM orders WHERE client_id=?", (client_id,))
        rows = self.cursor.fetchall()
        return [Orders(*row) for row in rows]

    def fetch_work_and_washer_list(self):
        self.cursor.execute("SELECT work_day, washer_id FROM schedule")
        rows = self.cursor.fetchall()
        return rows

    def fetch_washer_id_list(self):
        self.cursor.execute("SELECT id FROM washers")
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def fetch_client_id_list(self):
        self.cursor.execute("SELECT id FROM clients")
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def insert(self, orders):
        self.cursor.execute("""
        INSERT INTO orders (id, client_id, services, washer_id, status, order_data, order_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (orders.id, orders.client_id, orders.services, orders.washer_id, orders.status, orders.order_data, orders.order_time))
        self.commit()

    def update(self, orders):
        self.cursor.execute("""
        UPDATE orders
        SET client_id=?, services=?, washer_id=?, status=?, order_data=?, order_time=?
        WHERE id=?
        """, (orders.client_id, orders.services, orders.washer_id, orders.status, orders.order_data, orders.order_time, orders.id))
        self.commit()

    def delete(self, id):
        self.cursor.execute("DELETE FROM orders WHERE id=?", (id,))
        self.commit()


class ScheduleRepository(BaseRepository):
    def __init__(self, db_path):
        super().__init__(db_path)

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM schedule")
        rows = self.cursor.fetchall()
        return [Schedule(*row) for row in rows]

    def fetch_by_pk(self, work_day, washer_id):
        self.cursor.execute("SELECT * FROM schedule WHERE work_day=? AND washer_id=?", (work_day, washer_id))
        row = self.cursor.fetchone()
        print(row)
        return Schedule(*row)

    def fetch_last_work_day(self, washer_id):
        self.cursor.execute("SELECT work_day FROM schedule WHERE washer_id=? ORDER BY work_day DESC",
                            (washer_id,))
        row = self.cursor.fetchone()
        return row[0]

    def insert(self, schedule_item):
        self.cursor.execute('''
            INSERT INTO schedule (work_day, washer_id, "8am", "9am", "10am", "11am", "12am", "1pm", "2pm", "3pm", "4pm",
             "5pm", "6pm")
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (schedule_item.work_day, schedule_item.washer_id, schedule_item.hour_8am, schedule_item.hour_9am,
                      schedule_item.hour_10am, schedule_item.hour_11am, schedule_item.hour_12am, schedule_item.hour_1pm,
                      schedule_item.hour_2pm, schedule_item.hour_3pm, schedule_item.hour_4pm, schedule_item.hour_5pm,
                      schedule_item.hour_6pm))
        self.commit()

    def update(self, schedule_item):
        self.cursor.execute("""
        UPDATE schedule
        SET washer_id=?, "8am"=?, "9am"=?, "10am"=?, "11am"=?, "12am"=?, "1pm"=?, "2pm"=?, "3pm"=?, "4pm"=?, "5pm"=?, "6pm"=?
        WHERE work_day=?
        """, (schedule_item.washer_id, schedule_item.hour_8am, schedule_item.hour_9am,
                      schedule_item.hour_10am, schedule_item.hour_11am, schedule_item.hour_12am, schedule_item.hour_1pm,
                      schedule_item.hour_2pm, schedule_item.hour_3pm, schedule_item.hour_4pm, schedule_item.hour_5pm,
                      schedule_item.hour_6pm, schedule_item.work_day))
        self.commit()

    def delete(self, work_day):
        self.cursor.execute("DELETE FROM schedule WHERE work_day=?", (work_day,))
        self.commit()


class WorkshopRepository(BaseRepository):
    def __init__(self, db_path):
        super().__init__(db_path)

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM workshops")
        rows = self.cursor.fetchall()
        return [Workshop(*row) for row in rows]

    def insert(self, workshop):
        self.cursor.execute("""
        INSERT INTO workshops (name, address, equipment_list)
        VALUES (?, ?, ?)
        """, (workshop.name, workshop.address, workshop.equipment_list))
        self.commit()

    def update(self, workshop):
        self.cursor.execute("""
        UPDATE workshops
        SET name=?, address=?, equipment_list=?
        WHERE id=?
        """, (workshop.name, workshop.address, workshop.equipment_list, workshop.id))
        self.commit()

    def delete(self, id):
        self.cursor.execute("DELETE FROM workshops WHERE id=?", (id,))
        self.commit()


class EquipmentRepository(BaseRepository):
    def __init__(self, db_path):
        super().__init__(db_path)

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM equipment")
        rows = self.cursor.fetchall()
        return [Equipment(*row) for row in rows]

    def insert(self, equipment):
        self.cursor.execute("""
        INSERT INTO equipment (name, status)
        VALUES (?, ?)
        """, (equipment.name, equipment.status))
        self.commit()

    def update(self, equipment):
        self.cursor.execute("""
        UPDATE equipment
        SET name=?, status=?
        WHERE id=?
        """, (equipment.name, equipment.status, equipment.id))
        self.commit()

    def delete(self, id):
        self.cursor.execute("DELETE FROM equipment WHERE id=?", (id,))
        self.commit()


class AuthRepository:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('PRAGMA foreign_keys = ON')

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def hash_password(self, password):
        if isinstance(password, str):
            password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        return hashed

    def check_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    def fetch_client_id(self, login):
        self.cursor.execute("""SELECT id FROM clients WHERE login=?""", (login,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def check_valid_user(self, login, password):
        try:
            self.cursor.execute("""SELECT password_hash FROM clients WHERE login=?""", (login,))
            row = self.cursor.fetchone()
            if row:
                hashed_password = row[0]
                return self.check_password(password, hashed_password)
            return False
        except sqlite3.Error as e:
            print(f"Ошибка при проверке пользователя: {e}")
            return False

    def insert(self, client):
        hashed_password = self.hash_password(client.password)
        self.cursor.execute("""
        INSERT INTO clients (name, email, phone, reg_date, birth_date, admin, login, password_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (client.name, client.email, client.phone, client.reg_date, client.birth_date, client.admin, client.login, hashed_password))
        self.commit()
