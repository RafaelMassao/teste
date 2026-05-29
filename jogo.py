import pygame

from pygame.locals import * #sub modulo que contem diversas constantes e funções

from sys import exit #função pra fechar a janela

from random import randint

pygame.init() #iniciar todas as variavés e funçoes do pygame

pygame.mixer.music.set_volume(0.5)
musica = pygame.mixer.music.load('assets/sounds/music.mp3')
pygame.mixer.music.play(-1)
eat=pygame.mixer.Sound('assets/sounds/eat.mp3')
eat.set_volume(0.2)
#criar nossa tela do jogo
# largura = 640
# altura = 480
# x_s = largura // 2-20
# y_s = altura // 2 -25
# # x_b = randint(40,600)
# # y_b = randint(50,430)
# speed = 10
# x_move=speed
# y_move=0

bg = pygame.image.load("assets/images/background.png")  #carregar o plano de fundo

appleimg = pygame.image.load("assets/images/apple.png") #Carrega a imagem
appleimg = pygame.transform.scale(appleimg, (20, 20)) # Redimensiona a imagem vai para a linha 143

fps=10

fonte=pygame.font.SysFont('arial',20,True,True)
GameOverFont = pygame.font.SysFont('arial', 20, True, True)
# pontos=0

# lenght_snake=5
# list_body=[]





def randonApple():
    global x_a,y_a

    x_a = randint(0, (largura - speed) // speed) * speed
    y_a = randint(2, (altura - speed) // speed) * speed
    if y_a < 40:
        y_a += 40  # Move para baixo se estiver na área do status




def reiniciar():
    global largura, altura, x_s, y_s,speed, x_move, y_move,pontos,lenght_snake,list_body, morreu,score
    largura = 640
    altura = 480
    x_s = largura // 2 - 20
    y_s = altura // 2 - 20
    speed = 20
    x_move = speed
    y_move = 0
    pontos = 0
    lenght_snake = 5
    morreu=False
    list_body = []
    randonApple()
    scorefile = open("score.txt", "r")
    score=scorefile.read()
    scorefile.close()


def grow_snake(lista_corpo):
    for XY in lista_corpo:
        # if XY[1] <= 39:
        #     pygame.draw.rect(tela, (0, 0, 0), (XY[0], XY[1], 20,20))
        if XY == lista_corpo[0]:
            pygame.draw.rect(tela, (255, 165, 25), (XY[0], XY[1], 20, 20))
        else:
            pygame.draw.rect(tela, (255, 165, 25), (XY[0], XY[1], 20, 20))

reiniciar()

tela = pygame.display.set_mode((largura,altura)) #recebe uma tupla de largura x altura
pygame.display.set_caption("Jogo")
#toodo jogo fica em um loop principal
framerate = pygame.time.Clock()

while True:
    framerate.tick(fps)
    tela.fill((255, 255, 255))
    mensagem = f"Pontos: {pontos}"
    mensagem_record = f"Record: {score}"
    texto_tela = fonte.render(mensagem, True, (255,255,255))
    texto_record = fonte.render(mensagem_record, True, (255, 255, 255))
    tela.blit(bg, (0, 0))  #COLOCAR O BG ANTES DE OUTRAS COIAS ESSE É UM BOM PONTO

    for event in pygame.event.get(): #verificar se algum evento ocorre
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if x_move == speed:
                    pass
                else:
                    x_move = -speed
                    y_move = 0


            if event.key == K_RIGHT:
                if x_move == -speed:
                    pass
                else:
                    x_move = speed
                    y_move = 0


            if event.key == K_UP:
                if y_move == speed:
                    pass
                else:
                    y_move = -speed
                    x_move = 0


            if event.key == K_DOWN:
                if y_move == -speed:
                    pass
                else:
                    y_move = speed
                    x_move = 0


    if x_s >= largura:
        x_s = 0
    if x_s < 0:
        x_s = largura-20
    if y_s >= altura:
        y_s = 40  # Evita que apareça no stats
    if y_s < 40:
        y_s = altura-20


    x_s+=x_move
    y_s+=y_move

    snake = pygame.draw.rect(tela, (255, 165, 25), (x_s, y_s, 20, 20))
    #apple = pygame.draw.rect(tela, (255, 0, 0), (x_a, y_a, 20, 20))
    apple = appleimg.get_rect() #RECEBE O RETANGULO EM TORNO DO SPRIT
    apple.topleft = (x_a, y_a) #POSICIONA O RATANGULO NO MESMO LUGAR DO SPRIT
    #hitbox=pygame.draw.rect(tela,(0,0,255),apple,2)


    if snake.colliderect(apple):
        randonApple()
        pontos+=1
        eat.play()
        lenght_snake+=1

    if pontos == 15:
        fps=12
    if pontos == 50:
        fps = 15
    grow_snake(list_body)

    list_head=[]
    list_head.append(x_s)
    list_head.append(y_s)
    list_body.append(list_head)

    if list_body.count(list_head) > 1 :


        texto_GameOVer = GameOverFont.render("GAME OVER PRESSIONE R PARA REINICIAR", True, (255, 255, 255))

        morreu=True
        if pontos > int(score):
            scorefile = open("score.txt", "w")
            scorefile.write(str(pontos))
            scorefile.close()

        tela.fill((0, 0, 0))
        while morreu:
            for event in pygame.event.get(): #verificar se algum evento ocorre
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key==K_r:
                        reiniciar()
            tela.blit(texto_GameOVer, (100, 200))
            pygame.display.flip()



    if len(list_body) > lenght_snake:
        del list_body[0]

    stats = pygame.draw.rect(tela, (0, 0, 0), (0, 0, 680, 40))
    tela.blit(texto_tela,(480,7))
    tela.blit(texto_record, (50, 7)) #blita a imagem na tela
    tela.blit(appleimg, (x_a, y_a))  #Blita a imagem da maça no msm lugar do retangulo (HitBox)

    pygame.display.flip()  #linha pra atualizar a tela

