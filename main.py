import os

_45_degs_char_up = "/"
_45_degs_char_down = "\\"
_90_degs_char = "|"
_0_degs_char = "-"
background_char = "."

def draw_line(x1, y1, x2, y2):
    """
    Draws a line from (x1, y1) to (x2, y2) using ASCII characters.
    """
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0:  # vertical line
        if dy > 0:
            return _90_degs_char * dy
        else:
            return _90_degs_char * (-dy)
    elif dy == 0:  # horizontal line
        if dx > 0:
            return _0_degs_char * dx
        else:
            return _0_degs_char * (-dx)
    else:
        # diagonal line
        if dx > 0 and dy > 0:
            return _45_degs_char_up * min(dx, dy)
        elif dx < 0 and dy < 0:
            return _45_degs_char_down * min(-dx, -dy)
        elif dx > 0 and dy < 0:
            return _45_degs_char_down * min(dx, -dy)
        elif dx < 0 and dy > 0:
            return _45_degs_char_up * min(-dx, dy)
        else:
            return _0_degs_char * min(abs(dx), abs(dy))
        
def gen_grid(width, height):
    """
    Draws a grid of the specified width and height using ASCII characters.
    """
    grid = []
    for _ in range(height):
        row = []
        for _ in range(width):
            row.append(background_char)
        grid.append(row)

    return grid

def print_grid(grid):
    """
    Prints the grid to the console.
    """
    for row in grid:
        print("".join(row))

def clear_grid(grid):
    """
    Clears the grid by filling it with background characters.
    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j] = background_char
    return grid

def clear_console():
    """
    Clears the console screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def open_file(filename):
    """
    Opens a file and returns its content.
    """
    with open(filename, 'r') as file:
        content = file.read()
    return content

def decode_line(line):
    """
    A line in the file is in the format:
    x1,y1,x2,y2
    where (x1, y1) and (x2, y2) are the coordinates of the line.
    The line also have a prefix of:
    lift - no args, lifts the pen
    down - no args, puts the pen down
    move - args of the coordinates to move from and to, moves the pen without drawing
    draw - args of the coordinates to draw from and to, draws a line
    turn - args of the angle to turn in ("left90", "right90", "frontleft45", "frontright45", "backleft45", "backright45", "180"), turns the pen
    repetition - args of the number of repetitions, repeats the next block of code
    end - no args, ends the repetition
    """
    line = line.strip()
    if line.startswith("lift"):
        return "lift", []
    elif line.startswith("down"):
        return "down", []
    elif line.startswith("move"):
        args = line.split()[1:]
        return "move", [int(arg) for arg in args]
    elif line.startswith("draw"):
        args = line.split()[1:]
        return "draw", [int(arg) for arg in args]
    elif line.startswith("turn"):
        args = line.split()[1:]
        return "turn", args
    elif line.startswith("repetition"):
        args = line.split()[1:]
        return "repetition", [int(arg) for arg in args]
    elif line.startswith("end"):
        return "end", []
    else:
        raise ValueError(f"Unknown command: {line}")

def execute_commands_from_file(filename, grid_width, grid_height):
    """
    Executes a series of drawing commands from a file and updates a grid accordingly.

    The function reads a file line by line, decodes each line into a command and its arguments,
    and performs the corresponding action on a grid. The commands can include lifting or 
    lowering the pen, moving to a new position, drawing lines, turning, and handling repetitions.

    Args:
        filename (str): The path to the file containing the commands.
        grid_width (int): The width of the grid to be created.
        grid_height (int): The height of the grid to be created.

    Raises:
        ValueError: If a line in the file cannot be decoded into a valid command.

    Notes:
        - The grid is initialized as a 2D array and updated based on the commands.
        - The "draw" command updates the grid with lines if the pen is down.
        - Placeholder logic is included for "turn", "repetition", and "end" commands.
        - The function prints the final state of the grid after processing all commands.
    
    Reads a file line by line, decodes each line using decode_line, and executes the commands.
    """
    grid = gen_grid(grid_width, grid_height)  # Create a grid
    pen_down = False  # Track whether the pen is down
    current_position = (0, 0)  # Start at the top-left corner of the grid

    with open(filename, 'r') as file:
        for line in file:
            if line.strip():  # Skip empty lines
                try:
                    command, args = decode_line(line)

                    if command == "lift":
                        pen_down = False  # Lift the pen
                    elif command == "down":
                        pen_down = True  # Put the pen down
                    elif command == "move":
                        # Move the pen to the new position without drawing
                        current_position = tuple(args[:2])
                    elif command == "draw":
                        # Draw a line if the pen is down
                        if pen_down:
                            x1, y1, x2, y2 = args
                            line = draw_line(x1, y1, x2, y2)
                            # Update the grid with the drawn line
                            for i, char in enumerate(line):
                                if x1 == x2:  # Vertical line
                                    grid[y1 + i][x1] = char
                                elif y1 == y2:  # Horizontal line
                                    grid[y1][x1 + i] = char
                                else:  # Diagonal line
                                    grid[y1 + i][x1 + i] = char
                        current_position = tuple(args[2:])
                    elif command == "turn":
                        # Handle turning logic (e.g., update direction)
                        pass  # Placeholder for turning logic
                    elif command == "repetition":
                        # Handle repetition logic (e.g., loop over a block of commands)
                        pass  # Placeholder for repetition logic
                    elif command == "end":
                        # End a repetition block
                        pass  # Placeholder for ending repetition logic

                except ValueError as e:
                    print(f"Error decoding line: {line.strip()} - {e}")

    print_grid(grid)  # Display the final grid

def main():
    clear_console()  # Clear the console
    filename = input("> ")  # Replace with your file name
    grid_width = input("> ")  # Set the desired grid width
    grid_height = input("> ")  # Set the desired grid height

    execute_commands_from_file(filename, grid_width, grid_height)  # Execute commands from file