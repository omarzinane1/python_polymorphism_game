import tkinter as tk
from PIL import Image, ImageTk
import random
from player import Player
from obstacle import Cactus, Rock, Flying, Special

# === Fenêtre ===
root = tk.Tk()
root.title("🏜️ Desert Runner - Omar Edition")
root.geometry("1000x500")
root.resizable(False, False)

# === Canvas ===
canvas = tk.Canvas(root, width=1000, height=500, highlightthickness=0)
canvas.pack()

# === Images ===
def load_image(path, size=None):
    img = Image.open(path)
    if size:
        img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

background_img = load_image("assets/background2.png")
player_img = load_image("assets/player2.png", (70, 70))
cactus_img = load_image("assets/cactus.png", (90, 100))
rock_img = load_image("assets/rock.png", (90, 100))
bird_img = load_image("assets/bird.png", (50, 50))
special_img = load_image("assets/special.png", (100,120))

# === Variables ===
player_x = 880
player_y = 350
player = None
score = 0
score_text = None
health_bar = None
game_running = False
obstacles = []

# === Fond ===
canvas.create_image(0, 0, image=background_img, anchor="nw")

# === Fonctions ===
def jump():
    if player:
        player.jump()

def update_health_bar():
    global health_bar
    if health_bar:
        canvas.delete(health_bar)
    health_bar = canvas.create_rectangle(player_x-45, player_y-80,
                                         player_x-45 + (player.health/100)*90, player_y-70, fill="green")

def check_collision(a, b):
    x1, y1 = a.coords()
    x2, y2 = b.coords()
    return abs(x1 - x2) < 45 and abs(y1 - y2) < 45

def create_obstacle():
    if not game_running:
        return
    obs_class = random.choice([Cactus, Rock])
    obs_img = cactus_img if obs_class==Cactus else rock_img
    obs = obs_class(canvas, -50, 360, obs_img)
    obstacles.append(obs)
    root.after(random.randint(1000,1600), create_obstacle)

def create_flying_obstacle():
    if not game_running:
        return
    if random.random() < 0.7:
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
    if score >= 100:
        game_win()
        return
    root.after(30, move_obstacles)

def update_player():
    if not game_running:
        return
    player.update()
    root.after(20, update_player)

# === Démarrage et boutons ===
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
    canvas.create_image(0,0,image=background_img, anchor="nw")
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
    canvas.create_image(0,0,image=background_img, anchor="nw")
    canvas.create_rectangle(0,0,1000,500,fill="#000",stipple="gray50")
    canvas.create_text(500,150,text="🎉 YOU WIN! 🎉", font=("Impact",48,"bold"), fill="#00FF00")
    canvas.create_text(500,220,text=f"Your Score: {score}", font=("Arial",28,"bold"), fill="#FFD700")
    retry_btn = tk.Button(root,text="Play Again", font=("Arial",16), bg="#0A0", fg="white", command=start_game_run)
    exit_btn = tk.Button(root,text="Exit", font=("Arial",16), bg="#A00", fg="white", command=root.destroy)
    canvas.create_window(400,320,window=retry_btn)
    canvas.create_window(600,320,window=exit_btn)

def retry_game():
    canvas.delete("all")
    canvas.create_image(0,0,image=background_img, anchor="nw")
    global obstacles, player, score_text
    obstacles.clear()
    player = None
    score_text = None
    start_game_button()

# --- Buttons ---
start_btn = tk.Button(root,text="START GAME", font=("Arial",20,"bold"), bg="#222", fg="white", command=start_game_button)
start_btn.place(x=380,y=220)

jump_button = tk.Button(root,text="JUMP", font=("Arial",16,"bold"), bg="#222", fg="white",
                        activebackground="#444", activeforeground="yellow", command=jump)

root.mainloop()
