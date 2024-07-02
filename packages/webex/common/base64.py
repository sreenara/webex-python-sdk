import base64

def from_base64url(string):
  return base64.urlsafe_b64decode(string).decode()

def to_base64url(string):
  return base64.urlsafe_b64encode(string.encode()).decode()

def encode(string):
  return to_base64url(string)

def decode(string):
  return from_base64url(string)

def validate(string):
  try:
    base64.urlsafe_b64decode(string)
    return True
  except (TypeError, ValueError):
    return False

