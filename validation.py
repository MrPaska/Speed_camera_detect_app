import re
import user

name_pattern = r"^[a-žA-Ž\s]+$"
email_pattern = r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"
password_pattern = r"^(?=.*[a-ž])(?=.*[A-Ž])(?=.*\d)[a-žA-Ž\d]{8,}$"


def login_valid(email, password):
    user_id = None
    email.helper_text = ""
    password.helper_text = ""
    valid = False
    if email.text != "":
        if password.text != "":
            valid, user_id = user.login(email.text, password.text)
            print(f"validation.py {valid}")
        else:
            valid = None
            password.error = True
            password.helper_text = "Laukas tuščias!"
    else:
        valid = None
        email.error = True
        email.helper_text = "Laukas tuščias!"

    return valid, user_id


def signup_valid(name, surname, email, password):
    valid = None
    if not bool(re.match(name_pattern, name.text)):
        name.error = True
        name.helper_text = "Neatitinka įvestas vardas formato!"
    else:
        name_txt = name.text
    if not bool(re.match(name_pattern, surname.text)):
        surname.error = True
        surname.helper_text = "Neatitinka įvestas vardas formato!"
    else:
        surname_txt = surname.text
    if not bool(re.match(email_pattern, email.text)):
        email.error = True
        email.helper_text = "Neatitinka pašto formato!"
    else:
        email_txt = email.text
    if not bool(re.match(password_pattern, password.text)):
        password.error = True
        password.helper_text = "Nemažiau 8 simboliai!"
    else:
        password_txt = password.text

    try:
        valid = user.creating_user(name_txt, surname_txt, email_txt, password_txt, email)
    except Exception as e:
        pass
    return valid







