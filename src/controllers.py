import re
from datetime import datetime, timedelta
from models import clients, washers, services, orders, schedule


class ValidateRegEx:
    @staticmethod
    def is_integer(text):
        integer_pattern = re.compile(r'^\d+$')
        return bool(integer_pattern.match(text))

    @staticmethod
    def is_date(text):
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        return bool(date_pattern.match(text))

    @staticmethod
    def is_phone_number(text):
        phone_pattern = re.compile(r'^\+7\d{10}$')
        return bool(phone_pattern.match(text))

    @staticmethod
    def is_status(text):
        if text in ('pending', 'confirmed', 'cancelled', 'completed'):
            return True
        return False

    @staticmethod
    def is_invalid(text, type):
        if type == "INTEGER":
            return not ValidateRegEx.is_integer(text)
        elif type == "DATE":
            return not ValidateRegEx.is_date(text)
        elif type == "PHONE":
            return not ValidateRegEx.is_phone_number(text)
        elif type == "STATUS":
            return not ValidateRegEx.is_status(text)
        if text == "":
            return True
        return False

    @staticmethod
    def is_where(text):
        where_pattern = re.compile(r'^[><=].+$')
        return bool(where_pattern.match(text))

    @staticmethod
    def is_attribute(text, attributes):
        lst = [s.strip() for s in text.split(',')]
        return all(attr in attributes for attr in lst), len(lst)

    @staticmethod
    def is_direction(text):
        lst = [s.strip() for s in text.split(',')]
        return all(direct in ["ASC", "DESC", ""] for direct in lst), len(lst)

    @staticmethod
    def validate_filter_data(condition, attribute, attributes, direction):
        check1 = ValidateRegEx.is_where(condition)
        check2, len1 = ValidateRegEx.is_attribute(attribute, attributes)
        check3, len2 = ValidateRegEx.is_direction(direction)
        return check1 and check2 and check3 and len1 == len2


class BaseController:
    def __init__(self, table_name, repo):
        self.table_name = table_name
        self.repo = repo
        self.validation = ValidateRegEx
        self.attr_types = self.repo.get_attr_types(self.table_name)
        self.attr_names = self.repo.get_attr_names(self.table_name)

    def get_attr_names(self):
        return self.attr_names

    def get_attr_types(self):
        return self.attr_types

    def get_columns_count(self):
        return len(self.attr_names)

    def get_all(self):
        return self.repo.fetch_all()

    def add(self, model):
        self.repo.insert(model)

    def update(self, model):
        self.repo.update(model)

    def delete(self, model_id):
        self.repo.delete(model_id)

    def filter(self, order_by=None, order_direction="ASC", **kwargs):
        if not order_by:
            order_by = self.get_attr_names()[0]
        if not kwargs:
            return self.repo.filter_by(self.table_name, self.get_model, order_by, order_direction)
        return self.repo.filter_by(self.table_name, self.get_model, order_by, order_direction, **kwargs)

    def validate_filter(self, condition, attribute, direction):
        return self.validation.validate_filter_data(condition, attribute, self.attr_names, direction)

    def get_model(self, *args):
        raise NotImplementedError("Subclasses must implement this method")

    def validate_record_types(self, record):
        raise NotImplementedError("Subclasses must implement this method")

    def validate_edit_permission(self, selected_col):
        raise NotImplementedError("Subclasses must implement this method")


class ClientController(BaseController):
    def __init__(self, client_repo):
        super().__init__("clients", client_repo)

    def get_model(self, *args):
        return clients(*args)

    def is_invalid_type(self, text, column):
        current_type = self.attr_types[column]
        if self.attr_names[column] == "phone":
            current_type = "PHONE"

        res = self.validation.is_invalid(text, current_type)
        return res

    def validate_record_types(self, record):
        if len(record) != len(self.attr_names):
            record = [None, *record]
        for col in range(1, len(record)):
            if self.is_invalid_type(record[col], col):
                return False, "Invalid type of " + self.attr_names[col]
        return True, "All good"

    def validate_edit_permission(self, selected_col):
        return True


class WasherController(BaseController):
    def __init__(self, washer_repo):
        super().__init__("washers", washer_repo)

    def get_model(self, *args):
        return washers(*args)

    def is_invalid_type(self, text, column):
        current_type = self.attr_types[column]
        if self.attr_names[column] == "phone":
            current_type = "PHONE"
        res = self.validation.is_invalid(text, current_type)
        return res

    def validate_record_types(self, record):
        if len(record) != len(self.attr_names):
            record = [None, *record]
        for col in range(1, len(record)):
            if self.is_invalid_type(record[col], col):
                return False, "Invalid type of " + self.attr_names[col]
        return True, "All good"

    def validate_edit_permission(self, selected_col):
        current_col_name = self.attr_names[selected_col]
        # if current_col_name == "price" or current_col_name == "available_place":
        #     return False
        return True


class ServiceController(BaseController):
    def __init__(self, service_repo):
        super().__init__("services", service_repo)

    def get_model(self, *args):
        return services(*args)

    def is_invalid_type(self, text, column):
        current_type = self.attr_types[column]
        if self.attr_names[column] == "status":
            current_type = "STATUS"
        # elif self.attr_names[column] == "client_id" and not self.validation.is_invalid(text, current_type):
        #     return int(text) not in self.repo.fetch_clients_id_list()
        # elif self.attr_names[column] == "tour_id" and not self.validation.is_invalid(text, current_type):
        #     return int(text) not in self.repo.fetch_tours_id_list()

        res = self.validation.is_invalid(text, current_type)
        return res

    def validate_record_types(self, record):
        if len(record) != len(self.attr_names):
            record = [None, *record]
        for col in range(1, len(record)):
            if self.is_invalid_type(record[col], col):
                return False, "Invalid type of " + self.attr_names[col]
        return True, "All good"

    def validate_edit_permission(self, selected_col):
        current_col_name = self.attr_names[selected_col]
        # if current_col_name == "people_number" or current_col_name == "total_price":
        #     return False
        return True


class OrderController(BaseController):
    def __init__(self, payment_repo):
        super().__init__("orders", payment_repo)

    def get_model(self, *args):
        return orders(*args)

    def is_invalid_type(self, text, column):
        current_type = self.attr_types[column]
        # if self.attr_names[column] == "booking_id" and not self.validation.is_invalid(text, current_type):
        #     return int(text) not in self.repo.fetch_bookings_id_list()

        res = self.validation.is_invalid(text, current_type)
        return res

    def validate_record_types(self, record):
        if len(record) != len(self.attr_names):
            record = [None, *record]
        for col in range(1, len(record)):
            if self.is_invalid_type(record[col], col):
                return False, "Invalid type of " + self.attr_names[col]
        return True, "All good"

    def validate_edit_permission(self, selected_col):
        # current_col_name = self.attr_names[selected_col]
        # if current_col_name == "amount":
        #     return False
        return True


class ScheduleController(BaseController):
    def __init__(self, schedule_repo):
        super().__init__("schedule", schedule_repo)

    def get_model(self, *args):
        return schedule(*args)

    def fetch_last_work_day(self, washer_id):
        return self.repo.fetch_last_work_day(washer_id)

    def add(self, model):
        last_work_day = self.fetch_last_work_day(model.washer_id)
        date = datetime.strptime(last_work_day, "%Y-%m-%d")
        next_day = date + timedelta(days=1)
        next_day_str = datetime.strftime(next_day, "%Y-%m-%d")

        model.work_day = next_day_str
        return self.repo.insert(model)

    def is_invalid_type(self, text, column):
        current_type = self.attr_types[column]
        # if self.attr_names[column] == "booking_id" and not self.validation.is_invalid(text, current_type):
        #     return int(text) not in self.repo.fetch_bookings_id_list()

        res = self.validation.is_invalid(text, current_type)
        return res

    def validate_record_types(self, record):
        if len(record) != len(self.attr_names):
            record = [None, *record]
        for col in range(1, len(record)):
            if self.is_invalid_type(record[col], col):
                return False, "Invalid type of " + self.attr_names[col]
        return True, "All good"

    def validate_edit_permission(self, selected_col):
        # current_col_name = self.attr_names[selected_col]
        # if current_col_name == "amount":
        #     return False
        return True
