import oauth_authorization_keys.splitwise_keys as splitwise_keys
from splitwise import Splitwise

splitwise_object = Splitwise(
    splitwise_keys.CONSUMER_KEY,
    splitwise_keys.CONSUMER_SECRET,
    splitwise_keys.ACCESS_KEY
)
user = splitwise_object.getCurrentUser()
print(user.getFirstName())