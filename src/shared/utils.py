import uuid


def is_uuid(raw: str):
    try:
        uuid.UUID(raw)
    except ValueError:
        return False
    return True
