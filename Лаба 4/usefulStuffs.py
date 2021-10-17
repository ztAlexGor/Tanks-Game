from enum import Enum

class Direction(Enum):
    NONE = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


def isIn(t, x, y):
    if (x >= t.x and x < t.x + t.width) and (y >= t.y and y < t.y + t.height):
        return True
    return False


def checkEntityCollision(entity1, entity2):
    if isIn(entity1, entity2.x, entity2.y) or isIn(entity1, entity2.x, entity2.y + entity2.height - 1):
        return True
    
    if isIn(entity1, entity2.x + entity2.width - 1, entity2.y) or isIn(entity1, entity2.x + entity2.width - 1, entity2.y + entity2.height - 1):
        return True
    return False


def checkShotPossibility(tank1, tank2, map):
    if abs(tank1.x - tank2.x) < 30:
        if tank1.y > tank2.y:
            x = tank1.x + (tank1.width - 12) // 2
            y = tank1.y + tank1.height // 2
            
            while y > tank2.y + tank2.height:
                y -= map.cellSize
                if map.checkObstacle(x, y, 12, 32) == 1:
                    return Direction.NONE
            return Direction.UP
        else:
            x = tank1.x + (tank1.width - 12) // 2
            y = tank1.y + tank1.height // 2
            
            while y < tank2.y:
                y += map.cellSize
                if map.checkObstacle(x, y, 12, 32) == 1:
                    return Direction.NONE
            return Direction.DOWN
    if abs(tank1.y - tank2.y) < 30:
        if tank1.x > tank2.x:
            y = tank1.y + (tank1.height - 12) // 2
            x = tank1.x + tank1.width // 2
            while x > tank2.x + tank2.width:
                x -= map.cellSize
                if map.checkObstacle(x, y, 32, 12) == 1:
                    return Direction.NONE
            return Direction.LEFT
        else:
            y = tank1.y + (tank1.height - 12) // 2
            x = tank1.x + tank1.width // 2
            while x < tank2.x:
                x += map.cellSize
                if map.checkObstacle(x, y, 32, 12) == 1:
                    return Direction.NONE
            return Direction.RIGHT
    return Direction.NONE