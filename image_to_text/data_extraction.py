import json

# file = open('jasiu.txt', 'r')
# file_temp = file.read()
# file.close()
# file_temp = file_temp.replace("\'", "\"")
# data_dict = json.loads(file_temp)


class Receipt:
    def __init__(self):
        self.items = []
        self.total_price = 0

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

    def add_total_price(self, total_price):
        self.total_price = total_price


class ReceiptItem:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f'{self.name}: {self.quantity} * {self.price}'


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

class Data_Processor:
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


# processed_data = Data_Processor(data_dict)
# receipt = Receipt()
# for item in processed_data.item_list:
#     receipt.add_item(item)
# receipt.add_total_price(processed_data.total_price)
# print(receipt)
