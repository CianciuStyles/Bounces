import pygame
import random

from pygame.locals import *

class Circle(pygame.sprite.Sprite):
	def __init__(self, pos, screen_rect):
		# Call the __init__ method for the parent Sprite class
		pygame.sprite.Sprite.__init__(self)

		# Initialize the properties for the Circle
		self.pos = pos
		self.color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
		self.radius = random.randint(20, 40)
		self.x_vel = self.y_vel = random.randint(2, 7)

		# Make sure the newly created Circle is within the viewport, otherwise adjust its position to make it so
		if self.pos[0] + self.radius >= screen_rect.right:
			self.pos = (screen_rect.right - self.radius - self.x_vel, self.pos[1])
		if self.pos[0] - self.radius <= screen_rect.left:
			self.pos = (self.radius + self.x_vel, self.pos[1])
		if self.pos[1] + self.radius >= screen_rect.bottom:
			self.pos = (self.pos[0], screen_rect.bottom - self.radius - self.y_vel)
		if self.pos[1] - self.radius <= screen_rect.top:
			self.pos = (self.pos[0], self.radius + self.y_vel)

		# Randomly change the orientation of the velocities along the X-Axis or the Y-Axis
		if random.randint(0, 1) == 1:
			self.x_vel = - self.x_vel
		if random.randint(0, 1) == 1:
			self.y_vel = - self.y_vel

	def update(self, screen_rect):
		# Update the position with the current velocities along the X-Axis and the Y-Axis
		self.pos = (self.pos[0] + self.x_vel, self.pos[1] + self.y_vel)

		# Adjust the Circle position if the new position falls out the viewport
		if self.pos[0] + self.radius >= screen_rect.right:
			self.x_vel = - self.x_vel
		if self.pos[0] - self.radius <= screen_rect.left:
			self.x_vel = - self.x_vel
		if self.pos[1] + self.radius >= screen_rect.bottom:
			self.y_vel = - self.y_vel
		if self.pos[1] - self.radius <= screen_rect.top:
			self.y_vel = - self.y_vel		

	def draw(self, screen):
		# Call the Pygame primitive for drawing a Circle
		pygame.draw.circle(screen, self.color, self.pos, self.radius)

def handle_input(events, sprites, screen_rect):
	# Analyze each of the events generated by Pygame
	for event in events:
		# If the user presses the ESC or the Q key, or clicks the Exit button on the window, True is returned to make the game loop halt
		if event.type == pygame.QUIT:
			return True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_q:
				return True
			elif event.key == pygame.K_ESCAPE:
				return True

		# If the user clicks the left mouse button within the viewport, a new Circle will be added where the user clicked
		if event.type == pygame.MOUSEBUTTONDOWN:
			circle = Circle(event.pos, screen_rect)
			sprites.add(circle)

	# Returning False will make the game loop go on
	return False

def main():
	# Initiazlie the Pygame library
	pygame.init()

	# Create the window which contains the viewport in which the bouncing ball will be displayed
	screen = pygame.display.set_mode((random.randint(320, 800), random.randint(240, 600)))
	screen_rect = screen.get_rect()
	pygame.display.set_caption("Bouncing balls by CianciuStyles - Click to add a new ball, press Q or ESC to quit")
	pygame.mouse.set_visible(1)
	random.seed()

	# The endgame variable acts as the sentry variable to see if the game loop can go on or need to be halted
	endgame = False

	clock = pygame.time.Clock()
	sprites = pygame.sprite.Group()

	while not endgame:
		clock.tick(30)

		# Check if any event generated by Pygame requests the halt of the game loop
		endgame = handle_input(pygame.event.get(), sprites, screen_rect)

		# Re-paint the viewport as black
		screen.fill(Color(0, 0, 0))

		# Update the position for each of the Circles stored in the sprites Group
		sprites.update(screen_rect)

		# Draw onto the screen each of the Circles stored in the sprites Group
		for sprite in sprites:
			sprite.draw(screen)

		# Update the contents of the entire display
		pygame.display.flip()

	# If an event made the endgame variable False, then we can exit the Pygame application
	pygame.quit()


if __name__ == '__main__':
	main()