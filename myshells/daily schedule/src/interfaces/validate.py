from typing import Optional, Union, Any


class ValidationObject:
    def __init__(self, success: bool,
                 wrong_param: Optional[int] = None,
                 types: Optional[tuple] = None):
        """ This class defines a validation object representing the state of
            a validation. If the validation was successful then the success flag
            will be true and the other parameters none, else they will describe the error.

            :param success: a flag representing the success state of the validation
            :param wrong_param: optional, the index of the parameter who failed the validation
            :param types: optional, a couple of types: the type required and the actual wrong_param's one
            """
        self.success = success
        self.wrong_param = wrong_param
        self.types = types


class Validate:
    @staticmethod
    def validate_params(args: Union[tuple, Any], types: Union[tuple, Any]) -> ValidationObject:
        """Checks if each parameter of a method respects the type requested.

        :param args: the parameters of the method
        :param types: the required types for the args
        :return: an object with success flag
        """
        if not isinstance(args, tuple) and not isinstance(types, tuple):
            args = (args,)
            types = (types,)
        for i, (arg, _type) in enumerate(zip(args, types)):
            if not isinstance(arg, _type):
                return ValidationObject(False, i, (_type, type(arg)))

        return ValidationObject(True)

    @classmethod
    def validate_params_ex(cls, args: Union[tuple, Any], types: Union[tuple, Any]) -> None:
        check = cls.validate_params(args, types)
        if not check.success:
            raise TypeError(f"Parameter {check.wrong_param} expected with type {check.types[0]}, got {check.types[1]} instead")
