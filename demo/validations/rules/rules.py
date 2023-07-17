from rest_framework import serializers, status


def even_number(value):
    if value % 2 != 0:
        raise serializers.ValidationError('This field must be an even number.')

def unique():
    pass

def test(field, args=[], kwargs={}):
    print('test')
    print(field)
    print(args)
    print(kwargs)

    def func():
        # if field == 'test':
        raise serializers.ValidationError(detail='This field must be an even number.', code=status.HTTP_400_BAD_REQUEST)

    return func