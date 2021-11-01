# safex

Safe and simple python expression evaluator.

## Installation

```
pip install safex
```

## Usage

```
from safex import eval_expression


assert eval_expression("1 + 2 * 12 / 3") == 9
assert eval_expression("a + b", {"a": 1, "b": 2}) == 3

assert eval_expression("not True") == False
assert eval_expression("not False") == True

assert eval_expression("1 < 2 < 3") == True

assert eval_expression("a", {"a": 1}) == 1
assert eval_expression("inc(x)", {"inc": lambda x: x + 1, "x": 1}) == 2


assert eval_expression("[0, 1, 2, 3, 4, 5][0]") == 0
assert eval_expression("{'a': 1, 'b': 2}['a']") == 1

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