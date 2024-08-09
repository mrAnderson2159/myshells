from src.functions.tools import usage

def raiseFlagError(wrong_flag: str) -> ValueError:
    raise ValueError(f"{wrong_flag} is not a valid flag\n\n{usage()}")

def raiseMissingFlag() -> ValueError:
    raise ValueError(f"Missing flags\n\n{usage()}")
