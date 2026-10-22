import secrets as s


def generate_otp(digits):
    otp_generated = ""
    for i in range(digits):
        otp_generated += str(s.randbelow(9))
    return str(otp_generated)

print(generate_otp(6))
