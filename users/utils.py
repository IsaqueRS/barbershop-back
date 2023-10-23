import secrets


def get_unique_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except (model.DoesNotExist, model.MultipleObjectsReturned):
        return None


def generate_random_password():
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    password = ''.join(secrets.choice(alphabet) for i in range(12))
    return password
