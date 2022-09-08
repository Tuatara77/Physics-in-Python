from math import radians, sin
import pygame

FPS = 120

class Wave:
    def __init__(self, equilibrium_line, pointslist): 
        self.equilibrium_line = equilibrium_line
        self.points = pointslist

    def draw(self, surface): pygame.draw.polygon(surface, (255,255,255), self.points, 1)

    def rotate_points(self, dx, screenwidth, buffer): 
        for point in self.points: 
            point[0] += dx
            if point[0] < buffer: 
                point[0] = screenwidth-buffer-(buffer-point[0])
                self.points.append(self.points.pop(0))
            elif point[0] > screenwidth-buffer:
                point[0] = buffer+(point[0]-(screenwidth-buffer))
                self.points.insert(0, self.points.pop())

    def interfere(self, wave1, wave2):
        for point1, point2, point in zip(wave1.points, wave2.points, self.points):
            point[1] = self.equilibrium_line - (wave2.equilibrium_line-point2[1] + wave1.equilibrium_line-point1[1])


sliders = []
class Slider:
    def __init__(self, x, y, length, min, max, colour, font:str="ebrima", fontsize:int=20):
        self.x = x
        self.y = y
        self.min = min
        self.max = max
        self.length = length
        self.step = round(length/(max-min))
        self.colour = colour

        self.slider = pygame.Surface((20, 30))
        self.slider.fill(colour)
        self.sliderrect = self.slider.get_rect(center=(x,y))

        try:
            if font[-4:] == ".ttf": 
                self.font = pygame.font.Font(font, fontsize)
            else:
                self.font = pygame.font.SysFont(font, fontsize, bold=True)
        except IndexError: pass


        sliders.append(self)

    def draw(self, surface: pygame.Surface):
        pygame.draw.line(surface, self.colour, 
                         (self.x, self.y), 
                         (self.x+self.length, self.y), 1)

        slidervaltext = self.font.render(str(((self.sliderrect.centerx-self.x)//self.step)+1), True, (0,0,0))
        sliderstarttext = self.font.render(str(self.min), True, (255,255,255))
        sliderendtext = self.font.render(str(self.max), True, (255,255,255))

        self.slider.fill(self.colour)
        self.slider.blit(slidervaltext, slidervaltext.get_rect(center=(10,15)))

        surface.blit(sliderstarttext, sliderstarttext.get_rect(center=(self.x, self.y+30)))
        surface.blit(sliderendtext, sliderendtext.get_rect(center=(self.x+self.length, self.y+30)))
        surface.blit(self.slider, self.sliderrect)
    

    def getMin(self): return self.min
    def getMax(self): return self.max
    def getval(self): return ((self.sliderrect.centerx-self.x)//self.step)+1

    def slide(self, pos):
        self.sliderrect.centerx = ((pos[0]+(self.step//2)-self.x)//self.step)*self.step + self.x
        if   self.sliderrect.centerx <= self.x:             self.sliderrect.centerx = self.x
        elif self.sliderrect.centerx >= self.x+self.length: self.sliderrect.centerx = self.x+self.length


def main():
    pygame.init()
    screensize = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    bufferx = (screensize[0]-(360*(screensize[0]//360)))//2
    buffery = screensize[1]//8

    screen = pygame.display.set_mode(screensize, pygame.FULLSCREEN)
    font = pygame.font.SysFont("ebrima", 20, True)
    clock = pygame.time.Clock()

    wave1 = Wave(1*buffery, [[x+bufferx, sin(radians(x+90))*75+1*buffery] for x in range(screensize[0]-2*bufferx)])#+[[x+bufferx, sin(radians(x))*75+1*buffery+1] for x in range(screensize[0]-2*bufferx+1)[::-1]])
    wave2 = Wave(3*buffery, [[x+bufferx, sin(radians(x+270))*75+3*buffery] for x in range(screensize[0]-2*bufferx)])
    wave3 = Wave(5*buffery, [[x+bufferx, 6*buffery] for x in range(screensize[0]-2*bufferx)])

    print(wave1.points[0], wave1.points[-1])

    slider1 = Slider(screensize[0]//7, 7*buffery, screensize[0]//4, 1, 5, (255,255,255))
    slider2 = Slider(4*screensize[0]//7, 7*buffery, screensize[0]//4, 1, 5, (255,255,255))

    leftclick = False

    wave1vel = 1
    wave2vel = 1

    running = True
    while running:
        clock.tick(FPS//2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT: 
                    if slider1.sliderrect.collidepoint(pygame.mouse.get_pos()):
                        leftclick = slider1
                    elif slider2.sliderrect.collidepoint(pygame.mouse.get_pos()):
                        leftclick = slider2
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT: 
                    leftclick = False
                    wave1vel = slider1.getval()
                    wave2vel = slider2.getval()

        wave1.rotate_points(wave1vel, screensize[0], bufferx)
        wave2.rotate_points(-wave2vel, screensize[0], bufferx)
        wave3.interfere(wave1, wave2)

        if leftclick == slider1: slider1.slide(pygame.mouse.get_pos())
        elif leftclick == slider2: slider2.slide(pygame.mouse.get_pos())

        screen.fill((0,0,0))
        wave1.draw(screen)
        wave2.draw(screen)
        wave3.draw(screen)
        for slider in sliders: slider.draw(screen)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__": 
    main()