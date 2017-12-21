import logging
from logging import FileHandler, StreamHandler

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
#default_formatter = logging.Formatter(
#    fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
#    datefmt=DATE_FORMAT,
#)

default_formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s",
    datefmt=DATE_FORMAT,
)

console_handler = StreamHandler()
console_handler.setFormatter(default_formatter)

file_handler = FileHandler("/tmp/dataset.log", "a")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(default_formatter)

root = logging.getLogger()
root.addHandler(console_handler)
root.addHandler(file_handler)
root.setLevel(logging.DEBUG)

