import pygame

pygame.mixer.init(44100, -16, 1, 1024)
pygame.mixer.music.load("samples/321967__n-audioman__sheep-bleat.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
   continue
