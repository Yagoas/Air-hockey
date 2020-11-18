from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.core.audio import SoundLoader
import math
# Define o elemento "raquete"

class Raquete(Widget):
    """
    Define a raquete do nosso jogo. Também faz a verificação de colisão
    da raquete com a bolinha à fim de inverter sua direção.
    """

    # Cada raquete mantém seu placar
    placar = NumericProperty(0)
  
    # Carrega o som da colisão do disco com a raquete
    sound_disco_raquete = SoundLoader.load("audio/sfx-disco_raquete.mp3")

    # Define a colisão da raquete com a bola
    def rebate_bola(self, bola):

        dx = self.center_x - bola.center_x
        dy = self.center_y - bola.center_y
        distancia = math.hypot(dx, dy)
        acc = 3

        # Verifica se houve a colisão do widget "raquete" com o widget "bola"
        if distancia < (self.width + bola.width)/2:
            
            # Toca o áudio da colisão disco - raquete
            if self.sound_disco_raquete:
                self.sound_disco_raquete.play()
            
            bola.velocidade = 0, 0
            bx, by = bola.pos
            rx, ry = self.pos
            teste_x = (bx - rx)/(math.pi**2) + bx
            teste_y = (by - ry)/(math.pi**2) + by

            vetor_x = (bx - teste_x)*acc
            vetor_y = (by - teste_y)*acc

            bola.velocidade = (-vetor_x) , (-vetor_y) 