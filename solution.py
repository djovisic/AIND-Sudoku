assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]
    pass

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
diag_down = {}
diag_up = {}

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
   
    no_more_twins = False
    # We have to iterate through all units until there are no more twins to be found. The way we do that is to compare the board before
    # and after the naked twins detection. If the board is the same then no new twins have been found. We have to do it in a while loop
    # because we might uncover new twins when possible values are removed from peers
    while not no_more_twins:
        board_before = values        
        for unit in unitlist:
            # we select all the boxes which have length of their digits 2
            twins = [box for box in unit if len(values[box])==2]
            # if we have exact two matches (not triplets or more) and the values are the same then we have a naked twin
            if len(twins)==2 and values[twins[0]] == values[twins[1]]:
                # for each box in the unit which is not one of the two naked twins remove the possible values
                for box in unit:
                    if values[box] != values[twins[0]]:
                        assign_value(values,box,values[box].replace(values[twins[0]][0],'').replace(values[twins[0]][1],''))             
        board_after = values
        # if boards before and after naked twin detection are the same then there are no more twins thus we end the while loop
        if board_before == board_after:
            no_more_twins = True
    return values



def diagonal(values):
    #this function creates two diagonals needed for solving the diagonal sudoku    
    for row,column in zip(rows, cols):
            diag_down[row+column] = values[row+column]
    for row,column in zip(rows, cols[::-1]):
            diag_up[row+column] = values[row+column]
    pass
    

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))    
    pass

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print    
    pass

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:        
        digit = values[box]
        # if a single digit appears in a diagonal then we must eliminate that possibility from all the peers of the respecting diagonal
        if box in diag_up:
            for diag_up_peer in diag_up:
                if len(values[diag_up_peer])>1:
                    values = assign_value(values,diag_up_peer,values[diag_up_peer].replace(digit,''))
        if box in diag_down:
            for diag_peer_down in diag_down:
                if len(values[diag_peer_down])>1:
                    values = assign_value(values,diag_peer_down,values[diag_peer_down].replace(digit,''))                 
        for peer in peers[box]:
            values= assign_value(values,peer,values[peer].replace(digit,''))        

    return values    
    pass

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values  
    pass

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    pass

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    pass

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    #print("##############################################")
 
    diagonal(values)   
    return search(values)
    
    

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        #visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
