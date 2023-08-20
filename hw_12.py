from collections import UserDict
from datetime import datetime
import pickle

FILE_DATA = "adress_book.bin"
class Birthday:
    def __init__(self, day_birth: str):
        self.__value = None
        self.value = day_birth

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, day_birth):
        """
        :param day_birth: day.month (23.07)
        :return:
        """
        try:
            day, month = (map(int, day_birth.split(".")))
        except ValueError:
            return f"Birthday {day_birth} not in right format. Right format 'Day.Month' (31.12)"
        if 1 <= day <= 31 and 1 <= month <= 12:
            self.__value = (day, month)

        else:
            return f"Birthday {day_birth} not in right format. Right format 'Day.Month' (31.12)"

    def __repr__(self):
        return str(self.__value)

class Phone:
    def __init__(self, phone_number: str):
        self.__value = None
        self.value = phone_number

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone_number):
        if phone_number.isdigit() and len(phone_number) == 10:
            self.__value = phone_number
        else:
            return f"Phone number {phone_number} not in right format. Right format 0501234567"

    def __repr__(self):
        return self.__value


class Name:
    def __init__(self, name: str):
        self.value = name

    def __repr__(self):
        return self.value


class Record:
    def __init__(self, name: Name, phone: Phone = None, birth_day: Birthday = None):
        self.phones = [phone]
        self.name = name
        self.birthday = birth_day

    def __repr__(self):
        return f'Record({self.name}, {[ph.value for ph in self.phones]}, {self.birthday})'

    def add_phone(self, phone_to_add: Phone):
        for exist_phone in self.phones:
            if phone_to_add.value == exist_phone.value:
                return f"You try to add phone {phone_to_add} that already exists"
        self.phones.append(phone_to_add)

    def del_phone(self, phone: Phone):
        try:
            self.phones.remove(phone)
        except ValueError:
            return f"You try to delete number {phone} that is absent in the list!"

    def edit_phone(self, current_phone: Phone, new_phone: Phone):
        try:
            index = self.phones.index(current_phone)
            self.phones[index] = new_phone
        except ValueError:
            return f"You try to edit number {current_phone} that is absent in the list!"

    @property
    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today()
            next_birth_day = datetime(year=today.year + 1, month=self.birthday.value[1], day=self.birthday.value[0])
            delta = next_birth_day - today
            return f"{delta.days} days left to the next birth day."


class AddressBook(UserDict):

    def __init__(self, book=None):
        if book is None:
            super(AddressBook, self).__init__()
        else:
            super(AddressBook, self).__init__(book)

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record
        with open(FILE_DATA, "wb") as fh:
            pickle.dump(self.data, fh)

    def iterator(self, number_records):
        return AddressBookIterator(number_records, self)


class AddressBookIterator:

    def __init__(self, number_records: int, address_book: AddressBook):
        self.number_records = number_records
        self.address_book = address_book
        self._start = 0
        self._stop = number_records
        self._keys = tuple(address_book.data.keys())


    def __next__(self):
        res = []
        for key in self._keys[self._start:self._stop]:
            res.append((key, self.address_book.data[key]))

        if not res:
            raise StopIteration
        self._start = self._stop
        self._stop += self.number_records
        return res


def main(ab: AddressBook):
    # name = Name('Bill')
    # phone = Phone('1234567890')
    # day = Birthday("19.08")
    # rec1 = Record(name, phone, day)
    #
    # name2 = Name('Ted')
    # phone2 = Phone('4444444444')
    # rec2 = Record(name2, phone2)
    #
    # name3 = Name('Bob')
    # phone3 = Phone('55555555')
    # rec3 = Record(name3, phone3)
    #
    # name4 = Name('Clod')
    # phone4 = Phone('6666666')
    # rec4 = Record(name4, phone4)
    # adress_book.add_record(rec1)
    # adress_book.add_record(rec2)
    # adress_book.add_record(rec3)
    # adress_book.add_record(rec4)
    # print(rec1.days_to_birthday)
    print(ab)
    iter = ab.iterator(2)
    while True:
        try:
            print(next(iter))
        except StopIteration:
            break

    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '1234567890'

def add_records(ab: AddressBook):
    name = Name('Gosha')
    phone = Phone('0503615749')
    day = Birthday("24.07")
    rec1 = Record(name, phone, day)
    ab.add_record(rec1)

if __name__ == '__main__':
    try:
        with open(FILE_DATA, "rb") as fh:
            load_dict = pickle.load(fh)
            ab = AddressBook(load_dict)
    except FileNotFoundError:
        ab = AddressBook()

    main(ab)
    # add_records(ab)





