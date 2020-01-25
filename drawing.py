import pygame, random, PIL, numpy, network2, skimage
from PIL import Image
pygame.init()

#Initialization section, including creating surface, etc.
screen = pygame.display.set_mode((760,560))
orange = (255, 127,0)
screen.fill(orange, pygame.Rect(560,0,200,560))
draw_on = False
last_pos = (0, 0)
color = (255, 255, 255)
radius = 20
guess = '5'
guessstring = 'I See A ' + guess
pygame.display.set_caption('Number Guesser - Westra2020')
#Creating the message in the top right
mfont = pygame.font.Font('freesansbold.ttf', 14)
text = mfont.render('Press E to Erase', True, color)
textrect = text.get_rect()
textrect.center = (660, 40)

#Initial render of display message
mfont2 = pygame.font.Font('freesansbold.ttf', 30)
text2 = mfont2.render(guessstring, True, color)
text2rect = text2.get_rect()
text2rect.center = (660, 280)

#render the two messages
screen.blit(text, textrect)
screen.blit(text2, text2rect)

#load neural network
nnet = network2.load("finalnetwork.json")

#separate drawing area from other area
drawing_area = screen.subsurface(pygame.Rect(0,0,560,560))

#for drawing a line between circles (so to get a smooth line)
def roundline(srf, color, start, end, radius=1):
    dx = end[0]-start[0]
    dy = end[1]-start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int( start[0]+float(i)/distance*dx)
        y = int( start[1]+float(i)/distance*dy)
        pygame.draw.circle(srf, color, (x, y), radius)
#game loop
try:
    while True:
        e = pygame.event.wait()
        keys = pygame.key.get_pressed()
        #event statement to 'erase' screen (really just paint over it)
        if keys[pygame.K_e]:
            screen.fill((0,0,0), pygame.Rect(0,0,560,560))
        #redundant, but turns the color of the drawer white
        if keys[pygame.K_p]:
            color = (255, 255, 255)
            radius = 20
        #stop program
        if e.type == pygame.QUIT:
            raise StopIteration
        #draw event
        if e.type == pygame.MOUSEBUTTONDOWN and e.pos[0]<560:
            pygame.draw.circle(screen, color, e.pos, radius)
            draw_on = True
        #stop draw event
        if e.type == pygame.MOUSEBUTTONUP:
            draw_on = False
        #so you can only draw on first half of the screen
        if (pygame.mouse.get_pos())[0] >560:
                draw_on = False
        #continue draw event
        if e.type == pygame.MOUSEMOTION:
            if draw_on:
                pygame.draw.circle(screen, color, e.pos, radius)
                roundline(screen, color, e.pos, last_pos,  radius)
            last_pos = e.pos
        #update screen
        pygame.display.flip()
        
        
        ###code to handle image translation to an input for nn
        ###first, a screen capture is taken of the drawing area, and then
        ###converted to a grayscale image using pillow. then its
        ###converted to a np array, and then rescaled to a 28x28 array.
        ###Its finally converted to a flattened array (784,1) (must be reshaped as otherwise there will be problems with the input
        orignialimage = pygame.image.save(drawing_area, "image.jpg")
        pilorignialimage = PIL.Image.open("image.jpg").convert(mode = 'L')
        narray = numpy.array(pilorignialimage)
        downscaled = skimage.transform.rescale(narray, (.05,.05), anti_aliasing = True)
        flatdownscaled = (downscaled.flatten()).reshape((784,1))
        
        #find the nn output based on the array input
        guess = str(numpy.argmax(nnet.feedforward(flatdownscaled)))
        
        #code to handle the updates to the display text
        guessstring = 'I See... '+guess
        mfont2 = pygame.font.Font('freesansbold.ttf', 30)
        text2 = mfont2.render(guessstring, True, color)
        text2rect = text2.get_rect()
        text2rect.center = (660, 280)
        screen.fill(orange, pygame.Rect(600,200,200,100))
        screen.blit(text2,text2rect)
        
                
except StopIteration:
    pass

pygame.quit()
