import firebase_conn
import bcrypt


def creating_user(name, surname, email, password, email_field):
    valid = None
    ref = firebase_conn.db.reference("/users")
    users = ref.get()
    email_list = []
    try:
        salt = bcrypt.gensalt()
        hashed_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
    except Exception as e:
        print(f"Bcrypt_Error: {e}")

    if users is not None:
        for key, value in users.items():
            email_list.append(value["email"])

    if email not in email_list:
        try:
            new_user = ref.push(
                {
                    "name": name,
                    "surname": surname,
                    "email": email,
                    "password": hashed_pass.decode("utf-8")
                }
            )
            valid = True
        except Exception as e:
            print(e)
    else:
        email_field.error = True
        email_field.helper_text = "Vartotojas su tokiu el. paštu jau egzistuoja!"
        print("No user added")
    print(f"User added: {new_user.key}")
    return valid


def login(email, password):
    valid = False
    ref = firebase_conn.db.reference("/users")
    users = ref.get()
    user_id = None
    if users is not None:
        for key, value in users.items():
            if value["email"] == email:
                hashed_pass = value["password"]
                user_id = key
        try:
            match = bcrypt.checkpw(password.encode("utf-8"), hashed_pass.encode("utf-8"))
            if match:
                valid = True
        except Exception as e:
            print(e)
    return valid, user_id





