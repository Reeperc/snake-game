import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)
        self.canvas_size = 800  # Taille de la fenêtre
        self.cell_size = 40     # Taille d'une cellule
        self.grid_count = self.canvas_size // self.cell_size  # Nombre de cellules par ligne/colonne
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="black")
        self.canvas.pack()

        self.score = 0
        self.speed = 150
        self.direction = 'Right'
        self.snake = [(40, 40), (40, 80), (40, 120)]  # Positions initiales
        self.food = None
        self.game_running = True
        self.paused = False
        self.high_score = 0

        self.create_objects()
        self.bind_keys()
        self.update_snake()

    def create_objects(self):
        # Dessine la grille
        for i in range(0, self.canvas_size, self.cell_size):
            self.canvas.create_line([(i, 0), (i, self.canvas_size)], fill="gray")
            self.canvas.create_line([(0, i), (self.canvas_size, i)], fill="gray")
        
        # Affiche les scores
        self.canvas.create_text(70, 20, text=f"Score: {self.score}", tag="score", fill="white", font=('Arial', 16))
        self.canvas.create_text(self.canvas_size - 100, 20, text=f"High Score: {self.high_score}", tag="high_score", fill="white", font=('Arial', 16))
        
        # Dessine le serpent
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + self.cell_size, segment[1] + self.cell_size, fill="green", tag="snake")
        
        # Ajoute la nourriture
        self.create_food()

    def create_food(self):
        if self.food:
            self.canvas.delete(self.food)
        x = random.randint(0, self.grid_count - 1) * self.cell_size
        y = random.randint(0, self.grid_count - 1) * self.cell_size
        self.food = self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill="red", tag="food")

    def bind_keys(self):
        self.root.bind("<Up>", self.change_direction)
        self.root.bind("<Down>", self.change_direction)
        self.root.bind("<Left>", self.change_direction)
        self.root.bind("<Right>", self.change_direction)
        self.root.bind("<p>", self.toggle_pause)
        self.root.bind("<r>", self.restart_game)

    def change_direction(self, event):
        new_direction = event.keysym
        all_directions = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
        if new_direction != all_directions.get(self.direction):
            self.direction = new_direction

    def toggle_pause(self, event):
        self.paused = not self.paused
        if not self.paused:
            self.update_snake()

    def update_snake(self):
        if self.game_running and not self.paused:
            head_x, head_y = self.snake[-1]
            if self.direction == 'Up':
                new_head = (head_x, head_y - self.cell_size)
            elif self.direction == 'Down':
                new_head = (head_x, head_y + self.cell_size)
            elif self.direction == 'Left':
                new_head = (head_x - self.cell_size, head_y)
            elif self.direction == 'Right':
                new_head = (head_x + self.cell_size, head_y)

            self.snake.append(new_head)
            if self.check_collision(new_head):
                self.end_game()
                return

            if self.check_food_collision(new_head):
                self.score += 1
                self.high_score = max(self.high_score, self.score)
                self.canvas.itemconfigure("score", text=f"Score: {self.score}")
                self.canvas.itemconfigure("high_score", text=f"High Score: {self.high_score}")
                self.create_food()
                if self.score % 5 == 0:
                    self.speed = max(50, self.speed - 10)
            else:
                self.canvas.delete(self.snake[0])
                self.snake.pop(0)

            self.canvas.create_rectangle(new_head[0], new_head[1], new_head[0] + self.cell_size, new_head[1] + self.cell_size, fill="green", tag="snake")
            self.root.after(self.speed, self.update_snake)

    def check_collision(self, head):
        x, y = head
        if x < 0 or x >= self.canvas_size or y < 0 or y >= self.canvas_size:
            return True
        if head in self.snake[:-1]:
            return True
        return False

    def check_food_collision(self, head):
        return self.canvas.coords(self.food) == [head[0], head[1], head[0] + self.cell_size, head[1] + self.cell_size]

    def end_game(self):
        self.game_running = False
        self.canvas.create_text(self.canvas_size // 2, self.canvas_size // 2, text="Game Over", fill="red", font=('Arial', 40))
        self.canvas.create_text(self.canvas_size // 2, self.canvas_size // 2 + 50, text="Press R to Restart", fill="white", font=('Arial', 20))

    def restart_game(self, event):
        self.canvas.delete("all")
        self.score = 0
        self.speed = 150
        self.direction = 'Right'
        self.snake = [(40, 40), (40, 80), (40, 120)]
        self.food = None
        self.game_running = True
        self.create_objects()
        self.update_snake()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
