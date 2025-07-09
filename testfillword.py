import pygame

from GUI.fillWord import FillWord
def on_correct():
    print("🎉 ĐÚNG RỒI!")

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()  

fill_word = FillWord(100,100,500,500,'hello',['h','e','l','o','l','k','u','o','z','b','m'])

running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        fill_word.handle_event(event)


    screen.fill((30, 30, 30))
    fill_word.draw(screen)
    pygame.display.update()

pygame.quit()
