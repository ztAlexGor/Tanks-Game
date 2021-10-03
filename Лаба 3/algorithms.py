import collections
from queue import PriorityQueue


class SA:
    visited = set()
    path = []
    history = {}
    algorithm = 1

    def nextAlgorithm():
        SA.algorithm += 1
        SA.algorithm %= 3
    

    def getAlgorithm():
        return SA.algorithm


    def getHighlights():
        return SA.path


    def DFS(x, y, finX, finY, map):

        SA.visited.add((x, y))

        if map.checkObstacle(x * 100, y * 100, 1, 1) != 0:
            return False

        if x == finX and y == finY:
            SA.path.append((x, y))
            return True

        # for tank in enemies:
        #     if (tank.x + 50) // 100 == x and (tank.y + 50) // 100 == y:
        #         if not (tank in SA.tanksFounded):
        #             SA.tanksFounded.append(tank)
        #             SA.highlights.append([])
        #             SA.highlights[len(SA.tanksFounded) - 1].append((x, y))
        #             return len(SA.tanksFounded) - 1
        #         else:
        #             return -1


        status = False

        if not ((x + 1, y) in SA.visited) and status == False:
            status = SA.DFS(x + 1, y, finX, finY, map)
        if not ((x - 1, y) in SA.visited) and status == False:
            status = SA.DFS(x - 1, y, finX, finY, map)
        if not ((x, y + 1) in SA.visited) and status == False:
            status = SA.DFS(x, y + 1, finX, finY, map)
        if not ((x, y - 1) in SA.visited) and status == False:
            status = SA.DFS(x, y - 1, finX, finY, map)


        if status == True:
            SA.path.append((x, y))

        return status


    def BFS(startX, startY, finX, finY, map):

        queue = collections.deque([(startX, startY)])

        SA.history[(startX, startY)] = (-1, -1)

        SA.visited.add((startX, startY))

        while queue:
            x, y = queue.popleft()
            
            if map.checkObstacle(x * 100, y * 100, 1, 1) != 0:
                continue
            
            u = False

            if x == finX and y == finY:
                u = True
                SA.path.append((x, y))
                if len(SA.path) != 0:
                    SA.backtracking()

            # for tank in enemies:
            #     if (tank.x + 50) // 100 == x and (tank.y + 50) // 100 == y:
            #         u = True
            #         if tank not in SA.tanksFounded:
            #             SA.tanksFounded.append(tank)
            #             SA.path.append([])
            #             SA.path[len(SA.tanksFounded) - 1].append((x, y))
            #             if len(SA.path[len(SA.tanksFounded) - 1]) != 0:
            #                 SA.backtracking()
            #             return
            if u:
                continue

            if (x + 1, y) not in SA.visited:
                SA.visited.add((x + 1, y))
                queue.append((x + 1, y))
                SA.history[(x + 1, y)] = (x, y)
            if (x - 1, y) not in SA.visited:
                SA.visited.add((x - 1, y))
                queue.append((x - 1, y))
                SA.history[(x - 1, y)] = (x, y)
            if (x, y + 1) not in SA.visited:
                SA.visited.add((x, y + 1))
                queue.append((x, y + 1))
                SA.history[(x, y + 1)] = (x, y)
            if (x, y - 1) not in SA.visited:
                SA.visited.add((x, y - 1))
                queue.append((x, y - 1))
                SA.history[(x, y - 1)] = (x, y)


    def UCS(startX, startY, finX, finY, map):

        queue = PriorityQueue()
        queue.put([0, (startX, startY)])

        
        SA.history[(startX, startY)] = (-1, -1)

        while not queue.empty():
            
            cost, pair = queue.get()
            x, y = pair

            if map.checkObstacle(x * 100, y * 100, 1, 1) != 0:
                SA.visited.add((x, y))
                continue

            if x == finX and y == finY:
                u = True
                SA.path.append((x, y))
                if len(SA.path) != 0:
                    SA.backtracking()
                    return
            # for tank in enemies:
            #     if (tank.x + 50) // 100 == x and (tank.y + 50) // 100 == y:
            #         if tank not in SA.tanksFounded:
            #             SA.tanksFounded.append(tank)
            #             SA.path.append([])
            #             SA.path[len(SA.tanksFounded) - 1].append((x, y))
            #             if len(SA.path[len(SA.tanksFounded) - 1]) != 0:
            #                 SA.backtracking()
            #             return
                    
            #         SA.visited.add((x, y))

            if (x, y) not in SA.visited:
                queue.put([cost + 1, (x + 1, y)])
                if SA.history.get((x + 1, y)) is None:
                    SA.history[(x + 1, y)] = (x, y)

                queue.put([cost + 1, (x - 1, y)])
                if SA.history.get((x - 1, y)) is None:
                    SA.history[(x - 1, y)] = (x, y)

                queue.put([cost + 1, (x, y + 1)])
                if SA.history.get((x, y + 1)) is None:
                    SA.history[(x, y + 1)] = (x, y)

                queue.put([cost + 1, (x, y - 1)])
                if SA.history.get((x, y - 1)) is None:
                    SA.history[(x, y - 1)] = (x, y)

            SA.visited.add((x, y))


    def aStar(startX, startY, finX, finY, map):
        queue = PriorityQueue()
        queue.put([SA.aStarCost((startX, startY), (finX, finY)), 0, (startX, startY)])

        
        SA.history[(startX, startY)] = (-1, -1)

        while not queue.empty():
            
            cost, way, pair = queue.get()
            x, y = pair

            if map.checkObstacle(x * 100, y * 100, 1, 1) != 0:
                SA.visited.add((x, y))
                continue

            if x == finX and y == finY:
                u = True
                SA.path.append((x, y))
                if len(SA.path) != 0:
                    SA.backtracking()
                    return

            if (x, y) not in SA.visited:
                queue.put([way + 1 + SA.aStarCost((x + 1, y), (finX, finY)), way + 1, (x + 1, y)])
                if SA.history.get((x + 1, y)) is None:
                    SA.history[(x + 1, y)] = (x, y)

                queue.put([way + 1 + SA.aStarCost((x - 1, y), (finX, finY)), way + 1, (x - 1, y)])
                if SA.history.get((x - 1, y)) is None:
                    SA.history[(x - 1, y)] = (x, y)

                queue.put([way + 1 + SA.aStarCost((x, y + 1), (finX, finY)), way + 1, (x, y + 1)])
                if SA.history.get((x, y + 1)) is None:
                    SA.history[(x, y + 1)] = (x, y)

                queue.put([way + 1 + SA.aStarCost((x, y - 1), (finX, finY)), way + 1, (x, y - 1)])
                if SA.history.get((x, y - 1)) is None:
                    SA.history[(x, y - 1)] = (x, y)

            SA.visited.add((x, y))


    def backtracking():

        pair = SA.path[0]

        while SA.history[pair] != (-1, -1):
            pair = SA.history[pair]
            SA.path.append(pair)


    def aStarCost(point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


    def search(enemies, map, tank1, tank2, algorithm):

        SA.path = []
        SA.history.clear()
        SA.visited.clear()

        if (algorithm == 0):
            SA.DFS((tank1.x + 50) // 100, (tank1.y + 50) // 100, (tank2.x + 50) // 100, (tank2.y + 50) // 100, map)
        elif (algorithm == 1):
            SA.BFS((tank1.x + 50) // 100, (tank1.y + 50) // 100, (tank2.x + 50) // 100, (tank2.y + 50) // 100, map)
        elif (algorithm == 2):
            SA.UCS((tank1.x + 50) // 100, (tank1.y + 50) // 100, (tank2.x + 50) // 100, (tank2.y + 50) // 100, map)
        elif (algorithm == 3):
            SA.aStar((tank1.x + 50) // 100, (tank1.y + 50) // 100, (tank2.x + 50) // 100, (tank2.y + 50) // 100, map)

        return SA.path

                