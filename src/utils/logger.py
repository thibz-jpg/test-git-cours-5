import json
import logging
import random
import sys
import time
import traceback
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable, Optional, Union

from tqdm import tqdm


def strip_tags(html: str) -> str:
    """
    Strip HTML tags from a string
    """

    class MLStripper(HTMLParser):
        def __init__(self):
            super().__init__()
            self.reset()
            self.strict = False
            self.convert_charrefs = True
            self.text = []

        def handle_data(self, d):
            self.text.append(d)

        def get_data(self):
            return "".join(self.text)

    s = MLStripper()
    s.feed(html)
    return s.get_data()


def sanitize(v):
    """
    Helper function to convert non-serializable values to string representations.
    """
    if isinstance(v, (str, int, float, bool, type(None))):
        return v
    elif isinstance(v, (list, tuple)):
        return [sanitize(x) for x in v]
    elif isinstance(v, dict):
        return {str(k): sanitize(val) for k, val in v.items()}
    else:
        # For custom objects, include class name in representation
        return f"{v.__class__.__name__}({str(v)})"


def pprint(o):
    """Format any object to a printable string"""
    if isinstance(o, str):
        if "html" in o:
            return strip_tags(o)[:500]
        try:
            return json.dumps(json.loads(o), indent=4, sort_keys=True)
        except ValueError:
            return o
    elif isinstance(o, dict) or isinstance(o, list):
        try:
            return json.dumps(o, indent=4, sort_keys=True)
        except TypeError:
            try:
                if isinstance(o, dict):
                    sanitized = {str(k): sanitize(v) for k, v in o.items()}
                else:
                    sanitized = [sanitize(v) for v in o]
                return json.dumps(sanitized, indent=4, sort_keys=True)
            except Exception:
                return str(o)
    return str(o)


class Logger:
    """
    Unified logger for the IIIF downloader that handles:
    - Console output with colors
    - File logging
    - Progress bars
    - Error tracking
    """

    # ANSI Color codes
    COLORS = {
        "error": "\033[91m",  # red
        "warning": "\033[93m",  # yellow
        "info": "\033[94m",  # blue
        "success": "\033[92m",  # green
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "black": "\033[90m",
        "bold": "\033[1m",
        "underline": "\033[4m",
        "end": "\033[0m",
    }

    EMOJIS = {
        "error": "🚨",
        "warning": "⚠️",
        "info": "ℹ️",
        "success": "✅",
        "magenta": "🔮",
        "cyan": "🪼",
        "white": "🏳",
        "black": "🏴",
    }

    def __init__(self, log_dir: Union[str, Path] = "logs"):
        """
        Initialize the logger with a directory for log files

        Args:
            log_dir: Directory where log files will be stored
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.error_log = self.log_dir / "error.log"

        # Setup logging
        self.logger = logging.getLogger("python-project")
        self.logger.setLevel(logging.INFO)

        # Write errors in log file
        fh = logging.FileHandler(self.error_log)
        fh.setLevel(logging.ERROR)
        self.logger.addHandler(fh)

        # Only write info messages to console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        self.logger.addHandler(ch)

    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp in readable format."""
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def get_color(self, color: str) -> str:
        """Get the ANSI color code for a message type."""
        return self.COLORS.get(color, "")

    def get_emoji(self, color: str) -> str:
        """Get the ANSI color code for a message type."""
        return self.EMOJIS.get(color, "")

    def format_message(self, *msg: Any, msg_type: str = "info") -> str:
        """Format a message with timestamp and colors."""
        color = self.get_color(msg_type)
        emoji = self.get_emoji(msg_type)
        timestamp = self._get_timestamp()

        formatted = "\n".join([f"{color}{self.COLORS['bold']}{pprint(m)}" for m in msg])
        return (
            f"\n\n\n{emoji}  {timestamp}\n{color}{formatted}{self.COLORS['end']}\n\n\n"
        )

    @staticmethod
    def format_exception(exception: Exception) -> str:
        """Format an exception with timestamp and colors."""
        msg = f"\n[{exception.__class__.__name__}] {str(exception)}"
        msg += f"\n{traceback.format_exc()}"

        return msg

    def error(self, *msg: Any, exception: Optional[Exception] = None):
        """
        🚨 Log an error message and optionally an exception

        Args:
            msg: Message to log
            exception: Optional exception to include in log
        """
        error_msg = self.format_message(*msg, msg_type="error")
        if exception:
            error_msg += self.format_exception(exception)

        self.logger.error(error_msg)

    def warning(self, *msg: Any):
        """⚠️ Log a warning message."""
        self.logger.warning(self.format_message(*msg, msg_type="warning"))

    def info(self, *msg: Any):
        """ℹ️ Log an info message."""
        self.logger.info(self.format_message(*msg, msg_type="info"))

    def magic(self, *msg: Any):
        """🔮 Log a magical message."""
        self.logger.info(self.format_message(*msg, msg_type="magenta"))

    def water(self, *msg: Any):
        """🪼 Log a watery message."""
        self.logger.info(self.format_message(*msg, msg_type="cyan"))

    def white(self, *msg: Any):
        """🏳 Log a white message."""
        self.logger.info(self.format_message(*msg, msg_type="white"))

    def black(self, *msg: Any):
        """️🏴 Log a black message."""
        self.logger.info(self.format_message(*msg, msg_type="black"))

    def success(self, *msg: Any):
        """✅ Log a success message."""
        self.logger.info(self.format_message(*msg, msg_type="success"))

    @staticmethod
    def stdout(txt: str):
        """Print text to stdout without newline at the end."""
        sys.stdout.write(txt)
        sys.stdout.flush()

    def glitch(self, *msg: Any, intensity: float = 0.4):
        """🪞 Log a glitch message."""
        glitched_chars = [
            "█",
            "▓",
            "▒",
            "░",
            "▄",
            "▀",
            "▐",
            "▌",
            "▄",
            "|",
            "/",
            "\\",
            "#",
            "@",
            "&",
            "?",
            "!",
        ]
        colors = ["error", "success", "warning", "info", "magenta", "cyan"]
        for m in msg:
            m = pprint(m)
            for char in m:
                if random.random() < intensity:
                    self.stdout(
                        f"{self.get_color('white')}{random.choice(glitched_chars)}{self.COLORS['end']}"
                    )
                    time.sleep(0.05)
                color = self.get_color(random.choice(colors))
                self.stdout(f"{color}{char}{self.COLORS['end']}")
                time.sleep(0.075)

    @staticmethod
    def progress(
        iterable: Iterable, desc: str = "", total: Optional[int] = None
    ) -> tqdm:
        """
        Create a progress bar for an iteration

        Args:
            iterable: The iterable to track
            desc: Description of the progress
            total: Total number of items (optional)

        Returns:
            tqdm: Progress bar object
        """
        return tqdm(
            iterable,
            desc=desc,
            total=total,
            unit="img",
            ncols=80,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
        )


# Create a global logger instance
logger = Logger()
