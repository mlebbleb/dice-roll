# MIT License
#
# Copyright (c) 2024 Kallen Murphy
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import typer
import typing_extensions as tpe
import random
import rich
import dataclasses as dc
import enum

class RollOperation(enum.Enum):
    ADD = 0
    SUB = 1

    INDV_ADD = 2
    INDV_SUB = 3
    NO_OPERATION = 4


@dc.dataclass
class DiceRoll:
    """Class For describing a dice roll"""
    count: int
    die_type: int
    operation: RollOperation = RollOperation.NO_OPERATION
    operand: int = 0

def print_error(msg: str):
    """Print an error message inside of a red panel"""
    rich.print("[dim white]Try [blue]'roll.py --help' [white]for help.")
    rich.print(rich.panel.Panel(f"[white]{msg}", title = "Error", style = "red", title_align="left"))

def print_output(title: str,msg: str):
    """Print a message in a panel titled with the title passed in"""
    rich.print(rich.panel.Panel(f"[bright]{msg}", title = title, style = "dim white", title_align="left"))

def get_count(dice: str):
    """Exctracts the number of dice to roll from the dice string"""
    split = dice.split('d')
    if not split[0].isnumeric() or len(split) != 2:
        raise ValueError()
    return (int(split[0]), split[1])

def get_die_type(dice: str):
    """Extracts the die_type from the provided string"""
    count = 0

    i = 0
    while i < len(dice) and dice[i].isnumeric():
        count = count * 10 + int(dice[i])
        i = i + 1
    
    if i == 0:
        raise ValueError()
    
    return (count, dice[i:])
    
def get_operation(dice: str):
    """Extracts the roll operation from the dice string"""
    if len(dice) == 0:
        return (RollOperation.NO_OPERATION, "")
    
    if dice[0] == '+':
        return (RollOperation.ADD, dice[1:])
    elif dice[0] == '-':
        return (RollOperation.SUB, dice[1:])
    elif dice[0] == '.':
        if len(dice) == 1:
            raise ValueError()
        elif dice[1] == '+':
            return (RollOperation.INDV_ADD, dice[2:])
        elif dice[1] == '-':
            return (RollOperation.INDV_SUB, dice[2:])
    
    raise ValueError()

def get_operand(dice: str) -> int:
    """Gets the operand from the dice string"""
    if len(dice) == 0:
        return 0
    
    if not dice.isnumeric():
        raise ValueError()
    
    return int(dice)
    
    

def process_dice(dice: str) -> DiceRoll:
    """Parses the dice input string"""
    try:
        (count, dice) = get_count(dice)
        (die_type, dice) = get_die_type(dice)
        (op, dice) = get_operation(dice)
        operand = get_operand(dice)
    except:
        return None
    
    return DiceRoll(count=count, die_type=die_type, operation=op, operand=operand)

def roll(num: int, die_type: int, operation = lambda x: x) -> int:
    """Executes the a die roll with a given operation"""
    return [operation(random.randint(1, die_type)) for _ in range(num)]
    
def roll_main(
    dice: tpe.Annotated[
        str, typer.Argument(
            help="The dice to roll\n\n"\
                +"    Usage: <COUNT>d<DIE TYPE>[<OPERATION><OPERAND>]\n\n"\
                +"    COUNT, DIE TYPE: Positive integer\n\n"\
                +"    OPERATION: + (add), - (subtract), .+ (add to individual), .- (subtract individual)\n\n"\
                +"    OPERAND: Positive integer")], 
    use_max: tpe.Annotated[bool, typer.Option("--max", help = "Use maximum value rolled")] = False,
    use_min: tpe.Annotated[bool, typer.Option("--min", help = "Use minimum value rolled")] = False
):
    dice_roll = process_dice(dice)
    
    if dice_roll is None:
        print_error("Invalid format for argument 'Dice'")
        return
    
    if dice_roll.count <= 0:
        print_error("The number of dice rolled must be positive")

    if dice_roll.operation == RollOperation.INDV_ADD:
        dice_roll_result = roll(dice_roll.count, dice_roll.die_type, lambda x: x + dice_roll.operand)
    elif dice_roll.operation == RollOperation.INDV_SUB:
        dice_roll_result = roll(dice_roll.count, dice_roll.die_type, lambda x: x - dice_roll.operand)
    else:
        dice_roll_result = roll(dice_roll.count, dice_roll.die_type)

    if use_max:
        result = max(dice_roll_result)
    elif use_min:
        result = min(dice_roll_result)
    else:
        result = sum(dice_roll_result)

    if dice_roll.operation == RollOperation.ADD:
        result = result + dice_roll.operand
    elif dice_roll.operation == RollOperation.SUB:
        result = result - dice_roll.operand
    
    print_output("Roll", f"{dice}: {dice_roll_result} -> {result}")

def main():
    typer.run(roll_main)

if __name__ == "__main__":
    main()