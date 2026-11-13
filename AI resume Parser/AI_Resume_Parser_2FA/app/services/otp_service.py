from datetime import datetime, timedelta
from ..security import new_otp, hash_otp

SUPPORTED = {"email", "whatsapp", "browser"}

def create_challenge(email: str, channel: str):
    if channel not in SUPPORTED:
        raise ValueError("Channel must be email, whatsapp, or browser")
    code = new_otp()
    return code, {
        "email": email,
        "channel": channel,
        "otp_hash": hash_otp(code),
        "expires_at": datetime.utcnow() + timedelta(minutes=5),
        "verified": False
    }

def dispatch_demo(channel: str, destination: str, code: str):
    # Replace this development adapter with SMTP / WhatsApp Business API in production.
    print(f"[DEMO OTP] channel={channel} destination={destination} code={code}")
