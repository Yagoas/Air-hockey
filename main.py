#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Imports
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector     import Vector
from kivy.lang       import Builder
from kivy.config     import Config
from kivy.core.audio import SoundLoader
from widgets         import Pong, Raquete, Bola
from telas           import *
from kivy.uix.screenmanager import ScreenManager, Screen

# Carrega nosso arquivo de configurações
Config.read("config.ini")

# Cria nosso Gerenciador de Telas
screen_manager = ScreenManager()

class PongApp(App):
    # Variaveis para verificar o modo de jogo e as opções de som
    modo = 0
    efeitos = 1

    # Carrega o áudio
    sound = SoundLoader.load('audio/bg-music.mp3')

    # Pausa música
    def Stop(self):
        self.sound.stop()

    # Toca música
    def Play(self):
        if self.sound:
            self.sound.play()

    def build(self):
        self.Play()

        # Objeto do nosso jogo
        pong = Pong(screen_manager=screen_manager)

        # Cria a Tela de Jogo
        tela_jogo = TelaJogo(name="jogo")

        # Adiciona o Widget Pong
        tela_jogo.add_widget(pong)

        # Adiciona as telas ao nosso gerenciador
        screen_manager.add_widget(TelaMenu(name='menu'))
        screen_manager.add_widget(tela_jogo)
        screen_manager.add_widget(TelaModos(name='modos'))
        screen_manager.add_widget(TelaOpt(name='opt'))
        screen_manager.add_widget(TelaVencedor1(name='vencedor_1'))
        screen_manager.add_widget(TelaVencedor2(name='vencedor_2'))
        return screen_manager

if __name__ == '__main__':
    PongApp().run()
