from tkinter import *
from random import randint, choice
from tkinter import messagebox


class window:
    def __init__(self):
        self.root = Tk()
        self.root.title("Snake Game")
        self.root.config(background="black")
        self.root.geometry("800x600")

        self.width = 700
        self.height = 500

        self.x = 0
        self.y = 0
        self.random_x = randint(20, self.width - 40)
        self.random_y = randint(20, self.height - 40)
        self.enemy_random_x = randint(20, self.width - 40)
        self.enemy_random_y = randint(20, self.height - 40)

        self.new_cordinates = []
        self.score = 0
        self.enemies_list = []

        self.label = Label(self.root, text="Score : {}".format(self.score), bg="black", fg="white", height=2)
        self.label.pack()
        self.canvas = Canvas(bg="black", height=self.height, width=self.width)
        self.snake = self.canvas.create_rectangle(10, 10, 30, 30, fill="blue")
        self.enemy = self.canvas.create_rectangle(310, 310, 330, 330, fill="red")

        self.food = self.canvas.create_rectangle(self.random_x, self.random_y, self.random_x + 20, self.random_y + 20,
                                                 fill="green")
        self.show_screen = FALSE

        self.canvas.pack()
        self.keybinds()
        self.movemnet()
        self.enemy_move()
        self.root.mainloop()

    def end_screen(self):
        if self.show_screen == TRUE:
            self.button = Button(text = "Game Over !\n Click to Continue", height=33, width=100, bg = "black", command = self.refresh, fg = "white", activebackground = "black")
            self.button.place(x = 47 , y = 35)


    def refresh(self):
        self.root.destroy()
        enemy()


class snake(window):
    def keybinds(self):
        self.canvas.bind_all("<Key>", self.direction)

    def direction(self, event):
        if event.keysym == "Left":
            self.x = -10
            self.y = 0

        elif event.keysym == "Right":
            self.x = 10
            self.y = 0


        elif event.keysym == "Up":
            self.x = 0
            self.y = -10

        elif event.keysym == "Down":
            self.x = 0
            self.y = 10
        self.canvas.move(self.snake, self.x, self.y)

    def movemnet(self):
        if self.show_screen == TRUE:
            self.x = 0
            self.y = 0

        self.canvas.move(self.snake, self.x, self.y)
        self.canvas.after(40, self.movemnet)
        self.out_of_bounds()
        self.food_properties()

    def out_of_bounds(self):
        if self.canvas.coords(self.snake)[0] > self.width - 20 or self.canvas.coords(self.snake)[1] > self.height - 20 \
                or self.canvas.coords(self.snake)[0] < 0 or self.canvas.coords(self.snake)[1] < 0:
            self.canvas.coords(self.snake, 350, 250, 370, 270)
            self.show_screen = TRUE
            self.score = 0
            self.label.config(text="Score : {}".format(self.score))
            self.label.pack()
            self.end_screen()


class food(snake):
    def food_properties(self):
        self.random_x = randint(20, self.width - 40)
        self.random_y = randint(20, self.height - 40)

        self.postion_min_x = int(self.canvas.coords(self.food)[1]) - 15
        self.postion_max_x = int(self.canvas.coords(self.food)[1]) + 15
        self.postion_min_y = int(self.canvas.coords(self.food)[2]) - 15
        self.postion_max_y = int(self.canvas.coords(self.food)[2]) + 15

        self.eaten()

    def eaten(self):
        for i in range(self.postion_min_x, self.postion_max_x):
            for c in range(self.postion_min_y, self.postion_max_y):
                if self.canvas.coords(self.snake)[2] == c and self.canvas.coords(self.snake)[1] == i:
                    self.canvas.coords(self.food, self.random_x, self.random_y, self.random_x + 20, self.random_y + 20)
                    self.score += 1
                    self.score_board()

    def score_board(self):
        self.label.config(text="Score : {}".format(self.score))
        self.label.pack()


class enemy(food):
    def enemy_properties(self):

        self.enemy_postion_min_x = int(self.canvas.coords(self.enemy)[2]) - 35
        self.enemy_postion_max_x = int(self.canvas.coords(self.enemy)[2]) + 35
        self.enemy_postion_min_y = int(self.canvas.coords(self.enemy)[3]) - 35
        self.enemy_postion_max_y = int(self.canvas.coords(self.enemy)[3]) + 35

    def enemy_directions(self):
        self.enemy_direction_list = ["left", "right", "up", "down"]

        if self.canvas.coords(self.enemy)[0] < 20:
            self.enemy_direction_list.remove("left")
        elif self.canvas.coords(self.enemy)[0] > self.width - 20:
            self.enemy_direction_list.remove("right")

        if self.canvas.coords(self.enemy)[3] < 20:
            self.enemy_direction_list.remove("up")
        elif self.canvas.coords(self.enemy)[3] > self.height - 20:
            self.enemy_direction_list.remove("down")

        self.enemy_direction = choice(self.enemy_direction_list)

        if self.enemy_direction == "left":
            self.enemy_random_x = -20
            self.enemy_random_y = 0
        elif self.enemy_direction == "right":
            self.enemy_random_x = 20
            self.enemy_random_y = 0
        elif self.enemy_direction == "up":
            self.enemy_random_x = 0
            self.enemy_random_y = -20
        elif self.enemy_direction == "down":
            self.enemy_random_x = 0
            self.enemy_random_y = 20
        if self.show_screen == TRUE:
            self.enemy_random_x = 0
            self.enemy_random_y = 0
        self.canvas.move(self.enemy, self.enemy_random_x, self.enemy_random_y)

    def enemy_move(self):
        self.enemy_directions()
        self.canvas.after(500, self.enemy_move)
        self.enemy_properties()
        self.enemy_eaten()

    def enemy_eaten(self):
        for i in range(self.enemy_postion_min_x, self.enemy_postion_max_x)[::5]:
            for c in range(self.enemy_postion_min_y, self.enemy_postion_max_y)[::5]:
                if self.canvas.coords(self.snake)[3] == c and self.canvas.coords(self.snake)[2] == i:
                    self.score = 0
                    self.show_screen = TRUE
                    #self.canvas.coords(self.snake, 350, 250, 370, 270)
                    self.score_board()
                    self.end_screen()
game = enemy()

if __name__ == '__main__':
    def refresh():
        game.root.destroy()
