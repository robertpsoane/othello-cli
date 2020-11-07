# Othello

Text based Othello game with AI

## 2 Player Mode
- Two player mode allows two players on same computer to play

## Play vs Computer
- Computer uses minimax algorithm to play the game.
- Currently scored simply based on number of available moves - needs changing

```
def scoreBoard(board, player, opponent):

    player_score = len(generateMoveList(board, player, opponent))
    
    opponent_score = len(generateMoveList(board, opponent, player))
    
    return player_score -  opponent_score
```
