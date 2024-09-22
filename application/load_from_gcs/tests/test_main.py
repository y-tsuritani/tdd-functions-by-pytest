from src.main import add


def test_add_typeerror():
    # try:
    #     add(1, "2")
    # except TypeError as e:
    #     assert str(e) == "unsupported operand type(s) for +: 'int' and 'str'"
    # try:
    #     add("1", 2)
    # except TypeError as e:
    #     assert str(e) == 'can only concatenate str (not "int") to str'
    try:
        add("1", "2")
    except TypeError as e:
        assert str(e) == "unsupported operand type(s) for +: 'str' and 'str'"
    try:
        add(1.0, 2.0)
    except TypeError as e:
        assert str(e) == "unsupported operand type(s) for +: 'float' and 'float'"


def test_add():
    assert add(1, 2) == 3
    assert add(1, -1) == 0
    assert add(0, 0) == 0
    assert add(-1, -1) == -2


def test_add_valueerror():
    try:
        add(1)
    except TypeError as e:
        assert str(e) == "add() missing 1 required positional argument: 'y'"
    try:
        add()
    except TypeError as e:
        assert str(e) == "add() missing 2 required positional arguments: 'x' and 'y'"
