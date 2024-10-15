import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pickle
import os

# Initialize the CustomTkinter theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class MapEditor(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Doom-maker Map Editor")
        self.geometry("900x700")

        # Variables to hold the current mode and textures
        self.current_mode = None  # Can be 'wall', 'ground', or 'enemy'
        self.wall_texture = None
        self.ground_texture = None
        self.enemy_texture = None

        # Variables to hold the texture previews
        self.wall_preview_image = None
        self.ground_preview_image = None
        self.enemy_preview_image = None

        # Create a frame for the grid and control panel
        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.grid(row=0, column=0, padx=10, pady=10)

        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # Initialize the map grid
        self.map_grid = [[None for _ in range(20)] for _ in range(20)]
        self.create_grid()

        # Create control buttons and previews
        self.create_controls()

    def create_grid(self):
        for row in range(20):
            for col in range(20):
                btn = ctk.CTkButton(self.grid_frame, text="", width=30, height=30,
                                    command=lambda r=row, c=col: self.on_tile_click(r, c))
                btn.grid(row=row, column=col, padx=1, pady=1)
                self.map_grid[row][col] = {'button': btn, 'label': None}

    def create_controls(self):
        # Mode buttons
        self.wall_button = ctk.CTkButton(self.control_frame, text="Place Walls",
                                         command=self.set_wall_mode)
        self.wall_button.pack(pady=5)

        self.ground_button = ctk.CTkButton(self.control_frame, text="Place Ground",
                                           command=self.set_ground_mode)
        self.ground_button.pack(pady=5)

        self.enemy_button = ctk.CTkButton(self.control_frame, text="Place Enemies",
                                          command=self.set_enemy_mode)
        self.enemy_button.pack(pady=5)

        # Texture selection buttons and previews
        self.wall_texture_button = ctk.CTkButton(self.control_frame, text="Choose Wall Texture",
                                                 command=self.choose_wall_texture)
        self.wall_texture_button.pack(pady=5)

        self.wall_texture_preview = ctk.CTkLabel(self.control_frame, text="")
        self.wall_texture_preview.pack(pady=5)

        self.ground_texture_button = ctk.CTkButton(self.control_frame, text="Choose Ground Texture",
                                                   command=self.choose_ground_texture)
        self.ground_texture_button.pack(pady=5)

        self.ground_texture_preview = ctk.CTkLabel(self.control_frame, text="")
        self.ground_texture_preview.pack(pady=5)

        self.enemy_texture_button = ctk.CTkButton(self.control_frame, text="Choose Enemy Texture",
                                                  command=self.choose_enemy_texture)
        self.enemy_texture_button.pack(pady=5)

        self.enemy_texture_preview = ctk.CTkLabel(self.control_frame, text="")
        self.enemy_texture_preview.pack(pady=5)

        # Save and Load buttons
        self.save_button = ctk.CTkButton(self.control_frame, text="Save Map",
                                         command=self.save_map)
        self.save_button.pack(pady=5)

        self.load_button = ctk.CTkButton(self.control_frame, text="Load Map",
                                         command=self.load_map)
        self.load_button.pack(pady=5)

    # Mode setting methods
    def set_wall_mode(self):
        self.current_mode = 'wall'
        messagebox.showinfo("Mode", "Wall placement mode activated.")

    def set_ground_mode(self):
        self.current_mode = 'ground'
        messagebox.showinfo("Mode", "Ground placement mode activated.")

    def set_enemy_mode(self):
        self.current_mode = 'enemy'
        messagebox.showinfo("Mode", "Enemy placement mode activated.")

    # Texture selection methods
    def choose_wall_texture(self):
        file_path = filedialog.askopenfilename(title="Select Wall Texture",
                                               filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.wall_texture = file_path
            self.update_texture_preview('wall')

    def choose_ground_texture(self):
        file_path = filedialog.askopenfilename(title="Select Ground Texture",
                                               filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.ground_texture = file_path
            self.update_texture_preview('ground')

    def choose_enemy_texture(self):
        file_path = filedialog.askopenfilename(title="Select Enemy Texture",
                                               filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.enemy_texture = file_path
            self.update_texture_preview('enemy')

    # Update texture previews
    def update_texture_preview(self, texture_type):
        if texture_type == 'wall' and self.wall_texture:
            image = Image.open(self.wall_texture)
            image = image.resize((100, 100), Image.ANTIALIAS)
            self.wall_preview_image = ImageTk.PhotoImage(image)
            self.wall_texture_preview.configure(image=self.wall_preview_image)
        elif texture_type == 'ground' and self.ground_texture:
            image = Image.open(self.ground_texture)
            image = image.resize((100, 100), Image.ANTIALIAS)
            self.ground_preview_image = ImageTk.PhotoImage(image)
            self.ground_texture_preview.configure(image=self.ground_preview_image)
        elif texture_type == 'enemy' and self.enemy_texture:
            image = Image.open(self.enemy_texture)
            image = image.resize((100, 100), Image.ANTIALIAS)
            self.enemy_preview_image = ImageTk.PhotoImage(image)
            self.enemy_texture_preview.configure(image=self.enemy_preview_image)

    # Tile click handler
    def on_tile_click(self, row, col):
        if self.current_mode == 'wall':
            self.map_grid[row][col]['label'] = 1
            self.map_grid[row][col]['button'].configure(text="1", fg_color="gray")
        elif self.current_mode == 'ground':
            self.map_grid[row][col]['label'] = 0
            self.map_grid[row][col]['button'].configure(text="0", fg_color="green")
        elif self.current_mode == 'enemy':
            self.map_grid[row][col]['label'] = 2
            self.map_grid[row][col]['button'].configure(text="2", fg_color="red")
        else:
            messagebox.showwarning("No Mode Selected", "Please select a placement mode first.")

    # Save and Load methods
    def save_map(self):
        if not all([self.wall_texture, self.ground_texture, self.enemy_texture]):
            messagebox.showerror("Missing Data", "Please select all textures before saving.")
            return

        map_data = {
            'grid': [[self.map_grid[row][col]['label'] for col in range(20)] for row in range(20)],
            'wall_texture': self.wall_texture,
            'ground_texture': self.ground_texture,
            'enemy_texture': self.enemy_texture
        }

        save_path = filedialog.asksaveasfilename(defaultextension=".dbo", initialfile="GAME.dbo",
                                                 filetypes=[("DBO Files", "*.dbo")])
        if save_path:
            with open(save_path, 'wb') as file:
                pickle.dump(map_data, file)
            messagebox.showinfo("Save Successful", f"Map saved to {save_path}.")

    def load_map(self):
        load_path = filedialog.askopenfilename(title="Load Map", filetypes=[("DBO Files", "*.dbo")])
        if load_path:
            with open(load_path, 'rb') as file:
                map_data = pickle.load(file)

            self.wall_texture = map_data.get('wall_texture')
            self.ground_texture = map_data.get('ground_texture')
            self.enemy_texture = map_data.get('enemy_texture')

            # Update texture previews
            self.update_texture_preview('wall')
            self.update_texture_preview('ground')
            self.update_texture_preview('enemy')

            grid_labels = map_data.get('grid')
            for row in range(20):
                for col in range(20):
                    label = grid_labels[row][col]
                    self.map_grid[row][col]['label'] = label
                    btn = self.map_grid[row][col]['button']
                    if label == 1:
                        btn.configure(text="1", fg_color="gray")
                    elif label == 0:
                        btn.configure(text="0", fg_color="green")
                    elif label == 2:
                        btn.configure(text="2", fg_color="red")
                    else:
                        btn.configure(text="", fg_color="default")
            messagebox.showinfo("Load Successful", f"Map loaded from {load_path}.")

if __name__ == "__main__":
    # Ensure that PIL is available
    try:
        from PIL import Image, ImageTk
    except ImportError:
        messagebox.showerror("Missing Dependency", "Please install Pillow: pip install Pillow")
        exit()

    app = MapEditor()
    app.mainloop()
