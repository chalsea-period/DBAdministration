import sqlite3
from repositories import ClientRepository, WasherRepository, ServiceRepository, OrderRepository,ScheduleRepository
from models import clients, washers, services, orders, schedule


def recreate_all(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    # Удаление таблиц
    cursor.execute('DROP TABLE IF EXISTS clients')
    cursor.execute('DROP TABLE IF EXISTS washers')
    cursor.execute('DROP TABLE IF EXISTS services')
    cursor.execute('DROP TABLE IF EXISTS orders')

    # Создание таблиц
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id int IDENTITY not null primary key,
            name varchar(50) not null,
            email varchar(50) null,
            phone varchar(15) not null unique,
            reg_date date not null,
            birth_date date null
    )
    ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS washers (
                id int IDENTITY not null primary key,
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
                id int IDENTITY not null primary key,
                name varchar(50) not null,
                price smallmoney not null,
                execution_time int not null
        )
        ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id int IDENTITY not null primary key,
                services varchar(200) not null,
                washer int not null,
                status varchar(15) default 'awaiting',
                constraint washer_link foreign key (washer) references washers(id)
                
        )
        ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedule (
                work_day date not null primary key,
                washer_id int null,
                constraint washer_link foreign key (washer_id) references washers(id)
        )
        ''')




    conn.commit()
    conn.close()


'''def insert_initial_data(db_path):
    client_repo = ClientRepository(db_path)
    tour_repo = TourRepository(db_path)
    booking_repo = BookingRepository(db_path)
    payment_repo = PaymentRepository(db_path)

    tours = [
        Tour(None, 'Tropical Paradise', 'New York', 'Hawaii', '2023-12-20', '2023-12-30', 2500, 20),
        Tour(None, 'European Adventure', 'Los Angeles', 'Paris', '2024-03-15', '2024-03-25', 3000, 15),
        Tour(None, 'Asian Expedition', 'Chicago', 'Tokyo', '2024-06-01', '2024-06-10', 3500, 10)
    ]
    for tour in tours:
        tour_repo.insert(tour)

    clients = [
        Client(None, 'John Doe', 'john.doe@example.com', '+72345678900', '123 Main St, New York', '1980-05-15'),
        Client(None, 'Jane Smith', 'jane.smith@example.com', '+72345678910', '456 Elm St, Los Angeles', '1985-08-22'),
        Client(None, 'Alice Johnson', 'alice.johnson@example.com', '+72345678920', '789 Oak St, Chicago', '1990-11-30'),
        Client(None, 'Bob Brown', 'bob.brown@example.com', '+72345678930', '321 Pine St, Houston', '1975-03-10'),
        Client(None, 'Charlie Davis', 'charlie.davis@example.com', '+72345678940', '654 Maple St, Phoenix', '1982-07-25'),
        Client(None, 'Diana White', 'diana.white@example.com', '+72345678950', '987 Cedar St, Philadelphia', '1995-09-18'),
        Client(None, 'Edward Green', 'edward.green@example.com', '+72345678960', '159 Birch St, San Antonio', '1978-12-05'),
        Client(None, 'Fiona Black', 'fiona.black@example.com', '+72345678970', '753 Walnut St, San Diego', '1987-04-12'),
        Client(None, 'George Grey', 'george.grey@example.com', '+72345678980', '357 Chestnut St, Dallas', '1992-06-20'),
        Client(None, 'Helen Yellow', 'helen.yellow@example.com', '+72345678990', '246 Spruce St, San Jose', '1984-10-08')
    ]
    for client in clients:
        client_repo.insert(client)

    bookings = [
        Booking(None, 1, 1, '2023-11-01', 2, 5000, 'confirmed'),
        Booking(None, 2, 2, '2023-11-02', 1, 3000, 'pending'),
        Booking(None, 3, 3, '2023-11-03', 3, 10500, 'confirmed'),
        Booking(None, 4, 1, '2023-11-04', 1, 2500, 'cancelled'),
        Booking(None, 5, 2, '2023-11-05', 2, 6000, 'confirmed'),
        Booking(None, 6, 3, '2023-11-06', 1, 3500, 'completed'),
        Booking(None, 7, 1, '2023-11-07', 2, 5000, 'confirmed'),
        Booking(None, 8, 2, '2023-11-08', 1, 3000, 'pending'),
        Booking(None, 9, 3, '2023-11-09', 2, 7000, 'confirmed'),
        Booking(None, 10, 1, '2023-11-10', 1, 2500, 'cancelled'),
        Booking(None, 1, 2, '2023-11-11', 1, 3000, 'confirmed'),
        Booking(None, 2, 3, '2023-11-12', 1, 3500, 'pending')
    ]
    for booking in bookings:
        booking_repo.insert(booking)

    payments = [
        Payment(None, 1, '2023-11-02', 5000, 'credit_card'),
        Payment(None, 3, '2023-11-04', 10500, 'credit_card'),
        Payment(None, 5, '2023-11-06', 6000, 'credit_card'),
        Payment(None, 6, '2023-11-07', 3500, 'credit_card'),
        Payment(None, 7, '2023-11-08', 5000, 'credit_card'),
        Payment(None, 9, '2023-11-10', 7000, 'credit_card'),
        Payment(None, 11, '2023-11-12', 3000, 'credit_card'),
        Payment(None, 12, '2023-11-13', 3500, 'credit_card')
    ]
    for payment in payments:
        payment_repo.insert(payment)


if __name__ == '__main__':
    recreate_all("../databases/TravelAgency.db")
    insert_initial_data("../databases/TravelAgency.db")'''

if __name__ == '__main__':
    recreate_all("../databases/auto_washer.db")