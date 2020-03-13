import random

DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "RIGHT": (1, 0),
    "LEFT": (-1, 0)
}


class SnakBase:
    def __init__(self, width, height):
        self.player = None
        self.direction = None
        self.width = width
        self.height = height
        self.fruit = None
        self.game_over = False
        self.INITIAL_LENGTH = None
        self._eat_locations = []
        self._has_updated = False
        self.reset()

    def reset(self):
        player_head = (int(self.width / 4), int(self.height / 3))
        self.player = [player_head, (player_head[0] - 1, player_head[1])]
        self.direction = (0, -1)
        self.fruit = (0, 0)
        self.spawn_fruit()
        self._eat_locations = []
        self.game_over = False
        self.INITIAL_LENGTH = len(self.player)

    @staticmethod
    def _is_horizontal(direction):
        return abs(direction[0]) == 1 and abs(direction[1]) == 0

    @staticmethod
    def _is_vertical(direction):
        return not SnakBase._is_horizontal(direction)

    @property
    def score(self):
        return len(self.player) - self.INITIAL_LENGTH

    @property
    def _head(self):
        return self.player[0]

    def _get_new_head(self):
        old_head = self.player[0]
        x = old_head[0] + self.direction[0]
        y = old_head[1] + self.direction[1]
        if x < 0 or y < 0:
            if x < 0:
                x = self.width - 1
            if y < 0:
                y = self.height - 1
        else:
            x %= self.width
            y %= self.height
        return x, y

    def update(self):
        self._has_updated = True
        if self.player[-1] in self._eat_locations:
            self._eat_locations.remove(self.player[-1])
        new_head = self._get_new_head()
        if new_head in self.player:
            self.game_over = True
        self.player.insert(0, new_head)
        if new_head == self.fruit:
            self._eat_locations.append(self.fruit)
            self.player.insert(0, new_head)
            self.spawn_fruit()
        self.player.pop()

    def spawn_fruit(self):
        loc = self.player[0]
        while loc in self.player:
            loc = (random.randint(1, self.width - 1), random.randint(1, self.height - 1))
        else:
            self.fruit = loc

    def update_direction(self, direction: tuple):
        if not self._has_updated:
            # At least one update needs to happen before a new move can be made
            return
        if not self._is_horizontal(direction) and not self._is_vertical(direction):
            raise AttributeError('Invalid direction')

        # Direction can only be updated when these conditions are false
        if self._is_horizontal(direction) and self._is_horizontal(self.direction):
            return
        if self._is_vertical(direction) and self._is_vertical(self.direction):
            return

        self.direction = direction
        self._has_updated = False  # Require to do at least one update

    def __str__(self):
        res = '  '
        for i in range(self.width): res += '_ '
        res += '\n'
        for y in range(self.height):
            for x in range(self.width):
                if x == 0:
                    res += '| '
                if (x, y) in self.player:
                    if (x, y) in self._eat_locations:
                        res += 'X '
                    else:
                        res += 'x '
                elif (x, y) == self.fruit:
                    res += 'F '
                else:
                    res += '0 '
                if x == self.width - 1:
                    res += '| '
            res += '\n'
        res += '  '
        for i in range(self.width): res += '_ '
        res += '\n'
        return res

    def display(self, *args, **kwargs):
        print(self)


class SimpleLinkedList():
    def __init__(self, content: list):
        self._current = -1
        self._content = content

    def next(self):
        self._current += 1
        if (len(self._content) - 1) > self._current < 0:
            raise IndexError('list index out of range')
        self._current %= len(self._content)
        return self._content[self._current]


if __name__ == '__main__':
    import os
    from time import sleep

    # os.system('cls')
    b = SnakBase(10, 10)
    b.fruit = (b._head[0] + 4, b._head[1])

    directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    l = SimpleLinkedList(directions)

    print(str(b))
    b.display()
    exit(0)
    sleep(0.5)
    for i in range(1, 101):
        if i % 10 == 0:
            # b.update_direction(l.next())
            pass
        os.system('cls')
        b.update()
        b.display()
        sleep(0.5)
