class Player:
    def __init__(self, canvas, x, y, image):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.id = canvas.create_image(x, y, image=image)
        self.health = 100
        self.invincible = False

        # === Physique ===
        self.velocity_y = 0
        self.gravity = 1.2
        self.jump_force = -20
        self.min_y = 50
        self.max_y = y  # sol du joueur

        # === Saut ===
        self.jump_count = 0          # nombre de sauts effectués
        self.max_jumps = 3           # double saut autorisé
        self.jump_cooldown = False   # empêche le spam de saut

    def jump(self):
        """Gère le saut (simple ou double)"""
        if not self.jump_cooldown and self.jump_count < self.max_jumps:
            self.velocity_y = self.jump_force
            self.jump_count += 1
            self.jump_cooldown = True
            # petit délai pour éviter double saut instantané
            self.canvas.after(150, lambda: setattr(self, 'jump_cooldown', False))

    def on_ground(self):
        """Vérifie si le joueur touche le sol"""
        x, y = self.coords()
        return y >= self.max_y

    def update(self, obstacles=None):
        """Met à jour la position du joueur"""
        # Gravité
        self.velocity_y += self.gravity
        self.canvas.move(self.id, 0, self.velocity_y)
        x, y = self.coords()

        # Limite haute
        if y < self.min_y:
            self.canvas.coords(self.id, self.x, self.min_y)
            self.velocity_y = 0

        # Limite basse (sol)
        if y > self.max_y:
            self.canvas.coords(self.id, self.x, self.max_y)
            self.velocity_y = 0
            self.jump_count = 0  # 🔹 reset du saut quand on retombe

        # 🔹 Gestion du saut sur obstacle (si présent)
        if obstacles:
            for obs in obstacles:
                ox, oy = obs.coords()
                if abs(x - ox) < 60 and 0 < (oy - y) < 70 and self.velocity_y > 0:
                    # Joueur tombe sur l’obstacle
                    self.canvas.coords(self.id, self.x, oy - 70)
                    self.velocity_y = 0
                    self.jump_count = 0
                    break

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

    def coords(self):
        return self.canvas.coords(self.id)
