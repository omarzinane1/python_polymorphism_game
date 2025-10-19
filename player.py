class Player:
    def __init__(self, canvas, x, y, image):
        self.canvas = canvas
        self.x = x
        self.y = y  # ground
        self.id = canvas.create_image(x, y, image=image)
        self.health = 100
        self.invincible = False

        # Physique
        self.velocity_y = 0
        self.gravity = 1.3   
        self.jump_force = -30  
        self.min_y = 10          
        self.max_y = y      

    def jump(self):
        if self.on_ground():
            self.velocity_y = self.jump_force

    def on_ground(self):
        x, y = self.coords()
        return y >= self.max_y

    def update(self):
        self.velocity_y += self.gravity
        self.canvas.move(self.id, 0, self.velocity_y)
        x, y = self.coords()

        # Limite le joueur en haut
        if y < self.min_y:
            self.canvas.coords(self.id, self.x, self.min_y)
            self.velocity_y = 0

        # Limite le joueur en bas
        if y > self.max_y:
            self.canvas.coords(self.id, self.x, self.max_y)
            self.velocity_y = 0

    def activate_bonus(self, duration=3000):
        self.invincible = True
        self._bonus_animation(0, duration)

    def _bonus_animation(self, count, duration):
        if count % 2 == 0:
            self.canvas.itemconfig(self.id, state="hidden")
        else:
            self.canvas.itemconfig(self.id, state="normal")
        if duration <= 0:
            self.invincible = False
            self.canvas.itemconfig(self.id, state="normal")
            return
        self.canvas.after(150, lambda: self._bonus_animation(count+1, duration-150))

    def coords(self):
        return self.canvas.coords(self.id)
