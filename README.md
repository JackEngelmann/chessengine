# Chess Mini-Project

## Idea

- app to play chess against a self-made chess AI
- experiment with different approaches to chess AI
  - reinforcement learning model
  - min-max algorithm

## Idea Technical Approach

- web app
- react front end
- python backend

## Plan API

The API will be a simple REST API for the start.

objects:

- game
- figure

### PUT /game

- create game, creates all figures

### GET /game/:id

- get current state of game
  - whose turn is it?
  - check?
  - checkmate?

### GET /game/:id/figures

- get all figures
- figures know there current location

### GET /game/:game_id/figure/:figure_id

- get more detail about figure:
  - location
  - possible moves

### PATCH /game/:game_id/figure/:fugre_id

- send target location when moving a figure
- backend checks if move is valid
