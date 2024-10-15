from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from panda3d.core import Filename  # Add this line
import pickle
import os
import time
import math  # Import math for distance calculation

# Initialize Ursina application
app = Ursina()

# Disable the default exit button
window.exit_button.visible = False

# Player settings
player = FirstPersonController(collider='box.obj', position=(20, 1, 20))

# Gun settings
gun = Entity(model='quad', texture='DOOMGUN.png', parent=camera.ui, scale=(0.2, 0.2), position=(0, -0.4), z=-1)
gun_shooting_texture = 'DOOMGUN1.png'

# Game variables
health = 4  # Player starts with 4 lives
shoot_cooldown = 0.3  # Cooldown time between shots
last_shot_time = time.time()

# Load the shooting sound
shooting_sound = Audio('ak.mp3', autoplay=False)  # Load the sound but don't autoplay

# Load the walking sound
walking_sound = Audio('walk.mp3', autoplay=False, loop=True)  # Load the walking sound in loop mode

# List to store all enemies
enemies = []

# Load the map from GAME.dbo
def load_map(map_file):
    if os.path.exists(map_file):
        with open(map_file, 'rb') as f:
            map_data = pickle.load(f)

        # Extract filenames only from paths
        wall_texture_name = os.path.basename(map_data['wall_texture'])  # Extract filename
        wall_texture = load_texture(wall_texture_name)
        if wall_texture is None:
            print("Failed to load wall texture!")

        ground_texture_name = os.path.basename(map_data['ground_texture'])  # Extract filename
        ground_texture = load_texture(ground_texture_name)
        print(f"Ground Texture: {ground_texture}")

        enemy_texture_name = os.path.basename(map_data['enemy_texture'])  # Extract filename
        enemy_texture = load_texture(enemy_texture_name)
        print(f"Enemy Texture: {enemy_texture}")

        # Create ground and walls
        for row in range(20):
            for col in range(20):
                label = map_data['grid'][row][col]
                if label == 0 or label == 2:  # Ground tiles
                    ground_tile = Entity(model='plane.obj', scale=(2, 2), position=(col * 2, 0, row * 2), texture=ground_texture, collider='phys.obj')
                    ground_tile.texture_scale = (2, 2)  # Adjust tiling to ensure the texture repeats correctly

                if label == 1:  # Wall tiles
                    wall = Entity(model='cube', scale=(2, 2.2, 2), position=(col * 2, 1, row * 2), texture=wall_texture, collider='box')
                    wall.texture_scale = (1, 1)  # Adjust this depending on how the texture should be displayed

                if label == 2:  # Enemies
                    create_enemy(col * 2, row * 2, enemy_texture)
    else:
        print(f"Map file {map_file} not found!")

# Create enemy
def create_enemy(x, z, enemy_texture):
    enemy = Entity(
        model='quad',
        texture=enemy_texture,
        position=(x, 1, z),
        scale=2,
        collider='box',
        billboard=True  # This makes the enemy always face the player
    )
    enemy.is_enemy = True
    enemy.health = 3  # Each enemy starts with 3 health points
    enemy.take_damage = lambda: enemy_hit(enemy)  # Assign the take_damage function
    enemies.append(enemy)  # Add enemy to the enemies list

# Function to handle enemy taking damage
def enemy_hit(enemy):
    enemy.health -= 1  # Reduce health by 1 with each hit
    if enemy.health <= 0:
        destroy(enemy)  # Destroy the enemy if health reaches 0
        enemies.remove(enemy)  # Remove enemy from the list

# Setup lives UI
lives_images = []
for i in range(4):
    heart = Entity(model='quad', texture='heart.png', parent=camera.ui, scale=0.06, position=(-0.77 + (i * 0.13), -0.4), z=-1)
    lives_images.append(heart)

# Update player's health
def update_health():
    global health
    health -= 1
    if health <= 0:
        game_over()
    else:
        destroy(lives_images[health])

# Game over logic
def game_over():
    Text(text='Game Over', scale=3, origin=(0, 0), color=color.red)
    player.disable()

# Reset gun texture to idle
def reset_gun():
    gun.texture = 'DOOMGUN.png'

# Shooting logic
def shoot():
    global last_shot_time
    current_time = time.time()
    if current_time - last_shot_time < shoot_cooldown:
        return  # Cooldown

    last_shot_time = current_time
    gun.texture = gun_shooting_texture  # Change gun texture to shooting state
    invoke(reset_gun, delay=0.1)  # Reset gun after delay

    # Play the shooting sound once per shot
    shooting_sound.play()

    # Raycasting to detect enemy hit
    start_position = Vec3(player.position.x, 1.75, player.position.z)  # Set the height to 1.75
    shoot_ray = raycast(start_position, camera.forward, distance=10, ignore=[player])
    
    print("You shot a bullet")

    if shoot_ray.hit:
        if shoot_ray.entity and hasattr(shoot_ray.entity, 'is_enemy'):
            shoot_ray.entity.take_damage()
            print("you shoot an enemy")


# Input handling
def input(key):
    if key == 'left mouse down':
        shoot()

    if key == 'escape':
        application.quit()

# Track the player's previous position to detect movement
prev_position = player.position

# Chasing logic and player health loss when close to enemies
def update():
    global health, prev_position

    # Check if the player is moving along the x or z axis
    if player.position.x != prev_position.x or player.position.z != prev_position.z:
        if not walking_sound.playing:
            walking_sound.play()  # Start playing the walking sound if not already playing
    else:
        if walking_sound.playing:
            walking_sound.stop()  # Stop playing the walking sound when the player stops

    # Update the previous position to the current one
    prev_position = Vec3(player.position.x, player.position.y, player.position.z)

    for enemy in enemies:
        # Lock the enemy's scale and y-position to ensure they don't change
        enemy.scale = 2  # Lock scale
        enemy.y = 1  # Lock y-position

        # Calculate distance to player
        distance_to_player = math.sqrt((player.x - enemy.x)**2 + (player.z - enemy.z)**2)

        if distance_to_player < 6:  # If player is within 3 meters, the enemy moves towards the player
            direction = (player.position - enemy.position).normalized()  # Get direction to player
            # Only update the x and z positions to move towards the player, keeping y unchanged
            enemy.position += Vec3(direction.x, 0, direction.z) * time.dt * 0.5  # Move towards the player at 0.5 m/s

        if distance_to_player < 2:  # If player is within 2 meters, start losing health
            if not hasattr(enemy, 'damage_timer'):  # Start damage timer if not already active
                enemy.damage_timer = time.time()
            else:
                # Check if 1 second has passed since the last health loss
                if time.time() - enemy.damage_timer >= 1:
                    update_health()  # Lose 1 heart
                    enemy.damage_timer = time.time()  # Reset the timer
        else:
            # Reset the enemy's damage timer if the player moves out of range
            if hasattr(enemy, 'damage_timer'):
                del enemy.damage_timer


# Load the map
load_map("GAME.dbo")

# Run the game
app.run()
