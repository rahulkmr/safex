"""Tests for expressions."""
import pytest

from safex import __version__, eval_expression


def test_version():
    assert __version__ == "0.1.0"


def test_binary_operators():
    """Tests for binary operators."""
    assert eval_expression("1 + 2") == 3
    assert eval_expression("1 * 2") == 2
    assert eval_expression("10 / 2") == 5
    assert eval_expression("1 - 2") == -1
    assert eval_expression("2 - 1") == 1
    assert eval_expression("1 + 2 * 3") == 7
    assert eval_expression("1 + 2 * 12 / 3") == 9
    assert eval_expression("10 % 2") == 0
    assert eval_expression("11 % 2") == 1
    assert eval_expression("2 ** 3") == 8
    assert eval_expression("2 << 2") == 8
    assert eval_expression("8 >> 2") == 2
    assert eval_expression("9 // 2") == 4

    assert eval_expression("a + b", {"a": 1, "b": 2}) == 3
    assert eval_expression("a * b", {"a": 1, "b": 2}) == 2
    assert eval_expression("a / b", {"a": 10, "b": 2}) == 5


def test_unary_operators():
    """Tests for unary operators."""
    assert eval_expression("-1") == -1
    assert eval_expression("+1") == 1
    assert eval_expression("not True") is False
    assert eval_expression("not False") is True

    assert eval_expression("-a", {"a": 1}) == -1
    assert eval_expression("+a", {"a": 1}) == 1


def test_comparisons():
    """Tests for comparisons"""
    assert eval_expression("2 > 1") is True
    assert eval_expression("2 < 1") is False
    assert eval_expression("2 != 1") is True
    assert eval_expression("2 == 2") is True
    assert eval_expression("5 <= 6") is True
    assert eval_expression("5 <= 5") is True
    assert eval_expression("5 >= 4") is True
    assert eval_expression("5 >= 5") is True
    assert eval_expression("1 < 2 < 3") is True
    assert eval_expression("5 in (1, 2, 5)") is True
    assert eval_expression("5 in (1, 2, 4)") is False
    assert eval_expression("5 not in (1, 2, 4)") is True
    assert eval_expression("True is True") is True
    assert eval_expression("True is False") is False


def test_name():
    """Tests for name evaluation"""
    assert eval_expression("a", {"a": 1}) == 1
    assert eval_expression("all((True, False))") is False
    assert eval_expression("any((True, False))") is True
    assert eval_expression("sum((1, 2, 3))") == 6
    assert eval_expression("None") is None

    with pytest.raises(ValueError):
        eval_expression("a")


def test_boolean_operators():
    """Tests for boolean operators."""
    assert eval_expression("True and False") is False
    assert eval_expression("True or False") is True


def test_call():
    """Tests for function calls"""
    assert eval_expression("inc(x)", {"inc": lambda x: x + 1, "x": 1}) == 2
    with pytest.raises(ValueError):
        eval_expression("fn(1)")


def test_if_expression():
    """Tests for if expression"""
    assert eval_expression("5 if True else 6") == 5
    assert eval_expression("5 if False else 6") == 6


def test_collections():
    """Tests for collections."""
    assert eval_expression("[1, 2, 3]") == [1, 2, 3]
    assert eval_expression("(1, 2, 3)") == (1, 2, 3)
    assert eval_expression("{'a': 1, 'b': 2}") == {"a": 1, "b": 2}


def test_subscript():
    """Tests for subscripts"""
    assert eval_expression("[0, 1, 2, 3, 4, 5][0]") == 0
    assert eval_expression("[0, 1, 2, 3, 4, 5][-1]") == 5
    assert eval_expression("[0, 1, 2, 3, 4, 5][0:3]") == [0, 1, 2]
    assert eval_expression("[0, 1, 2, 3, 4, 5][0:4:2]") == [0, 2]
    assert eval_expression("[0, 1, 2, 3, 4, 5][:4]") == [0, 1, 2, 3]
    assert eval_expression("[0, 1, 2, 3, 4, 5][4:]") == [4, 5]
    assert eval_expression("{'a': 1, 'b': 2}['a']") == 1


def test_lambda():
    """Tests for lambdas"""
    assert eval_expression("(lambda x: x)(1)") == 1
    assert eval_expression("(lambda x: x * a)(1)", {"a": 10}) == 10
    assert eval_expression(
        "list(filter(lambda x: x % 2 == 1, a))", {"a": [0, 1, 2, 3, 4, 5]}
    ) == [1, 3, 5]
    assert (
        eval_expression(
            "list(filter(lambda x: x % 2 == 1, map(lambda x: x * 3, a)))",
            {"a": [0, 1, 2, 3, 4, 5]},
        )
        == [3, 9, 15]
    )
    assert eval_expression("list(filter(lambda x: x % 2 == 1, range(6)))") == [1, 3, 5]
    assert eval_expression("list(filter(lambda x: x % 2 == 1, range(6)))") == [1, 3, 5]
    assert eval_expression("list(sorted(range(5), reverse=True))") == [4, 3, 2, 1, 0]
    assert eval_expression("(lambda *args: sum(args))(1, 2, 3)") == 6


def test_expression():
    """Tests for expressions."""
    event = {
        "type": "user_added",
        "payload": {
            "name": "test",
            "age": 17,
            "emails": [
                {"type": "primary", "email": "test@test.com"},
                {"type": "secondary", "email": "test2@test.com"},
            ],
        },
    }
    assert (
        eval_expression(
            "event['type'] == 'user_added' and event['payload']['age'] < 18",
            {"event": event},
        )
        is True
    )
    assert (
        eval_expression("event['payload']['emails'][0]['email']", {"event": event})
        == "test@test.com"
    )
