# Alien Invasion

Alien Invasion is a challenging sicescrolling Shoot Em' Up inspired by arcade games.The longer you survive, the faster the game becomes, but the greater your score multiplier rises. Programmed in Python using PyGame and built using PyInstaller. Heavily inspired by Eric Matthes' Alien Invasion.





https://user-images.githubusercontent.com/85529046/154772296-d154fe15-096b-4d85-875b-8c8250f58ca5.mp4











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
##### ARROWS-2:
- Arrow keys (Left, Right, Up, Down): Move the ship in that respective direction
- S: Fire a missile
- D: Flip Ship across the y-axis
- A: Fire a beam charge
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
##### QWOP:
- QWOP: Move the ship left, right, up, and down, respectively
- Spacebar: Fire a missile
- F: Flip ship across the y-axis
- K: Fire a beam charge
##### ESDF:
- ESDF: Move the ship up, left, down, and right, respectively
- LMB: Fire a missile
- RMB: Flip Ship across the y-axis
- MMB: Fire a beam charge
##### SPACE:
- Arrow keys (Left, Right, Up, Down): Move the ship in that respective direction
- Spacebar: Fire a missile
- Left Shift: Flip ship across the y-axis
- Left Control: Fire a beam charge
##### SPACE-2:
- Arrow keys (Left, Right, Up, Down): Move the ship in that respective direction
- Spacebar: Fire a missile
- X: Flip Ship across the y-axis
- Left Shift: Fire a beam charge


#### Game Over
- Left Click: Activate menu option

### Controller:

#### Menu
- A: Enter Game
- B: Exit Game 
- X: Enter Options Menu

#### Options Menu
- B: Return to Main Menu 
- X: Toggle Game Speed
- Y: Toggle Cinematic VFX
- Left Bumper (LB): Toggle Music
- Right Bumper (RG): Toggle Sound

#### Game
- D-pad: Move ship
- A: Fire a missile
- B: Flip ship direction horizontally
- X: Fire Beam Charge
- Start: Pauses game

#### Game Over
- B: Go to Main Menu
- A: Restart Game


### <b>Menu Options:</b>
(![menu](https://user-images.githubusercontent.com/85529046/152646746-f338293e-800c-4258-9b09-8d802ab49a4b.png)



- **Start**: Enters the game 
- **Game Speed**: Normal is the default game speed. Turbo plays at 1.5x the speed of normal.
- **Control Scheme**: Defaults to "ARROWS". See controls section for exact bindings. Controller not affected.
- **Music**: Toggles in-game and menu music. Disabled when the button is red, enabled when the button is green.
- **Sound**: Toggles in-game sound. Disabled when the button is red, enabled when the button is green.
- **Movie VFX**: Toggles cinematic black bars on the top and bottom of the screen, forcing a 16:9 aspect ratio instead of 3:2 (when red).
- **Resolution**: Toggles between "Native" resolution (960x640) and "Scaled" (upscales base resolution to fit display).
- **Quit**: Exits the game

### <b>Tips:</b>

- While your ship is flipped, your bullets move at 2.5x speed and your ship moves at 1.25x speed. This affects existing bullets.
- You can only have 5 missiles out at once. Missiles disappear if they fly offscreen or hit an enemy.
- Beam charges have a much larger hitbox than missiles, move 25% more quickly, and pierce enemies, but are consumable. 
- You have 3 lives, this is displayed by the current amount of ships on your HUD
- Base score is 50 points per trash ship, 100 per mine, and 250 per gunner. This is increased by 1.5x if playing on Turbo Mode. 
- Killing an enemy in close range has a 4x score multiplier. (200 pixels or less --> calculated using pythagorean theorem) 
- Shooting an enemy in their back has a 4x score multiplier.
- If both multipliers are active, you instead receive a larger score multiplier (10x instead of 8x)
- If on normal speed, the game will speed up by 25% (base) every 90 seconds and increase score by 15 points.
- If on turbo speed, the game will speed up by 50% (base, 33% turbo) every 90 seconds and increases by 30 points.
- Every 5000 points earns you a beam charge. If you're at capacity (3), then you instead earn 1000 bonus points.
- Hitboxes for mines and trash mobs are circular, not rectangular, so you have some room to dodge and flank enemies.
- Movement is restricted in the top and bottom of the screen (60 pixels for each). Cinematic Bars will help cover this up.
- Mines will always follow your current position and can overlap, kite them for an easy beam charge.
- Mines will always spawn from the edge of a screen, so the middle will always be a safe spot.
- Gunners will always spawn from the rightmost center of the screen before following your position.
- Gunners fire every 1.5 seconds and will slowly move to your current y position, use this to your advantage.
- There is enough room behind a gunner to perform a backstab



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


