import oauth_authorization_keys.splitwise_keys as splitwise_keys
import splitwise
from data_extraction import Receipt
from splitwise.picture import Picture

import json

splitwise_object = splitwise.Splitwise(
    splitwise_keys.CONSUMER_KEY,
    splitwise_keys.CONSUMER_SECRET,
    splitwise_keys.ACCESS_KEY
)

test_receipt = Receipt()
test_receipt.add_item({'Name': 'item1', 'Price': 1000, 'Quantity': 1})
test_receipt.add_item({'Name': 'item2', 'Price': 3500, 'Quantity': 2})
test_receipt.add_item({'Name': 'item3', 'Price': 200, 'Quantity': 4})
test_receipt.add_total_price(4700)

groups = splitwise_object.getGroups()
test_group_id = groups[1].getId()

members = groups[1].getMembers()
members_id = [members[0].getId(), members[1].getId(), members[2].getId(), members[3].getId()]

member0_dict = {
    'user': {
        'first_name': members[0].getFirstName(),
        'last_name': members[0].getLastName(),
        'id': members[0].getId(),
        'email': members[0].getEmail(),
        'registration_status': members[0].getRegistrationStatus(),
        # 'picture': members[0].getPicture()
    },
    'paid_share': None,
    'owed_share': None,
    'net_balance': None
}

test_expense_user = splitwise.user.ExpenseUser(member0_dict)

# members[0].__class__ = splitwise.user.ExpenseUser
# members[1].__class__ = splitwise.user.ExpenseUser
# members[0].setPaidShare('1000')
# members[0].setOwedShare('600')
# members[1].setOwedShare('400')

test_expense = splitwise.expense.Expense()
test_expense.setGroupId(test_group_id)
test_expense.setDescription(test_receipt.items[1].name)
test_expense.setCost(test_receipt.items[1].price)
# test_expense.addUser(members[0])
# test_expense.addUser(members[1])
test_expense.setSplitEqually(should_split=True)

x = splitwise_object.getExpenses(visible=True, group_id=test_group_id)

# a, b = splitwise_object.createExpense(test_expense)
print('cos')
