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
            res.append(ConcreteAction(self._piece_id, self._from,
                       self._from.applyDiff(self._single_move.repeat(i+1))))

        return res


class ActionTreeNode:
    def __init__(self, parent, action: ConcreteAction) -> None:
        self._parent = parent
        self._children = {}
        self._action = action
        self._result = None
        self.selected_child = None
        self._depth = 0 if parent is None else parent._depth + 1

        if parent is not None:
            self._alpha = parent._alpha
            self._beta = parent._beta
        else:
            self._alpha = None
            self._beta = None

    @property
    def parent(self):
        return self._parent

    @property
    def action(self):
        return self._action

    @property
    def alpha(self):
        return self._alpha

    @property
    def beta(self):
        return self._beta

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, result):
        self._result = result

    @property
    def depth(self):
        return self._depth

    def same_player_as_root(self) -> bool:
        return self._depth % 2 == 1

    def addChild(self, action: ConcreteAction):
        if action not in self._children:
            self._children[action] = ActionTreeNode(self, action)
        return self._children[action]

    def update_alpha(self, new_alpha):
        if self.parent is not None:
            if self.parent._alpha is None or self.parent._alpha < new_alpha:
                #print(f'Update alpha at depth {self.parent.depth} to {new_alpha}')
                self.parent._alpha = new_alpha

    def update_beta(self, new_beta):
        if self.parent is not None:
            if self.parent._beta is None or self.parent._beta > new_beta:
                #print(f'Update beta at depth {self.parent.depth} to {new_beta}')
                self.parent._beta = new_beta

    def finalizeResult(self) -> None:
        assert self._result is not None
        if self.same_player_as_root():
            self.update_alpha(new_alpha=self._result)
        else:
            self.update_beta(new_beta=self._result)
