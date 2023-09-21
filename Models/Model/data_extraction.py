class Receipt:
    def __init__(self):
        self.items = []
        self.total_price = 0
        self.receipt_members = None

    def __str__(self):
        receipt_string = f''
        nl = '\n'
        for item in self.items:
            receipt_string += f'{nl}{item}'
        receipt_string += f'{nl}{nl}Total price: {self.total_price}'
        return receipt_string

    def add_item(self, item_dict):
        item = ReceiptItem(
            item_dict['Name'],
            item_dict['Price'],
            item_dict['Quantity']
        )
        self.items.append(item)

    def set_total_price(self, total_price):
        self.total_price = total_price

    def set_receipt_members(self, receipt_members):
        self.receipt_members = receipt_members

    def set_payer(self, payer):
        payer.setPaidShare(self.total_price)
        """total_price mustn't be 0"""

    def set_detail_message(self):
        message = f''
        for item in self.items:
            message += item.set_detail_message()
        return message

    def check_data_correctness(self):
        item_sum = 0
        for item in self.items:
            item_sum += item.total_price
        while item_sum != self.total_price:
            counter = 0
            for item in self.items:
                print(f'{counter}. {item.name}: {item.quantity} * {item.price}')
                counter += 1
            incorrect_item_number = int(input('Select incorrect item: '))
            incorrect_data = int(input('Select incorrect data (0 - Name, 1 - Quantity, 2 - Price: '))
            if incorrect_data == 0:
                self.items[incorrect_item_number].name = input('Insert correct Name: ')
            elif incorrect_data == 1:
                self.items[incorrect_item_number].quantity = int(input('Insert correct Quantity: '))
                self.items[incorrect_item_number].update_total_price()
            elif incorrect_data == 2:
                self.items[incorrect_item_number].price = int(input('Insert correct Price: '))
                self.items[incorrect_item_number].update_total_price()
            item_sum = 0
            for item in self.items:
                item_sum += item.total_price


class ReceiptItem:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.involved = []
        self.total_price = price * quantity
        self.group_members_number = None

    def __str__(self):
        return f'{self.name}: {self.quantity} * {self.price}'

    def update_total_price(self):
        self.total_price = self.price * self.quantity

    def set_involved(self, involved_list):
        self.involved = involved_list

    def add_involved(self, involved):
        self.involved.append(involved)

    def split_equally(self):
        number_of_involved = len(self.involved)
        cost = self.total_price
        i = 0
        while i < number_of_involved:
            while cost % number_of_involved != 0:
                self.involved[i].setOwedShare(
                    self.involved[i].getOwedShare() + (cost // number_of_involved + 1))
                i += 1
                cost -= 1

            self.involved[i].setOwedShare(
                self.involved[i].getOwedShare() + (cost // number_of_involved))
            i += 1

    def set_group_members_number(self, group_members):
        self.group_members_number = len(group_members)

    def set_detail_message(self):
        nl = '\n'
        message = f'{self.name}: {self.quantity} * {self.price} split between ->{nl}'
        if self.group_members_number == len(self.involved):
            message += f'everyone{nl}'
        else:
            for member in self.involved:
                message += f'{member.getFirstName()}{nl}'
        return message


# Item name
# print(data_dict['analyzeResult']['documentResults'][0]['fields']
#       ['Items']['valueArray'][0]['valueObject']['Name']['valueString'])

# Item price in grosz
# print(data_dict['analyzeResult']['documentResults'][0]['fields']
#       ['Items']['valueArray'][0]['valueObject']['Price']['valueNumber'])

# Item quantity
# print(data_dict['analyzeResult']['documentResults'][0]['fields']
#       ['Items']['valueArray'][0]['valueObject']['Quantity']['valueNumber'])

# Total Price
# print(data_dict['analyzeResult']['documentResults'][0]['fields']['Total']['valueNumber']

class DataProcessor:
    def __init__(self, data_dict):
        self.total_price = data_dict['analyzeResult']['documentResults'][0]['fields']['Total']['valueNumber']
        path = data_dict['analyzeResult']['documentResults'][0]['fields']['Items']['valueArray']
        self.item_list = []
        for item in path:
            try:
                self.item_list.append({
                    'Name': item['valueObject']['Name']['valueString'],
                    'Price': item['valueObject']['Price']['valueNumber'],
                    'Quantity': item['valueObject']['Quantity']['valueNumber']
                })
            except KeyError:
                pass
