from repository.researchers import create_or_modify_researcher


def create_or_modify_researchers():
    create_or_modify_researcher({
        'email': 'max.foo@gmail.com',
        'firstName': 'Max',
        'lastName': 'Foo'
    })
