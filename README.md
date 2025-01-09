# Alien Invasion



https://github.com/user-attachments/assets/da539b6e-36d2-469d-9b05-b850e59fbfec


Alien Invasion is a challenging sidescrolling Shoot Em' Up inspired by classic arcade games.The longer you survive, the faster the game becomes, but the greater your score multiplier rises. Being aggressive will further increase your score Programmed in Python using PyGame and built using Nuitka3. Heavily inspired by Eric Matthes' Alien Invasion.


## <b>REQUIREMENTS:</b> 

- Python 3.10
- Pygame 2.1 
- Nuitka3 1.4.6 (for building releases)

NOTE: I have only tested with these versions installed. You can use older or newer versions, but they might not be compatible! 

## <b>INSTALLATION:</b>

### Cloning:

clone this repository using git in your terminal:

```
$ git clone https://github.com/simurghi/Alien_Invasion.git

$ cd alien_invasion/src

$ python alien_invasion.py

```
NOTE: Some systems need to run python 3 using "python3" instead of "python"

### Releases:

Download the latest release, extract the zip, and run the alien invasion .bin launch script (Linux) or .exe (Windows). 

To create your own release, once you've cloned the repository, inside of your terminal, type:

```
$ cd alien_invasion/src

$ nuitka3 --standalone --onefile alien_invasion.py

```
NOTE: The finished binary _must_ be able to find the stats and assets folders or else it won't work. You can move them into the same directory or use symlinks. 



## <b>Controls:</b>

### Keyboard and Mouse:

#### Menus 
- Left Mouse: Activate menu option 
- Right Mouse: Clear Keybind (Controls Menu only)
- Up/Down Arrow: Move menu cursor up and down
- Enter: Confirm action highlighted by menu cursor
- ESC: Exit game, return down menu one level (if not at main menu)

#### Game
- ESC: Toggle Pause 
- WASD: Move the ship up, left, down, and right, respectively
- LMB/J: Fire a missile
- RMB/K: Flip Ship across the y-axis
- MMB/L: Fire a beam charge

##### CUSTOM:
- The user can define their own preferred keyboard and mouse control scheme by assigning button presses as follows:
- MOVELEFT: (Defaults to Left Arrow)
- MOVERIGHT: (Defaults to Right Arrow)
- MOVEUP: (Defaults to Up Arrow)
- MOVEDOWN: (Defaults to Down Arrow)
- BEAMATTACK: (Defaults to the "C" Key)
- FLIPSHIP: (Defaults to the "Z" Key)
- MISSILEATTACK: (Defaults to the "X" Key)

- Keys cannot overlap and the user will need to use an alternative key. 
- If a Key is unbound, it must be mapped to leave the control screen (the application can still be exited normally.)

#### Game Over
- Left Click: Activate menu option

### Controller:

#### Menu
- Up/Down D-pad: Move cursor up/down
- A: Confirm action highlighted by menu cursor
- B: Exit Game, return down menu one level (if not at main menu)

#### Game
- Left Analogue Stick/D-pad: Move ship
- A: Fire a missile
- B: Flip ship direction horizontally
- X: Fire Beam Charge
- Start: Pauses game


### <b>Menu Options:</b>


- **Game Speed**: Normal is the default game speed. Can select from "Slow", "Normal", "Fast", "Very Fast", or "Ludicrous". Score multiplier is increased on faster speeds.
- **Music**: Adjusts in-game and menu music by increments of 10%. Disabled when at 0%
- **Sound**: Adjusts in-game and menu sound by increments of 10%. Disabled when at 0%
- **Resolution**: Toggles between "Native" resolution (960x640), "Scaled" (upscales base resolution to fit display in integer increments, if possible), and "Full Scaled" (upscales base resolution to fit display in exclusive fullscreen).
- **Score**: If set to "All" displays high score on the main menu, and current/high score in-game. Each element can be toggled between or disabled entirely.
- **HUD**: Adjusts position of missile and beam counters, as well as lives. Can be disabled entirely.
- **Arrows**: If set to "All" displays direction arrow in front of player and warning arrows for mine spawns offscreen. Each element can be toggled between or disabled entirely.
- **Back**: Returns to the main menu

### <b>Tips:</b>

- While your ship is flipped, your bullets move at 2.5x speed and your ship moves at 1.25x speed. This affects existing bullets.
- You can only have 5 missiles out at once. Missiles disappear if they fly offscreen or hit an enemy.
- Beam charges have a much larger hitbox than missiles, move 25% more quickly, and pierce enemies, but are consumable. 
- You have 3 lives, this is displayed by the current amount of ships on your HUD
- Base score is 50 points per trash ship, 100 per mine, and 250 per gunner. This is increased by 1.5x if playing on Turbo Mode. 
- Killing an enemy in close range has a 4x score multiplier. (200 pixels or less --> calculated using pythagorean theorem) 
- Shooting an enemy in their back has a 4x score multiplier (i.e. if your bullet is travelling to the left).
- If both multipliers are active, you instead receive a larger score multiplier (10x instead of 8x)
- If on normal speed, the game will speed up by +10% (base) every 20 seconds and increase score by 5 points.
- If on turbo speed, the game will speed up by +20% (base) every 20 seconds and increases by 10 points.
- Every 5000 points earns you a beam charge. If you're at capacity (3), then you instead earn 1000 bonus points.
- Hitboxes for mines and trash mobs are circular, not rectangular, so you have some room to dodge and flank enemies.
- Hitboxes for Gunners and their bullets are pixel accurate, so you can die if you clip into their wings. 
- Movement is restricted in the top and bottom of the screen (60 pixels for each). Cinematic Bars will help cover this up.
- Mines will always follow your current position and can overlap, kite them for an easy beam charge.
- Mines will always spawn from the a left or center edge of the screen, so the middle or right will always be a safe spot.
- Mines will play a sound and blink faster if near a player (150 pixels distance) 
- Gunners will always spawn from the rightmost center of the screen before following your position.
- Gunners fire on a cooldown and will slowly move to your current y position, use this to your advantage.
- Gunners have 10 HP and take 1 damage from every missile shot, and 5 from every beam shot. 
- There can only ever be one Gunner on the screen at once, if a gunner already exists when another one would spawn, a new enemy wave consisting of mines and trash mobs will be spawned instead.
- There is enough room behind a gunner to perform a backstab




