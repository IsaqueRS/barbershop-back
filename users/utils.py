

def get_unique_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except (model.DoesNotExist, model.MultipleObjectsReturned):
        return None