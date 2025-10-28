# player.py
from interfaces import IDrawable, IMovable

class Player(IDrawable, IMovable):
    def __init__(self, canvas, x, y, image):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.id = canvas.create_image(x, y, image=image)
        self.health = 100
        self.invincible = False
        self.velocity_y = 0
        self.gravity = 1.2
        self.jump_force = -20
        self.min_y = 50
        self.max_y = y
        self.jump_count = 0
        self.max_jumps = 3
        self.jump_cooldown = False

    def jump(self):
        if not self.jump_cooldown and self.jump_count < self.max_jumps:
            self.velocity_y = self.jump_force
            self.jump_count += 1
            self.jump_cooldown = True
            self.canvas.after(150, lambda: setattr(self, 'jump_cooldown', False))

    def on_ground(self):
        _, y = self.coords()
        return y >= self.max_y

    def update(self, obstacles=None):
        self.velocity_y += self.gravity
        self.canvas.move(self.id, 0, self.velocity_y)
        x, y = self.coords()

        if y < self.min_y:
            self.canvas.coords(self.id, self.x, self.min_y)
            self.velocity_y = 0

        if y > self.max_y:
            self.canvas.coords(self.id, self.x, self.max_y)
            self.velocity_y = 0
            self.jump_count = 0

        if obstacles:
            for obs in obstacles:
                ox, oy = obs.coords()
                if abs(x - ox) < 60 and 0 < (oy - y) < 70 and self.velocity_y > 0:
                    self.canvas.coords(self.id, self.x, oy - 70)
                    self.velocity_y = 0
                    self.jump_count = 0
                    break

    def move(self):
        """Obligatoire selon IMovable, mais ici on ne bouge que sur Y (update)."""
        self.update()

    def coords(self):
        return self.canvas.coords(self.id)

    def activate_bonus(self, duration=1000):
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
