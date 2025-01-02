import base64
from lib.rubiks.rCube import Cube, insertToCube, getColors

DELIMITER = 54

if __name__ == "__main__":
    # with open("sad.jpg", "rb") as file:
    #     tempString = base64.b64encode(file.read())

    # tempString = (range(1, 55))
    tempString = "AAAAAAAAABBBBBBBBBCCCCCCCCCDDDDDDDDDEEEEEEEEEFFFFFFFFF"

    colors = getColors()
    for j in range(1, len(tempString), DELIMITER):
        tc = Cube(name=f"Cube{j // 53}")
        insertToCube(tc, tempString[j - 1:j + DELIMITER - 1])
        tc.rotate("column", 0, "up")
        print(tc)
