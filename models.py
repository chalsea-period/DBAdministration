class Client:
    def __init__(self, client_id, name, email, phone, address, date_of_birth):
        self.client_id = client_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.date_of_birth = date_of_birth


class Tour:
    def __init__(self, tour_id, title, city_of_departure, destination, start_date, end_date, price, available_place):
        self.tour_id = tour_id
        self.title = title
        self.city_of_departure = city_of_departure
        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date
        self.price = price
        self.available_place = available_place


class Booking:
    def __init__(self, booking_id, client_id, tour_id, booking_date, people_number, total_price, status):
        self.booking_id = booking_id
        self.client_id = client_id
        self.tour_id = tour_id
        self.booking_date = booking_date
        self.people_number = people_number
        self.total_price = total_price
        self.status = status


class Payment:
    def __init__(self, payment_id, booking_id, payment_date, amount, payment_method):
        self.payment_id = payment_id
        self.booking_id = booking_id
        self.payment_date = payment_date
        self.amount = amount
        self.payment_method = payment_method
