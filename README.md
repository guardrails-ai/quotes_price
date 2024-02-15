## Overview

| Developed by | Cartesia AI |
| --- | --- |
| Date of development | Feb 15, 2024 |
| Validator type | Format |
| Blog |  |
| License | Apache 2 |
| Input/Output | Output |

## Description

This validator checks if a price quote in an unexpected currency is present in the text.

## Requirements
* Dependencies: None

## Installation

```bash
$ guardrails hub install hub://cartesia/quotes_price
```

## Usage Examples

### Validating string output via Python

In this example, we use the `quotes_price` validator on any prompt.

```python
# Import Guard and Validator
from guardrails.hub import QuotesPrice
from guardrails import Guard

# Initialize Validator
val = QuotesPrice()

# Setup Guard
guard = Guard.from_string(
    validators=[val, ...],
)

# Pass LLM output through guard
guard.parse(
    "The price of a loaf of bread is not yet known.",
    metadata={}
)  # Pass

guard.parse(
    "The Windsor castle tour costs £20.00.",
    metadata={
        "currency": "GBP"
    }
)  # Fail

```

## API Reference

**`__init__(self, on_fail="noop")`**
<ul>

Initializes a new instance of the Validator class.

**Parameters:**

- **`on_fail`** *(str, Callable):* The policy to enact when a validator fails. If `str`, must be one of `reask`, `fix`, `filter`, `refrain`, `noop`, `exception` or `fix_reask`. Otherwise, must be a function that is called when the validator fails.

</ul>

<br>

**`__call__(self, value, metadata={}) → ValidationOutcome`**

<ul>

Validates the given `value` using the rules defined in this validator, relying on the `metadata` provided to customize the validation process. This method is automatically invoked by `guard.parse(...)`, ensuring the validation logic is applied to the input data.

Note:

1. This method should not be called directly by the user. Instead, invoke `guard.parse(...)` where this method will be called internally for each associated Validator.
2. When invoking `guard.parse(...)`, ensure to pass the appropriate `metadata` dictionary that includes keys and values required by this validator. If `guard` is associated with multiple validators, combine all necessary metadata into a single dictionary.

**Parameters:**

- **`value`** *(Any):* The input value to validate.
- **`metadata`** *(dict):* A dictionary containing metadata required for validation. Keys and values must match the expectations of this validator.
    
    
    | Key | Type | Description | Default | Required |
    | --- | --- | --- | --- | --- |
    | `currency` | String | Desired currency | `"USD"` | No |

</ul>
