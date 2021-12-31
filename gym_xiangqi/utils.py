from gym_xiangqi.constants import TOTAL_POS
from gym_xiangqi.position import Position
from gym_xiangqi.action import ConcreteAction


def move_to_action_space(piece_id, start, end):
    """
    The action space is a 1D flat array. We can convert piece id,
    start position and end position to a corresponding index value
    in the action space.

    Parameters:
        piece_id (int): a piece ID integer
        start (tuple(int)): (row, col) start coordinate
        end (tuple(int)): (row, col) end coordinate
    Return:
        Index within the self.possible_actions
    """
    piece_id_val = (piece_id - 1) * pow(TOTAL_POS, 2)
    start_val = (start[0] * 9 + start[1]) * TOTAL_POS
    end_val = end[0] * 9 + end[1]
    return piece_id_val + start_val + end_val


def action_space_to_move(action):
    """
    This is exact opposite of move_to_action_space() method.
    With index value, we can convert this back to piece id,
    start position and end position values.

    Parameters:
        action (int): index value within action space
    Return:
        piece ID, start coordinate, end coordinate
    """
    piece_id, r = divmod(action, pow(TOTAL_POS, 2))
    start_val, end_val = divmod(r, TOTAL_POS)
    start = [0, 0]
    end = [0, 0]
    start[0], start[1] = divmod(start_val, 9)
    end[0], end[1] = divmod(end_val, 9)
    return piece_id + 1, start, end

def action_space_to_action(action_index: int) -> ConcreteAction:
    piece_id, start, end = action_space_to_move(action_index)
    from_pos = Position(start[0], start[1])
    to_pos = Position(end[0], end[1])
    return ConcreteAction(piece_id, from_pos, to_pos)

def action_to_action_space(action: ConcreteAction) -> int:
    return move_to_action_space(piece_id=action.piece, start=(action.from_pos.row, action.from_pos.col), end=(action.to_pos.row, action.to_pos.col))

def is_ally(piece_id):
    """
    Determines if given input piece_id is ally or enemy piece
    This function CANNOT guarantee if the piece is an enemy piece

    Parameters:
        piece_id (int): a piece ID integer
    Return:
        True: given piece ID is an ally piece
        False: given piece ID is either an empty space or an enemy piece
    """
    return piece_id > 0
