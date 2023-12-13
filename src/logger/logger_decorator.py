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
            result = func(*args, **kwargs)
            timestamp = datetime.datetime.now()
            log_message = self.log_format.format(
                timestamp=timestamp,
                args=args,
                kwargs=kwargs,
                result=result
            )
            filename = os.path.join(self.log_dir, f"{func.__name__}_log.txt")
            self._write_log(filename, log_message)
            return result

        return wrapper

    def _write_log(self, filename, message):
        with open(filename, "a") as file:
            file.write(f"{self.log_level}: {message}\n")
            file.write("-" * 40 + "\n")


# Example Usage
logger = LoggerDecorator("logs")


@logger.log_decorator
def sample_function(a, b):
    return a + b


@logger.log_decorator
def triangle(x: int, y: int, z: int) -> str:
    if x == y == z:
        return "Equilateral triangle"
    elif x == y or y == z or x == z:
        return "Isosceles triangle"
    else:
        return "Scalene triangle"


if __name__ == "__main__":
    # Testing the decorator
    sample_function(5, 3)
    sample_function(2, 4)
    triangle(3, 3, 3)
    triangle(3, 3, 4)
