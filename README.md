
# DoomMaker Game Engine

Welcome to **DoomMaker**, a Python-based game engine designed to help you create your own Doom-inspired maps and game experiences. Whether you're building classic first-person shooter levels or experimenting with your own game mechanics, DoomMaker provides powerful yet simple tools to bring your ideas to life.

## Key Features

- **Map Creation**: Easily design and generate maps with intuitive Python scripts.
- **Game Logic**: Implement core Doom-like mechanics including movement, shooting, and enemy behavior.
- **Extensible**: Fully customizable for your game ideas, whether you're sticking to the original Doom aesthetic or adding modern touches.
- **Lightweight**: Built with Python, DoomMaker is fast and easy to set up, with minimal dependencies.

## Getting Started

### Installation

To get started with DoomMaker, simply clone the repository and install the necessary dependencies by reading the script header.



### Structure of the Game Engine

The main components of the DoomMaker engine are located in two core files:

1. **DOOMPY3.py**: This is the core engine file that defines the main logic for rendering maps and handling gameplay mechanics. It is responsible for:
   - Rendering 2D or pseudo-3D environments.
   - Handling player inputs and interactions.
   - Managing object collisions and game physics.
   
2. **map_creator_2.py**: This file contains utilities for map generation. It provides an easy-to-use interface for designing levels, defining map features, and exporting them into a format readable by the DoomMaker engine. It includes:
   - Functions for creating rooms, walls, and interactive elements.
   - Tools for specifying player spawn points and enemy placement.
   - Output functionality to generate ready-to-play maps.

### Usage

#### 1. Creating a Map

You can use the map creation utility provided in `map_creator_2.py` to design your game levels. Here's an example of how to create a simple room with a player spawn point:

```python
from map_creator_2 import MapCreator

# Initialize the map creator
map = MapCreator(width=100, height=100)

# Create a simple room
map.create_room(x=10, y=10, width=20, height=20)

# Set the player spawn point
map.set_player_spawn(x=15, y=15)

# Export the map to the engine-readable format
map.export_map("my_first_map.doom")
```

#### 2. Running the Game

Once your map is created, you can load it into the DoomMaker engine using `DOOMPY3.py`:

```bash
python DOOMPY3.py --map my_first_map.doom
```

This will launch the game with your custom map, allowing you to explore and test it in the engine.

### Customizing the Engine

DoomMaker is designed to be flexible and extendable. If you want to modify the game mechanics, AI behavior, or rendering, you can dive into `DOOMPY3.py` to tweak the engine. For example, you could add new weapon types, enemy behaviors, or even entirely new gameplay mechanics.

### Example: Adding a Custom Enemy

In `DOOMPY3.py`, you can define a new enemy class by extending the existing enemy system. Here's a simple example of how you could add a new type of enemy:

```python
class FastEnemy(Enemy):
    def __init__(self, speed, health):
        super().__init__(health)
        self.speed = speed

    def move(self):
        # Custom movement logic for a faster enemy
        self.position.x += self.speed
```

After defining this new enemy type, you can place it in your map and watch as it chases the player at high speed!

## Contributing

We welcome contributions from the community! If you have ideas for improvements or bug fixes, feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create a new branch (`git checkout -b my-new-feature`)
3. Make your changes and commit them (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new pull request

## License

DoomMaker is open-source software licensed under the MIT License. Feel free to use, modify, and distribute it as you like.(LICENSE WILL BE ACTIVATED AFTER YOU JOIN OUR DISCORD CHANNEL: https://discord.gg/yMugmymnYz)

