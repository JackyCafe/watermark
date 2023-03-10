class Point:
    x: int
    y: int

    def __init__(self,x:int, y:int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'x:{self.x}, y:{self.y}'        