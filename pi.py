import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=600, height=600, bg="black")
        self.canvas.pack()
        self.score = 0
        self.speed = 100
        self.direction = 'Right'
        self.snake = [(20, 20), (20, 40), (20, 60)]
        self.food = None
        self.create_objects()
        self.bind_keys()
        self.game_running = True
        self.update_snake()

    def create_objects(self):
        self.canvas.create_text(50, 10, text=f"Score: {self.score}", tag="score", fill="white", font=('Arial', 14))
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green", tag="snake")
        self.create_food()

    def create_food(self):
        if self.food:
            self.canvas.delete(self.food)
        x = random.randint(0, 29) * 20
        y = random.randint(0, 29) * 20
        self.food = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="red", tag="food")

    def bind_keys(self):
        self.root.bind("<Up>", self.change_direction)
        self.root.bind("<Down>", self.change_direction)
        self.root.bind("<Left>", self.change_direction)
        self.root.bind("<Right>", self.change_direction)

    def change_direction(self, event):
        new_direction = event.keysym
        all_directions = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
        if new_direction != all_directions.get(self.direction):
            self.direction = new_direction

    def update_snake(self):
        if self.game_running:
            head_x, head_y = self.snake[-1]
            if self.direction == 'Up':
                new_head = (head_x, head_y - 20)
            elif self.direction == 'Down':
                new_head = (head_x, head_y + 20)
            elif self.direction == 'Left':
                new_head = (head_x - 20, head_y)
            elif self.direction == 'Right':
                new_head = (head_x + 20, head_y)

            self.snake.append(new_head)
            if self.check_collision(new_head):
                self.end_game()
                return

            if self.check_food_collision(new_head):
                self.score += 1
                self.canvas.itemconfigure("score", text=f"Score: {self.score}")
                self.create_food()
                if self.score % 5 == 0:
                    self.speed = max(10, self.speed - 10)
            else:
                self.canvas.delete(self.snake[0])
                self.snake.pop(0)

            self.canvas.create_rectangle(new_head[0], new_head[1], new_head[0] + 20, new_head[1] + 20, fill="green", tag="snake")
            self.root.after(self.speed, self.update_snake)

    def check_collision(self, head):
        x, y = head
        if x < 0 or x >= 600 or y < 0 or y >= 600:
            return True
        if head in self.snake[:-1]:
            return True
        return False

    def check_food_collision(self, head):
        return self.canvas.coords(self.food) == [head[0], head[1], head[0] + 20, head[1] + 20]

    def end_game(self):
        self.game_running = False
        self.canvas.create_text(300, 300, text="Game Over", fill="red", font=('Arial', 30))
        self.canvas.create_text(300, 340, text="Press R to Restart", fill="white", font=('Arial', 20))
        self.root.bind("<r>", self.restart_game)

    def restart_game(self, event):
        self.canvas.delete("all")
        self.score = 0
        self.speed = 100
        self.direction = 'Right'
        self.snake = [(20, 20), (20, 40), (20, 60)]
        self.food = None
        self.game_running = True
        self.create_objects()
        self.update_snake()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()