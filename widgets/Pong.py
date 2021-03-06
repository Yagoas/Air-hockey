from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.clock      import Clock
from random          import randint, choice
from kivy.core.audio import SoundLoader
import math

class Pong(Widget):
    """
    Esse elemento contém todos os elementos do jogo (campo, raquetes e
    bolinha). Nele também está a lógica de colisão da bolinha com as
    paredes da janela à fim de atualizar o placar do jogo.
    """
    # Variavel que define o tamanho do gol
    # diminuí um pouco o tamanho do gol pq ainda estava um pouco fora de lugar
    tamanho_do_gol = 220

    # Variaveis para verificar o modo de jogo e as opções de som
    modo = 0
    efeitos = 1

    # Carrega os efeitos sonoros
    sound_gol = SoundLoader.load("audio/sfx-gol.mp3")
    sound_vitoria = SoundLoader.load("audio/sfx-vitoria.mp3")
    sound_disco_parede = SoundLoader.load("audio/sfx-disco_parade.mp3")

    # Referencia o objeto Bola definido no nosso arquivo .kv
    bola = ObjectProperty(None)

    # Referencia os objetos Raquete definidos no nosso arquivo .kv
    raquete_1 = ObjectProperty(None)
    raquete_2 = ObjectProperty(None)

    def __init__(self, screen_manager=None):
        super(Pong, self).__init__()
        self.screen_manager = screen_manager

    # Define o modo de jogo a ser iniciado
    def modo_jogo (self, tipo):
        if tipo == 1: self.modo = 1
        elif tipo == 2: self.modo = 2

    # Define se havera som no jogo
    def efeitos_campo (self, estado):
        if estado == 1: self.efeitos = 1
        elif estado == 0: self.efeitos = 0

    # Coloca a bola em jogo
    # aqui a var 'lado' vai servir para reconhecer onde a bola vai iniciar, dependendo de quem fez o último ponto
    def servico(self, vel = (0, 0), lado = 0):
        if lado == 1:  # lado = 1, a bola começa no campo do jogador 1
            self.bola.center_x = self.width / 4 + 25
            self.bola.center_y = self.height / 2 + 25
            self.bola.velocidade = vel
        elif lado == 2:  # lado = 2, a bola começa no campo do jogador 2
            self.bola.center_x = self.width * 3 / 4 + 25
            self.bola.center_y = self.height / 2 + 25
            self.bola.velocidade = vel
        else:
            # Posiciona a bola no centro da tela
            self.bola.center_y = self.center_y + 25
            self.bola.center_x = self.center_x
            self.bola.velocidade = vel

    # Atualiza nosso jogo
    def atualiza(self, dt):
        # Verifica modo escolhido pelo jogador
        if self.modo == 1:
            # Faz a bola se mover (modo normal)
            self.bola.movimenta_atrito()

             # Rebate a bola caso haja colisão com a bolinha
            self.raquete_1.rebate_bola_impacto(self.bola, self.efeitos)
            self.raquete_2.rebate_bola_impacto(self.bola, self.efeitos)

        elif self.modo == 2:
            # Faz a bola se mover (modo hard)
            self.bola.movimenta()

            # Rebate a bola caso haja colisão com a bolinha
            self.raquete_1.rebate_bola(self.bola, self.efeitos)
            self.raquete_2.rebate_bola(self.bola, self.efeitos)

        # Verifica se a bola atingiu a parte de baixo ou de cima do campo
        if (self.bola.y < 60) or (self.bola.top > self.height):
    
            # Toca o áudio da colisão disco - parede
            if self.sound_disco_parede and self.efeitos == 1:
                self.sound_disco_parede.play()

            # Inverte a velocidade da bola caso colida com a parede
            if self.modo == 1:
                # Modo normal
               self.bola.velocidade_y *= -1.015

            elif self.modo == 2:
                # Modo hard
                self.bola.velocidade_y *= -1

        # Verifica se a bola atingiu as traves no lado esquerdo
        if self.bola.x < self.x and not self.tamanho_do_gol < self.bola.y < (self.height + self.tamanho_do_gol)/2:
            self.bola.velocidade_x *= -1
            if self.sound_disco_parede and self.efeitos == 1:
                self.sound_disco_parede.play()

        # Verifica se a bola atingiu as traves no lado direito
        if self.bola.x > self.width-self.bola.width+1 and not self.tamanho_do_gol < self.bola.y < (self.height + self.tamanho_do_gol)/2:
            self.bola.velocidade_x *= -1
            if self.sound_disco_parede and self.efeitos == 1:
                self.sound_disco_parede.play()

        # Verifica se colidiu com o gol esquerdo  para atualizar o
        # placar do jogo
        if self.bola.x < self.x and self.tamanho_do_gol < self.bola.y < (self.height + self.tamanho_do_gol)/2:
            # +1 para o placar da raquete_2
            self.raquete_2.placar += 1

            # Toca o áudio do gol
            if self.sound_gol and self.efeitos == 1:
                self.sound_gol.play()

            if self.raquete_2.placar >= 5:
                self.servico()
                self.raquete_1.placar = 0
                self.raquete_2.placar = 0
                # Aqui as raquetes voltam pra frente do gol
                # o '+25' é por causa do novo tamanho do campo
                self.raquete_1.center_y = self.center_y + 25
                self.raquete_2.center_y = self.center_y + 25
                self.raquete_1.x = self.x
                self.raquete_2.x = self.width - 90
                self.screen_manager.current = "vencedor_2"
                if self.sound_vitoria and self.efeitos == 1:
                    self.sound_vitoria.play()
                return

            # Reinicia o jogo com a bola saindo pelo lado esquerdo
            self.servico(lado=1)
            # A partir daqui as raquetes se posicionarem na frente do gol de novo
            self.raquete_1.center_y = self.center_y + 25
            self.raquete_2.center_y = self.center_y + 25
            self.raquete_1.x = self.x
            self.raquete_2.x = self.width - 90

        # Verifica se colidiu com o gol direito para atualizar o
        # placar do jogo
        if self.bola.x > self.width and self.tamanho_do_gol < self.bola.y < (self.height+self.tamanho_do_gol)/2:
            # +1 para o placar da raquete_1
            self.raquete_1.placar += 1

            # Toca o áudio do gol
            if self.sound_gol and self.efeitos == 1:
                self.sound_gol.play()

            if self.raquete_1.placar >= 5:
                self.servico()
                self.raquete_1.placar = 0
                self.raquete_2.placar = 0
                # Aqui as raquetes voltam pra frente do gol
                self.raquete_1.center_y = self.center_y + 25
                self.raquete_2.center_y = self.center_y + 25
                self.raquete_1.x = self.x
                self.raquete_2.x = self.width - 90
                self.screen_manager.current = "vencedor_1"
                if self.sound_vitoria and self.efeitos == 1:
                    self.sound_vitoria.play()
                return

            # Reinicia o jogo com a bola saindo pelo lado direito
            self.servico(lado=2)
            self.raquete_1.center_y = self.center_y + 25  # raquetes ficam na frente do gol
            self.raquete_2.center_y = self.center_y + 25
            self.raquete_1.x = self.x
            self.raquete_2.x = self.width - 90

    # Captura o evento on_touch_move (arrastar de dedo na tela)
    def on_touch_move(self, touch):       
        # Verifica se toque foi do lado esquerdo da tela
        # impede que a raquete passe os limites superior, inferior e da lateral
        if touch.x < self.width / 2 and (touch.y - 90.0/2.0 > 60 and touch.y + 90.0/2.0 < self.height and touch.x - 90/2. > self.x + 5):
            # Atualiza a posição da raquete esquerda
            self.raquete_1.center_y = touch.y
            self.raquete_1.center_x = touch.x

        # Verifica se toque foi do lado direito da tela
        # impede que a raquete passe os limites superior, inferior e da lateral
        if touch.x > self.width - self.width / 2 and (touch.y - 90.0/2.0 > 60 and touch.y + 90.0/2.0 < self.height and touch.x + 90/2. < self.width - 5):  
            # Atualiza a posição da raquete direita
            self.raquete_2.center_y = touch.y
            self.raquete_2.center_x = touch.x

    def reseta(self):
        # Zera o placar
        self.raquete_1.placar = 0
        self.raquete_2.placar = 0

        # Reposiciona as raquetes
        self.raquete_1.center_y = self.center_y + 25
        self.raquete_2.center_y = self.center_y + 25
        self.raquete_1.x = self.x
        self.raquete_2.x = self.width - 90

        # Posiciona a bola fora do campo e zera sua velocidade
        self.bola.velocidade = (0,0)
        self.bola.center_y = self.center_y + 25
        self.bola.center_x = self.center_x

        self.modo = 0

    def comeca_jogo(self):
        # Coloca a bola em jogo
        self.servico()

        # Posiciona as raquetes na frente do gol
        self.raquete_1.center_y = self.center_y + 25
        self.raquete_2.center_y = self.center_y + 25
        self.raquete_1.x = self.x
        self.raquete_2.x = self.width - 90

        # Agendamento da função "atualiza" a cada 1/60 = 0,004s
        Clock.schedule_interval(self.atualiza, 1.0 / 60.0)

    def reinicia_jogo(self):
        # Coloca a bola em jogo
        self.servico()

        # Zera o placar
        self.raquete_1.placar = 0
        self.raquete_2.placar = 0

        # Posiciona as raquetes na frente do gol
        self.raquete_1.center_y = self.center_y + 25
        self.raquete_2.center_y = self.center_y + 25
        self.raquete_1.x = self.x
        self.raquete_2.x = self.width - 90