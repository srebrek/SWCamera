from Views import MainView as mainView


if __name__ == "__main__":
    mainView.SwCameraApp().run()


# tempRequest = Communicator()
#
# sObj = Splitwise('', '')
# url, secret = sObj.getAuthorizeURL()
# tempRequest.auth(url)
# oauth_token = token
# oauth_verifier = verifier
#
# access_token = sObj.getAccessToken(oauth_token[0], secret, oauth_verifier[0])
# sObj.setAccessToken(access_token)
# x = sObj.getCurrentUser()
#
# name = x.first_name
#
# print(name)
