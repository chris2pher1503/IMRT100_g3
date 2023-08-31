import pygame
import time
import sys
import threading
image_path='MyMans.jpg'
mp3_file_path='Barbiesong.mp3'

def display_image(image_path, screen):
    image = pygame.image.load(image_path)
    image_width, image_height = image.get_rect().size

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill((0, 0, 0))
        screen.blit(image, ((screen_width - image_width) // 2, (screen_height - image_height) // 2))
        pygame.display.flip()

def play_music(mp3_file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file_path)
    pygame.mixer.music.play()
    time.sleep(30)  # Adjust the duration as needed
    pygame.mixer.music.stop()

# Initialize pygame
pygame.init()

# Set the dimensions of the screen
screen_width = 800
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the path to your MP3 file and image
mp3_file_path = 'Barbiesong.mp3'
image_path = 'MyMans.jpg'

# Start playing the music in a separate thread
music_thread = threading.Thread(target=play_music, args=(mp3_file_path,))
music_thread.start()

# Display the image
display_image(image_path, screen)

# Wait for the music thread to finish before quitting
music_thread.join()

# Quit pygame
pygame.quit()
sys.exit()
