from typing import List
from collections import deque


class _Square:
    def __init__(self, color: str, data: int = 0x00) -> None:
        """
        Represents a single square on a Rubik's Cube face.

        Args:
            color (str): The color of the square.
            data (int): Additional data associated with the square (default: 0x00).
        """
        self.color = color
        self.data = data

    def insertData(self, info: int) -> None:
        """Updates the square's data."""
        self.data = info

    def __repr__(self) -> str:
        """String representation of the square."""
        return f"({self.color}, {self.data})"


class _Face:
    def __init__(self, color: str) -> None:
        """
        Represents one face of the Rubik's Cube.

        Args:
            color (str): The color of the face.
        """
        self.color = color
        self.face: List[List[_Square]] = [[_Square(color=color) for _ in range(3)] for _ in range(3)]

    def insertToFace(self, x: int, y: int, data: int) -> None:
        """
        Inserts data into a specific square on the face.

        Args:
            x (int): Row index (0-2).
            y (int): Column index (0-2).
            data (int): Data to insert.
        """
        assert 0 <= x < 3 and 0 <= y < 3, f"X ({x}) and/or Y ({y}) positions should be between 0 and 2"
        self.face[x][y].insertData(data)

    def __repr__(self) -> str:
        """String representation of the face."""
        return "\n".join([" ".join([repr(self.face[r][c]) for c in range(3)]) for r in range(3)])


class Cube:
    def __init__(self, name: str) -> None:
        """
        Represents a Rubik's Cube.

        Args:
            name (str): Name of the cube instance.
        """
        self.name = name
        self.colors = ["yellow", "blue", "red", "green", "orange", "white"]
        self.cube: dict[str, _Face] = {
            color: _Face(color) for color in self.colors
        }

    def insertToFace(self, face: str, x: int, y: int, data: (int, str)) -> None:
        """
        Inserts data into a specific face of the cube.

        Args:
            face (str): The face color name.
            x (int): Row index (0-2).
            y (int): Column index (0-2).
            data (int): Data to insert.
        """
        face = face.lower()
        self.cube[face].insertToFace(x, y, data)

    def rotate(self, axis: str, index: int, direction: str) -> None:
        """
        Rotates a row or column of the cube.

        Args:
            axis (str): "row" or "column" to specify the rotation type.
            index (int): The row or column index (0-2).
            direction (str): Direction of rotation ("left", "right", "up", "down").
        """
        if 0 <= index <= 2:
            if axis == "row":
                faces = ["blue", "red", "green", "orange"]
                rowList = [self.cube[f].face[index] for f in faces]
                rotatedRows = rowList[1:] + rowList[:1] if direction == "left" else rowList[-1:] + rowList[:-1]
                for i, f in enumerate(faces):
                    self.cube[f].face[index] = rotatedRows[i]
                if index == 0:
                    self.cube["yellow"].face = self._rotateFaceCounterclockwise(
                        self.cube["yellow"].face) if direction == "left" else self._rotateFaceClockwise(
                        self.cube["yellow"].face)
                elif index == 2:
                    self.cube["white"].face = self._rotateFaceClockwise(
                        self.cube["white"].face) if direction == "left" else self._rotateFaceCounterclockwise(
                        self.cube["white"].face)

            elif axis == "column":
                faces = ["yellow", "blue", "white", "green"]
                # Collect the specified column from each face
                columnList = [[self.cube[f].face[row][index] for row in range(3)] for f in faces]
                # Flatten the list of columns for rotation
                columnList = [col for face_col in columnList for col in face_col]
                rotatedColumns = columnList[3:] + columnList[:3] if direction == "up" else columnList[-3:] + columnList[
                                                                                                             :-3]
                # Update the columns on the side faces with the rotated columns
                for face_idx, f in enumerate(faces):
                    for row_idx in range(3):
                        self.cube[f].face[row_idx][index] = rotatedColumns[face_idx * 3 + row_idx]
                if index == 0:
                    self.cube["orange"].face = self._rotateFaceCounterclockwise(
                        self.cube["orange"].face) if direction == "up" else self._rotateFaceClockwise(
                        self.cube["orange"].face)
                elif index == 2:
                    self.cube["red"].face = self._rotateFaceClockwise(
                        self.cube["red"].face) if direction == "up" else self._rotateFaceCounterclockwise(
                        self.cube["red"].face)

            else:
                raise ValueError("Invalid axis. Use 'row' or 'column'.")
        else:
            raise ValueError("Invalid index. Index should be between 0-2")

    def _rotateFaceClockwise(self, face: List[List[_Square]]) -> List[List[_Square]]:
        """Rotates a face 90 degrees clockwise."""
        return [[face[2 - c][r] for c in range(3)] for r in range(3)]

    def _rotateFaceCounterclockwise(self, face: List[List[_Square]]) -> List[List[_Square]]:
        """Rotates a face 90 degrees counterclockwise."""
        return [[face[c][2 - r] for c in range(3)] for r in range(3)]

    def __repr__(self) -> str:
        """String representation of the cube."""
        faces_repr = "\n".join([f"{str(self.cube[face])}" for face in self.cube])
        return f"{self.name}(\n{faces_repr}\n)"


def getColors() -> List[str]:
    """Returns a list of face colors."""
    return ["yellow", "blue", "red", "green", "orange", "white"]


def insertToCube(cube: Cube, data: (str, int, bytes)) -> None:
    """
    Inserts data into the cube's faces.

    Args:
        cube (Cube): The Cube object.
        data (str, int, bytes): A string of 54 characters representing the cube's state.
    """
    x, y = 0, 0
    for index, char in enumerate(data):
        face = getColors()[index // 9]
        cube.insertToFace(face, y, x, char)
        x += 1
        if x > 2:
            y += 1
            x = 0
        if y > 2:
            x, y = 0, 0


# Example Usage
if __name__ == "__main__":
    myCube = Cube("MyRubiksCube")
    cubeData = "yyyyyyyyybbbbbbbbrrrrrrrrggggggggoooooooowwwwwwwww"
    insertToCube(myCube, cubeData)
    print("Initial Cube State:")
    print(myCube)

    myCube.rotate("row", 0, "left")
    myCube.rotate("column", 2, "down")
