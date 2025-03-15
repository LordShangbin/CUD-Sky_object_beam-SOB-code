import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1066
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 64

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sky beam V.2")

# Set up the font
font = pygame.font.Font(None, FONT_SIZE)

# Keyboard layout
KEYBOARD_LAYOUT = [
  ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'ENTER', 'DEL'],
  ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D'],
  ['F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
]

# Function to draw the keyboard
def draw_keyboard(keys, start_x, start_y, button_width, button_height, spacing):
  buttons = []
  for row_index, row in enumerate(keys):
    for col_index, key in enumerate(row):
      y = start_y + row_index * (button_height + spacing)
      if key == 'ENTER':
        x = start_x + col_index * (button_width + spacing)
        rect = pygame.Rect(x, y, 160 + spacing, button_height)
      elif key == 'DEL':
        x = start_x + col_index * (button_width + spacing) + 102
        rect = pygame.Rect(x, y, 100 + spacing, button_height)
      else:
        x = start_x + col_index * (button_width + spacing)
        rect = pygame.Rect(x, y, button_width, button_height)
      buttons.append((key, rect))
      pygame.draw.rect(screen, BLACK, rect, 2)
      txt_surface = font.render(key, True, BLACK)
      screen.blit(txt_surface, (x + (rect.width - txt_surface.get_width()) // 2, y + (button_height - txt_surface.get_height()) // 2))
  return buttons

# Function to draw buttons
def draw_buttons(button_texts, start_x, start_y, button_width, button_height, spacing):
  buttons = []
  for i, text in enumerate(button_texts):
    x = start_x + i * (button_width + spacing)
    y = start_y
    rect = pygame.Rect(x, y, button_width, button_height)
    buttons.append((text, rect))
    pygame.draw.rect(screen, BLACK, rect, 2)
    txt_surface = font.render(text, True, BLACK)
    screen.blit(txt_surface, (x + (rect.width - txt_surface.get_width()) // 2, y + (button_height - txt_surface.get_height()) // 2))
  return buttons

def main():
  input_box = pygame.Rect(35, 20, 140, FONT_SIZE)
  color_inactive = pygame.Color('lightskyblue3')
  color_active = pygame.Color('dodgerblue2')
  color = color_inactive
  active = False
  text = ''
  done = False

  button_width = 60
  button_height = 60
  spacing = 2
  start_x = 50
  start_y = 400
  keyboard_buttons = []

  button_texts = ["Reset position"]
  button_start_x = 350
  button_start_y = 325
  button_buttons = []

  while not done:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        done = True
      elif event.type == pygame.MOUSEBUTTONUP and event.type != pygame.MOUSEWHEEL:
        if input_box.collidepoint(event.pos):
          active = True
        else:
          button_clicked = False
          for key, rect in keyboard_buttons:
            if rect.collidepoint(event.pos):
              active = True
              button_clicked = True
              if key == 'ENTER':
                print(text)
                text = ''
              elif key == 'DEL':
                text = text[:-1]
              else:
                if len(text) <= 15:
                  text += key
              break
          for button_text, rect in button_buttons:
            if rect.collidepoint(event.pos):
              if button_text == "Button 1":
                print("1")
              elif button_text == "Button 2":
                print("2")
              button_clicked = True
              break
          if not button_clicked:
            active = False
        color = color_active if active else color_inactive
      elif event.type == pygame.KEYDOWN and active:
        if event.key == pygame.K_RETURN:
          print(text)
          text = ''
        elif event.key == pygame.K_BACKSPACE:
          text = text[:-1]
        else:
          text += event.unicode

    screen.fill(WHITE)
    txt_surface = font.render(text, True, BLACK)
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 2)

    # Draw additional text to the right of the input box
    additional_texts = ["RA", "Azi calculated", "Azi read", "Latitude"]
    for i, line in enumerate(additional_texts):
      additional_surface = font.render(line, True, BLACK)
      screen.blit(additional_surface, (20, 97 + i * (FONT_SIZE - 5)))
    # Draw more additional text to the right of the input box
    additional_texts = ["DEC", "Alt calculated", "Azi read", "Longitude"]
    for i, line in enumerate(additional_texts):
      additional_surface = font.render(line, True, BLACK)
      screen.blit(additional_surface, (520, 97 + i * (FONT_SIZE - 5)))

    # Draw buttons below the additional text
    button_buttons = draw_buttons(button_texts, button_start_x, button_start_y, 450, button_height, 0)
    
    # Draw the keyboard
    keyboard_buttons = draw_keyboard(KEYBOARD_LAYOUT, start_x, start_y, button_width, button_height, spacing)

    pygame.display.flip()

  pygame.quit()
  sys.exit()

if __name__ == "__main__":
  main()