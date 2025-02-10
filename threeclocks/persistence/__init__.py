"""Package persistence.
Persists the game state in some files:

items.json:
  Persists changes to the items defined in each level.
  It only persists items from the levels that the player has visited,
  since levels not visited will not be changed.
  Note that when recovering the saved game, we look up in this file
  just the item ids that are present in the game levels and update
  the items state regarding their attributes on the file.

player.json:
  Persists the Player's state.

Notes:
  * We assume that the levels in the game are contiunous in a way that:
    * A level's id is a number. First level's id is: 1.
      * If a game has five levels, their ids should be: 1, 2, 3, 4, 5.
    * The levels in a game are stored in a sequence, starting with 0.
      * If a game has five levels, their position inside the sequence
        would be: 0, 1, 2, 3, 4.
"""
