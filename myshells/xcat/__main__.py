import sys

from myshells.xcat.src.cli import parse_args
from myshells.xcat.src.core.config import settings
from myshells.xcat.src.core.logger import setup_logger
from myshells.xcat.src.output import configure_stdout, write_output
from myshells.xcat.src.resolver import resolve_ignore_patterns, resolve_root
from myshells.xcat.src.scanner import scan_path

logger = setup_logger("xcat", settings.LOG_PATH, settings.LOGGING_LEVEL)


def main() -> None:
    configure_stdout()

    args = parse_args()

    try:
        root = resolve_root(args.path)
        ignore_patterns = resolve_ignore_patterns(args, root)
        output = scan_path(root, ignore_patterns)

        write_output(output, args.output)

    except Exception as exc:
        logger.debug("xcat failed", exc_info=True)
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
