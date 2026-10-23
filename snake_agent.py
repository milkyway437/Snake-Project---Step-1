import random
from collections import deque

class SnakeAgent:
    """عامل هوشمند Snake با جست‌وجوی مسیر BFS و بررسی ایمنی حرکت."""

    def __init__(self, grid_size=20):
        self.grid_size = grid_size
        self.directions = {
            'UP':    (-1, 0),
            'DOWN':  (1, 0),
            'LEFT':  (0, -1),
            'RIGHT': (0, 1),
        }
        self.opposite = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        self.last_action = None

    def choose_action(self, snake, food, direction):
        """
        انتخاب حرکت بر اساس:
        1. بررسی حرکت‌های امن (عدم برخورد با دیوار/بدن/حرکت معکوس)
        2. جست‌وجوی BFS به سمت غذا
        3. انتخاب حرکت با بیشترین فضای آزاد در صورت عدم دسترسی به غذا
        """
        head = snake[0]
        safe_moves = self._safe_moves(snake, direction)

        if not safe_moves:
            return direction  # هیچ حرکت امنی نیست؛ ادامه مسیر فعلی

        # ۱. تلاش برای یافتن مسیر به غذا با BFS
        path_move = self._bfs_to_food(snake, food)
        if path_move and path_move in safe_moves:
            self.last_action = path_move
            return path_move

        # ۲. اگر مسیر به غذا نبود، حرکتی با بیشترین فضای آزاد انتخاب کن
        best_move = max(safe_moves, key=lambda m: self._free_space(snake, m))
        self.last_action = best_move
        return best_move

    def _safe_moves(self, snake, direction):
        """حرکت‌هایی که به دیوار، بدن مار یا حرکت معکوس منتهی نمی‌شوند."""
        head = snake[0]
        body = set(snake[1:])
        safe = []
        for move, (dr, dc) in self.directions.items():
            if move == self.opposite.get(direction):
                continue
            nr, nc = head[0] + dr, head[1] + dc
            if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size and (nr, nc) not in body:
                safe.append(move)
        return safe

    def _bfs_to_food(self, snake, food):
        """کوتاه‌ترین مسیر از سر مار تا غذا با BFS؛ جهت اولین گام را برمی‌گرداند."""
        head = snake[0]
        body = set(snake[1:])
        queue = deque([(head, None)])
        visited = {head}
        while queue:
            (r, c), first_move = queue.popleft()
            if (r, c) == food:
                return first_move
            for move, (dr, dc) in self.directions.items():
                nr, nc = r + dr, c + dc
                if (nr, nc) in visited:
                    continue
                if not (0 <= nr < self.grid_size and 0 <= nc < self.grid_size):
                    continue
                if (nr, nc) in body:
                    continue
                visited.add((nr, nc))
                queue.append(((nr, nc), first_move or move))
        return None

    def _free_space(self, snake, move):
        """تعداد خانه‌های آزاد قابل دسترس از خانه بعدی (برای انتخاب حرکت ایمن)."""
        dr, dc = self.directions[move]
        start = (snake[0][0] + dr, snake[0][1] + dc)
        body = set(snake[1:])
        visited = {start}
        queue = deque([start])
        while queue:
            r, c = queue.popleft()
            for dr2, dc2 in self.directions.values():
                nr, nc = r + dr2, c + dc2
                if (nr, nc) in visited or (nr, nc) in body:
                    continue
                if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        return len(visited)