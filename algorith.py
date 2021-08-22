from aux_structure import Stack
from problem_definition import Action


class DFS:
    def __init__(self, initial_state, max_depth):
        self.stack = Stack()
        self.stack.append(initial_state)
        self.max_depth = max_depth
        self.end = False
        self.visited = []

    def start(self):
        final_state = None
        while len(self.stack) > 0 and not self.end:
            current_state = self.stack.pop()
            if current_state.g == self.max_depth or current_state in self.visited:
                continue
            #print(f"{current_state.g}  {len(current_state.sudoku)}")
            #print(f"{len(self.stack)}  {len(self.visited)}")
            self.visited.append(current_state)
            action = Action(current_state)
            actions = action.get_successors()
            for posible_state in actions:
                posible_state.g = current_state.g + 1
                if posible_state.complete:
                    self.end = True
                    final_state = posible_state
                elif posible_state not in self.visited:
                    self.stack.append(posible_state)
        return final_state
