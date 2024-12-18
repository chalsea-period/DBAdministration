class Clients:
    def __init__(self, id, name, email, phone, reg_date, birth_date, admin=0, login="", password=""):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.reg_date = reg_date
        self.birth_date = birth_date
        self.admin = admin
        self.login = login
        self.password = password


class Washers:
    def __init__(self, id, name, email, phone, work_experience, birth_date, qualification):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.work_experience = work_experience
        self.birth_date= birth_date
        self.qualification = qualification


class Services:
    def __init__(self, id, name, price, execution_time):
        self.id =id 
        self.name = name
        self.price = price
        self.execution_time = execution_time


class Orders:
    def __init__(self, id, client_id, services, washer_id, status, order_data, order_time):
        self.id = id
        self.client_id = client_id
        self.services = services
        self.washer_id = washer_id
        self.status = status
        self.order_data = order_data
        self.order_time = order_time


class Schedule:
    def __init__(self, work_day, washer_id, hour_8am=0, hour_9am=0, hour_10am=0, hour_11am=0, hour_12am=0, hour_1pm=0,
                 hour_2pm=0, hour_3pm=0, hour_4pm=0, hour_5pm=0, hour_6pm=0):
        self.work_day = work_day
        self.washer_id = washer_id
        self.hour_8am = hour_8am
        self.hour_9am = hour_9am
        self.hour_10am = hour_10am
        self.hour_11am = hour_11am
        self.hour_12am = hour_12am
        self.hour_1pm = hour_1pm
        self.hour_2pm = hour_2pm
        self.hour_3pm = hour_3pm
        self.hour_4pm = hour_4pm
        self.hour_5pm = hour_5pm
        self.hour_6pm = hour_6pm


class Workshop:
    def __init__(self, id, name, address, equipment_list):
        self.id = id
        self.name = name
        self.address = address
        self.equipment_list = equipment_list


class Equipment:
    def __init__(self, id, name, status):
        self.id = id
        self.name = name
        self.status = status
