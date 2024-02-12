import datetime

def is_valid_text(value, min_length=1):
    return bool(value and len(value.strip()) >= min_length)

def is_valid_date(value):
    try:
        date = datetime.datetime.fromisoformat(value)
        return True
    except ValueError:
        return False

def is_valid_image_url(value):
    return bool(value and value.startswith('http'))

def is_valid_email(value):
    return bool(value and '@' in value)

# print(is_valid_date("2023-11-30"))