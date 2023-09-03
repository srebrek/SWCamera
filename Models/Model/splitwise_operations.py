import oauth_authorization_keys.splitwise_keys as splitwise_keys
import splitwise
import data_extraction as de


def friend_list_to_expense_user_list(friend_list):
    expense_user_list = []
    for friend in friend_list:
        expense_user = splitwise.user.ExpenseUser()
        expense_user.paid_share = 0
        expense_user.owed_share = 0
        expense_user.setId(friend.getId())
        expense_user.setFirstName(friend.getFirstName())
        expense_user.setLastName(friend.getLastName())
        expense_user.picture = friend.getPicture()
        expense_user_list.append(expense_user)
    return expense_user_list


splitwise_object = splitwise.Splitwise(
    splitwise_keys.CONSUMER_KEY,
    splitwise_keys.CONSUMER_SECRET,
    splitwise_keys.ACCESS_KEY
)

test_receipt = de.Receipt()
test_receipt.add_item({'Name': 'item0', 'Price': 1000, 'Quantity': 1})
test_receipt.add_item({'Name': 'item1', 'Price': 3500, 'Quantity': 2})
test_receipt.add_item({'Name': 'item2', 'Price': 200, 'Quantity': 4})
test_receipt.set_total_price(8800)

groups = splitwise_object.getGroups()
test_group_id = groups[1].getId()

members = groups[1].getMembers()
members_id = [members[0].getId(), members[1].getId(), members[2].getId(), members[3].getId()]

expense_users = friend_list_to_expense_user_list(members)
test_receipt.set_receipt_members(expense_users)

test_receipt.items[0].add_involved(expense_users[0])
test_receipt.items[0].add_involved(expense_users[1])
test_receipt.items[0].split_equally()
test_receipt.items[0].set_group_members_number(test_receipt.receipt_members)

test_receipt.items[1].add_involved(expense_users[0])
test_receipt.items[1].add_involved(expense_users[1])
test_receipt.items[1].add_involved(expense_users[2])
test_receipt.items[1].add_involved(expense_users[3])
test_receipt.items[1].split_equally()
test_receipt.items[1].set_group_members_number(test_receipt.receipt_members)

test_receipt.items[2].add_involved(expense_users[3])
test_receipt.items[2].add_involved(expense_users[1])
test_receipt.items[2].split_equally()
test_receipt.items[2].set_group_members_number(test_receipt.receipt_members)

test_receipt.set_payer(test_receipt.receipt_members[0])

test_expense = splitwise.expense.Expense()
test_expense.setGroupId(test_group_id)
test_expense.setDescription('testing_extended_classes')
test_expense.setCost(test_receipt.total_price)
test_expense.setUsers(test_receipt.receipt_members)
message = test_receipt.set_detail_message()
test_expense.setDetails(test_receipt.set_detail_message())

member0_dict = {
    'user': {
        'first_name': members[0].getFirstName(),
        'last_name': members[0].getLastName(),
        'id': members[0].getId(),
        'email': members[0].getEmail(),
        'registration_status': members[0].getRegistrationStatus(),
        'picture': {
            'small': members[0].getPicture().small,
            'medium': members[0].getPicture().medium,
            'large': members[0].getPicture().large
        }
    },
    'paid_share': None,
    'owed_share': None,
    'net_balance': None
}
# member1_dict = {
#     'user': {
#         'first_name': members[1].getFirstName(),
#         'last_name': members[1].getLastName(),
#         'id': members[1].getId(),
#         'email': members[1].getEmail(),
#         'registration_status': members[1].getRegistrationStatus(),
#         'picture': {
#             'small': members[1].getPicture().small,
#             'medium': members[1].getPicture().medium,
#             'large': members[1].getPicture().large
#         }
#     },
#     'paid_share': None,
#     'owed_share': None,
#     'net_balance': None
# }
#
# test_expense_user0 = splitwise.user.ExpenseUser(member0_dict)
# test_expense_user1 = splitwise.user.ExpenseUser(member1_dict)
# test_expense_user2 = splitwise.user.ExpenseUser()

# test_expense = splitwise.expense.Expense()
# test_expense.setGroupId(test_group_id)
# test_expense.setDescription('equal_test2_set_after_add')
# test_expense.setCost('101')
# test_expense.addUser(test_expense_user0)
# test_expense.addUser(test_expense_user1)
# test_expense.addUser(test_expense_user2)

# set_equal(test_expense)

# test_expense_user0.setPaidShare('100')
# test_expense_user0.setOwedShare('50.20')
# test_expense_user1.setOwedShare('49.80')

# test_expense.setSplitEqually(should_split=True)

x = splitwise_object.getExpenses(visible=True, group_id=test_group_id)

a, b = splitwise_object.createExpense(test_expense)
print('cos')
