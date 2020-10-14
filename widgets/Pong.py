from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock
from random import randint, choice
from kivy.core.window import Window
from kivy.core.audio import SoundLoader

num = [
    -4,
    4,
]  # MATHEUS: essas variáveis vão fazer com que no começo do jogo o disco saia para uma direção aleatória
nx = choice(num)  # estão nas linhas 31 e 130
ny = randint(-3, 3)


# Definição do
class Pong(Widget):
    """
    Esse elemento contém todos os elementos do jogo (campo, raquetes e
    bolinha). Nele também está a lógica de colisão da bolinha com as
    paredes da janela à fim de atualizar o placar do jogo.
    """

    # Referencia o objeto Bola definido no nosso arquivo .kv
    bola = ObjectProperty(None)

    # Referencia os objetos Raquete definidos no nosso arquivo .kv
    raquete_1 = ObjectProperty(None)
    raquete_2 = ObjectProperty(None)

    def __init__(self, screen_manager=None):
        super(Pong, self).__init__()
        self.screen_manager = screen_manager
        Window.bind(on_keyboard=self.keyDown)

    # Põe a bola em jogo
    def servico(
        self, vel=(nx, ny), lado=0
    ):  # MATHEUS: aqui a var 'lado' vai servir para reconhecer onde a bola vai iniciar, dependendo de quem fez o último ponto
        if lado == 1:  # lado = 1, a bola começa no campo do jogador 1
            self.bola.center_x = self.width / 4
            self.bola.center_y = self.height / 2
            self.bola.velocidade = vel
        elif lado == 2:  # lado = 2, a bola começa no campo do jogador 2
            self.bola.center_x = self.width * 3 / 4
            self.bola.center_y = self.height / 2
            self.bola.velocidade = vel
        else:  # aqui a bola sai para um direção aleatória com velocidade aleatória
            # Posiciona a bola no centro da tela
            self.bola.center = self.center

            # Seta a velocidade da bola
            self.bola.velocidade = vel

    # Atualiza nosso jogo
    def atualiza(self, dt):
        sound_gol = SoundLoader.load("audio/sfx-gol.mp3")
        sound_disco_parede = SoundLoader.load("audio/sfx-disco_parade.mp3")

        # Faz a bola se mover
        self.bola.movimenta()

        # Rebate a bola caso haja colisão com a bolinha
        self.raquete_1.rebate_bola(self.bola)
        self.raquete_2.rebate_bola(self.bola)

        # Verifica se a bola atingiu o topo da janela
        if (self.bola.y < 0) or (self.bola.top > self.height):

            # Toca o áudio da colisão disco - parede
            sound_disco_parede.play()

            # Reduz a velocidade da bola caso colida com a parede
            self.bola.velocidade_y *= -0.8

        # Verifica se colidiu com o lado esquerdo da janela para atualizar o
        # placar do jogo
        if self.bola.x < self.x:
            # +1 para o placar da raquete_2
            self.raquete_2.placar += 1

            # Toca o áudio do gol
            sound_gol.play()

            if self.raquete_2.placar >= 5:
                self.servico(vel=(0, 0))
                self.raquete_1.placar = 0
                self.raquete_2.placar = 0
                self.screen_manager.current = "vencedor_2"

                return

            # Reinicia o jogo com a bola saindo pelo lado esquerdo
            self.servico(
                vel=(-1, 0), lado=1
            )  # MATHEUS: antes tava vel=(4,0) mudei pra (-1,0) pra bola sair com uma velocidade menor e pro lado esquerdo
            self.raquete_1.center_y = (
                self.center_y
            )  # a partir daqui faz as raquetes se posicionarem no centro dnv
            self.raquete_2.center_y = self.center_y
            self.raquete_1.x = self.x
            self.raquete_2.x = self.width - 90

        # Verifica se colidiu com o lado direito da janela para atualizar o
        # placar do jogo
        if self.bola.x > self.width:
            # +1 para o placar da raquete_1
            self.raquete_1.placar += 1

            # Toca o áudio do gol
            sound_gol.play()

            if self.raquete_1.placar >= 5:
                self.servico(vel=(0, 0))
                self.raquete_1.placar = 0
                self.raquete_2.placar = 0
                self.screen_manager.current = "vencedor_1"

                return

            # Reinicia o jogo com a bola saindo pelo lado direito
            self.servico(
                vel=(1, 0), lado=2
            )  # MATHEUS: antes tava (-4,0) mudei pra (1,0) pra sair pelo lado direito e com velocidade menor
            self.raquete_1.center_y = (
                self.center_y
            )  # a partir daqui as raquetes começam no meio
            self.raquete_2.center_y = self.center_y
            self.raquete_1.x = self.x
            self.raquete_2.x = self.width - 90

    # Captura o evento on_touch_move (arrastar de dedo na tela)
    def on_touch_move(self, touch):
        # Verifica se toque foi do lado esquerdo da tela
        if touch.x < self.width / 2:
            # Atualiza altura da raquete esquerda
            self.raquete_1.center_y = touch.y
            self.raquete_1.center_x = (
                touch.x
            )  # MATHEUS: aqui a raquete pode se movimentar pelo campo

        # Verifica se toque foi do lado direito da tela
        if touch.x > self.width - self.width / 2:
            # Atualiza altura da raquete direita
            self.raquete_2.center_y = touch.y
            self.raquete_2.center_x = touch.x

    # Captura o movimento pelo teclado
    def keyDown(self, a, b, keycode, *args):
        # seta para cima
        if keycode == 26:
            self.raquete_1.center_y += 10
        # seta para baixo
        if keycode == 22:
            self.raquete_1.center_y -= 10
        # seta para direita
        if keycode == 7:
            self.raquete_1.center_x += 10
        # seta para esquerda
        if keycode == 4:
            self.raquete_1.center_x -= 10
        # d
        if keycode == 79:
            self.raquete_2.center_x += 10
        # a
        if keycode == 80:
            self.raquete_2.center_x -= 10
        # w
        if keycode == 82:
            self.raquete_2.center_y += 10
        # s
        if keycode == 81:
            self.raquete_2.center_y -= 10

    def remove_btn(self, btn):

        # Remove o botão de iniciar jogo
        self.remove_widget(btn)

    def comeca_jogo(self):

        # Pôe a bola em jogo
        self.servico()

        # Agendamento da função "atualiza" a cada 1/120 = 0,008s
        Clock.schedule_interval(self.atualiza, 1.0 / 120.0)

    def reinicia_jogo(self):
        # Pôe a bola em jogo
        nx = choice(num)
        ny = randint(-3, 3)

        self.servico(vel=(nx, ny))

        self.raquete_1.placar = 0
        self.raquete_2.placar = 0

        self.raquete_1.center_y = (
            self.center_y
        )  # MATIAS: a partir daqui as raquetes começam no meio
        self.raquete_2.center_y = self.center_y
        self.raquete_1.x = self.x
        self.raquete_2.x = self.width - 90
