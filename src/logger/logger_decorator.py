import os
import datetime
import functools

class LoggerDecorator:
    def __init__(self, log_dir, log_format="[{timestamp}] Args: {args}, Kwargs: {kwargs}, Result: {result}", log_level="INFO"):
        self.log_dir = log_dir
        self.log_format = log_format
        self.log_level = log_level
        os.makedirs(log_dir, exist_ok=True)

    def log_decorator(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                message = self.log_format.format(
                    timestamp=datetime.datetime.now(),
                    args=args,
                    kwargs=kwargs,
                    result=result
                )
            except Exception as e:
                message = f"[{datetime.datetime.now()}] Args: {args}, Kwargs: {kwargs}. Exception: {e}"
                result = f"Exception: {e}"
                self._write_log(os.path.join(self.log_dir, f"{func.__name__}_log.txt"), message, "ERROR")
                raise
            else:
                self._write_log(os.path.join(self.log_dir, f"{func.__name__}_log.txt"), message)

            return result

        return wrapper

    def _write_log(self, filename, message, log_level=None):
        if log_level is None:
            log_level = self.log_level
        with open(filename, "a") as file:
            file.write(f"{log_level}: {message}\n")
            file.write("-" * 40 + "\n")

# Example Usage
logger = LoggerDecorator("logs")

@logger.log_decorator
def sample_function(a, b):
    return a / b  # Example function that could raise an exception



@logger.log_decorator
def triangle(x: int, y: int, z: int) -> str:
    if x == y == z:
        return "Equilateral triangle"
    elif x == y or y == z or x == z:
        return "Isosceles triangle"
    else:
        return "Scalene triangle"


if __name__ == "__main__":
    sample_function(5, 3)
    triangle(3, 3, 3)
    sample_function(5, 1)
    sample_function(2, 2)
    try:
        sample_function(5, 0)  # This call should result in a ZeroDivisionError
    except ZeroDivisionError:
        pass
    sample_function(2, 1)
    triangle(3, 3, 4)
    triangle(3, 4, 5)
