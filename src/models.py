class clients:
    def __init__(self, id, name, email, phone, reg_date, birth_date):
        self.client_id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.reg_date = reg_date
        self.date_of_birth = birth_date


class washers:
    def __init__(self, id, name, email, phone, work_experience, birth_date, qualification):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.work_experience = work_experience
        self.birth_date= birth_date
        self.qualification = qualification


class services:
    def __init__(self, id, name, price, execution_time):
        self.id =id 
        self.name = name
        self.price = price
        self.execution_time = execution_time


class orders:
    def __init__(self, id, services, washer, status):
        self.id = id
        self.services = services
        self.washer = washer
        self.status = status

class schedule:
    def __init__(self,work_day,washer_id):
        self.work_day=work_day
        self.washer_id = washer_id

