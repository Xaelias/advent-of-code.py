import math
from collections import defaultdict
from typing import Any
from typing import Optional

import numpy as np

from aocl.base import AoCInput
from aocl.base import Base


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        normal = {}
        flip = {}
        conj = {}
        for line in input_data.as_list_of_str:
            k, v = line.split(" -> ")
            if k[0] == "%":
                flip[k[1:]] = v.split(", ")
            elif k[0] == "&":
                conj[k[1:]] = v.split(", ")
            else:
                normal[k] = v.split(", ")

        flip_state: dict[str, bool] = defaultdict(lambda: False)
        conj_state: dict[str, dict[str, bool]] = defaultdict(dict)

        for k, v in (normal | flip).items():  # type: ignore
            for dst in v:
                if dst in conj:
                    conj_state[dst][k] = False

        return normal, flip, conj, flip_state, conj_state

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        normal, flip, conj, flip_state, conj_state = parsed_input

        pulse_counts = {True: 0, False: 0}
        for i in range(1000):
            to_process: list[tuple[Optional[str], bool, str]] = [(None, False, "broadcaster")]
            while to_process:
                src, high, module = to_process[0]
                pulse_counts[high] += 1
                to_process = to_process[1:]
                if module in normal:
                    for dst in normal[module]:
                        to_process.append((module, high, dst))
                elif module in flip:
                    if high:
                        continue
                    flip_state[module] = not flip_state[module]
                    send = flip_state[module]
                    for dst in flip[module]:
                        to_process.append((module, send, dst))
                elif module in conj:
                    if src:
                        conj_state[module][src] = high
                    send = not all(conj_state[module].values())
                    for dst in conj[module]:
                        to_process.append((module, send, dst))

        return math.prod(list(pulse_counts.values()))

    @classmethod
    def parse_part_two(cls, input_data: AoCInput) -> Any:
        normal, flip, conj, flip_state, conj_state = cls.parse(input_data)
        reverse_index = defaultdict(list)
        for k, v in (normal | flip | conj).items():
            for dst in v:
                reverse_index[dst].append(k)
        return normal, flip, conj, flip_state, conj_state, reverse_index

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int:
        normal, flip, conj, flip_state, conj_state, reverse_index = parsed_input

        cycles = {}
        requirements = defaultdict(list)
        to_process = [(src, False) for src in reverse_index["rx"]]
        requirements[("rx", False)] = to_process[:]
        while to_process:
            head, *to_process = to_process
            dst, pulse = head
            for src in reverse_index[dst]:
                if src in conj:
                    requirements[(dst, pulse)].append((src, not pulse))
                    cycles[(src, not pulse)] = -1
                    to_process.append((src, not pulse))
                else:
                    requirements[(dst, pulse)].append((src, pulse))
                    cycles[(src, pulse)] = -1

        cycle_count = 0
        while "rx" not in cycles:
            cycle_count += 1
            signals_to_process: list[tuple[Optional[str], bool, str]] = [
                (None, False, "broadcaster")
            ]
            while signals_to_process:
                src, high, module = signals_to_process[0]
                signals_to_process = signals_to_process[1:]

                if (src, high) in cycles and cycles[(src, high)] == -1:
                    cycles[(src, high)] = cycle_count
                    changed = True
                    while changed:
                        changed = False
                        for k, v in requirements.items():
                            if cycles.get(k, -1) != -1:
                                continue
                            for e in v:
                                if cycles.get(e, -1) == -1:
                                    break
                            else:
                                changed = True
                                cycles[k] = np.multiply.reduce([cycles[c] for c in v])
                        if ("rx", False) in cycles:
                            return cycles[("rx", False)]

                if module in normal:
                    for dst in normal[module]:
                        signals_to_process.append((module, high, dst))
                elif module in flip:
                    if high:
                        continue
                    flip_state[module] = not flip_state[module]
                    send = flip_state[module]
                    for dst in flip[module]:
                        signals_to_process.append((module, send, dst))
                elif module in conj:
                    if src:
                        conj_state[module][src] = high
                    send = not all(conj_state[module].values())
                    for dst in conj[module]:
                        signals_to_process.append((module, send, dst))

        return cycles[("rx", False)]
