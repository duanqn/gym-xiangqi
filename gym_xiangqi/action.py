from gym_xiangqi.position import Position, PositionDiff

class AbsAction:
    def __init__(self, piece_id: int, from_pos: Position):
        self._piece_id = piece_id
        self._from = from_pos

    @property
    def piece(self) -> int:
        '''
        Positive: Ally pieces; Negative: Enemy pieces.
        '''
        return self._piece_id

    @property
    def from_pos(self) -> Position:
        return self._from

class ConcreteAction(AbsAction):
    def __init__(self, piece_id: int, from_pos: Position, to_pos: Position):
        super().__init__(piece_id, from_pos)
        self._to = to_pos

    @property
    def to_pos(self) -> Position:
        return self._to

class RayAction(AbsAction):
    def __init__(self, piece_id: int, from_pos: Position, single_move: PositionDiff, max_repeat: int):
        super().__init__(piece_id, from_pos)
        self._single_move = single_move
        self._max_repeat = max_repeat

    @property
    def max_repeat(self) -> int:
        return self._max_repeat

    @property
    def single_move(self) -> PositionDiff:
        return self._single_move

    def breakdown(self) -> list[ConcreteAction]:
        res = []
        for i in range(0, self._max_repeat):
            res.append(ConcreteAction(self._piece_id, self._from, self._from.applyDiff(self._single_move.repeat(i+1))))

        return res
