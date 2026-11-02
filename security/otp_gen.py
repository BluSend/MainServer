# BluSend
#
# Basic functionality tests passed

import secrets as s
import bcrypt


def generate_otp(digits):
    otp_generated = ""
    for i in range(digits):
        otp_generated += str(s.randbelow(10))
    hashed_password = bcrypt.hashpw(bytes(otp_generated.encode('utf-8')), bcrypt.gensalt()).decode('utf-8')
    return [otp_generated, hashed_password]
