# Alien Invasion

Alien Invasion is a challenging sicescrolling Shoot Em' Up inspired by arcade games.The longer you survive, the faster the game becomes, but the greater your score multiplier rises. Programmed in Python using PyGame and built using PyInstaller. Heavily inspired by Eric Matthes' Alien Invasion.




https://user-images.githubusercontent.com/85529046/152647041-b6f0b2b9-0c6d-4bb0-b980-54453182fb8f.mp4






## <b>Controls:</b>

### Keyboard and Mouse:

#### Menus 
- Left Mouse: Activate menu option 
- ESC: Exit game

#### Game
- ESC: Toggle Pause 
- The Game Has 4 Different Keyboard + Mouse control schemes for combat + movement:
##### ARROWS:
- Arrow keys (Left, Right, Up, Down): Move the ship in that respective direction
- X: Fire a missile
- Z: Flip Ship across the y-axis
- C: Fire a beam charge
##### VIMLIKE:
- JKL; (offset to the right of traditional VIM): Move the ship left, down, up, and right, respectively.
- D: Fire a missile
- S: Flip Ship across the y-axis
- F: Fire a beam charge
##### WASD:
- WASD: Move the ship up, left, down, and right, respectively
- Left Mouse (LMB): Fire a missile
- Right Mouse (RMB): Flip Ship across the y-axis
- Middle Mouse (MMB): Fire a beam charge
##### ESDF:
- ESDF: Move the ship up, left, down, and right, respectively
- LMB: Fire a missile
- RMB: Flip Ship across the y-axis
- MMB: Fire a beam charge

#### Game Over
- Left Click: Activate menu option

### Controller:

#### Menu
- Start: Enter Game
- Select: Exit Game

#### Game
- D-pad: Move ship
- A: Fire a missile
- B: Flip ship direction horizontally
- X: Fire Beam Charge
- Select: Exit game (applies to menu too)

#### Game Over
- LB: Go to Main Menu
- RB: Restart Game


### <b>Menu Options:</b>
(![menu](https://user-images.githubusercontent.com/85529046/152646746-f338293e-800c-4258-9b09-8d802ab49a4b.png)



- **Start**: Enters the game 
- **Game Speed**: Normal is the default game speed. Turbo plays at 1.5x the speed of normal.
- **Control Scheme**: Defaults to "ARROWS". See controls section for exact bindings. Controller not affected.
- **Music**: Toggles in-game and menu music. Disabled when the button is red, enabled when the button is green.
- **Sound**: Toggles in-game sound. Disabled when the button is red, enabled when the button is green.
- **Movie VFX**: Toggles cinematic black bars on the top and bottom of the screen, forcing a 16:9 aspect ratio instead of 3:2 (when red).
- **Quit**: Exits the game

### <b>Tips:</b>

- While your ship is flipped, your bullets move at 2.5x speed. This affects existing bullets.
- You can only have 5 missiles out at once. Missiles disappear if they fly offscreen or hit an enemy.
- Beam charges have a much larger hitbox than missiles, move 25% more quickly, and pierce enemies, but are consumable. 
- You have 3 lives, this is displayed by the current amount of ships on your HUD
- Base score is 100 points per ship. This is increased to 150 if playing on Turbo Mode. 
- Killing an enemy in close range has a 2x score multiplier. (200 pixels or less --> calculated using pythagorean theorem) 
- Shooting an enemy in their back has a 2x score multiplier.
- If both multipliers are active, you instead receive a larger score multiplier (5x instead of 4x)
- If on normal speed, the game will speed up by 25% (base) every 90 seconds and increase score by 25 points.
- If on turbo speed, the game will speed up by 50% (base, 33% turbo) every 90 seconds and increases by 50 points.
- Every 5000 points earns you a beam charge. If you're at capacity (3), then you instead earn 1000 bonus points.
- Hitboxes are circular, not rectangular, so you have some room to dodge and flank enemies.
- Movement is restricted in the top and bottom of the screen (60 pixels for each). Cinematic Bars will help cover this up.


## <b>REQUIREMENTS:</b> 

- Python 3.10 +
- Pygame 2.1 + 

NOTE: I have only tested with these versions installed. You can use older versions, but they might not be compatible! 

## <b>INSTALLATION:</b>

### Releases:

Download the latest release, extract the zip, and run the alien invasion launch script (Linux). 

### Cloning:

clone this repository using git in your terminal:

```
$ git clone https://github.com/kck130030/alien_invasion.git

$ cd alien_invasion

$ python alien_invasion.py

```
NOTE: Some systems need to run python 3 using "python3" instead of "python"


