import sys

from myshells.xcat.src.cli import parse_args
from myshells.xcat.src.context import build_context
from myshells.xcat.src.core.config import settings
from myshells.xcat.src.core.logger import setup_logger
from myshells.xcat.src.output import configure_stdout, write_output
from myshells.xcat.src.resolver import (
    resolve_display_root,
    resolve_excluded_paths,
    resolve_roots,
)

logger = setup_logger("xcat", settings.LOGGING_LEVEL)


def main() -> None:
    configure_stdout()

    args = parse_args()

    try:
        roots = resolve_roots(args.paths)
        excluded_paths = resolve_excluded_paths(args.output)
        display_root = resolve_display_root(roots)

        output = build_context(roots, args, excluded_paths, display_root)

        write_output(output, args.output, args.force)

    except Exception as exc:
        logger.debug("xcat failed", exc_info=True)
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
