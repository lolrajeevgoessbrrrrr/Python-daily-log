import streamlit
import requests
import hashlib
import os
import dotenv


# This line loads variables from a file named .env into the environment.
# We use this so the n8n webhook base URL is not hardcoded into the script.
dotenv.load_dotenv()


# We read the n8n base URL from the environment.
# Example value: http://localhost:5678/webhook
N8N_BASE_URL = os.getenv("N8N_BASE_URL")


def hash_password(plain_text_password):
    # This function takes a plain text password and turns it into a hash.
    # A hash is a one-way scrambled version of the password.
    # n8n never sees or stores your real password, only this hash.
    password_as_bytes = plain_text_password.encode("utf-8")
    hash_object = hashlib.sha256(password_as_bytes)
    hashed_password = hash_object.hexdigest()
    return hashed_password


def call_register_webhook(username, email, password_hash):
    # This function sends a POST request to the /register webhook in n8n.
    # It tells n8n: here is a new user, please check if the username is free,
    # generate an OTP, save the user, and email the OTP.
    url = N8N_BASE_URL + "/register"
    request_body = {
        "username": username,
        "email": email,
        "password_hash": password_hash
    }
    try:
        response = requests.post(url, json=request_body, timeout=15)
        response_data = response.json()
        return response_data
    except requests.exceptions.RequestException as error:
        return {"status": "error", "message": "Could not reach n8n. Is it running on localhost:5678? Details: " + str(error)}


def call_verify_otp_webhook(username, otp):
    # This function sends the OTP the user typed back to n8n for checking.
    url = N8N_BASE_URL + "/verify-otp"
    request_body = {
        "username": username,
        "otp": otp
    }
    try:
        response = requests.post(url, json=request_body, timeout=15)
        response_data = response.json()
        return response_data
    except requests.exceptions.RequestException as error:
        return {"status": "error", "message": "Could not reach n8n. Details: " + str(error)}


def call_login_webhook(username, password_hash):
    # This function checks a username and password hash against what n8n has stored.
    url = N8N_BASE_URL + "/login"
    request_body = {
        "username": username,
        "password_hash": password_hash
    }
    try:
        response = requests.post(url, json=request_body, timeout=15)
        response_data = response.json()
        return response_data
    except requests.exceptions.RequestException as error:
        return {"status": "error", "message": "Could not reach n8n. Details: " + str(error)}


def call_forgot_password_webhook(email):
    # This function asks n8n to generate a new OTP for password reset
    # and email it to the given address.
    url = N8N_BASE_URL + "/forgot-password"
    request_body = {
        "email": email
    }
    try:
        response = requests.post(url, json=request_body, timeout=15)
        response_data = response.json()
        return response_data
    except requests.exceptions.RequestException as error:
        return {"status": "error", "message": "Could not reach n8n. Details: " + str(error)}


def call_reset_password_webhook(email, otp, new_password_hash):
    # This function sends the reset OTP plus the new password hash to n8n.
    # If the OTP is correct and not expired, n8n updates the stored password.
    url = N8N_BASE_URL + "/reset-password"
    request_body = {
        "email": email,
        "otp": otp,
        "new_password_hash": new_password_hash
    }
    try:
        response = requests.post(url, json=request_body, timeout=15)
        response_data = response.json()
        return response_data
    except requests.exceptions.RequestException as error:
        return {"status": "error", "message": "Could not reach n8n. Details: " + str(error)}


def show_welcome_page(username):
    # This is the final page shown after a successful login.
    streamlit.title("You're in!")
    streamlit.success("Well done, " + username + ", one more step forward towards the future you want.")


def main():
    streamlit.set_page_config(page_title="OTP Login System")

    # streamlit.session_state lets us remember values between reruns of the script.
    # Streamlit reruns this whole file top to bottom every time you click a button,
    # so without session_state we would lose track of things like "which step are we on".
    if "logged_in_username" not in streamlit.session_state:
        streamlit.session_state.logged_in_username = None

    if "pending_register_username" not in streamlit.session_state:
        streamlit.session_state.pending_register_username = None

    if "pending_reset_email" not in streamlit.session_state:
        streamlit.session_state.pending_reset_email = None

    # If someone is already logged in, skip straight to the welcome page.
    if streamlit.session_state.logged_in_username is not None:
        show_welcome_page(streamlit.session_state.logged_in_username)
        return

    streamlit.title("OTP Login System")

    chosen_tab = streamlit.tabs(["Login", "Register", "Forgot Password"])

    # ---------------- LOGIN TAB ----------------
    with chosen_tab[0]:
        streamlit.subheader("Log in")
        login_username = streamlit.text_input("Username", key="login_username_input")
        login_password = streamlit.text_input("Password", type="password", key="login_password_input")
        login_button_clicked = streamlit.button("Log In")

        if login_button_clicked:
            if login_username == "" or login_password == "":
                streamlit.error("Please fill in both username and password.")
            else:
                password_hash = hash_password(login_password)
                result = call_login_webhook(login_username, password_hash)

                if result.get("status") == "ok":
                    streamlit.session_state.logged_in_username = login_username
                    streamlit.rerun()
                elif result.get("status") == "denied":
                    streamlit.error(result.get("message", "Login failed."))
                else:
                    streamlit.error(result.get("message", "Something went wrong."))

    # ---------------- REGISTER TAB ----------------
    with chosen_tab[1]:
        streamlit.subheader("Create an account")

        # If we are waiting for an OTP, show the OTP box instead of the register form.
        if streamlit.session_state.pending_register_username is not None:
            streamlit.info("We sent a 6-digit OTP to your email. Enter it below (valid for 10 minutes).")
            entered_otp = streamlit.text_input("Enter OTP", key="register_otp_input")
            verify_button_clicked = streamlit.button("Verify OTP", key="verify_register_otp_button")

            if verify_button_clicked:
                result = call_verify_otp_webhook(streamlit.session_state.pending_register_username, entered_otp)

                if result.get("status") == "verified":
                    streamlit.success("Email verified! You can now log in from the Login tab.")
                    streamlit.session_state.pending_register_username = None
                else:
                    streamlit.error(result.get("message", "Invalid or expired OTP."))

            cancel_button_clicked = streamlit.button("Start over", key="cancel_register_button")
            if cancel_button_clicked:
                streamlit.session_state.pending_register_username = None
                streamlit.rerun()

        else:
            register_username = streamlit.text_input("Choose a username", key="register_username_input")
            register_email = streamlit.text_input("Email", key="register_email_input")
            register_password = streamlit.text_input("Choose a password", type="password", key="register_password_input")
            register_button_clicked = streamlit.button("Register")

            if register_button_clicked:
                if register_username == "" or register_email == "" or register_password == "":
                    streamlit.error("Please fill in all fields.")
                else:
                    password_hash = hash_password(register_password)
                    result = call_register_webhook(register_username, register_email, password_hash)

                    if result.get("status") == "otp_sent":
                        streamlit.session_state.pending_register_username = register_username
                        streamlit.rerun()
                    else:
                        streamlit.error(result.get("message", "Registration failed."))

    # ---------------- FORGOT PASSWORD TAB ----------------
    with chosen_tab[2]:
        streamlit.subheader("Reset your password")

        if streamlit.session_state.pending_reset_email is not None:
            streamlit.info("We sent a 6-digit OTP to your email. Enter it and your new password below.")
            reset_otp = streamlit.text_input("Enter OTP", key="reset_otp_input")
            new_password = streamlit.text_input("New password", type="password", key="new_password_input")
            reset_button_clicked = streamlit.button("Reset Password")

            if reset_button_clicked:
                if reset_otp == "" or new_password == "":
                    streamlit.error("Please fill in both fields.")
                else:
                    new_password_hash = hash_password(new_password)
                    result = call_reset_password_webhook(streamlit.session_state.pending_reset_email, reset_otp, new_password_hash)

                    if result.get("status") == "reset":
                        streamlit.success("Password reset! You can now log in with your new password.")
                        streamlit.session_state.pending_reset_email = None
                    else:
                        streamlit.error(result.get("message", "Reset failed."))

            cancel_reset_button_clicked = streamlit.button("Start over", key="cancel_reset_button")
            if cancel_reset_button_clicked:
                streamlit.session_state.pending_reset_email = None
                streamlit.rerun()

        else:
            forgot_email = streamlit.text_input("Enter your account email", key="forgot_email_input")
            send_reset_otp_button_clicked = streamlit.button("Send Reset OTP")

            if send_reset_otp_button_clicked:
                if forgot_email == "":
                    streamlit.error("Please enter your email.")
                else:
                    result = call_forgot_password_webhook(forgot_email)

                    if result.get("status") == "otp_sent":
                        streamlit.session_state.pending_reset_email = forgot_email
                        streamlit.rerun()
                    else:
                        streamlit.error(result.get("message", "Could not send reset OTP."))


if __name__ == "__main__":
    main()