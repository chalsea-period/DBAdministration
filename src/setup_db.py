import sqlite3
from repositories import *
from models import clients, washers, services, orders, schedule


def recreate_all(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    # Удаление таблиц
    cursor.execute('DROP TABLE IF EXISTS services')
    cursor.execute('DROP TABLE IF EXISTS orders')
    cursor.execute('DROP TABLE IF EXISTS schedule')
    cursor.execute('DROP TABLE IF EXISTS clients')
    cursor.execute('DROP TABLE IF EXISTS washers')
    cursor.execute('DROP TABLE IF EXISTS workshops')
    cursor.execute('DROP TABLE IF EXISTS equipment')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id integer primary key,
            name varchar(50) not null,
            email varchar(50) null,
            phone varchar(15) not null,
            reg_date date not null,
            birth_date date null,
            admin integer not null,
            login varchar(50) not null,
            password_hash varchar(50) not null
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS washers (
            id integer primary key,
            name varchar(50) not null,
            email varchar(50) null,
            phone varchar(15) not null unique,
            work_experience date not null,
            birth_date date null,
            qualification varchar(150) null
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id integer primary key,
            name varchar(50) not null,
            price smallmoney not null,
            execution_time integer not null
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id integer primary key,
            client_id integer not null,
            services varchar(20) not null,
            washer_id integer not null,
            status varchar(15) default 'awaiting',
            order_data date not null,
            order_time varchar(15) not null,
            constraint client_fk foreign key (client_id) references clients(id),
            constraint washer_fk foreign key (washer_id) references washers(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            work_day date not null,
            washer_id integer not null,
            "8am" integer not null,
            "9am" integer not null,
            "10am" integer not null,
            "11am" integer not null,
            "12am" integer not null,
            "1pm" integer not null,
            "2pm" integer not null,
            "3pm" integer not null,
            "4pm" integer not null,
            "5pm" integer not null,
            "6pm" integer not null,
            constraint schedule_pk primary key (work_day, washer_id),
            constraint washer_link foreign key (washer_id) references washers(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workshops (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            address VARCHAR(255) NOT NULL,
            equipment_list TEXT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            status VARCHAR(50) NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def insert_initial_data(db_path):
    client_repo = ClientRepository(db_path)
    washer_repo = WasherRepository(db_path)
    service_repo = ServiceRepository(db_path)
    order_repo = OrderRepository(db_path)
    schedule_repo = ScheduleRepository(db_path)
    workshop_repo = WorkshopRepository(db_path)
    equipment_repo = EquipmentRepository(db_path)

    clients_data = [
        clients(None, 'John Doe', 'john.doe@example.com', '+72345678900', '2023-10-01', '1980-05-15', 0, 'john_doe',
                'password123'),
        clients(None, 'Jane Smith', 'jane.smith@example.com', '+72345678910', '2023-10-02', '1985-08-22', 0,
                'jane_smith', 'password456'),
        clients(None, 'Alice Johnson', 'alice.johnson@example.com', '+72345678920', '2023-10-03', '1990-11-30', 0,
                'alice_johnson', 'password789'),
        clients(None, 'Bob Brown', 'bob.brown@example.com', '+72345678930', '2023-10-04', '1975-03-10', 0, 'bob_brown',
                'password101'),
        clients(None, 'Charlie Davis', 'charlie.davis@example.com', '+72345678940', '2023-10-05', '1982-07-25', 0,
                'charlie_davis', 'password112'),
        clients(None, 'Diana White', 'diana.white@example.com', '+72345678950', '2023-10-06', '1995-09-18', 0,
                'diana_white', 'password131'),
        clients(None, 'Edward Green', 'edward.green@example.com', '+72345678960', '2023-10-07', '1978-12-05', 0,
                'edward_green', 'password141'),
        clients(None, 'Fiona Black', 'fiona.black@example.com', '+72345678970', '2023-10-08', '1987-04-12', 0,
                'fiona_black', 'password151'),
        clients(None, 'George Grey', 'george.grey@example.com', '+72345678980', '2023-10-09', '1992-06-20', 0,
                'george_grey', 'password161'),
        clients(None, 'Helen Yellow', 'helen.yellow@example.com', '+72345678990', '2023-10-10', '1984-10-08', 0,
                'helen_yellow', 'password171')
    ]
    for client in clients_data:
        client_repo.insert(client)

    washers_data = [
        washers(None, 'Alice Johnson', 'alice.johnson@example.com', '+72345678920', '2020-01-01', '1990-11-30', 'Senior Washer'),
        washers(None, 'Bob Brown', 'bob.brown@example.com', '+72345678930', '2018-05-15', '1975-03-10', 'Junior Washer'),
        washers(None, 'Charlie Davis', 'charlie.davis@example.com', '+72345678940', '2019-07-20', '1982-07-25', 'Senior Washer'),
        washers(None, 'Diana White', 'diana.white@example.com', '+72345678950', '2021-03-10', '1995-09-18', 'Junior Washer'),
        washers(None, 'Edward Green', 'edward.green@example.com', '+72345678960', '2017-11-25', '1978-12-05', 'Senior Washer')
    ]
    for washer in washers_data:
        washer_repo.insert(washer)

    services_data = [
        services(None, 'Car Wash', 50.0, 60),
        services(None, 'Interior Cleaning', 30.0, 45),
        services(None, 'Full Detail', 100.0, 120)
    ]
    for service in services_data:
        service_repo.insert(service)

    orders_data = [
        orders(None, 1, 'Car Wash', 1, 'completed', '2023-10-01', '8am'),
        orders(None, 2, 'Interior Cleaning', 2, 'awaiting', '2023-10-01', '9am'),
        orders(None, 3, 'Full Detail', 3, 'completed', '2023-10-01', '10am'),
        orders(None, 4, 'Car Wash', 4, 'awaiting', '2023-10-01', '11am'),
        orders(None, 5, 'Interior Cleaning', 5, 'completed', '2023-10-01', '12am'),
        orders(None, 6, 'Full Detail', 1, 'awaiting', '2023-10-01', '1pm'),
        orders(None, 7, 'Car Wash', 2, 'completed', '2023-10-01', '2pm'),
        orders(None, 8, 'Interior Cleaning', 3, 'awaiting', '2023-10-01', '3pm'),
        orders(None, 9, 'Full Detail', 4, 'completed', '2023-10-01', '4pm'),
        orders(None, 10, 'Car Wash', 5, 'awaiting', '2023-10-01', '5pm')
    ]
    for order in orders_data:
        order_repo.insert(order)

    schedule_data = [
        schedule('2023-10-01', 1),
        schedule('2023-10-02', 2),
        schedule('2023-10-03', 3),
        schedule('2023-10-04', 4),
        schedule('2023-10-05', 5),
        schedule('2023-10-06', 1),
        schedule('2023-10-07', 2),
        schedule('2023-10-08', 3),
        schedule('2023-10-09', 4),
        schedule('2023-10-10', 5)
    ]
    for schedule_item in schedule_data:
        schedule_repo.insert(schedule_item)

    workshop_data = [
        Workshop(None, 'Main Workshop', '123 Main St', 'Equipment1, Equipment2, Equipment3')
    ]
    for workshop in workshop_data:
        workshop_repo.insert(workshop)

    equipment_data = [
        Equipment(None, 'Equipment1', 'Operational'),
        Equipment(None, 'Equipment2', 'Under Maintenance'),
        Equipment(None, 'Equipment3', 'Operational'),
        Equipment(None, 'Equipment4', 'Out of Order'),
        Equipment(None, 'Equipment5', 'Operational')
    ]
    for equipment in equipment_data:
        equipment_repo.insert(equipment)


if __name__ == '__main__':
    recreate_all("../databases/auto_washer.db")
    insert_initial_data("../databases/auto_washer.db")
