import collections
from queue import PriorityQueue


class SA:
    marked = []
    highlights = [[],[],[]]
    tanksFounded = []
    algorithm = 1

    def nextAlgorithm():
        SA.algorithm += 1
        SA.algorithm %= 3
    

    def getAlgorithm():
        return SA.algorithm


    def getHighlights():
        return SA.highlights


    def DFS(x, y, enemies, map):

        SA.marked.append((x, y))

        if map.checkObstacle(x * 100, y * 100, 1, 1) != 0:
            return -1

        for tank in enemies:
            if (tank.x + 50) // 100 == x and (tank.y + 50) // 100 == y:
                if not (tank in SA.tanksFounded):
                    SA.tanksFounded.append(tank)
                    SA.highlights[len(SA.tanksFounded) - 1].append((x, y))
                    return len(SA.tanksFounded) - 1
                else:
                    return -1


        status = -1

        if not ((x + 1, y) in SA.marked) and status == -1:
            status = SA.DFS(x + 1, y, enemies, map)
        if not ((x - 1, y) in SA.marked) and status == -1:
            status = SA.DFS(x - 1, y, enemies, map)
        if not ((x, y + 1) in SA.marked) and status == -1:
            status = SA.DFS(x, y + 1, enemies, map)
        if not ((x, y - 1) in SA.marked) and status == -1:
            status = SA.DFS(x, y - 1, enemies, map)


        if status != -1:
            SA.highlights[status].append((x, y))
            return status
        return -1


    def BFS(startX, startY, enemies, map): #tank as an obstacle

        queue = collections.deque([(startX, startY)])
        visited = set()
        history = {(startX, startY) : (-1, -1)}

        visited.add((startX, startY))

        while queue:
            x, y = queue.popleft()
            
            if map.checkObstacle(x * 100, y * 100, 1, 1) != 0:
                continue

            for tank in enemies:
                if (tank.x + 50) // 100 == x and (tank.y + 50) // 100 == y:
                    if tank not in SA.tanksFounded:
                        SA.tanksFounded.append(tank)
                        SA.highlights[len(SA.tanksFounded) - 1].append((x, y))
                        if len(SA.highlights[len(SA.tanksFounded) - 1]) != 0:
                            SA.backtracking(history)
                        return

            if (x + 1, y) not in visited:
                visited.add((x + 1, y))
                queue.append((x + 1, y))
                history[(x + 1, y)] = (x, y)
            if (x - 1, y) not in visited:
                visited.add((x - 1, y))
                queue.append((x - 1, y))
                history[(x - 1, y)] = (x, y)
            if (x, y + 1) not in visited:
                visited.add((x, y + 1))
                queue.append((x, y + 1))
                history[(x, y + 1)] = (x, y)
            if (x, y - 1) not in visited:
                visited.add((x, y - 1))
                queue.append((x, y - 1))
                history[(x, y - 1)] = (x, y)


    def UCS(startX, startY, enemies, map):

        queue = PriorityQueue()
        queue.put([0, (startX, startY)])

        visited = set()
        history = {(startX, startY) : (-1, -1)}

        while not queue.empty():
            
            cost, pair = queue.get()
            x, y = pair

            if map.checkObstacle(x * 100, y * 100, 1, 1) != 0:
                visited.add((x, y))
                continue

            for tank in enemies:
                if (tank.x + 50) // 100 == x and (tank.y + 50) // 100 == y:
                    if tank not in SA.tanksFounded:
                        SA.tanksFounded.append(tank)
                        SA.highlights[len(SA.tanksFounded) - 1].append((x, y))
                        if len(SA.highlights[len(SA.tanksFounded) - 1]) != 0:
                            SA.backtracking(history)
                        return
                    
                    visited.add((x, y))

            if (x, y) not in visited:
                queue.put([cost + 1, (x + 1, y)])
                if history.get((x + 1, y)) is None:
                    history[(x + 1, y)] = (x, y)

                queue.put([cost + 1, (x - 1, y)])
                if history.get((x - 1, y)) is None:
                    history[(x - 1, y)] = (x, y)

                queue.put([cost + 1, (x, y + 1)])
                if history.get((x, y + 1)) is None:
                    history[(x, y + 1)] = (x, y)

                queue.put([cost + 1, (x, y - 1)])
                if history.get((x, y - 1)) is None:
                    history[(x, y - 1)] = (x, y)

            visited.add((x, y))


    def backtracking(history):

        pair = SA.highlights[len(SA.tanksFounded) - 1][0]

        while history[pair] != (-1, -1):
            pair = history[pair]
            SA.highlights[len(SA.tanksFounded) - 1].append(pair)


    def search(enemies, map, player):

        SA.highlights = [[],[],[]]
        SA.tanksFounded = []

        for i in range (len(enemies)):
            SA.marked.clear()

            if (SA.algorithm == 0):
                SA.DFS((player.x + 50) // 100, (player.y + 50) // 100, enemies, map)
            elif (SA.algorithm == 1):
                SA.BFS((player.x + 50) // 100, (player.y + 50) // 100, enemies, map)
            elif (SA.algorithm == 2):
                SA.UCS((player.x + 50) // 100, (player.y + 50) // 100, enemies, map)
        