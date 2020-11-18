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

        # Calculo das distâncias entre os widgets para definir se houve colisão
        dx = self.center_x - bola.center_x
        dy = self.center_y - bola.center_y
        distancia = math.hypot(dx, dy)

        # Defini velocidade ganha pela bola (obs: achar formula para considerar "força" da colisão e usar para acc)
        acc = 3

        # Verifica se houve a colisão do widget "raquete" com o widget "bola"
        if distancia < (self.width + bola.width)/2:
            
            # Toca o áudio da colisão disco - raquete
            if self.sound_disco_raquete:
                self.sound_disco_raquete.play()
            
            # Seta velocidade da bola em 0 evitar bugs
            bola.velocidade = 0, 0

            # Pega tulpa da posição da bola na hora da colisão
            bx, by = bola.pos

            # Define um vetor resultante dados as posições e distancias no momento da colisão
            razao_x = (-dx)/(math.pi**2) + bx
            razao_y = (-dy)/(math.pi**2) + by
            vetor_x = (bx - razao_x)*acc
            vetor_y = (by - razao_y)*acc

            # Seta a velcidade da bola resultante da colisão
            bola.velocidade = (-vetor_x) , (-vetor_y) 