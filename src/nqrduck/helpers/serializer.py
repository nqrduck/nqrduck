"""Helper used  for serializing objects to json."""

import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    """This class is used to encode decimal values to json."""

    def default(self, obj):
        """This method is called by the json encoder to encode the object.

        Args:
            obj (object): The object to be encoded

        Returns:
            str: The encoded object

        Examples:
            >>> import json
            >>> from decimal import Decimal
            >>> json.dumps(Decimal("1.0"), cls=DecimalEncoder)
        """
        if isinstance(obj, Decimal):
            return str(obj)  # or float(obj) if you want to keep it as a number
        return super().default(obj)
