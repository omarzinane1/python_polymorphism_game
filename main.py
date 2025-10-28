import tkinter as tk
from PIL import Image, ImageTk
import random
from player import Player
from obstacle import Cactus, Rock, Flying, Special

# === Fenêtre ===
root = tk.Tk()
root.title("Desert Runner - Omar Edition")
root.geometry("1000x500")
root.resizable(False, False)

canvas = tk.Canvas(root, width=1000, height=500, highlightthickness=0)
canvas.pack()

# === FONCTION : BACKGROUND ===
def draw_background():
    # ciel
    for i in range(100):
        color = f"#%02x%02x%02x" % (255 - i, 200 - i, 100 + i)
        y = int(i * 5)
        canvas.create_rectangle(0, y, 1000, y + 5, outline=color, fill=color)

    # Dunes
    canvas.create_polygon(0, 350, 200, 300, 400, 350, 700, 320, 1000, 350, 1000, 500, 0, 500,
                          fill="#f4a65a", outline="")
    canvas.create_polygon(0, 370, 250, 340, 500, 380, 800, 360, 1000, 380, 1000, 500, 0, 500,
                          fill="#e39243", outline="")

    # Sol
    canvas.create_rectangle(0, 400, 1000, 500, fill="#c16a3d", outline="")

# === NUAGES ===
clouds = []
def create_cloud(x, y, scale=1.0):
    parts = [(-70, 0, 0, 40), (-40, -18, 40, 36), (10, -8, 80, 44), (50, -20, 120, 36)]
    cloud_parts = []
    for (lx, ly, rx, ry) in parts:
        cid = canvas.create_oval(x + lx*scale, y + ly*scale,
                                 x + rx*scale, y + ry*scale,
                                 outline='', fill='white')
        cloud_parts.append(cid)
    clouds.append(cloud_parts)

def move_clouds():
    for parts in clouds:
        for cid in parts:
            canvas.move(cid, -0.7, 0)
        x1, _, x2, _ = canvas.bbox(parts[0])
        if x2 < 0:
            for cid in parts:
                canvas.move(cid, 1200, random.randint(-20, 20))
    root.after(50, move_clouds)

# === DESSIN DU BACKGROUND ===
draw_background()
for i in range(4):
    create_cloud(random.randint(0, 1000), random.randint(50, 200), scale=random.uniform(0.8, 1.3))
move_clouds()

# === Chargement images ===
def load_image(path, size=None):
    img = Image.open(path)
    if size:
        img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

player_img = load_image("assets/player2.png", (90, 90))
cactus_img = load_image("assets/cactus.png", (90, 100))
rock_img = load_image("assets/rock.png", (100, 120))
bird_img = load_image("assets/bird.png", (50, 50))
special_img = load_image("assets/special.png", (100,120))

# === VARIABLES ===
player_x = 880
player_y = 375  # position
player = None
score = 0
score_text = None
health_bar = None
game_running = False
obstacles = []

# === FONCTIONS ===
def jump():
    if player:
        player.jump()

def update_health_bar():
    global health_bar
    if health_bar:
        canvas.delete(health_bar)
    if player.health > 50:
        color = "green"
    elif player.health > 20:
        color = "orange"
    else:
        color = "red"
    health_bar = canvas.create_rectangle(player_x-45, player_y-80,
                                         player_x-45 + (player.health/100)*90, player_y-70, fill=color)

def check_collision(a, b):
    x1, y1 = a.coords()
    x2, y2 = b.coords()
    return abs(x1 - x2) < 45 and abs(y1 - y2) < 45 

def create_obstacle():
    if not game_running:
        return
    obs_class = random.choice([Cactus, Rock])
    obs_img = cactus_img if obs_class == Cactus else rock_img
    obs = obs_class(canvas, -50, 360, obs_img)
    obstacles.append(obs)
    root.after(random.randint(1000,1600), create_obstacle)

def create_flying_obstacle():
    if not game_running:
        return
    if random.random() < 0.10:
        obs = Flying(canvas, -50, random.randint(150,250), bird_img)
        obstacles.append(obs)
    if random.random() < 0.05:
        obs = Special(canvas, -50, 360, special_img)
        obstacles.append(obs)
        obs.animate()
    root.after(random.randint(2000,3000), create_flying_obstacle)

def move_obstacles():
    global score, game_running
    if not game_running:
        return
    for obs in obstacles[:]:
        obs.move()
        x, y = obs.coords()
        if x > player_x + 100:
            obs.delete()
            obstacles.remove(obs)
            score += 1
            canvas.itemconfig(score_text, text=f"Score: {score}")
            continue
        if check_collision(player, obs):
            obs.affect_player(player)
            obs.delete()
            obstacles.remove(obs)
    update_health_bar()
    if player.health <= 0:
        game_over()
        return
    if score >= 10:
        game_win()
        return
    root.after(30, move_obstacles)

def update_player():
    if not game_running:
        return
    player.update()
    root.after(20, update_player)

# === DÉMARRAGE ===
def countdown(n):
    if n>0:
        canvas.delete("countdown")
        canvas.create_text(500,250,text=str(n),font=("Arial",72,"bold"),fill="red",tag="countdown")
        root.after(1000, lambda: countdown(n-1))
    else:
        canvas.delete("countdown")
        start_game_run()

def start_game_button():
    start_btn.destroy()
    countdown(3)

def start_game_run():
    global player, score, score_text, game_running, obstacles
    game_running = True
    score = 0
    obstacles.clear()
    player = Player(canvas, player_x, player_y, player_img)
    if score_text:
        canvas.delete(score_text)
    score_text = canvas.create_text(500, 30, text="Score: 0", font=("Arial",24,"bold"), fill="#FFD700")
    update_health_bar()
    update_player()
    create_obstacle()
    create_flying_obstacle()
    move_obstacles()
    jump_button.place(x=500, y=420, anchor="center")

def game_over():
    global game_running
    game_running = False
    canvas.delete("all")
    draw_background()
    for i in range(3):
        create_cloud(random.randint(0,1000), random.randint(50,200))
    canvas.create_rectangle(0,0,1000,500,fill="#000",stipple="gray50")
    canvas.create_text(500,150,text="💀 GAME OVER 💀", font=("Impact",48,"bold"), fill="#FF3333")
    canvas.create_text(500,220,text=f"Your Score: {score}", font=("Arial",28,"bold"), fill="#FFD700")
    retry_btn = tk.Button(root,text="Retry", font=("Arial",16), bg="#0A0", fg="white", command=retry_game)
    exit_btn = tk.Button(root,text="Exit", font=("Arial",16), bg="#A00", fg="white", command=root.destroy)
    canvas.create_window(400,320,window=retry_btn)
    canvas.create_window(600,320,window=exit_btn)

def game_win():
    global game_running
    game_running = False
    canvas.delete("all")
    draw_background()
    canvas.create_rectangle(0, 0, 1000, 500, fill="#000", stipple="gray50")
    canvas.create_text(500, 150, text="🎉 YOU WIN! 🎉", font=("Impact", 48, "bold"), fill="#00FF00")
    canvas.create_text(500, 220, text=f"Your Score: {score}", font=("Arial", 28, "bold"), fill="#FFD700")

    def restart_game():
        canvas.delete("all")
        retry_btn.destroy()
        exit_btn.destroy()
        draw_background()
        start_game_run()

    retry_btn = tk.Button(root, text="Play Again", font=("Arial", 16), bg="#0A0", fg="white", command=restart_game)
    exit_btn = tk.Button(root, text="Exit", font=("Arial", 16), bg="#A00", fg="white", command=root.destroy)

    canvas.create_window(400, 320, window=retry_btn)
    canvas.create_window(600, 320, window=exit_btn)


def retry_game():
    canvas.delete("all")
    draw_background()
    global obstacles, player, score_text
    obstacles.clear()
    player = None
    score_text = None
    start_game_button()

# --- Boutons ---
start_btn = tk.Button(root,text="START GAME", font=("Arial",20,"bold"), bg="#222", fg="white", command=start_game_button)
start_btn.place(x=380,y=220)

jump_button = tk.Button(root,text="JUMP", font=("Arial",16,"bold"), bg="#222", fg="white",
                        activebackground="#444", activeforeground="yellow", command=jump)

root.mainloop()
