from claims_validation.custom_exception import DoesNotExist


def get_object_by_pk(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise DoesNotExist(f'{model.__name__} does not exist')
