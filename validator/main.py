import re
from typing import Any, Callable, Dict, Optional

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)


@register_validator(name="cartesia/quotes-price", data_type="string")
class QuotesPrice(Validator):
    """Validates that the generated text contains a price quote.

    **Key Properties**

    | Property                     | Description                   |
    |------------------------------|-------------------------------|
    | Name for `format` attribute  | `cartesia/quotes-price`       |
    | Supported data types         | `string`                      |
    | Programmatic fix             | N/A                           |
    """

    DEFAULT_CURRENCY = "USD"
    SYMBOLS = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "AUD": "A$",
        "CAD": "C$",
        "CNY": "¥",
        "NZD": "NZ$",
    }

    def __init__(self, on_fail: Optional[Callable] = None, **kwargs):
        super().__init__(on_fail, **kwargs)

    def quotes_price(
        self,
        value: str,
        currency: str,
    ) -> bool:
        """Check if the generated text contains a price quote in the given currency.

        Args:
            value (str): The generated text.

        Returns:
            bool: Whether the generated text has a price quote.
        """
        symbol = self.SYMBOLS[currency]
        # Create a regex pattern to match the currency symbol and a number
        pattern = rf"{re.escape(symbol)}\s*\d+(?:\.\d+)?"

        # Check if the pattern is present in the generated text
        return bool(re.search(pattern, value))

    def _unpack_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Unpacks the metadata and returns the relevant fields."""
        currency = metadata.get("currency", self.DEFAULT_CURRENCY)
        assert currency in set(
            self.SYMBOLS.keys()
        ), f"Currency {currency} not supported."
        return currency

    def validate(self, value: str, metadata: Dict[str, Any]) -> ValidationResult:
        """Validate that the generated text has a certain financial tone."""
        currency = self._unpack_metadata(metadata)
        if self.quotes_price(value, currency):
            return FailResult(
                metadata=metadata,
                error_message="The generated text contains a price quote.",
            )
        return PassResult()


# Run tests via `pytest -rP ./test.py`
class TestTest:
    def test_success_case(self):
        validator = QuotesPrice()
        result = validator.validate("The price is $131.45.", {"currency": "JPY"})
        assert isinstance(result, PassResult) is True
        result = validator.validate("The price is not included.", {"currency": "USD"})
        assert isinstance(result, PassResult) is True

    def test_failure_case(self):
        validator = QuotesPrice()
        result = validator.validate("The price is $100.", {"currency": "USD"})
        assert isinstance(result, FailResult) is True
        result = validator.validate("The price is $131.45.", {"currency": "USD"})
        assert isinstance(result, FailResult) is True


if __name__ == "__main__":
    validator = QuotesPrice()
    print(validator.validate("The price is $100.", {"currency": "USD"}))
    print(validator.validate("The price is $131.45.", {"currency": "USD"}))
    print(validator.validate("The price is $131.45.", {"currency": "JPY"}))
