"""! Simple example app demonstrating the use of the Smart Sensor Actuator Hardware Abstraction Layer."""

import random
from ssa_core import SSACore


@SSACore.sync_executor
def random_event(ssa: SSACore) -> None:
    """
    Triggers a random event with a 50% probability.

    This asynchronous function performs a random check and, if the condition
    is met, emits an event named "random_event" with a corresponding message.
    """
    if random.randint(0, 1):
        ssa.emit_event("random_event", "Event triggered")


@SSACore.sync_executor
def random_property_with_event(ssa: SSACore) -> None:
    """
    Update the 'random_value' property and emit an event for high values.

    This function generates a random integer between 0 and 100 and sets the 'random_value'
    property asynchronously with a quality-of-service of 0. If the new value exceeds 70,
    it emits a 'random_value_event' with an appropriate message.
    """
    new_value: int = random.randint(0, 100)
    ssa.set_property("random_value", new_value, qos=0)
    if new_value > 70:
        ssa.emit_event("random_value_event", "Random value is greater than 70")


@SSACore.sync_executor
def print_action(_ssa: SSACore, msg: str) -> None:
    """
    Prints a formatted action message.

    This function outputs a message prefixed with a static identifier,
    indicating that an action has been triggered.
    The SSA instance parameter is provided by the framework and is not used within the function.

    Args:
        msg: The message payload to display.
    """
    print(f"Simple action triggered with message: {msg}")


@SSACore.App()
def main(ssa: SSACore):
    """
    Main entry point for the SSA application.

    Initializes the 'random_value' property to 0, schedules periodic tasks for emitting random events every 1000 ms and updating the random property every 2000 ms, and registers the print action callback.
    """
    ssa.create_property("random_value", 0)

    ssa.task_create("random_event", random_event, 1000)
    ssa.task_create("random_property", random_property_with_event, 2000)
    ssa.register_action_executor("print_action", print_action)
