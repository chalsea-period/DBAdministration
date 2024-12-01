import sqlite3
from repositories import ClientRepository, TourRepository, BookingRepository, PaymentRepository
from models import Client, Tour, Booking, Payment


def recreate_all(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    # Удаление таблиц
    cursor.execute('DROP TABLE IF EXISTS payments')
    cursor.execute('DROP TABLE IF EXISTS bookings')
    cursor.execute('DROP TABLE IF EXISTS tours')
    cursor.execute('DROP TABLE IF EXISTS clients')

    # Создание таблиц
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        client_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT NOT NULL,
        address TEXT NOT NULL,
        date_of_birth DATE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tours (
        tour_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        city_of_departure TEXT,
        destination TEXT NOT NULL,
        start_date DATE,
        end_date DATE NOT NULL,
        price INTEGER NOT NULL,
        available_place INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INTEGER PRIMARY KEY,
        client_id INTEGER NOT NULL,
        tour_id INTEGER NOT NULL,
        booking_date DATE NOT NULL,
        people_number INTEGER NOT NULL,
        total_price INTEGER,
        status TEXT,
        CONSTRAINT fk_client FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE,
        CONSTRAINT fk_tour FOREIGN KEY (tour_id) REFERENCES tours(tour_id) ON DELETE CASCADE,
        CONSTRAINT chk_status CHECK (status IN ('pending', 'confirmed', 'cancelled', 'completed'))
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY,
        booking_id INTEGER NOT NULL,
        payment_date DATE NOT NULL,
        amount INTEGER NOT NULL,
        payment_method TEXT NOT NULL DEFAULT 'credit_card',
        CONSTRAINT fk_booking FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    conn.close()


def insert_initial_data(db_path):
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
        tour_repo.add(tour)

    clients = [
        Client(None, 'John Doe', 'john.doe@example.com', '+1234567890', '123 Main St, New York', '1980-05-15'),
        Client(None, 'Jane Smith', 'jane.smith@example.com', '+1234567891', '456 Elm St, Los Angeles', '1985-08-22'),
        Client(None, 'Alice Johnson', 'alice.johnson@example.com', '+1234567892', '789 Oak St, Chicago', '1990-11-30'),
        Client(None, 'Bob Brown', 'bob.brown@example.com', '+1234567893', '321 Pine St, Houston', '1975-03-10'),
        Client(None, 'Charlie Davis', 'charlie.davis@example.com', '+1234567894', '654 Maple St, Phoenix', '1982-07-25'),
        Client(None, 'Diana White', 'diana.white@example.com', '+1234567895', '987 Cedar St, Philadelphia', '1995-09-18'),
        Client(None, 'Edward Green', 'edward.green@example.com', '+1234567896', '159 Birch St, San Antonio', '1978-12-05'),
        Client(None, 'Fiona Black', 'fiona.black@example.com', '+1234567897', '753 Walnut St, San Diego', '1987-04-12'),
        Client(None, 'George Grey', 'george.grey@example.com', '+1234567898', '357 Chestnut St, Dallas', '1992-06-20'),
        Client(None, 'Helen Yellow', 'helen.yellow@example.com', '+1234567899', '246 Spruce St, San Jose', '1984-10-08')
    ]
    for client in clients:
        client_repo.add(client)

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
        booking_repo.add(booking)

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
        payment_repo.add(payment)


if __name__ == '__main__':
    recreate_all("TravelAgency.db")
    insert_initial_data("TravelAgency.db")
