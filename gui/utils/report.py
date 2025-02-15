
import logging
from tkinter.messagebox import showinfo, showwarning, showerror

logging.basicConfig(level=logging.INFO)

SUPPRESS_INFO = True
SUPPRESS_WARN = False
SUPPRESS_ERROR = False


def info(msg):
    logging.info(msg)
    if SUPPRESS_INFO:
        return
    showinfo(msg)


def warning(msg):
    logging.warning(msg)
    if SUPPRESS_WARN:
        return
    showwarning(msg)


def error(msg):
    logging.error(msg)
    if SUPPRESS_ERROR:
        return
    showerror(msg)
