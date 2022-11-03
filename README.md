# CLI Games
This repo contains a bunch of Games that are played in the *Terminal* or *Command Prompt*.<br>
The code for these games is written in `python`.<br>
Only works on Unix-like systems as it needs [curses](https://en.wikipedia.org/wiki/Curses_(programming_library))

# Requirements
`python 3.x`
`curses`

# Snake
The well known classic game [Snake](https://en.wikipedia.org/wiki/Snake_(video_game_genre)).<br>

## How to run
You can run the game with the command `python3 snake_game.py`

## Controls
`arrow keys` navigate your snake through the field.<br>
`p` pause the game.<br>
`r` restart the game.<br>
`q` quit the game.<br>

## Game Objects
`#` these are part of your Snake.<br>
`&` these are generated obstacles you must avoid.<br>
`*` these are foods randomly placed on the field. They increase your *Snake* length by 1.<br>
`%` these are super foods. They increase your *Snake* length by 5.<br>

Scoring is equal to the size of your *Snake*.

# Maze Runner
A self made game trying out the [Wave Function Collapse Algorithm](https://github.com/mxgmn/WaveFunctionCollapse) to generate an endless maze.

## How to run
You can run the game with the command `python3 maze_runner.py`

## Controls
`arrow keys` navigate your character through the maze.<br>
`f` fire a laser, destroying enemies or walls on it's path.<br>
`p` pause the game.<br>
`r` restart the game.<br>
`q` quit the game.<br>

## Game Objects
`@` your character.<br>
`#` maze walls.<br>
`.` points to be gathered in the maze.<br>
`>` missiles flying through the maze, killing your character on collision.<br>
`%` ammo box refilling your laser gun.<br>

Scoring is equal to amount of points you gathered.

# Tetris (WIP)
The well known classic game [Tetris](https://en.wikipedia.org/wiki/Tetris).<br>

## How to run
You can run the game with the command `python3 tetris.py`

## Controls
`arrow up` rotate the piece.<br>
`arrow down` move the piece.<br>
`arrow left/right` move the piece to the left/right.<br>
`p` pause the game.<br>
`r` restart the game.<br>
`q` quit the game.<br>
