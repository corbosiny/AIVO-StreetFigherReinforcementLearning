from enum import Enum
import random

class Moves(Enum):
    """Enum of the set of possible moves the agent is allowed to perform"""
    Idle = 0
    Right = 1
    DownRight = 2
    Down = 3
    DownLeft = 4
    Left = 5
    UpLeft = 6
    Up = 7
    UpRight = 8
    LightPunch = 9
    MediumPunch = 10
    HeavyPunch = 11
    LightKick = 12
    MediumKick = 13
    HeavyKick = 14
    CrouchLightPunch = 15
    CrouchMediumPunch = 16
    CrouchHeavyPunch = 17
    CrouchLightKick = 18
    CrouchMediumKick = 19
    CrouchHeavyKick = 20
    LeftShoulderThrow = 21
    RightShoulderThrow = 22
    LeftSomersaultThrow = 23
    RightSomersaultThrow = 24
    Fireball = 25
    HurricaneKick = 26
    DragonUppercut = 27

    def getMoveInputs(moveName):
        """Takes in the enum moveName and returns the set of frame inputs to perform that move"""
        return MovesDict[moveName]
    
    def getRandomMove():
        """Returns the name and frame inputs of a randomly selected move"""
        moveName = random.choice(list(Moves))
        moveInputs = MovesDict[moveName]
        return moveName, moveInputs

    def isDirectionalMove(move):
        """Determines if the selected move's inputs are depend on the players direction"""
        if move == Moves.Fireball or move == Moves.HurricaneKick or move == Moves.DragonUppercut:
            return True

"""
    Dictionary mapping the move enum types to the set of frame inputs
    In the case of directionally based moves they contain multiple sets
    one for each possible input direction.
"""
MovesDict = {
    Moves.Idle : [0],

    # Movement/Directional Inputs
    Moves.Right : [6],
    Moves.DownRight : [8],
    Moves.Down : [2],
    Moves.DownLeft : [5],
    Moves.Left : [3],
    Moves.UpLeft : [4],
    Moves.Up : [1],
    Moves.UpRight : [7],

    # Basic attacks
    Moves.LightPunch : [26],
    Moves.MediumPunch : [21],
    Moves.HeavyPunch : [32],
    Moves.LightKick : [13],
    Moves.MediumKick : [9],
    Moves.HeavyKick : [17],

    # Crouch Attacks
    Moves.CrouchLightPunch : [2, 27],
    Moves.CrouchMediumPunch : [2, 22],
    Moves.CrouchHeavyPunch : [2, 33],
    Moves.CrouchLightKick : [2, 14],
    Moves.CrouchMediumKick : [2, 10],
    Moves.CrouchHeavyKick : [2, 18],

    # Throws
    Moves.LeftShoulderThrow : [34],
    Moves.RightShoulderThrow : [36],
    Moves.LeftSomersaultThrow : [19],
    Moves.RightSomersaultThrow : [20],

    # Special Moves
    Moves.Fireball : [[2, 8, 30], [2, 5, 28]],
    Moves.HurricaneKick : [[2, 5, 19 ], [2, 8, 20]],
    Moves.DragonUppercut : [[6, 2, 37], [3, 2, 35]]
}
    

if __name__ == "__main__":
    for move in Moves:
        print(MovesDict[move])
