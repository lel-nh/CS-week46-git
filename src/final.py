import csv
import pygame
import random
import os
import serial
import serial.tools.list_ports
from datetime import datetime as Datetime
#classes
class Gru:
    def __init__(self,x,y):
        self.image = pygame.image.load('asset/img/gru.png')
        self.image = pygame.transform.scale(self.image, (106,200))
        self.rect = self.image.get_rect(bottomleft=(x, y))
        
    def draw(self):
        screen.blit(self.image, self.rect)
    def move(self, dx,dy=0 ):
        self.rect.x += dx
        self.rect.y += dy

class Minions:
    def __init__(self,x,y):
        #minion = choose_random_minion()
        self.image = pygame.image.load("asset/img/bob.png")
        self.image = pygame.transform.scale(self.image, (96, 100))
        self.rect = self.image.get_rect(bottomleft=(x, y-50))
        self.speed = minions_speed
    def draw(self):
        screen.blit(self.image, self.rect)
    def move(self):
        self.rect.y += self.speed
    def double(self):
        self.speed = self.speed/2
        self.image = pygame.transform.scale(self.image, (192, 200))

class Game:
    def __init__(self,score,duration):
        self.score = score
        self.duration = duration


class Player:
    def __init__(self,name,age,sexe="F",droiter=1):
        self.name = name
        self.age = age
        self.lastscore = 0
        self.highscore = 0
        self.score_total = 0
        self.droitier = 1
        self.sexe = sexe
    def player_text(self):
        return self.name + "\t\t\t" + str(self.age) + "\t\t\t" + str(self.highscore) + "\t\t\t" + str(self.lastscore)
        
#functions
#utilities

def enregistre_game(game,name):
    try:

    # Vérifier si le fichier existe déjà
        chemin_fichier = "données/"+name+".csv"
        file_exists = os.path.isfile(chemin_fichier)

    # Ouvrir le fichier en mode ajout sans toucher les deux premières lignes
        with open(chemin_fichier, mode='a', newline='') as fichier_csv:
            writer = csv.writer(fichier_csv)
        # Ajouter les données du jeu sous forme de ligne
            writer.writerow([game.score, game.duration])
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du jeu: {e}")
        pass

def draw_text(text, x, y, size=24, color=None):
    if color is None:
       color = COLOR2
    FONT = pygame.font.Font("asset/LilitaOne.ttf", size)
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, (x, y))

def check_player_collision(player_rect):
    for minion in minions[:]:
        if player_rect.colliderect(minion.rect):
            return True
    return False

def check_minion_collision(new_minion):
    for other_minion in minions:
        # Vérifie la collision uniquement si `new_minion` est différent de `other_minion`
        if new_minion != other_minion and new_minion.rect.colliderect(other_minion.rect):
            return True
    return False

def create_falling_minion():
    minion_x = random.randint(20, sizeX-100)  # Position horizontale aléatoire
    minion_y = 0  # Position verticale (commence en haut)
    minion = Minions(minion_x, minion_y)
    minions.append(minion)

def update_minions():
    global score, end, running_player
    for minion in minions:
        minion.move()
        if check_ground_collision(minion):
            
            score += 1  # Augmenter le score si un minion touche le sol
            global minions_speed
            minions_speed += 0.5
            minions.remove(minion)
        if check_player_collision(gru.rect):
            #set score to 0 if player collides with minion
            minions.clear()
            running_player.lastscore = score
            running_player.score_total += score
            if score > running_player.highscore:
                running_player.highscore = score
            this_game = Game(score,(Datetime.now()-timer).seconds)
            enregistrer_donnee(running_player)
            enregistre_game(this_game,running_player.name)
            
            global State
            end = True
        if check_minion_collision(minion):
            minions.remove(minion)
        minion.draw()

def check_ground_collision(minion):
    if minion.rect.y > sizeY-200: 
        return True
    return False

def enregistrer_donnee(player):
    # Créer le dossier "données" s'il n'existe pas
    if not os.path.exists("données"):
        os.makedirs("données")
    
    # Définir le nom du fichier pour chaque joueur
    file_path = f"données/{player.name}.csv"
    
    # En-têtes pour le fichier CSV
    fieldnames = ["Name", "Age", "LastScore", "HighScore", "ScoreTotal", "Droitier", "Sexe"]
    
    # Vérifier si le fichier existe déjà pour le joueur
    file_exists = os.path.isfile(file_path)
    
    if file_exists:
        # Si le fichier existe, on met à jour les données existantes
        with open(file_path, mode="r", newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        
        # Si le fichier contient des données, on met à jour la ligne existante
        if rows:
            rows[0]["Age"] = str(player.age)
            rows[0]["LastScore"] = str(player.lastscore)
            rows[0]["HighScore"] = str(player.highscore)
            rows[0]["ScoreTotal"] = str(player.score_total)
            rows[0]["Droitier"] = str(player.droitier)
            rows[0]["Sexe"] = str(player.sexe)


        else:
            rows.append({
                "Name": player.name,
                "Age": str(player.age),
                "LastScore": str(player.lastscore),
                "HighScore": str(player.highscore),
                "ScoreTotal": str(player.score_total),
                "Droitier": str(player.droitier),
                "Sexe": str(player.sexe),
            })
        
        # Réécrire le fichier avec les nouvelles données
        with open(file_path, mode="w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    else:
        # Si le fichier n'existe pas encore, on le crée
        with open(file_path, mode="w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                "Name": player.name,
                "Age": str(player.age),
                "LastScore": str(player.lastscore),
                "HighScore": str(player.highscore),
                "ScoreTotal": str(player.score_total),
                "Droitier": str(player.droitier),
                "Sexe": str(player.sexe),

            })


def recuperer_donnee():
    global players
    players = []
    
    # Vérifier si le dossier "données" existe
    if os.path.exists("données"):
        
        # Parcourir tous les fichiers du dossier "données"
        for file_name in os.listdir("données"):
            if file_name.endswith(".csv"):
                file_path = os.path.join("données", file_name)
                
                # Lire les données du fichier CSV pour chaque joueur
                try:
                    with open(file_path, mode="r", newline='') as file:
                        reader = csv.DictReader(file)
                        row = next(reader)  # Lire la première ligne (qui est le seul enregistrement pour chaque joueur)
                        
                        # Créer un objet Player avec les données du fichier
                        player = Player(name=row["Name"], age=int(row["Age"]))
                        player.lastscore = int(row["LastScore"])
                        player.highscore = int(row["HighScore"])
                        player.score_total = int(row["ScoreTotal"])
                        player.droitier = int(row["Droitier"])
                        player.sexe = str(row["Sexe"])
                        
                        # Ajouter l'objet Player à la liste
                        players.append(player)
                        
                except Exception as e:
                   
                   print(f"Erreur lors de la lecture du fichier {file_name}: {e}")
                   pass
    else:
        os.makedirs("données")

def msg_serial():
    if(arduino.in_waiting > 0):
        if arduino.readline().decode("utf-8").strip()=="L": 
            return "L"
        if arduino.readline().decode("utf-8").strip()=="R":
            return "R"
        
def reintialiser():
    global x_arrow, y_arrow, State, arrow, minions, players, score, minions_speed, paused, gru, running_player, indice, end, position_arrow, msg
    State = "menu"
    arrow = pygame.image.load("asset/img/arrow.png")
    arrow = pygame.transform.scale(arrow, (40, 35))
    minions = [] #minions list
    players = [] #players list
    score = 0
    minions_speed = 3
    paused = False
    gru = Gru(sizeX/2, sizeY-95)
    indice=0
    end = False 
    position_arrow = 0
    msg = ""      
    recuperer_donnee()  
#Screens
def menu(screen):
    global x_arrow, y_arrow, State, arrow
    arrow = pygame.transform.scale(arrow, (40, 35))

    screen.fill(COLOR3)
    draw_text("Minions Dodge", 200, 100, 80, COLOR4)
    draw_text("New player", 450, 300, 40, COLOR2)       
    draw_text("Start game", 500, 400, 40, COLOR2)
    draw_text("Leaderboard", 550, 500, 40, COLOR2)
    screen.blit(arrow, (x_arrow, y_arrow)) 
    
def game(screen):
        global end, score, minions_speed, running_player
        end = False
        #draw gru
        gru.draw() 
        #spawn a new minion
        if random.randint(1, int(100-score)) == 1:
            create_falling_minion()
        #update the minions
        update_minions()
        #draw the floor
        ground = pygame.draw.rect(screen, COLOR1, (50, sizeY-100, sizeX-100, 20))
        #draw the score
        draw_text("Score: " + str(score), 20, sizeY-50);
        #move the player
        keys = pygame.key.get_pressed()
        if (msg=="L" or keys[pygame.K_LEFT]) and gru.rect.left >50:
            gru.move(-(10+int(minions_speed)))
        if (msg=="R" or keys[pygame.K_RIGHT]) and gru.rect.right < sizeX-50:
            gru.move(10+int(minions_speed))



def new_player(screen):
    global State, running_player, players, timer
    
    recuperer_donnee()
    
    input_box_name = pygame.Rect(600, 300, 200, 50)
    input_box_age = pygame.Rect(600, 400, 200, 50)
    
    color_inactive = COLOR2
    color_active = COLOR5
    color_name = color_inactive
    color_age = color_inactive
    active_name = False
    active_age = False
    name_text = ''
    age_text = ''
    
    # Ajouter des variables pour les cases à cocher pour le sexe et la main dominante
    sexe_f = True   # Par défaut, sexe "F" est coché
    sexe_m = False
    droitier = True  # Par défaut, droitier est coché
    gaucher = False

    player_droitier = 1
    player_sexe = "F"
    
    # Définir les rectangles des cases à cocher
    checkbox_f = pygame.Rect(500, 500, 20, 20)
    checkbox_m = pygame.Rect(700, 500, 20, 20)
    checkbox_droitier = pygame.Rect(500, 550, 20, 20)
    checkbox_gaucher = pygame.Rect(700, 550, 20, 20)
    
    while State == "new_player":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_name.collidepoint(event.pos):
                    active_name = True
                    active_age = False
                elif input_box_age.collidepoint(event.pos):
                    active_age = True
                    active_name = False
                else:
                    active_name = False
                    active_age = False

                # Changer la couleur du champ actif
                color_name = color_active if active_name else color_inactive
                color_age = color_active if active_age else color_inactive

                # Gestion des clics pour les cases à cocher
                if checkbox_f.collidepoint(event.pos):
                    sexe_f = True
                    sexe_m = False
                elif checkbox_m.collidepoint(event.pos):
                    sexe_m = True
                    sexe_f = False
                
                if checkbox_droitier.collidepoint(event.pos):
                    droitier = True
                    gaucher = False
                elif checkbox_gaucher.collidepoint(event.pos):
                    gaucher = True
                    droitier = False

            if gaucher:
                player_droitier = 0
            if sexe_m:
                player_sexe = "M"


            if event.type == pygame.KEYDOWN:
                if active_name:
                    if event.key == pygame.K_RETURN:
                        active_name = False
                    elif event.key == pygame.K_BACKSPACE:
                        name_text = name_text[:-1]
                    else:
                        name_text += event.unicode

                if active_age:
                    if event.key == pygame.K_RETURN:
                        active_age = False
                    elif event.key == pygame.K_BACKSPACE:
                        age_text = age_text[:-1]
                    elif event.unicode.isdigit():  # Assurer que l'âge est un nombre
                        age_text += event.unicode
                        
                name_text = name_text.strip()
                if event.key == pygame.K_RETURN and name_text and age_text:
                    sexe = "F" if sexe_f else "M"
                    main_droite = 1 if droitier else 0
                    running_player = None
                
                    if len(players) > 0:
                        exist = False
                        for p in players:
                            if p.name == name_text:
                                running_player = p
                                exist = True
                        if exist==False:
                                try:
                                    # Créer une instance de Player et enregistrer
                                    player = Player(name_text, int(age_text),player_sexe,player_droitier)
                                    player.sexe = sexe
                                    player.droitier = main_droite
                                    running_player = player
                                    players.append(player)
                                    
                                except ValueError:
                                    pass
                                  #  print("Erreur : L'âge doit être un nombre entier.", 200, 500, 30, COLOR5)
                        enregistrer_donnee(running_player)
                        timer = Datetime.now()
                        State = "game"    
                    else:
                        try:
                            # Créer une instance de Player et enregistrer
                            player = Player(name_text, int(age_text),player_sexe,player_droitier)
                            player.sexe = sexe
                            player.droitier = main_droite
                            running_player = player
                            players.append(player)
                            enregistrer_donnee(player)
                            timer= Datetime.now()
                            State = "game"
                        except ValueError:
                            pass
                            #print("Erreur : L'âge doit être un nombre entier.", 200, 500, 30, COLOR5)


        # Affichage de l'écran
        screen.fill(COLOR3)
        draw_text("Entrez le nom du joueur :", 200, 300, 30, COLOR2)
        draw_text("Entrez l'âge du joueur :", 200, 400, 30, COLOR2)
        draw_text(name_text, input_box_name.x + 5, input_box_name.y + 10, 30, color_name)
        draw_text(age_text, input_box_age.x + 5, input_box_age.y + 10, 30, color_age)
        
        # Dessiner les cases à cocher
        pygame.draw.rect(screen, COLOR5 if sexe_f else COLOR2, checkbox_f)
        pygame.draw.rect(screen, COLOR5 if sexe_m else COLOR2, checkbox_m)
        pygame.draw.rect(screen, COLOR5 if droitier else COLOR2, checkbox_droitier)
        pygame.draw.rect(screen, COLOR5 if gaucher else COLOR2, checkbox_gaucher)
        
        # Ajouter des libellés pour les cases à cocher
        draw_text("F", checkbox_f.x + 30, checkbox_f.y, 30, COLOR2)
        draw_text("M", checkbox_m.x + 30, checkbox_m.y, 30, COLOR2)
        draw_text("Droitier", checkbox_droitier.x + 30, checkbox_droitier.y, 30, COLOR2)
        draw_text("Gaucher", checkbox_gaucher.x + 30, checkbox_gaucher.y, 30, COLOR2)

        # Dessiner les rectangles pour les champs de texte
        pygame.draw.rect(screen, color_name, input_box_name, 2)
        pygame.draw.rect(screen, color_age, input_box_age, 2)

        pygame.display.flip()
        clock.tick(30)

def leaderboard(screen):
    screen.fill(COLOR3)

    # Titre de la page
    draw_text("Leaderboard", 200, 100, 50, COLOR4)

    # En-têtes des colonnes (on ajoute un peu d'espacement pour l'alignement)
    draw_text("Rank", 250, 150, 30, COLOR4)
    draw_text("Name", 350, 150, 30, COLOR4)
    draw_text("HighScore", 550, 150, 30, COLOR4)

    # Récupérer les données des joueurs
    recuperer_donnee()

    # Trier les joueurs en fonction du highscore de manière décroissante
    players_sorted = sorted(players, key=lambda player: player.highscore, reverse=True)

    indice = 0
    for i, player in enumerate(players_sorted):
        # Affichage du classement (rank)
        draw_text(str(i + 1), 250, 200 + (indice * 30), 20, COLOR2)
        # Affichage du nom, highscore et dernier score
        draw_text(player.name, 350, 200 + (indice * 30), 20, COLOR2)
        draw_text(str(player.highscore), 550, 200 + (indice * 30), 20, COLOR2)
        indice += 1



#constants
COLOR1 = pygame.Color(0, 0, 0)        # Black
COLOR2 = pygame.Color(255, 255, 255)  # White
COLOR3 = pygame.Color(67, 97, 238)    # Blue
COLOR4 = pygame.Color(114, 9, 183)    # Purple
COLOR5 = pygame.Color(247, 37, 133)   # Pink

#serial

ports = serial.tools.list_ports.comports()
for port in ports:
    try :
        arduino = serial.Serial(port.device, 9600, timeout=1)
    except:
        print("No serial connection")
        pass


#Pygame
pygame.init()
pygame.mixer.init()

#music
music = ["asset/minions.mp3","asset/oiseau.mp3"]
pygame.mixer.music.load(music[random.randint(0,1)])
pygame.mixer.music.play(-1)


#create clock object
clock = pygame.time.Clock()
#set the title of the window
pygame.display.set_caption("Minions Dodge")
#the window
sizeX = 1200
sizeY = 800
screen = pygame.display.set_mode((sizeX, sizeY))

#variables
State = "menu"
x_arrow = 400
y_arrow = 305
arrow = pygame.image.load("asset/img/arrow.png")
arrow = pygame.transform.scale(arrow, (40, 35))
minions = [] #minions list
players = [] #players list
score = 0
minions_speed = 3
paused = False
gru = Gru(sizeX/2, sizeY-95)
indice=0
end = False 
global position_arrow
position_arrow = 0
msg = ""
actiondone = False
running_player = None

timer = None



runing = True
while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and State == "game" and end==False:  # Toggle pause on pressing Esc
                paused = not paused
            if State == "menu":
                if (msg=="L" or event.key == pygame.K_LEFT) and x_arrow > 400:
                    x_arrow -= 50
                    y_arrow -= 100
                if (msg=="R" or event.key == pygame.K_RIGHT) and  x_arrow < 500:
                    x_arrow += 50
                    y_arrow += 100
                if event.key == pygame.K_RETURN:
                    if y_arrow == 305:
                        State = "new_player"
                    if y_arrow == 405:
                        if running_player != None:
                            State = "game"
                            x_arrow = 225
                            y_arrow = 200 
                            position_arrow = 0
                            timer = Datetime.now()
                        else :
                            State = "new_player"
                    if y_arrow == 505:
                        State = "leaderboard"
                    actiondone = True
                    pygame.event.clear()
    
            if event.key == pygame.K_ESCAPE and end and State=="game":
                State = "menu"  
                end = False
                x_arrow = 400
                y_arrow = 305 
                score = 0
                minions_speed = 3
            if event.key == pygame.K_ESCAPE and State=="leaderboard":
                State = "menu"  
                end = False
                x_arrow = 400
                y_arrow = 305   
                score = 0
                minions_speed = 3         
    
    if State == "menu":
        reintialiser()
        menu(screen)

     
        
    if State == "game":
        screen.fill(COLOR3)
        if paused:
            # Draw pause screen
            draw_text("Paused", 200, 50, 80,COLOR4)
            draw_text("Score: " + str(score), 200, 150,60)
            draw_text("Press Esc to resume", 200, 250,30)
        if end:
            draw_text("End", 200, 50, 80,COLOR4)
            draw_text("Score: " + str(score), 200, 150,60)
            draw_text("Press Esc to return home", 200, 250,30)
            enregistrer_donnee(running_player)

        if not paused and not end:
            game(screen)
            msg = msg_serial()

    if State == "new_player":
        new_player(screen)
    if State == "leaderboard":
        leaderboard(screen)

    clock.tick(100) 
    pygame.display.update()
    
pygame.quit()


