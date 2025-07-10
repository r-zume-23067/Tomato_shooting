import random
#タイマー関係
scene = 0
count = 0
elapsed_time = 1

#難易度
easy_mode = False
normal_mode = True
hard_mode = False

#移動
up = False
down = False
left = False
right = False

#初期座標
xs = 600
ys = 300

#出現時間
enemy_interval = 1000
enemy_timer = 0 

#初期体力
hp = 3
hp_max = 3

#当たり判定
muteki_time = 0
isHit = False

tomatos = []
enemies = []
#-------------------------------------------------------------------------#
#スコア
Score = 0

#経験値
EXP = 0

#攻撃力
AT_1 = False
AT_2 = False
AT_3 = False

AT = 0

#発射速度
SB_1 = False
SB_2 = False
SB_3 = False

SB = 0

#俊敏力
SP_1 = False
SP_2 = False
SP_3 = False

SP = 0

#生命力（HP）
HP_1 = False
HP_2 = False
HP_3 = False

#必殺技（変形）
UL_1 = False
UL_2 = False
UL_3 = False

#-------------------------------------------------------------------------#
class Bullet():
    def __init__(self, xp, yp, r, s, R, c):
        self.xpos = xp
        self.ypos = yp
        self.angle = r
        self.speed = s
        self.radius = R
        self.color_b = c
        self.delete = False

    def move(self):
        fill(self.color_b)
        stroke(0)
        strokeWeight(1)
        ellipse(self.xpos, self.ypos, self.radius * 2, self.radius * 2)
        self.xpos += self.speed * cos(self.angle)
        self.ypos += self.speed * sin(self.angle)
        if self.xpos < 0:
            self.delete = True
        if self.ypos < 0:
            self.delete = True
        if self.xpos > width:
            self.delete = True
        if self.ypos > height:
            self.delete = True
        
bullets = []
    
#-------------------------------------------------------------------------#
class Tomato():
    def __init__(self, x, y, s, c, sw, sh):
        self.xpos = x
        self.ypos = y
        self.obsize = s
        self.crown = c
        self.sword = sw
        self.shield = sh
        
    def display(self):
        tomato(self.xpos, self.ypos, self.obsize)
        if self.crown:
            crown(self.xpos, self.ypos,self.obsize)
        if self.sword:
            sword(self.xpos, self.ypos,self.obsize)
        if self.shield:
            shield(self.xpos,self.ypos,self.obsize)

#-------------------------------------------------------------------------#
class Enemy():
    def __init__(self, sp_e, hp_e, r_e, c_e):
        self.speed_e = sp_e
        self.hp_e = hp_e
        self.radius = r_e
        self.color_e = c_e
        self.reset_position()  # 初期位置の設定
        self.delete = False

    def reset_position(self):
        side = random.randint(1, 4)
        #上辺
        if side == 1:
            self.xpos_e = random.randint(0, width)
            self.ypos_e = -self.radius
        #右辺
        elif side == 2:
            self.xpos_e = width + self.radius
            self.ypos_e = random.randint(0, height)
        #下辺
        elif side == 3:
            self.xpos_e = random.randint(0, width)
            self.ypos_e = height + self.radius
        #左辺
        else:
            self.xpos_e = -self.radius
            self.ypos_e = random.randint(0, height)

    def move(self):
        global EXP
        theta = atan2(ys - self.ypos_e, xs - self.xpos_e)
        self.xpos_e += self.speed_e * cos(theta)
        self.ypos_e += self.speed_e * sin(theta)
        for bullet in bullets:
            if dist(self.xpos_e, self.ypos_e, bullet.xpos, bullet.ypos) <= self.radius + bullet.radius:
                bullet.delete = True
                self.hp_e -= 1
                if self.hp_e <= 0:
                    EXP += 1
                    self.delete = True

    def display(self):
        stroke(0)
        strokeWeight(2)
        fill(self.color_e)
        ellipse(self.xpos_e, self.ypos_e, self.radius * 2, self.radius * 2)

#-------------------------------------------------------------------------#
def find_nearest_enemy1(player1_pos, enemies):
    nearest_distance1 = 13000
    nearest_enemy1 = None
    
    if len(enemies) == 0:
        distance1 = sqrt((player1_pos[0] - xs) ** 2 + (player1_pos[1] - ys) ** 2)
        nearest_distance1 = distance1
        nearest_enemy1 = (xs,ys)
        
    for enemy in enemies:
        distance1 = sqrt((player1_pos[0] - enemy.xpos_e) ** 2 + (player1_pos[1] - enemy.ypos_e) ** 2)
        if distance1 < nearest_distance1:
            nearest_distance1 = distance1
            nearest_enemy1 = enemy
            
    return nearest_enemy1
#-------------------------------------------------------------------------#
def find_nearest_enemy2(player2_pos, enemies):
    nearest_distance2 = 13000
    nearest_enemy2 = None
    
    if len(enemies) == 0:
        distance2 = sqrt((player2_pos[0] - xs) ** 2 + (player2_pos[1] - ys) ** 2)
        nearest_distance2 = distance2
        nearest_enemy2 = (xs,ys)
        
    for enemy in enemies:
        distance2 = sqrt((player2_pos[0] - enemy.xpos_e) ** 2 + (player2_pos[1] - enemy.ypos_e) ** 2)
        if distance2 < nearest_distance2:
            nearest_distance2 = distance2
            nearest_enemy2 = enemy
            
    return nearest_enemy2
#-------------------------------------------------------------------------#
def find_nearest_enemy3(player3_pos, enemies):
    nearest_distance3 = 13000
    nearest_enemy3 = None
    
    if len(enemies) == 0:
        distance3 = sqrt((player3_pos[0] - xs) ** 2 + (player3_pos[1] - ys) ** 2)
        nearest_distance3 = distance3
        nearest_enemy3 = (xs,ys)
        
    for enemy in enemies:
        distance3 = sqrt((player3_pos[0] - enemy.xpos_e) ** 2 + (player3_pos[1] - enemy.ypos_e) ** 2)
        if distance3 < nearest_distance3:
            nearest_distance3 = distance3
            nearest_enemy3 = enemy
            
    return nearest_enemy3
#-------------------------------------------------------------------------#
def keyPressed():
    global up, down, left, right
    if scene == 10:
        if key == 'w':
            up = True
        if key == 's':
            down = True
        if key == 'a':
            left = True
        if key == 'd':
            right = True

#-------------------------------------------------------------------------# 
def keyReleased():
    global up, down, left, right
    global AT_1, AT_2, AT_3, SB_1, SB_2, SB_3, SP_1, SP_2, SP_3, HP_1, HP_2, HP_3, UL_1, UL_2, UL_3
    global AT, SB, SP, HP, UL, EXP
    if easy_mode:
        if scene == 10:
            if key == 'w':
                up = False
            if key == 's':
                down = False
            if key == 'a':
                left = False
            if key == 'd':
                right = False
            
            if key == 'e':
                fill( 0, 255, 0)
                if EXP >= 10:
                    if (AT_3 == True and AT_2 == True and AT_1 == True):
                        AT_3 = True
                        AT_2 = True
                        AT_1 = True
                        rect(30,100,130,60)
                        fill(255)
                    if (AT_2 == True and AT_3 == False and AT_1 == True):
                        AT_3 = True
                        EXP = EXP - 10
                        rect(30,100,130,60)
                        fill(255)
                    if (AT_1 == True and AT_2 == False and AT_3 == False):
                        AT_2 = True
                        EXP = EXP - 10 
                        rect(30,100,130,60)
                        fill(255)
                    if (AT_1 == False and AT_2 == False and AT_3 == False):
                        AT_1 = True
                        EXP = EXP - 10
                        rect(30,100,130,60)
                        fill(255)
                            
            if key == 'r':
                fill( 0, 255, 0)
                if EXP >= 10:
                    if (SB_3 == True and SB_2 == True and SB_1 == True):
                        SB_3 = True
                        SB_2 = True
                        SB_1 = True
                        rect(30,200,130,60)
                        fill(255)
                    if (SB_2 == True and SB_3 == False and SB_1 == True):
                        SB_3 = True
                        EXP = EXP - 10
                        rect(30,200,130,60)
                        fill(255)
                    if (SB_1 == True and SB_2 == False and SB_3 == False):
                        SB_2 = True
                        EXP = EXP - 10 
                        rect(30,200,130,60)
                        fill(255)
                    if (SB_1 == False and SB_2 == False and SB_3 == False):
                        SB_1 = True
                        EXP = EXP - 10   
                        rect(30,200,130,60)
                        fill(255)
                        
            if key == 't':
                fill( 0, 255, 0)
                if EXP >= 10:
                    if (SP_3 == True and SP_2 == True and SP_1 == True):
                        SP_3 = True
                        SP_2 = True
                        SP_1 = True
                        rect(30,300,130,60)
                        fill(255)
                    if (SP_2 == True and SP_3 == False and SP_1 == True):
                        SP_3 = True
                        EXP = EXP - 10 
                        rect(30,300,130,60)
                        fill(255)
                    if (SP_1 == True and SP_2 == False and SP_3 == False):
                        SP_2 = True
                        EXP = EXP - 10 
                        rect(30,300,130,60)
                        fill(255)
                    if (SP_1 == False and SP_2 == False and SP_3 == False):
                        SP_1 = True
                        EXP = EXP - 10   
                        rect(30,300,130,60)
                        fill(255)
                        
            if key == 'y':
                fill( 0, 255, 0)
                if EXP >= 10:
                    if (HP_3 == True and HP_2 == True and HP_1 == True):
                        HP_3 = True
                        HP_2 = True
                        HP_1 = True
                        rect(30,400,130,60)
                        fill(255)
                    if (HP_2 == True and HP_3 == False and HP_1 == True):
                        HP_3 = True
                        EXP = EXP - 10 
                        rect(30,400,130,60)
                        fill(255)
                    if (HP_1 == True and HP_2 == False and HP_3 == False):
                        HP_2 = True
                        EXP = EXP - 10
                        rect(30,400,130,60)
                        fill(255)
                    if (HP_1 == False and HP_2 == False and HP_3 == False):
                        HP_1 = True
                        EXP = EXP - 10 
                        rect(30,400,130,60)
                        fill(255)
                        
            if key == 'u':
                fill( 0, 255, 0)
                if EXP >= 30:
                    if (UL_3 == True and UL_2 == True and UL_1 == True):
                        UL_3 = True
                        UL_2 = True
                        UL_1 = True
                        rect(30,500,130,60)
                        fill(255)
                    if (UL_2 == True and UL_3 == False and UL_1 == True):
                        UL_3 = True
                        EXP = EXP - 30 
                        rect(30,500,130,60)
                        fill(255)
                    if (UL_1 == True and UL_2 == False and UL_3 == False):
                        UL_2 = True
                        EXP = EXP - 30 
                        rect(30,500,130,60)
                        fill(255)
                    if (UL_1 == False and UL_2 == False and UL_3 == False):
                        UL_1 = True
                        EXP = EXP - 30  
                        rect(30,500,130,60)
                        fill(255)
                        
        
    if normal_mode:
        if scene == 10:
            if key == 'w':
                up = False
            if key == 's':
                down = False
            if key == 'a':
                left = False
            if key == 'd':
                right = False
            
            if key == 'e':
                fill( 0, 255, 0)
                if EXP >= 30:
                    if (AT_3 == True and AT_2 == True and AT_1 == True):
                        AT_3 = True
                        AT_2 = True
                        AT_1 = True
                        rect(30,100,130,60)
                        fill(255)
                    if (AT_2 == True and AT_3 == False and AT_1 == True):
                        AT_3 = True
                        EXP = EXP - 30
                        rect(30,100,130,60)
                        fill(255)
                    if (AT_1 == True and AT_2 == False and AT_3 == False):
                        AT_2 = True
                        EXP = EXP - 30 
                        rect(30,100,130,60)
                        fill(255)
                    if (AT_1 == False and AT_2 == False and AT_3 == False):
                        AT_1 = True
                        EXP = EXP - 30
                        rect(30,100,130,60)
                        fill(255)
                            
            if key == 'r':
                fill( 0, 255, 0)
                if EXP >= 30:
                    if (SB_3 == True and SB_2 == True and SB_1 == True):
                        SB_3 = True
                        SB_2 = True
                        SB_1 = True
                        rect(30,200,130,60)
                        fill(255)
                    if (SB_2 == True and SB_3 == False and SB_1 == True):
                        SB_3 = True
                        EXP = EXP - 30
                        rect(30,200,130,60)
                        fill(255)
                    if (SB_1 == True and SB_2 == False and SB_3 == False):
                        SB_2 = True
                        EXP = EXP - 30 
                        rect(30,200,130,60)
                        fill(255)
                    if (SB_1 == False and SB_2 == False and SB_3 == False):
                        SB_1 = True
                        EXP = EXP - 30   
                        rect(30,200,130,60)
                        fill(255)
                        
            if key == 't':
                fill( 0, 255, 0)
                if EXP >= 30:
                    if (SP_3 == True and SP_2 == True and SP_1 == True):
                        SP_3 = True
                        SP_2 = True
                        SP_1 = True
                        rect(30,300,130,60)
                        fill(255)
                    if (SP_2 == True and SP_3 == False and SP_1 == True):
                        SP_3 = True
                        EXP = EXP - 30 
                        rect(30,300,130,60)
                        fill(255)
                    if (SP_1 == True and SP_2 == False and SP_3 == False):
                        SP_2 = True
                        EXP = EXP - 30 
                        rect(30,300,130,60)
                        fill(255)
                    if (SP_1 == False and SP_2 == False and SP_3 == False):
                        SP_1 = True
                        EXP = EXP - 30   
                        rect(30,300,130,60)
                        fill(255)
                        
            if key == 'y':
                fill( 0, 255, 0)
                if EXP >= 30:
                    if (HP_3 == True and HP_2 == True and HP_1 == True):
                        HP_3 = True
                        HP_2 = True
                        HP_1 = True
                        rect(30,400,130,60)
                        fill(255)
                    if (HP_2 == True and HP_3 == False and HP_1 == True):
                        HP_3 = True
                        EXP = EXP - 30 
                        rect(30,400,130,60)
                        fill(255)
                    if (HP_1 == True and HP_2 == False and HP_3 == False):
                        HP_2 = True
                        EXP = EXP - 30
                        rect(30,400,130,60)
                        fill(255)
                    if (HP_1 == False and HP_2 == False and HP_3 == False):
                        HP_1 = True
                        EXP = EXP - 30 
                        rect(30,400,130,60)
                        fill(255)
                        
            if key == 'u':
                fill( 0, 255, 0)
                if EXP >= 60:
                    if (UL_3 == True and UL_2 == True and UL_1 == True):
                        UL_3 = True
                        UL_2 = True
                        UL_1 = True
                        rect(30,500,130,60)
                        fill(255)
                    if (UL_2 == True and UL_3 == False and UL_1 == True):
                        UL_3 = True
                        EXP = EXP - 60 
                        rect(30,500,130,60)
                        fill(255)
                    if (UL_1 == True and UL_2 == False and UL_3 == False):
                        UL_2 = True
                        EXP = EXP - 60 
                        rect(30,500,130,60)
                        fill(255)
                    if (UL_1 == False and UL_2 == False and UL_3 == False):
                        UL_1 = True
                        EXP = EXP - 60  
                        rect(30,500,130,60)
                        fill(255)
                        
                        
    if hard_mode:
        if scene == 10:
            if key == 'w':
                up = False
            if key == 's':
                down = False
            if key == 'a':
                left = False
            if key == 'd':
                right = False
            
            if key == 'e':
                fill( 0, 255, 0)
                if EXP >= 60:
                    if (AT_3 == True and AT_2 == True and AT_1 == True):
                        AT_3 = True
                        AT_2 = True
                        AT_1 = True
                        rect(30,100,130,60)
                        fill(255)
                    if (AT_2 == True and AT_3 == False and AT_1 == True):
                        AT_3 = True
                        EXP = EXP - 60
                        rect(30,100,130,60)
                        fill(255)
                    if (AT_1 == True and AT_2 == False and AT_3 == False):
                        AT_2 = True
                        EXP = EXP - 60 
                        rect(30,100,130,60)
                        fill(255)
                    if (AT_1 == False and AT_2 == False and AT_3 == False):
                        AT_1 = True
                        EXP = EXP - 60
                        rect(30,100,130,60)
                        fill(255)
                            
            if key == 'r':
                fill( 0, 255, 0)
                if EXP >= 60:
                    if (SB_3 == True and SB_2 == True and SB_1 == True):
                        SB_3 = True
                        SB_2 = True
                        SB_1 = True
                        rect(30,200,130,60)
                        fill(255)
                    if (SB_2 == True and SB_3 == False and SB_1 == True):
                        SB_3 = True
                        EXP = EXP - 60
                        rect(30,200,130,60)
                        fill(255)
                    if (SB_1 == True and SB_2 == False and SB_3 == False):
                        SB_2 = True
                        EXP = EXP - 60 
                        rect(30,200,130,60)
                        fill(255)
                    if (SB_1 == False and SB_2 == False and SB_3 == False):
                        SB_1 = True
                        EXP = EXP - 60   
                        rect(30,200,130,60)
                        fill(255)
                        
            if key == 't':
                fill( 0, 255, 0)
                if EXP >= 60:
                    if (SP_3 == True and SP_2 == True and SP_1 == True):
                        SP_3 = True
                        SP_2 = True
                        SP_1 = True
                        rect(30,300,130,60)
                        fill(255)
                    if (SP_2 == True and SP_3 == False and SP_1 == True):
                        SP_3 = True
                        EXP = EXP - 60 
                        rect(30,300,130,60)
                        fill(255)
                    if (SP_1 == True and SP_2 == False and SP_3 == False):
                        SP_2 = True
                        EXP = EXP - 60 
                        rect(30,300,130,60)
                        fill(255)
                    if (SP_1 == False and SP_2 == False and SP_3 == False):
                        SP_1 = True
                        EXP = EXP - 60   
                        rect(30,300,130,60)
                        fill(255)
                        
            if key == 'y':
                fill( 0, 255, 0)
                if EXP >= 60:
                    if (HP_3 == True and HP_2 == True and HP_1 == True):
                        HP_3 = True
                        HP_2 = True
                        HP_1 = True
                        rect(30,400,130,60)
                        fill(255)
                    if (HP_2 == True and HP_3 == False and HP_1 == True):
                        HP_3 = True
                        EXP = EXP - 60 
                        rect(30,400,130,60)
                        fill(255)
                    if (HP_1 == True and HP_2 == False and HP_3 == False):
                        HP_2 = True
                        EXP = EXP - 60
                        rect(30,400,130,60)
                        fill(255)
                    if (HP_1 == False and HP_2 == False and HP_3 == False):
                        HP_1 = True
                        EXP = EXP - 60 
                        rect(30,400,130,60)
                        fill(255)
                        
            if key == 'u':
                fill( 0, 255, 0)
                if EXP >= 90:
                    if (UL_3 == True and UL_2 == True and UL_1 == True):
                        UL_3 = True
                        UL_2 = True
                        UL_1 = True
                        rect(30,500,130,60)
                        fill(255)
                    if (UL_2 == True and UL_3 == False and UL_1 == True):
                        UL_3 = True
                        EXP = EXP - 90 
                        rect(30,500,130,60)
                        fill(255)
                    if (UL_1 == True and UL_2 == False and UL_3 == False):
                        UL_2 = True
                        EXP = EXP - 90 
                        rect(30,500,130,60)
                        fill(255)
                    if (UL_1 == False and UL_2 == False and UL_3 == False):
                        UL_1 = True
                        EXP = EXP - 90  
                        rect(30,500,130,60)
                        fill(255)

        
#-------------------------------------------------------------------------#
def setup():
    size(1000, 600)
    frameRate(100)
    print("starting")
    Font = createFont(u'MS ゴシック', 30)
    textFont(Font)


#-------------------------------------------------------------------------#
def draw():
    print("Frame")
    print(frameCount)
    # タイトル画面
    if scene == 0:
        start_scene()
    # オプション画面
    if scene == 1:
        option_scene()
    # ゲーム画面１
    if scene == 10:
        game_scene()
    # Eスコア
    if scene == 100:
        scoreE_scene()
    # Dスコア
    if scene == 150:
        scoreD_scene()
    # Cスコア
    if scene == 200:
        scoreC_scene()
    # Bスコア
    if scene == 300:
        scoreB_scene()
    # Aスコア
    if scene == 400:
        scoreA_scene()
    # Sスコア
    if scene == 500:
        scoreS_scene()

#-------------------------------------------------------------------------#
def start_scene():
    global scene
    background(255)
    tomato(200,500,1)
    tomato(700,330,2.5)
    fill(255)
    rect(400, 350, 200, 50)
    rect(400, 450, 200, 50)
    textSize(35)
    strokeWeight(1)
    fill(0)
    text(u"スタート", 430, 390)
    text(u"オプション", 410, 490)
    fill(255,0,0)
    textSize(50)
    text("Tomato Shooting", 70, 100)
    fill(255)
    textSize(50)
    text("Tomato Shooting", 66, 100)
    if mousePressed:
        if ((mouseX >= 400) and (mouseX <= 600) and (mouseY >= 350) and (mouseY <= 400)):
            scene = 10
        if ((mouseX >= 400) and (mouseX <= 600) and (mouseY >= 450) and (mouseY <= 500)):
            scene = 1
    
#-------------------------------------------------------------------------#
def option_scene():
    global scene, easy_mode, normal_mode, hard_mode
    background(255)
    tomato(800,500,1)
    tomato(200,500,1.7)
    stroke(0)
    fill(255, 0, 0)
    rect(50, 30, 50, 50)
    strokeWeight(2)
    line(60, 40, 90, 70)
    line(90, 40, 60, 70)
    if mousePressed:
        if ((mouseX >= 50) and (mouseX <= 100) and (mouseY >= 30) and (mouseY <= 80)):
            scene = 0
    strokeWeight(1)
    textSize(40)
    fill(0)
    text(u"難易度選択", 140, 200)
    text("easy", 390, 145)
    text("normal", 520, 145)
    text("hard", 690, 145)
    fill(255)
    if easy_mode:
        fill(0, 255, 0)
    rect(380, 160, 100, 50)
    fill(255)

    if normal_mode:
        fill(0, 255, 0)
    rect(530, 160, 100, 50)
    fill(255)

    if hard_mode:
        fill(0, 255, 0)
    rect(680, 160, 100, 50)
    fill(255)

    if mousePressed:
        if ((mouseX >= 380) and (mouseX <= 480) and (mouseY >= 160) and (mouseY <= 210)):
            easy_mode = True
            normal_mode = False
            hard_mode = False

        if ((mouseX >= 530) and (mouseX <= 630) and (mouseY >= 160) and (mouseY <= 210)):
            easy_mode = False
            normal_mode = True
            hard_mode = False

        if ((mouseX >= 680) and (mouseX <= 780) and (mouseY >= 160) and (mouseY<= 210)):
            easy_mode = False
            normal_mode = False
            hard_mode = True


#-------------------------------------------------------------------------# 
def scoreE_scene():
    global up, down, left, right, xs, ys, bullets, count, hp, hp_max, muteki_time, isHit, scene
    global enemy_timer, enemies, EXP, tomatos, elapsed_time
    global hp, hp_max
    global scene, easy_mode, normal_mode, hard_mode
    global AT_1, AT_2, AT_3, SB_1, SB_2, SB_3, SP_1, SP_2, SP_3, HP_1, HP_2, HP_3, UL_1, UL_2, UL_3
    global AT, SB, SP, UL
    global scene, Score
    cursor()
    background(0)
    fill(255,0,0)
    textSize(70)
    text("Game Over", 140, 200)
    textSize(30)
    text(u"トマトはケチャップになった。", 500, 500)
    fill(255)
    text(u"スコア : " + str(elapsed_time), 50, 100)
    textSize(40)
    fill(255,0,0)
    text(u"ランク　E",250,100)
    noStroke()
    
#-------------------------------------------------------------------------#
def scoreD_scene():
    global up, down, left, right, xs, ys, bullets, count, hp, hp_max, muteki_time, isHit, scene
    global enemy_timer, enemies, EXP, tomatos, elapsed_time
    global hp, hp_max
    global scene, easy_mode, normal_mode, hard_mode
    global AT_1, AT_2, AT_3, SB_1, SB_2, SB_3, SP_1, SP_2, SP_3, HP_1, HP_2, HP_3, UL_1, UL_2, UL_3
    global AT, SB, SP, UL
    global scene, Score
    cursor()
    background(70)
    fill(255)
    textSize(70)
    text(u"ランク　D",140,200)
    textSize(40)
    text(u"ギリギリトマト。", 450, 450)
    fill(255)
    text(u"スコア : " + str(elapsed_time), 50, 100)
    noStroke()
    
#-------------------------------------------------------------------------#
def scoreC_scene():
    global up, down, left, right, xs, ys, bullets, count, hp, hp_max, muteki_time, isHit, scene
    global enemy_timer, enemies, EXP, tomatos, elapsed_time
    global hp, hp_max
    global scene, easy_mode, normal_mode, hard_mode
    global AT_1, AT_2, AT_3, SB_1, SB_2, SB_3, SP_1, SP_2, SP_3, HP_1, HP_2, HP_3, UL_1, UL_2, UL_3
    global AT, SB, SP, UL
    global scene, Score
    cursor()
    background(190)
    fill(255)
    textSize(70)
    text(u"ランク　C",140,200)
    textSize(40)
    text(u"まあまあなトマト。", 450, 450)
    fill(255)
    text(u"スコア : " + str(elapsed_time), 50, 100)
    noStroke()
   
    
#-------------------------------------------------------------------------#
def scoreB_scene():
    global up, down, left, right, xs, ys, bullets, count, hp, hp_max, muteki_time, isHit, scene
    global enemy_timer, enemies, EXP, tomatos, elapsed_time
    global hp, hp_max
    global scene, easy_mode, normal_mode, hard_mode
    global AT_1, AT_2, AT_3, SB_1, SB_2, SB_3, SP_1, SP_2, SP_3, HP_1, HP_2, HP_3, UL_1, UL_2, UL_3
    global AT, SB, SP, UL
    global scene, Score
    cursor()
    background(255)
    tomato(800,100,0.4)
    fill(125,160,255)
    textSize(70)
    text(u"ランク　B",140,200)
    textSize(40)
    text(u"そこそこなトマト。", 450, 450)
    fill(125,160,255)
    text(u"スコア : " + str(elapsed_time), 50, 100)
    noStroke()
    
#-------------------------------------------------------------------------#
def scoreA_scene():
    global up, down, left, right, xs, ys, bullets, count, hp, hp_max, muteki_time, isHit, scene
    global enemy_timer, enemies, EXP, tomatos, elapsed_time
    global hp, hp_max
    global scene, easy_mode, normal_mode, hard_mode
    global AT_1, AT_2, AT_3, SB_1, SB_2, SB_3, SP_1, SP_2, SP_3, HP_1, HP_2, HP_3, UL_1, UL_2, UL_3
    global AT, SB, SP, UL
    global scene, Score
    cursor()
    background(255)
    tomato(750,200,1.0)
    fill(225,255,56)
    textSize(70)
    text(u"ランク　A",140,200)
    textSize(40)
    text(u"ビッグなトマト ! !", 450, 450)
    text(u"プレイしてくれてありがとう！", 350, 500)
    text(u"スコア : " + str(elapsed_time), 50, 100)
    noStroke()
    
#-------------------------------------------------------------------------#
def scoreS_scene():
    global up, down, left, right, xs, ys, bullets, count, hp, hp_max, muteki_time, isHit, scene
    global enemy_timer, enemies, EXP, tomatos, elapsed_time
    global hp, hp_max
    global scene, easy_mode, normal_mode, hard_mode
    global AT_1, AT_2, AT_3, SB_1, SB_2, SB_3, SP_1, SP_2, SP_3, HP_1, HP_2, HP_3, UL_1, UL_2, UL_3
    global AT, SB, SP, UL
    global scene, Score
    cursor()
    background(255)
    tomato(750,200,1.0)
    tomato(200,530,0.2)
    tomato(300,500,0.3)
    tomato(600,50,0.1)
    tomato(100,500,0.2)
    tomato(400,400,0.2)
    tomato(950,500,0.2)
    tomato(50,200,0.2)
    tomato(200,300,0.2)
    fill(56,255,255)
    textSize(70)
    text(u"ランク　S",140,200)
    textSize(40)
    text(u"作者もびっくり！！", 450, 450)
    text(u"プレイしてくれてありがとう！", 350, 500)
    text(u"スコア : " + str(elapsed_time), 50, 100)
    noStroke()
    
#-------------------------------------------------------------------------#
def game_scene():
    global up, down, left, right, xs, ys, bullets, count, hp, hp_max, muteki_time, isHit, scene
    global easy_mode, normal_mode, hard_mode
    global enemy_timer, enemies, EXP, tomatos, elapsed_time
    global hp, hp_max
    global AT_1, AT_2, AT_3, SB_1, SB_2, SB_3, SP_1, SP_2, SP_3, HP_1, HP_2, HP_3, UL_1, UL_2, UL_3
    global AT, SB, SP, UL
#-------------------------------------------------------------------------#    
    player1_pos = ( xs + 80, ys)
    player2_pos = ( xs - 80, ys)
    player3_pos = ( xs, ys + 80)
#-------------------------------------------------------------------------#    
    background(255)
    count += 1
    enemy_timer += 1
    noStroke()
    fill(255)
    ellipse(xs, ys, 50, 50)
#-------------------------------------------------------------------------#    
    #発射速度
    if (SB_3 == True and SB_2 == True and SB_1 == True):
        SB = 15
    if (SB_3 == False and SB_2 == True and SB_1 == True):
        SB = 10
    if (SB_3 == False and SB_2 == False and SB_1 == True):
        SB = 5
    
    #俊敏力
    if (SP_3 == True and SP_2 == True and SP_1 == True):
        SP = 3
    if (SP_3 == False and SP_2 == True and SP_1 == True):
        SP = 2
    if (SP_3 == False and SP_2 == False and SP_1 == True):
        SP = 1
    
    #HP
    if (HP_3 == True and HP_2 == True and HP_1 == True):
        hp_max = 6
        if count % 3000 == 1:
            if hp < hp_max:
                hp = hp + 1
    if (HP_3 == False and HP_2 == True and HP_1 == True):
        hp_max = 5
        if count % 6000 == 1:
            if hp < hp_max:
                hp = hp + 1
    if (HP_3 == False and HP_2 == False and HP_1 == True):
        hp_max = 4
        if count % 9000 == 1:
            if hp < hp_max:
                hp = hp + 1
                
#-------------------------------------------------------------------------#    
    if hp > 0:
        elapsed_time = count / 100  # 経過した秒数
    
    if easy_mode:
        min_interval = 0.1
        max_interval = 5
        interval = max_interval - elapsed_time * (max_interval - min_interval) / (30 * 60)
        
    if normal_mode:
        min_interval = 0.1
        max_interval = 3
        interval = max_interval - elapsed_time * (max_interval - min_interval) / (15 * 60)        
        
    if hard_mode:
        min_interval = 0.1
        max_interval = 3
        interval = max_interval - elapsed_time * (max_interval - min_interval) / (5 * 60)
    
#-------------------------------------------------------------------------#
    if mousePressed:
        if count % (25 - SB) == 0:
            if (UL_3 == True and UL_2 == True and UL_1 == True):
                bullets.append(Bullet(xs, ys, atan2(mouseY - ys, mouseX - xs), (4 + SB / 5), 7, color(255, 0, 0)))
                bullets.append(Bullet(xs, ys, atan2(mouseY - ys, mouseX - xs) + 3.5415, (4 + SB / 5), 7, color(255, 0, 0)))
                bullets.append(Bullet(xs, ys, atan2(mouseY - ys, mouseX - xs) - 3.5415, (4 + SB / 5), 7, color(255, 0, 0)))
                bullets.append(Bullet(xs, ys, atan2(mouseY - ys, mouseX - xs) + 0.4, (4 + SB / 5), 7, color(255, 0, 0)))
                bullets.append(Bullet(xs, ys, atan2(mouseY - ys, mouseX - xs) - 0.4, (4 + SB / 5), 7, color(255, 0, 0)))
                bullets.append(Bullet(xs, ys, atan2(mouseY - ys, mouseX - xs) + 3.1415, (4 + SB / 5), 7, color(255, 0, 0)))
                
            if (UL_3 == False and UL_2 == True and UL_1 == True):
                bullets.append(Bullet(xs, ys, atan2(mouseY - ys, mouseX - xs), (4 + SB / 5), 7, color(255, 0, 0)))
                bullets.append(Bullet(xs, ys, atan2(mouseY - ys, mouseX - xs) + 3.5415, (4 + SB / 5), 7, color(255, 0, 0)))
                bullets.append(Bullet(xs, ys, atan2(mouseY - ys, mouseX - xs) - 3.5415, (4 + SB / 5), 7, color(255, 0, 0)))
                bullets.append(Bullet(xs, ys, atan2(mouseY - ys, mouseX - xs) + 3.1415, (4 + SB / 5), 7, color(255, 0, 0)))
                
            if (UL_3 == False and UL_2 == False and UL_1 == True):
                bullets.append(Bullet(xs, ys, atan2(mouseY - ys, mouseX - xs), (4 + SB / 5), 7, color(255, 0, 0)))
                bullets.append(Bullet(xs, ys, atan2(mouseY - ys, mouseX - xs) + 3.1415, (4 + SB / 5), 7, color(255, 0, 0)))
                
            if (UL_3 == False and UL_2 == False and UL_1 == False):
                bullets.append(Bullet(xs, ys, atan2(mouseY - ys, mouseX - xs), (4 + SB / 5), 7, color(255, 0, 0)))
#-------------------------------------------------------------------------#                        
    bullets = [bullet for bullet in bullets if not bullet.delete]
    for bullet in bullets:
        bullet.move()
#-------------------------------------------------------------------------#
    #トマト
    if (UL_3 == True and UL_2 == True and UL_1 == True):
        tomato3 = Tomato(xs, ys, 0.2, True, False, False)
        tomato3.display()
    
    if (UL_3 == False and UL_2 == True and UL_1 == True):
        tomato2 = Tomato(xs, ys, 0.2, False, True, False)
        tomato2.display()
    
    if (UL_3 == False and UL_2 == False and UL_1 == True):
        tomato1 = Tomato(xs, ys, 0.2, False, False, True)
        tomato1.display()
                       
    if (UL_3 == False and UL_2 == False and UL_1 == False):
        tomato0 = Tomato(xs, ys, 0.2, False, False, False)
        tomato0.display()
    
    if up:
        ys -= (2 + SP)
        if ys <= 6:
            ys += (2 + SP)
    if down:
        ys += (2 + SP)
        if ys >= height - 6:
            ys -= (2 + SP)
    if left:
        xs -= (2 + SP)
        if xs <= 200:
            xs += (2 + SP)
    if right:
        xs += (2 + SP) 
        if xs >= width - 6:
            xs -= (2 + SP)
    
    if count == 1:
        enemies.append(Enemy(0, 1000000, 0.001, color(255,255,255)))
#-------------------------------------------------------------------------#
    if easy_mode:
        if count > 6000:
            if count % 6000 == 1:
                enemies.append(Enemy(2, 1, 13, color(0, 255, 255)))
        if count > 18000:
            if count % 18000 == 1:
                enemies.append(Enemy(0.5, 50, 30, color(100, 100, 100)))
        if count > 36000:
            if count % 36000 == 1:
                enemies.append(Enemy(0.3, 100, 40, color(0, 0, 0)))
            
        if enemy_timer >= int(interval * 100) and count % 100 == 0:
            enemy_timer = 0
            num_enemies = int((max_interval - min_interval) / interval) + 1  # 同時に出現する敵の数
            for _ in range(num_enemies):
                enemies.append(Enemy(0.8, 3, 15, color(0, 255, 0)))

#-------------------------------------------------------------------------#                
    if normal_mode:
        if count > 3000:
            if count % 3000 == 1:
                enemies.append(Enemy(3, 1, 13, color(0, 255, 255)))
        if count > 18000:
            if count % 18000 == 1:
                enemies.append(Enemy(0.5, 100, 30, color(100, 100, 100)))
        if count > 36000:
            if count % 36000 == 1:
                enemies.append(Enemy(0.3, 500, 40, color(0, 0, 0)))
            
        if enemy_timer >= int(interval * 100) and count % 100 == 0:
            enemy_timer = 0
            num_enemies = int((max_interval - min_interval) / interval) + 1  # 同時に出現する敵の数
            for _ in range(num_enemies):
                enemies.append(Enemy(1, 3, 15, color(0, 255, 0)))

#-------------------------------------------------------------------------#            
    if hard_mode:
        if count > 1000:
            if count % 1000 == 1:
                enemies.append(Enemy(3, 1, 10, color(0, 255, 255)))
        if count > 18000:
            if count % 18000 == 1:
                enemies.append(Enemy(0.5, 300, 30, color(100, 100, 100)))
        if count > 36000:
            if count % 36000 == 1:
                enemies.append(Enemy(0.3, 700, 40, color(0, 0, 0)))
            
        if enemy_timer >= int(interval * 100) and count % 100 == 0:
            enemy_timer = 0
            num_enemies = int((max_interval - min_interval) / interval) + 1  # 同時に出現する敵の数
            for _ in range(num_enemies):
                enemies.append(Enemy(1, 3, 15, color(0, 255, 0)))

#-------------------------------------------------------------------------#    
    for enemy in enemies:
        enemy.display()
        enemy.move()
   
    nearest_enemy1 = find_nearest_enemy1(player1_pos, enemies)
    nearest_enemy2 = find_nearest_enemy2(player2_pos, enemies)
    nearest_enemy3 = find_nearest_enemy3(player3_pos, enemies)
    enemies = [enemy for enemy in enemies if not enemy.delete]
    
#-------------------------------------------------------------------------#    
    
    if (AT_3 == True and AT_2 == True and AT_1 == True):
        if count > 100:
            if count % 100 == 1:
                direction1 = atan2(nearest_enemy1.ypos_e - ys, nearest_enemy1.xpos_e - (xs + 80))
                bullets.append(Bullet(xs + 80, ys, direction1, (4 + SB / 5), 6, color(140, 140, 0)))
        if count > 50:
            if count % 50 == 1:
                direction2 = atan2(nearest_enemy2.ypos_e - ys, nearest_enemy2.xpos_e - (xs - 80))
                bullets.append(Bullet(xs - 80, ys, direction2, (4 + SB / 5), 6, color(140, 140, 0)))
        if count > 25:
            if count % 25 == 1:
                direction3 = atan2(nearest_enemy3.ypos_e - (ys + 80), nearest_enemy3.xpos_e - xs)
                bullets.append(Bullet(xs, ys + 80, direction3, (4 + SB / 5), 6, color(140, 140, 0)))
        noStroke()
        fill(255,140,140)
        ellipse(xs, ys + 80, 15, 15)
        fill(140,255,140)
        ellipse(xs - 80, ys, 15, 15)
        fill(140,140,255)
        ellipse(xs + 80, ys, 15, 15)
        stroke(0)
    
    if (AT_3 == False and AT_2 == True and AT_1 == True):
        if count > 100:
            if count % 100 == 1:
                direction1 = atan2(nearest_enemy1.ypos_e - ys, nearest_enemy1.xpos_e - (xs + 80))
                bullets.append(Bullet(xs + 80, ys, direction1, (4 + SB / 5), 6, color(140, 140, 0)))
        if count > 50:
            if count % 50 == 1:
                direction2 = atan2(nearest_enemy2.ypos_e - ys, nearest_enemy2.xpos_e - (xs - 80))
                bullets.append(Bullet(xs - 80, ys, direction2, (4 + SB / 5), 6, color(140, 140, 0)))
        noStroke()
        fill(240,255,140)
        ellipse(xs - 80, ys, 15, 15)
        fill(140,140,255)
        ellipse(xs + 80, ys, 15, 15)
        stroke(0)
    
    if (AT_3 == False and AT_2 == False and AT_1 == True):
        if count > 100:
            if count % 100 == 1:
                direction1 = atan2(nearest_enemy1.ypos_e - ys, nearest_enemy1.xpos_e - (xs + 80))
                bullets.append(Bullet(xs + 80, ys, direction1, (4 + SB / 5), 6, color(140, 140, 0)))
        noStroke()
        fill(140,140,255)
        ellipse(xs+80, ys, 15, 15)
        stroke(0)
   
    
    noStroke()
    
    fill(255,250,0)
    rect( 0, 0,194,height)
    
    stroke(0)
    strokeWeight(1)
    fill(255)
    rect(30,100,130,60)
    rect(30,200,130,60)
    rect(30,300,130,60)
    rect(30,400,130,60)
    rect(30,500,130,60)
    
    
    fill(0)
    textSize(50)
    text(u"協 E", 40, 160)
    text(u"速 R", 40, 260)
    text(u"俊 T", 40, 360)
    text(u"命 Y", 40, 460)
    text(u"変 U", 40, 560)
    textSize(20)
    
    if easy_mode:
        text("10 EXP", 40, 185)
        text("10 EXP", 40, 285)
        text("10 EXP", 40, 385)
        text("10 EXP", 40, 485)
        text("30 EXP", 40, 585)
        
    if normal_mode:
        text("30 EXP", 40, 185)
        text("30 EXP", 40, 285)
        text("30 EXP", 40, 385)
        text("30 EXP", 40, 485)
        text("60 EXP", 40, 585) 
               
    if hard_mode:
        text("60 EXP", 40, 185)
        text("60 EXP", 40, 285)
        text("60 EXP", 40, 385)
        text("60 EXP", 40, 485)
        text("90 EXP", 40, 585)
        
    fill(255)
    noStroke()
    fill(255,0,0)
    if AT_1:
        ellipse(170,110,5,5)
    if AT_2:
        ellipse(170,120,5,5)
    if AT_3:
        ellipse(170,130,5,5)

    if SB_1:
        ellipse(170,210,5,5)
    if SB_2:
        ellipse(170,220,5,5)
    if SB_3:
        ellipse(170,230,5,5)

    if SP_1:
        ellipse(170,310,5,5)
    if SP_2:
        ellipse(170,320,5,5)
    if SP_3:
        ellipse(170,330,5,5)
        
    if HP_1:
        ellipse(170,410,5,5)
    if HP_2:
        ellipse(170,420,5,5)
    if HP_3:
        ellipse(170,430,5,5)
        
    if UL_1:
        ellipse(170,510,5,5)
    if UL_2:
        ellipse(170,520,5,5)
    if UL_3:
        ellipse(170,530,5,5)
    fill(255)
    
    for j in range(hp_max):
        x = 35 + j * 50
        hp_max_heart(x, 50, 0.4)

    for j in range(hp):
        x = 35 + j * 50
        hp_heart(x, 50, 0.4)

    if (isHit == False and muteki_time == 0):
        for enemy in enemies:
            if dist(xs, ys, enemy.xpos_e, enemy.ypos_e) <= 40:
                hp -= 1
                isHit = True
                fill(255,0,0)
                rect( 0, 0, width, height)
                fill(255)

    if (isHit and muteki_time == 0):
        muteki_time = 70  # 無敵時間

    if (muteki_time > 0):
        muteki_time = muteki_time - 1
        if (muteki_time <= 0):
            muteki_time = 0
            isHit = False

    if (hp <= 0):
        if len(enemies):
            enemy.delete
        if len(bullets):
            bullet.delete
        if hard_mode:
            elapsed_time *= 3
            #Sランク
            if elapsed_time >= 1800:
                scene = 500
            #Aランク
            if 1800 > elapsed_time >= 1200:
                scene = 400
            #Bランク
            if 1200 > elapsed_time >= 600:
                scene = 300
            #Cランク
            if 600 > elapsed_time >= 360:
                scene = 200
            #Dランク
            if 360 > elapsed_time >= 120:
                scene = 150
            #Eランク
            if 120 > elapsed_time:
                scene = 100
        if normal_mode:
            elapsed_time *= 2
            #Sランク
            if elapsed_time >= 1800:
                scene = 500
            #Aランク
            if 1800 > elapsed_time >= 1200:
                scene = 400
            #Bランク
            if 1200 > elapsed_time >= 600:
                scene = 300
            #Cランク
            if 600 > elapsed_time >= 360:
                scene = 200
            #Dランク
            if 360 > elapsed_time >= 120:
                scene = 150
            #Eランク
            if 120 > elapsed_time:
                scene = 100
        if easy_mode:
            elapsed_time *= 1
            #Sランク
            if elapsed_time >= 1800:
                scene = 500
            #Aランク
            if 1800 > elapsed_time >= 1200:
                scene = 400
            #Bランク
            if 1200 > elapsed_time >= 600:
                scene = 300
            #Cランク
            if 600 > elapsed_time >= 360:
                scene = 200
            #Dランク
            if 360 > elapsed_time >= 120:
                scene = 150
            #Eランク
            if 120 > elapsed_time:
                scene = 100
            
    
    textSize(20)
    fill(0)
    textAlign(LEFT, BOTTOM)
    text("EXP: " + str(EXP), 10, 80)
    text("TIME: " + str(elapsed_time),90,80)
    if mouseX >= 200:
        noCursor()
        corsor(mouseX, mouseY)
    if mouseX < 200:
        cursor()
    


#-------------------------------------------------------------------------#
def tomato(x, y, s):
    pushMatrix()
    translate(x, y)
    #身の表示
    fill(255, 0, 0)
    noStroke()
    ellipse(-50 * s, 0 * s, 200 * s, 200 * s)
    ellipse(50 * s, 0 * s, 200 * s, 200 * s)
    rect(-50 * s, -100 * s, 100 * s, 200 * s)

    #目の表示
    fill(255, 255, 127)
    ellipse(-45 * s, -25 * s, 50 * s, 50 * s)
    ellipse(45 * s, -25 * s, 50 * s, 50 * s)
    fill(255, 255, 255)
    ellipse(40 * s, -30 * s, 20 * s, 20 * s)
    ellipse(-50 * s, -30 * s, 20 * s, 20 * s)

    #へたの表示
    #へた①
    fill(0, 255, 0)
    beginShape()
    vertex(-15 * s, -160 * s)
    vertex(0 * s, -140 * s)
    vertex(60 * s, -160 * s)
    vertex(50 * s, -125 * s)
    vertex(95 * s, -115 * s)
    vertex(50 * s, -100 * s)
    vertex(60 * s, -60 * s)
    vertex(0 * s, -95 * s)
    vertex(-70 * s, -60 * s)
    vertex(-55 * s, -105 * s)
    vertex(-100 * s, -110 * s)
    vertex(-60 * s, -125 * s)
    vertex(-70 * s, -155 * s)
    vertex(-30 * s, -140 * s)
    endShape(CLOSE)
    beginShape()
    vertex(-40 * s, -95 * s)
    vertex(0 * s, -65 * s)
    vertex(30 * s, -100 * s)
    endShape(CLOSE)

    #へた②
    fill(26, 130, 85)
    noStroke()
    scale(0.4)
    translate(-5 * s, -163 * s)
    beginShape()
    vertex(-15 * s, -163 * s)
    vertex(0 * s, -140 * s)
    vertex(60 * s, -160 * s)
    vertex(50 * s, -125 * s)
    vertex(95 * s, -115 * s)
    vertex(50 * s, -100 * s)
    vertex(60 * s, -60 * s)
    vertex(0 * s, -95 * s)
    vertex(-70 * s, -60 * s)
    vertex(-55 * s, -105 * s)
    vertex(-100 * s, -110 * s)
    vertex(-60 * s, -125 * s)
    vertex(-70 * s, -155 * s)
    vertex(-30 * s, -140 * s)
    endShape(CLOSE)
    beginShape()
    vertex(-40 * s, -95 * s)
    vertex(0 * s, -65 * s)
    vertex(30 * s, -100 * s)
    endShape(CLOSE)
    translate(5 * s, 163 * s)
    scale(2.5)
    
    #へた③
    fill(0,0,0,0)
    stroke(0,87,49)
    strokeWeight(4)
    bezier(-5*s,-110*s,-20*s,-170*s,10*s,-190*s,20*s,-170*s)
    
    #くつの表示
    fill(116,80,48)
    noStroke()
    ellipse(70*s,130*s,40*s,40*s)
    ellipse(105*s,120*s,50*s,50*s)
    beginShape()
    vertex(70*s,110*s)
    vertex(71*s,150*s)
    vertex(106*s,145*s)
    vertex(105*s,95*s)
    endShape(CLOSE)
    ellipse(-70*s,130*s,40*s,40*s)
    ellipse(-105*s,120*s,50*s,50*s)
    beginShape()
    vertex(-70*s,110*s)
    vertex(-71*s,150*s)
    vertex(-106*s,145*s)
    vertex(-105*s,95*s)
    endShape(CLOSE)
    
    #口の表示
    strokeWeight(2)
    stroke(0,0,0)
    fill(255,0,0)
    arc(0*s,30*s,20*s,20*s,radians(110),radians(320))
    arc(0*s,50*s,20*s,20*s,radians(40),radians(250))
    
    #ほっぺの表示
    fill(255,240,240)
    noStroke()
    ellipse(80*s,45*s,40*s,30*s)
    ellipse(-80*s,45*s,40*s,30*s)
    popMatrix()

def crown(x,y,s):
    pushMatrix()
    translate(x,y)
    rotate(13)
    translate(53*s,-75*s)
    scale(2.0)
    noStroke()
    fill(255,215,0)
    beginShape()
    vertex(0*s,0*s)
    vertex(20*s,0*s)
    vertex(25*s,-20*s)
    vertex(25*s,-25*s)
    vertex(15*s,-40*s)
    vertex(5*s,-25*s)
    vertex(0*s,-45*s)
    vertex(-5*s,-25*s)
    vertex(-15*s,-40*s)
    vertex(-25*s,-25*s)
    vertex(-25*s,-20*s)
    vertex(-20*s,0*s)
    endShape(CLOSE)
    rect(-15*s,-28*s,30*s,20*s)
    fill(255,0,0)
    ellipse(0*s,-45*s,7*s,7*s)
    ellipse(15*s,-40*s,7*s,7*s)
    ellipse(-15*s,-40*s,7*s,7*s)
    popMatrix()

def sword(x,y,s):
    pushMatrix()
    translate(x,y)
    rotate(13)
    scale(2.5)
    translate(65*s,-18*s)
    fill(175,175,175)
    noStroke()
    beginShape()
    vertex(0*s,-60*s)
    vertex(10*s,-45*s)
    vertex(5*s,0*s)
    vertex(-5*s,0*s)
    vertex(-10*s,-45*s)
    endShape(CLOSE)
    fill(255,215,0)
    rect(-10*s,0*s,20*s,5*s)
    rect(-15*s,5*s,30*s,5*s)
    fill(177,34,26)
    rect(-3*s,10*s,6*s,20*s)
    fill(255,215,0)
    ellipse(0*s,30*s,11*s,11*s)
    fill(243,1,0)
    ellipse(0*s,30*s,6*s,6*s)
    popMatrix()

def shield(x,y,s):
    pushMatrix()
    translate(x,y)
    rotate(13)
    translate(140*s,5*s)
    scale(1.8)
    fill(255,215,0)
    noStroke()
    beginShape()
    vertex(0*s,30*s)
    vertex(30*s,0*s)
    vertex(30*s,-60*s)
    vertex(-30*s,-60*s)
    vertex(-30*s,0*s)
    endShape(CLOSE)
    fill(101,154,210)
    scale(0.8)
    translate(0*s,-5*s)
    noStroke()
    beginShape()
    vertex(0*s,30*s)
    vertex(30*s,0*s)
    vertex(30*s,-60*s)
    vertex(-30*s,-60*s)
    vertex(-30*s,0*s)
    endShape(CLOSE)
    popMatrix()

def hp_heart(x, y, s):
    pushMatrix()
    translate(x, y)
    fill(255, 0, 0)
    stroke(0)
    strokeWeight(2)
    beginShape()
    vertex(0, 0)
    bezierVertex(-80 * s, -40 * s, -40 * s, -120 * s, 0, -80 * s)
    bezierVertex(40 * s, -120 * s, 80 * s, -40 * s, 0, 0)
    endShape()
    popMatrix()

def hp_max_heart(x, y, s):
    pushMatrix()
    translate(x, y)
    fill(150, 150, 150)
    stroke(0)
    noStroke()
    beginShape()
    vertex(0, 0)
    bezierVertex(-80 * s, -40 * s, -40 * s, -120 * s, 0, -80 * s)
    bezierVertex(40 * s, -120 * s, 80 * s, -40 * s, 0, 0)
    endShape()
    popMatrix()

def corsor(x, y):
    pushMatrix()
    translate(x, y)
    stroke(0)
    strokeWeight(2)
    line(-5, 0, 5, 0)
    line(0, 5, 0, -5)
    popMatrix()
