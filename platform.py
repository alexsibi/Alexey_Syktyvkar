# Импортируем библиотеку pygame
import pygame
from pygame import *
from PIL import Image
#Объявляем переменные
WIN_WIDTH = 800 #Ширина создаваемого окна
WIN_HEIGHT = 640 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#8ed4f5"
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
# Создание бабочки    
FPS = 50
screen = ''
level = []
MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR =  "#888888"
JUMP_POWER = 7
GRAVITY = 0.15 # Сила, которая будет тянуть нас вниз


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0   #скорость перемещения. 0 - стоять на месте
        self.startX = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = Surface((WIDTH,HEIGHT))
        self.image = image.load("blocks/bb.gif")
        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект
        self.yvel = 0 # скорость вертикального перемещения
        self.onGround = False # На земле ли я?        

    def update(self, left, right, up, platforms, apples):
        if up:
            if self.onGround: # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER        
        if left:
            self.xvel = -MOVE_SPEED # Лево = x- n
 
        if right:
            self.xvel = MOVE_SPEED # Право = x + n
         
        if not(left or right): # стоим, когда нет указаний идти
            self.xvel = 0
        if not self.onGround:
            self.yvel +=  GRAVITY
        
        self.onGround = False; # Мы не знаем, когда мы на земле((   
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)
        self.TakeApple(0, self.yvel, apples)
        
        self.rect.x += self.xvel # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)  
        self.TakeApple(self.xvel, 0, apples)
        
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p): # если есть пересечение платформы с игроком
    
                if xvel > 0:                      # если движется вправо
                    self.rect.right = p.rect.left # то не движется вправо
    
                if xvel < 0:                      # если движется влево
                    self.rect.left = p.rect.right # то не движется влево
    
                if yvel > 0:                      # если падает вниз
                    self.rect.bottom = p.rect.top # то не падает вниз
                    self.onGround = True          # и становится на что-то твердое
                    self.yvel = 0                 # и энергия падения пропадает
    
                if yvel < 0:                      # если движется вверх
                    self.rect.top = p.rect.bottom # то не движется вверх
                    self.yvel = 0                 # и энергия прыжка пропадает  
                    
    def TakeApple(self, xvel, yvel, apples):
        global level
        for i in range(len(apples)):
            if sprite.collide_rect(self, apples[i]): # если есть пересечение платформы с игроком
                x1 = apples[i].x // 32
                y1 = apples[i].y // 32
                level[y1] = level[y1][:x1] + ' ' + level[y1][x1 + 1:]
                apples[i].kill()
                break

# блоки
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("blocks/platform.png")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        
# цветы        
class Flower(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("blocks/apple.png")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.x = x
        self.y = y
        

def main():
    global level
    global screen
    pygame.init() # Инициация PyGame, обязательная строчка 
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("Super Mario Boy") # Пишем в шапку
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Создание видимой поверхности
                                         # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом
    bg = pygame.image.load("fon.jpg")
    screen.blit(bg, (0,0))      # Каждую итерацию необходимо всё перерисовывать 
    intro_text = ["Игра 'Бабочка собирает цветы'", "",
                      "Правила игры:",
                      "с помощью стрелок собрать бабочкой все цветы", " ",
                          "Для начала игры нажмите любую клавишу"]
    text_coord = 50
    font = pygame.font.Font(None, 30)
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height  
        screen.blit(string_rendered, intro_rect)
        
    
    pygame.display.update()     # Оновление и вывод всех изменений на экран    
    start = True
    while start: # Основной цикл программы
        for e in pygame.event.get(): # Обрабатываем события
            if e.type == QUIT:
                start = False
                again = False
                pygame.quit()
                exit(0)
                break
            elif e.type == pygame.KEYDOWN or e.type == pygame.MOUSEBUTTONDOWN:
                start = False
                break
    
    level = [
           "-------------------------",
           "-                       -",
           "-                       -",
           "-     --                -",
           "-            --         -",
           "-                       -",
           "--                      -",
           "-       --           +  -",
           "-                   --- -",
           "-                       -",
           "-       +               -",
           "-      ---              -",
           "-          +            -",
           "-          -            -",
           "-                       -",
           "-                -   +  -",
           "-                   --  -",
           "-                       -",
           "-                       -",
           "-------------------------"]
                
    again = True                                     
    while again:                                         
        pygame.display.set_caption("Super Mario Boy") # Пишем в шапку
        bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Создание видимой поверхности
                                             # будем использовать как фон
        bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом
        
        timer = pygame.time.Clock()  
    
        
        hero = Player(55,55) # создаем героя по (x,y) координатам
        left = right = False    # по умолчанию — стоим
        up = False
        entities = pygame.sprite.Group() # Все объекты
        platforms = [] # то, во что мы будем врезаться или опираться
        entities.add(hero)    
        
        flowers = pygame.sprite.Group()
        flow = []
        
        
        x = 0
        y = 0 # координаты
        for row in level: # вся строка
            for col in row: # каждый символ
                if col == "-":
                    pf = Platform(x, y)
                    entities.add(pf)
                    platforms.append(pf)
                if col == "+":
                    pf = Flower(x, y)
                    flowers.add(pf)
                    flow.append(pf)
    
                x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT    #то же самое и с высотой
            x = 0                   #на каждой новой строчке начинаем с нуля    
        running = True
        while running: # Основной цикл программы
            for e in pygame.event.get(): # Обрабатываем события
                if e.type == QUIT:
                    running = False
                    again = False
                    pygame.quit()
                    exit(0)
                    break                                        
                if e.type == KEYDOWN and e.key == K_UP:
                    up = True
                if e.type == KEYDOWN and e.key == K_LEFT:
                    left = True
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    right = True
            
            
                if e.type == KEYUP and e.key == K_UP:
                    up = False
                if e.type == KEYUP and e.key == K_RIGHT:
                    right = False
                if e.type == KEYUP and e.key == K_LEFT:
                    left = False
        
                        
            screen.blit(pygame.image.load("fon1.jpg"), (0,0))      # Каждую итерацию необходимо всё перерисовывать 
            timer.tick(60)
            
            hero.update(left, right, up, platforms, flow) # передвижение
            entities.draw(screen) # отображени   
            flowers.draw(screen)
            if len(flowers) == 0:
                running = False
            pygame.display.update()     # обновление и вывод всех изменений на экран
            
        bg = pygame.image.load("fon.jpg")
        pygame.draw.rect(bg, (122, 213, 255), (20, 200, 150, 50), 0) 
        pygame.draw.rect(bg, (122, 213, 255), (190, 200, 150, 50), 0)
        pygame.draw.rect(bg, (122, 213, 255), (190 + 150 + 20, 200, 150, 50), 0)        
    
        screen.blit(bg, (0,0))      # Каждую итерацию необходимо всё перерисовывать 
        
        intro_text = ["", "",
                          "                  Вы выиграли!",
                          "", " ",
                              "  Начать заново        Уровень 2             Выход", ""]
        text_coord = 50
        font = pygame.font.Font(None, 30)
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height  
            screen.blit(string_rendered, intro_rect)
            
        
        pygame.display.update()     # Оновление и вывод всех изменений на экран    
        start = True
        while start: # Основной цикл программы
            for e in pygame.event.get(): # Обрабатываем события
                if e.type == QUIT:
                    start = False
                    again = False
                    pygame.quit()
                    break
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    ax, ay = e.pos
                    if ax >= 20 and ax <= 170 and ay >= 200 and ay <= 250:
                        start = False
                        level = [
                            "-------------------------",
                            "-                       -",
                            "-                       -",
                            "-     --                -",
                            "-            --         -",
                            "-                       -",
                            "--                      -",
                            "-       --           +  -",
                            "-                   --- -",
                            "-                       -",
                            "-       +               -",
                            "-      ---              -",
                            "-          +            -",
                            "-          -            -",
                            "-                       -",
                            "-                -   +  -",
                            "-                   --  -",
                            "-                       -",
                            "-                       -",
                            "-------------------------"]
                            
                        break
                    if ax >= 190 and ax <= 190 + 150 and ay >= 200 and ay <= 250:
                        start = False
                        level = [
                            "-------------------------",
                            "-                       -",
                            "-    --                 -",
                            "-             +         -",
                            "-    --      --         -",
                            "-                +      -",
                            "--              ---     -",
                            "-       +               -",
                            "-      --               -",
                            "-             --        -",
                            "-       +               -",
                            "-      ---          --  -",
                            "-             +         -",
                            "-             -         -",
                            "-                       -",
                            "-      ---       -   +  -",
                            "-                   --  -",
                            "-   +                   -",
                            "-  --        --         -",
                            "-------------------------"]
                        break                    
                    elif ax >= 190 + 170 and ax <= 190 + 170 + 150 and ay >= 200 and ay <= 250:
                        start = False
                        again = False
                        pygame.quit()    
                        break    
        

if __name__ == "__main__":
    main()