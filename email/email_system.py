import os
import resend
from dotenv import load_dotenv
from resend.exceptions import ResendError

load_dotenv()
resend.api_key = os.environ["RESEND_API_KEY"]



def send_email(to_address, otp):
    standard_params: resend.Emails.SendParams = {
        "from": "BluSend <email@mail.blusend.tech>",
        "to": [to_address],
        "subject": "hello world",
        "html": f'''
            <strong>Mail coming!</strong>
            <p>Please use the following one-time password to authentication on the BluSend robot:</p>
            <p>{otp}</p>
        ''',
    }
    try:
        email = resend.Emails.send(standard_params)
        print(email)
    except ResendError as error:
        print(error)


send_email("pstaggar@outlook.com", "766768787887")
