import json
import Models.Model.oauth_authorization as oauth
import Models.Model.image_to_text as image_to_text
import Models.Model.splitwise_operations as sw_ops
import Models.Model.data_extraction as de

path_to_foto = 'Models/Model/image_to_text_resources/test_foto2.jpg'
access_key = oauth.save_access_key()
# receipt = image_to_text.recognise_foto(path_to_foto)

'''test receipt beginning'''
with open('training_receipt.json', 'r') as file:
    data = json.load(file)
processed_data = de.DataProcessor(data)
receipt = de.Receipt()
for item in processed_data.item_list:
    receipt.add_item(item)
receipt.set_total_price(processed_data.total_price)
'''test receipt ending'''

splitwise_object = sw_ops.make_splitwise_object(access_key)

groups = splitwise_object.getGroups()


def print_groups(groups):
    counter = 0
    for group in groups:
        print(f'{counter}. {group.name}')
        counter += 1


print_groups(groups)
selected_group = groups[int(input('Select group: '))]
members = sw_ops.friend_list_to_expense_user_list(selected_group.getMembers())
receipt.set_receipt_members(members)


def print_members(members):
    counter = 0
    for member in members:
        print(f'{counter}. {member.first_name}')
        counter += 1


# print('Group members:')
# print_members(members)


def set_involved(item):
    print_members(members)
    involved_tuple = tuple(input(f'Select involved in {item.name}: '))
    for involved in involved_tuple:
        item.add_involved(members[int(involved)])
    # item.split_equally()
    item.set_group_members_number(receipt.receipt_members)


for item in receipt.items:
    set_involved(item)

receipt.check_data_correctness()

for item in receipt.items:
    item.split_equally()

print_members(members)
payer = int(input('Set payer: '))
receipt.set_payer(receipt.receipt_members[payer])

expense = sw_ops.make_expense(selected_group.getId(), receipt)

splitwise_object.createExpense(expense)
