import numbers


class UnsignedInt(int):
    """A custom integer type that represents unsigned values.

    If a bit_width is defined, it enforces wrapping behavior.
    If no bit_width is defined, it enforces non-negativity.

    Operations involving UnsignedInt will:
    - Support any Python numeric type as the other operand.
    - If the *numeric result* (from Python's standard type promotion) is an integer
      AND falls within the UnsignedInt's valid range/condition, it returns an UnsignedInt.
    - Otherwise (e.g., negative int for unbounded, or any float/complex result),
      it returns the standard Python numeric type (int, float, complex, etc.).
    - Will raise TypeError if the operand is not a valid numeric type.
    """

    _bit_width = None

    def __new__(cls, value, bit_width=None):
        if not isinstance(value, int):
            raise TypeError("UnsignedInt value must be an integer.")

        effective_bit_width = bit_width
        max_value = float("inf")

        if effective_bit_width is not None:
            if not isinstance(effective_bit_width, int) or effective_bit_width <= 0:
                raise ValueError("Bit width must be a positive integer or None.")
            max_value = (1 << effective_bit_width) - 1
            value = value % (1 << effective_bit_width)
        elif value < 0:
            raise ValueError(
                "UnsignedInt cannot be initialized with a negative value unless a bit_width is specified for wrapping."
            )

        obj = super().__new__(cls, value)
        obj._bit_width = effective_bit_width
        obj._max_value = max_value
        return obj

    def __repr__(self):
        if self._bit_width is not None:
            return f"UnsignedInt({super().__repr__()}, bit_width={self._bit_width})"
        return f"UnsignedInt({super().__repr__()})"

    # Helper to determine the return type based on result and original UnsignedInt's properties
    def _determine_result_type(self, intermediate_result):
        if not isinstance(intermediate_result, int):
            return intermediate_result

        if self._bit_width is not None:
            wrapped_val = intermediate_result % (1 << self._bit_width)
            return UnsignedInt(wrapped_val, bit_width=self._bit_width)
        else:
            if intermediate_result >= 0:
                return UnsignedInt(intermediate_result, bit_width=None)
            else:
                return intermediate_result

    # --- Helper to get the value of 'other' suitable for Python's numeric operations ---
    # This now explicitly raises TypeError if 'other' is not a numbers.Number.
    def _get_operand_value(self, other):
        if isinstance(other, UnsignedInt):
            return other._value
        elif isinstance(other, numbers.Number):
            return other
        # If it's not an UnsignedInt or any other numeric type, raise TypeError
        raise TypeError(
            f"Unsupported operand type for UnsignedInt: '{type(other).__name__}'"
        )

    # --- Helper for getting integer-only operands for bitwise operations ---
    def _get_integer_operand_value(self, other):
        if isinstance(other, UnsignedInt):
            return other._value
        elif isinstance(other, numbers.Integral):  # Only integer-like types
            return other
        raise TypeError(
            f"Unsupported operand type for bitwise operation with UnsignedInt: '{type(other).__name__}' (must be an integer-like type)"
        )

    # --- Overriding Arithmetic Operations (simplified now that _get_operand_value raises errors) ---

    def __add__(self, other):
        other_value = self._get_operand_value(other)
        intermediate_result = super().__add__(other_value)
        return self._determine_result_type(intermediate_result)

    def __radd__(self, other):
        if isinstance(other, numbers.Number):  # Check if other is a number
            intermediate_result = other + self._value
            return self._determine_result_type(intermediate_result)
        return (
            NotImplemented  # If other is not a number, let it handle or raise TypeError
        )

    def __sub__(self, other):
        other_value = self._get_operand_value(other)
        intermediate_result = super().__sub__(other_value)
        return self._determine_result_type(intermediate_result)

    def __rsub__(self, other):
        if isinstance(other, numbers.Number):
            intermediate_result = other - self._value
            return self._determine_result_type(intermediate_result)
        return NotImplemented

    def __mul__(self, other):
        other_value = self._get_operand_value(other)
        intermediate_result = super().__mul__(other_value)
        return self._determine_result_type(intermediate_result)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        other_value = self._get_operand_value(other)
        if other_value == 0:
            raise ZeroDivisionError("UnsignedInt division by zero")
        return super().__truediv__(other_value)

    def __rtruediv__(self, other):
        if isinstance(other, numbers.Number):
            if self._value == 0:
                raise ZeroDivisionError("UnsignedInt division by zero")
            return other / self._value
        return NotImplemented

    def __floordiv__(self, other):
        other_value = self._get_operand_value(other)
        if other_value == 0:
            raise ZeroDivisionError("UnsignedInt division by zero")
        intermediate_result = super().__floordiv__(other_value)
        return self._determine_result_type(intermediate_result)

    def __rfloordiv__(self, other):
        if isinstance(other, numbers.Number):
            if self._value == 0:
                raise ZeroDivisionError("UnsignedInt division by zero")
            intermediate_result = other // self._value
            return self._determine_result_type(intermediate_result)
        return NotImplemented

    def __mod__(self, other):
        other_value = self._get_operand_value(other)
        if other_value == 0:
            raise ZeroDivisionError("UnsignedInt modulo by zero")
        intermediate_result = super().__mod__(other_value)
        return self._determine_result_type(intermediate_result)

    def __rmod__(self, other):
        if isinstance(other, numbers.Number):
            if self._value == 0:
                raise ZeroDivisionError("UnsignedInt modulo by zero")
            intermediate_result = other % self._value
            return self._determine_result_type(intermediate_result)
        return NotImplemented

    def __pow__(self, other):
        other_value = self._get_operand_value(other)
        intermediate_result = super().__pow__(other_value)
        return self._determine_result_type(intermediate_result)

    def __rpow__(self, other):
        if isinstance(other, numbers.Number):
            intermediate_result = pow(other, self._value)
            return self._determine_result_type(intermediate_result)
        return NotImplemented

    # --- Bitwise Operations ---
    def __and__(self, other):
        other_value = self._get_integer_operand_value(
            other
        )  # Use integer-specific helper
        intermediate_result = super().__and__(other_value)
        return self._determine_result_type(intermediate_result)

    def __rand__(self, other):
        if isinstance(other, numbers.Integral):
            intermediate_result = other & self._value
            return self._determine_result_type(intermediate_result)
        return NotImplemented

    def __or__(self, other):
        other_value = self._get_integer_operand_value(other)
        intermediate_result = super().__or__(other_value)
        return self._determine_result_type(intermediate_result)

    def __ror__(self, other):
        if isinstance(other, numbers.Integral):
            intermediate_result = other | self._value
            return self._determine_result_type(intermediate_result)
        return NotImplemented

    def __xor__(self, other):
        other_value = self._get_integer_operand_value(other)
        intermediate_result = super().__xor__(other_value)
        return self._determine_result_type(intermediate_result)

    def __rxor__(self, other):
        if isinstance(other, numbers.Integral):
            intermediate_result = other ^ self._value
            return self._determine_result_type(intermediate_result)
        return NotImplemented

    def __lshift__(self, other):
        other_value = self._get_integer_operand_value(other)
        intermediate_result = super().__lshift__(other_value)
        return self._determine_result_type(intermediate_result)

    def __rlshift__(self, other):
        if isinstance(other, numbers.Integral):
            intermediate_result = other << self._value
            return self._determine_result_type(intermediate_result)
        return NotImplemented

    def __rshift__(self, other):
        other_value = self._get_integer_operand_value(other)
        intermediate_result = super().__rshift__(other_value)
        return self._determine_result_type(intermediate_result)

    def __rrshift__(self, other):
        if isinstance(other, numbers.Integral):
            intermediate_result = other >> self._value
            return self._determine_result_type(intermediate_result)
        return NotImplemented

    def __invert__(self):
        if self._bit_width is None:
            raise ValueError(
                "Bitwise NOT (~) on UnsignedInt requires a defined bit_width to determine max value for inversion."
            )
        intermediate_result = self._max_value - self._value
        return UnsignedInt(intermediate_result, bit_width=self._bit_width)

    # --- Unary Operations ---
    def __neg__(self):
        if self._bit_width is not None:
            if self == 0:
                return UnsignedInt(0, bit_width=self._bit_width)
            intermediate_result = (1 << self._bit_width) - self._value
            return UnsignedInt(intermediate_result, bit_width=self._bit_width)
        else:
            return -self._value

    def __pos__(self):
        return self

    def __abs__(self):
        return self

    # --- Rich Comparisons ---
    def __eq__(self, other):
        if isinstance(other, UnsignedInt):
            return super().__eq__(other) and self._bit_width == other._bit_width
        return super().__eq__(other)

    # Other comparison operators (__lt__, __le__, __gt__, __ge__) inherited from int will typically
    # behave as desired. No explicit override needed unless specific mixed-type comparison logic is required.

    # --- Hashing ---
    def __hash__(self):
        return hash((super().__hash__(), self._bit_width))

    # --- Explicit Type Conversions ---
    def __int__(self):
        return super().__int__()

    def __float__(self):
        return float(super().__int__())
