from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector

# Define o elemento "raquete"
class Raquete(Widget):
    """
    Define a raquete do nosso jogo. Também faz a verificação de colisão
    da raquete com a bolinha à fim de inverter sua direção.
    """

    # Cada raquete mantém seu placar
    placar = NumericProperty(0)

    # Define a colisão da raquete com a bola
    def rebate_bola(self, bola):

        # Verifica se houve a colisão do widget "raquete" com o widget "bola"
        if self.collide_widget(bola):

            # Pega a tupla da velocidade da bola (velocidade_x e velocidade_y)
            vx, vy = bola.velocidade

            # Verifica se a bola bateu na parte de cima ou de baixo da raquete
            offset_raquete = (bola.center_y - self.center_y) / (self.height / 2)

            # Inverte a velocidade da bola
            inv_vel = Vector(-1 * vx, vy)

            # Verifica a velocidade e define se aumenta ou diminui a velocidade da bola
            if abs(vx + vy) <= 15:
                vel = inv_vel * 1.3
            else:
                vel = inv_vel

            # Seta a velocidade acelerada da bola, fazendo-a subir mais ou menos
            # dependendo de onde tenha batido na raquete
            bola.velocidade = vel.x, vel.y + (offset_raquete * 2)
