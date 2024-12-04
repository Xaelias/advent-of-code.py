from typing import Any

from aocl.base import AoCInput
from aocl.base import Base

WorkflowName = str
Attr = str  # x, m, a or s
Op = Any  # int.__lt__ or int.__gt__
Action = str  # A or R
Part = dict[Attr, int]
Condition = tuple[Attr, Op, int, Action | WorkflowName]
Workflows = dict[WorkflowName, list[Condition]]


def process_part(workflows: Workflows, part: Part) -> bool:
    wid = "in"
    while True:
        conditions = workflows[wid]
        for condition in conditions:
            attr, op, value, action = condition
            if op is None and action == "A":
                return True
            elif op is None and action == "R":
                return False
            elif op is None:
                wid = action
                break
            elif op(part[attr], value):
                if action == "A":
                    return True
                if action == "R":
                    return False
                wid = action
                break


def reduce_range(ranges: dict[Attr, range]) -> int:
    total = 1
    for r in ranges.values():
        total *= r.stop - r.start
    return total


def run_range_through_workflow(workflows: Workflows, wid: Action | Attr, ranges: dict[Attr, range]):
    if wid == "A":
        return reduce_range(ranges)
    elif wid == "R":
        return 0
    return run_range_through_conditions(workflows, workflows[wid], ranges)


def run_range_through_conditions(
    workflows: Workflows, conditions: list[Condition], ranges: dict[Attr, range]
) -> int:
    for r in ranges.values():
        if r.stop < r.start:
            return 0

    attr, op, value, action = conditions[0]
    if op is None and action == "A":
        return reduce_range(ranges)
    elif op is None and action == "R":
        return 0
    elif op is None:
        return run_range_through_workflow(workflows, action, ranges)

    if op == int.__lt__:
        below_ranges = ranges | {
            attr: range(
                ranges[attr].start,
                min(ranges[attr].stop, value),
            )
        }
        above_ranges = ranges | {
            attr: range(
                max(ranges[attr].start, value),
                ranges[attr].stop,
            )
        }
        return run_range_through_workflow(
            workflows, action, below_ranges
        ) + run_range_through_conditions(workflows, conditions[1:], above_ranges)
    else:
        below_ranges = ranges | {
            attr: range(
                ranges[attr].start,
                min(ranges[attr].stop, value + 1),
            )
        }
        above_ranges = ranges | {
            attr: range(
                max(ranges[attr].start, value + 1),
                ranges[attr].stop,
            )
        }
        return run_range_through_conditions(
            workflows, conditions[1:], below_ranges
        ) + run_range_through_workflow(workflows, action, above_ranges)


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        workflows_raw, parts_raw = input_data.as_chunks

        workflows: Workflows = {}
        for workflow in workflows_raw:
            workflow_name = workflow.split("{", maxsplit=1)[0]
            workflows[workflow_name] = []
            conditions = workflow.split("{", maxsplit=1)[1].split("}", maxsplit=1)[0].split(",")

            for condition in conditions:
                if ":" in condition:
                    workflows[workflow_name].append(
                        (
                            condition[0],
                            int.__gt__ if ">" in condition else int.__lt__,
                            int(condition.split(":")[0][2:]),
                            condition.split(":")[1],
                        )
                    )
                else:
                    workflows[workflow_name].append((None, None, None, condition))  # type: ignore

        parts = []
        for part in parts_raw:
            part_list = part[1:-1].split(",")
            parts.append({part[0]: int(part[1]) for e in part_list if (part := e.split("="))})  # type: ignore
        return workflows, parts

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        workflows, parts = parsed_input
        total = 0
        for part in parts:
            if process_part(workflows, part):
                total += sum(list(part.values()))
        return total

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int:
        workflows, _ = parsed_input
        range_min = 1
        range_max = 4000 + 1

        return run_range_through_workflow(
            workflows,
            "in",
            {
                "x": range(range_min, range_max),
                "m": range(range_min, range_max),
                "a": range(range_min, range_max),
                "s": range(range_min, range_max),
            },
        )
