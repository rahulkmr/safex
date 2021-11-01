# safex

Safe and simple python expression evaluator.

## Installation

```
pip install safex
```

## Usage

```
from safex import eval_expression

# Binary operators
assert eval_expression("1 + 2 * 12 / 3") == 9
assert eval_expression("a + b", {"a": 1, "b": 2}) == 3

# Unary operators
assert eval_expression("not True") == False
assert eval_expression("not False") == True

# Comparisons
assert eval_expression("1 < 2 < 3") == True

# Name lookups
assert eval_expression("a", {"a": 1}) == 1
assert eval_expression("inc(x)", {"inc": lambda x: x + 1, "x": 1}) == 2


# Lists and dicts
assert eval_expression("[0, 1, 2, 3, 4, 5][0]") == 0
assert eval_expression("{'a': 1, 'b': 2}['a']") == 1

# Lambdas, map, filter
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

# Attributes
assert eval_expression("person.name", {"person": person}) == "test"
assert eval_expression("person.address.city", {"person": person}) == "city"

event = {
    'type': 'user_added',
    'payload': {
        'name': 'test',
        'age': 17,
        'emails': [
            {'type': 'primary', 'email': 'test@test.com'},
            {'type': 'secondary', 'email': 'test2@test.com'}
        ]
    }
}
assert eval_expression(
    "event['type'] == 'user_added' and event['payload']['age'] < 18", {"event": event}) == True
assert eval_expression(
    "event['payload']['emails'][0]['email']", {"event": event}) == 'test@test.com'
```