import oauth_authorization_keys.splitwise_keys as splitwise_keys
import splitwise
from data_extraction import Receipt

splitwise_object = splitwise.Splitwise(
    splitwise_keys.CONSUMER_KEY,
    splitwise_keys.CONSUMER_SECRET,
    splitwise_keys.ACCESS_KEY
)


def set_equal(expense):
    involved = expense.getUsers()
    number_of_involved = len(involved)
    cost = int(expense.getCost())
    i = 0
    while i < number_of_involved:
        while cost % number_of_involved != 0:
            involved[i].setOwedShare(cost // number_of_involved + 1)
            i += 1
            cost -= 1

        involved[i].setOwedShare(cost // number_of_involved)
        i += 1


# test_receipt = Receipt()
# test_receipt.add_item({'Name': 'item1', 'Price': 1000, 'Quantity': 1})
# test_receipt.add_item({'Name': 'item2', 'Price': 3500, 'Quantity': 2})
# test_receipt.add_item({'Name': 'item3', 'Price': 200, 'Quantity': 4})
# test_receipt.add_total_price(4700)

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
member1_dict = {
    'user': {
        'first_name': members[1].getFirstName(),
        'last_name': members[1].getLastName(),
        'id': members[1].getId(),
        'email': members[1].getEmail(),
        'registration_status': members[1].getRegistrationStatus(),
        'picture': {
            'small': members[1].getPicture().small,
            'medium': members[1].getPicture().medium,
            'large': members[1].getPicture().large
        }
    },
    'paid_share': None,
    'owed_share': None,
    'net_balance': None
}

test_expense_user0 = splitwise.user.ExpenseUser(member0_dict)
test_expense_user1 = splitwise.user.ExpenseUser(member1_dict)
test_expense_user2 = splitwise.user.ExpenseUser()

test_expense = splitwise.expense.Expense()
test_expense.setGroupId(test_group_id)
test_expense.setDescription('equal_test2_set_after_add')
test_expense.setCost('101')
test_expense.addUser(test_expense_user0)
test_expense.addUser(test_expense_user1)
test_expense.addUser(test_expense_user2)

set_equal(test_expense)

# test_expense_user0.setPaidShare('100')
# test_expense_user0.setOwedShare('50.20')
# test_expense_user1.setOwedShare('49.80')

# test_expense.setSplitEqually(should_split=True)

x = splitwise_object.getExpenses(visible=True, group_id=test_group_id)

# a, b = splitwise_object.createExpense(test_expense)
print('cos')
