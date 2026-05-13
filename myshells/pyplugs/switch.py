class Switch:
    def __init__(self, variable:object):
        assert isinstance(variable, (int, str, float)), f"the switch variable should be basic data type such as int, str or float, not {type(variable)}"
        self.__var = variable
        self.__type = type(variable)
        self.__cases = []

    def __enter__(self):
        return self

    def __exit__(self, _, __, ___):
        return None

    def __add_case(self, case):
        self.__cases.append(case)

    def case(self, value:object, callback:callable, *args, **kwargs) -> object:
        try:
            if isinstance(value, str):
                raise TypeError()
            iter(value)
            try:
                for v in value:
                    self.case(v, callback, *args, **kwargs)
            except TypeError as e:
                print(f"\x1b[91m{e}\x1b[0m")
        except TypeError:
            if type(value) != self.__type:
                raise TypeError(f"Error in {value} case -> you're switching a {self.__type}, {value} is {type(value)} instead")
            self.__add_case(value)
            if value == self.__var:
                return callback(*args, **kwargs) or True
        except Exception as e:
            raise e

        return False

    def exit_case(self, value:object, callback:callable, *args, **kwargs) -> None:
        if self.case(value, callback, *args, **kwargs):
            exit(0)

    def default(self, callback:callable, *args, **kwargs) -> object:
        if not self.__var in self.__cases:
            return callback(*args, **kwargs)

    @property
    def _cases(self):
        return self.__cases
