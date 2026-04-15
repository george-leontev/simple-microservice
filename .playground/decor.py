def test_decor(func):
    def inner(*args, **kwargs):
        print('Before')
        func(*args, **kwargs)
        print('After')

    return inner


@test_decor
def example():
    print('Example')


example()
