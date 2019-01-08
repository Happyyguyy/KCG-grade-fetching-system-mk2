import pyrebase
import requests


class HTTPError (requests.exceptions.HTTPError):
    def __init__(self, message, e):
        self.e = e
        self.message = message

        if "EMAIL_NOT_FOUND" in str(self.e):
            self.error = "EMAIL_NOT_FOUND"
        elif "EMAIL_EXISTS" in str(self.e):
            self.error = "EMAIL_EXISTS"

    def __str__(self):
        return self.error, self.message





config = {
    "apiKey": "AIzaSyBCxSv9K2t35EqFEnH8ZpYVn4DT43WhZSY",
    "authDomain": "kcg-legislator-report-card.firebaseapp.com",
    "databaseURL": "https://kcg-legislator-report-card.firebaseio.com",
    "projectId": "kcg-legislator-report-card",
    "storageBucket": "kcg-legislator-report-card.appspot.com",
    "messagingSenderId": "794508163147"
    # "serviceAccount": "kcg-legislator-report-card-firebase-adminsdk-hnddn-9ad383d059.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# print(db.get().val())


# Get a reference to the auth service
auth = firebase.auth()

# Log the user in
email = input("Email: ")
password = input("Password: ")


def signin_create(email, password, first="", last="", key=""):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
    except requests.exceptions.HTTPError as e:
        if "EMAIL_NOT_FOUND" in str(e):
            print("Email not registered")
            print("Creating New Account")
            # email = input("Email: ").strip()
            # password = input("Password (must be 6+ characters): ")
            try:
                user = auth.create_user_with_email_and_password(
                    email, password)
            except requests.exceptions.HTTPError as ee:
                if "EMAIL_EXISTS" in str(ee):
                    print(
                        f"Email already registered input password for account '{email}'")
                    password = input("Password: ")
                    user = auth.sign_in_with_email_and_password(
                        email, password)
            else:
                if not first:
                    first = input("First Name?: ")
                if not last:
                    last = input("Last Name?: ")
                if not key:
                    key = input("Key?: ")

                data = {"first": first, "last": last, "key": key}

                db.child("users").child(user["localId"]).set(data)
