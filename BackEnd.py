import pygame


class QuitFunction:

    def execute(self):
        pygame.display.quit()
        pygame.quit()
        exit()


class PayFunction:

    def execute(self):
        print("Customer payed")

class OtherFunction:

    def execute(self):
        print("Performed something else")

