from __future__ import annotations

import queue
from collections import Counter
from dataclasses import dataclass, field

with open("inputs/d20input.txt") as f:
    lineFiles = f.readlines()


@dataclass
class FlipFlop:
    name: str
    state: bool = False
    output_modules: list[ModuleClasses] = field(default_factory=list)

    def send_pulse(self, pulse: bool, sender: ModuleClasses | None):
        if not pulse:
            self.state = not self.state
            if self.state:
                return [(module, True, self) for module in self.output_modules]
            else:
                return [(module, False, self) for module in self.output_modules]
        return None


@dataclass
class Conjunction:
    name: str
    # False = Low  True = high
    memory: dict[str, bool] = field(default_factory=dict)
    output_modules: list[ModuleClasses] = field(default_factory=list)

    def send_pulse(self, pulse: bool, sender: ModuleClasses | None):
        assert sender
        self.memory[sender.name] = pulse
        if all([i for i in self.memory.values()]):
            return [(module, False, self) for module in self.output_modules]
        else:
            return [(module, True, self) for module in self.output_modules]


@dataclass
class Sink:
    name: str
    output_modules: list[ModuleClasses] = field(default_factory=list)

    def send_pulse(self, pulse: bool, sender: ModuleClasses | None):
        return None


@dataclass
class Broadcaster:
    name: str
    output_modules: list[ModuleClasses] = field(default_factory=list)

    def send_pulse(self, pulse: bool, sender: ModuleClasses | None):
        return [(module, pulse, self) for module in self.output_modules]


ModuleClasses = FlipFlop | Conjunction | Broadcaster | Sink

all_modules = [
    (
        line.replace(" ", "").split("->")[0],
        line.replace(" ", "").replace("\n", "").split("->")[1].split(","),
    )
    for line in lineFiles
]

module_dict: dict[str, ModuleClasses] = {}
module_outputs: dict[str, list[str]] = {}
for module in all_modules:
    match module[0][0]:
        case "%":
            module_dict[module[0][1:]] = FlipFlop(name=module[0][1:])
            module_outputs[module[0][1:]] = module[1]
        case "&":
            module_dict[module[0][1:]] = Conjunction(name=module[0][1:])
            module_outputs[module[0][1:]] = module[1]
        case "b":
            module_dict["broadcaster"] = Broadcaster(name="broadcaster")
            module_outputs["broadcaster"] = module[1]


for key, val in module_outputs.items():
    for v in val:
        if module_dict.get(v, 0) == 0:
            module_dict[v] = Sink(v)
    outputs = [module_dict[v] for v in val]
    conjunction_outputs = [
        module for module in outputs if isinstance(module, Conjunction)
    ]
    module_dict[key].output_modules = outputs
    for conjunction in conjunction_outputs:
        conjunction.memory[key] = False


def button_click(module_dict: dict[str, ModuleClasses]):
    signal_queue: queue.Queue[
        tuple[ModuleClasses, bool, ModuleClasses | None]
    ] = queue.Queue()
    signal_queue.put((module_dict["broadcaster"], False, None))
    pulse_counter: Counter = Counter()
    while not signal_queue.empty():
        current_pulse = signal_queue.get()
        pulse_counter[current_pulse[1]] += 1
        next_pulse = current_pulse[0].send_pulse(current_pulse[1], current_pulse[2])
        if next_pulse:
            for individual_pulse in next_pulse:
                signal_queue.put(individual_pulse)

    return pulse_counter


res: Counter = Counter()
for i in range(1000):
    res.update(button_click(module_dict))

print(f"Result of Part 1 -> {res}\n{res[True]*res[False]}")
