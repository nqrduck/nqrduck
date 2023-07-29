import decimal
class UnitConverter:

    @classmethod
    def to_decimal(cls, value : str) -> decimal.Decimal:
        """This method checks if the last character of the string is a suffix. 
        The available suffixes are:
        - n for nano
        - u for micro
        - m for milli
        
        Args:
            value (str): The value to be converted

        Returns:
            decimal.Decimal: The converted value
        """

        if value[-1] == "n":
            return decimal.Decimal(value[:-1]) * decimal.Decimal("1e-9")
        elif value[-1] == "u":
            return decimal.Decimal(value[:-1]) * decimal.Decimal("1e-6")
        elif value[-1] == "m":
            return decimal.Decimal(value[:-1]) * decimal.Decimal("1e-3")
        else:
            return decimal.Decimal(value)

