import argparse
import cProfile
import importlib
import json
import os
import re
import sys
from contextlib import suppress
from datetime import datetime
from datetime import timezone
from typing import Any

from ipdb import launch_ipdb_on_exception
from loguru import logger
from rich_argparse import ArgumentDefaultsRichHelpFormatter

with suppress(Exception):
    # 5  == TRACE
    # 10 == DEBUG
    # 20 == INFO
    # 25 == SUCCESS
    # 30 == WARNING
    # 40 == ERROR
    # 50 == CRITICAL
    logger.level("FAILED", no=25, color="<red>")

ArgumentDefaultsRichHelpFormatter.styles["argparse.default"] = "magenta italic"


def parse_key_value_pairs(kv_strings: list[str]) -> dict[str, Any]:
    kv_pairs = {}
    for kv in kv_strings:
        k, v = map(str.strip, kv.split("=", maxsplit=1))
        kv_pairs[k] = json.loads(v)
    return kv_pairs


def cli() -> None:
    parser = argparse.ArgumentParser(
        formatter_class=ArgumentDefaultsRichHelpFormatter,
        add_help=False,
    )

    cwd = os.getcwd()
    if match := re.search(r"(\d{4})/day/(\d{1,2})$", cwd):
        yyyy = match.group(1)
        dd = match.group(2)
    else:
        yyyy = datetime.now(timezone.utc).year
        dd = datetime.now(timezone.utc).day

    parser.add_argument("-h", "--help", action="help", help=argparse.SUPPRESS)

    main_args_parser = parser.add_argument_group("Main Arguments")
    main_args_parser.add_argument(
        "-y", "--year", type=int, help="yyyy for the day you're trying to run", default=yyyy
    )
    main_args_parser.add_argument(
        "-d", "--day", type=int, help=R"\[d]d for the day you're trying to run", default=dd
    )
    main_args_parser.add_argument(
        "--continue",
        dest="continue_on_failure",
        action="store_true",
        help="Continue even if something fails",
    )
    main_args_parser.add_argument(
        "-l",
        "--llevel",
        type=str.upper,  # noqa
        help="Set log level",
        metavar="LEVEL",
        choices=["TRACE", "DEBUG", "INFO", "SUCCESS", "FAILED", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
    )
    main_args_parser.add_argument(
        "--profile",
        action="store_true",
        help="Run day through cProfile"
    )

    parts_args_parser = parser.add_argument_group("Parts Selector")
    parts_args_parser.add_argument(
        "--all", action="store_true", help="Run everything (default behavior)"
    )
    parts_args_parser.add_argument(
        "--part-one-examples", action="store_true", help="Run part one's examples"
    )
    parts_args_parser.add_argument("--part-one", action="store_true", help="Run part one")
    parts_args_parser.add_argument(
        "--part-two-examples", action="store_true", help="Run part two's examples"
    )
    parts_args_parser.add_argument("--part-two", action="store_true", help="Run part two")

    override_parser = parser.add_argument_group("Override Parameters")
    override_parser.add_argument("--answer-a", help="Override answer for Part One")
    override_parser.add_argument("--answer-b", help="Override answer for Part Two")
    override_parser.add_argument(
        "--kwargs1",
        metavar="KEY=VALUE",
        nargs="+",
        help="Provide arguments to be passed to the process method for Part One.",
        default={},
    )
    override_parser.add_argument(
        "--kwargs2",
        metavar="KEY=VALUE",
        nargs="+",
        help="Provide arguments to be passed to the process method for Part Two.",
        default={},
    )

    args = parser.parse_args()
    logger.remove()
    logger.add(sys.stderr, level=args.llevel)

    mod_name = "{}.day.{}.solution".format(args.year, args.day)
    mod = importlib.import_module(mod_name)
    logger.trace(mod.__file__)

    parts_default = True
    if args.part_one or args.part_one_examples or args.part_two or args.part_two_examples:
        parts_default = False
    parts_to_run = {
        "solve_part_one": parts_default or args.part_one or args.all,
        "solve_part_one_examples": parts_default or args.part_one_examples or args.all,
        "solve_part_two": parts_default or args.part_two or args.all,
        "solve_part_two_examples": parts_default or args.part_two_examples or args.all,
    }
    with launch_ipdb_on_exception():
        solution = mod.Solution(
            year=args.year,
            day=args.day,
            part_one_answer=args.answer_a,
            part_two_answer=args.answer_b,
            kwargs_part_one=parse_key_value_pairs(args.kwargs1),
            kwargs_part_two=parse_key_value_pairs(args.kwargs2),
            continue_on_failure=args.continue_on_failure,
            **parts_to_run,
        )
        if args.profile:
            with cProfile.Profile() as pr:
                solution.solve_all()
            pr.print_stats(sort="tottime")
        else:
            solution.solve_all()


def mysolve(year: int, day: int, data: str) -> None:
    mod_name = "{}.day.{}.solution".format(year, day)
    mod = importlib.import_module(mod_name)
    return mod.Solution(year=year, day=day, data=data).get_answers()
