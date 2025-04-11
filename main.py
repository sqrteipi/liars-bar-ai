import pygame
from random import randint

global easter_egg

# Initialization
pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
dt = 0
current_state = "main"
pygame.display.set_caption("Liar's Bar (v0.0r)")
easter_egg = False

# Drawing button with text (updated for newlines and wrapping)
def dbwt(screen, button_rect, text, font_size, text_color, button_color, align, border, multiline=False):
    font = pygame.font.Font(None, font_size)
    pygame.draw.rect(screen, button_color, button_rect)
    
    if multiline:
        lines = []
        max_width = button_rect.width - 2 * border  # Account for padding
        
        # Split text by explicit newlines first
        raw_lines = text.split("\n")
        
        for raw_line in raw_lines:
            words = raw_line.split(" ")
            current_line = ""
            
            # Wrap each raw line if it exceeds max_width
            for word in words:
                test_line = current_line + word + " "
                text_surface = font.render(test_line, True, text_color)
                if text_surface.get_width() <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                lines.append(current_line.strip())
        
        # Render each line
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, text_color)
            text_rect = text_surface.get_rect()
            if align == "left":
                text_rect.topleft = (button_rect.left + border, button_rect.top + border + i * font_size)
            else:  # Default to center
                text_rect.center = (button_rect.centerx, button_rect.top + border + i * font_size)
            screen.blit(text_surface, text_rect)
    else:
        # Original single-line rendering
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        if align == "left":
            text_rect.topleft = (button_rect.left + border, button_rect.top + border)
        screen.blit(text_surface, text_rect)

# Main Screen
def main():

    easter_egg = False
    
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            screen.fill("black")

            start_button = pygame.Rect(screen_width // 2 - 200, screen_height // 2 - 50, 400, 100)
            if start_button.collidepoint(mouse_pos) and mouse_click[0]:
                game()
            elif start_button.collidepoint(mouse_pos):
                dbwt(screen, start_button, "Start", 65, "black", "gray69", "centre", 10)
            else:
                dbwt(screen, start_button, "Start", 65, "black", "white", "centre", 10)
            
        pygame.display.flip()
        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

# Main game
def game():

    # Round: Now is which player's turn (Player = 0, AI1 = 1, AI2 = 2, AI3 = 3)
    round = 0

    # Card distribution code
    q = [0, 0, 0, 0]
    k = [0, 0, 0, 0]
    a = [0, 0, 0, 0]
    j = [0, 0, 0, 0]
    p = [0, 0, 0, 0]
    card_name = [" Queen", " King ", " Ace  ", " Joker"]
    cq = 6
    ck = 6
    ca = 6
    cj = 2
    send = [0, 0, 0, 0]

    for i in range(20):
        r = randint(0, 19-i)
        if r < cq:
            q[i//5] += 1
            cq -= 1
            if i < 5:
                p[0] += 1
        elif r < cq+ck and ck != 0:
            k[i//5] += 1
            ck -= 1
            if i < 5:
                p[1] += 1
        elif r < cq+ck+ca:
            a[i//5] += 1
            ca -= 1
            if i < 5:
                p[2] += 1
        else:
            j[i//5] += 1
            cj -= 1
            if i < 5:
                p[3] += 1

    textbox_active = False
    text_input = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            # Handle text input when textbox is active
            elif textbox_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Spacebar
                    text_input += " "
                elif event.key == pygame.K_BACKSPACE: # Deleting characters
                    text_input = text_input[:-1]
                elif event.key == pygame.K_RETURN:  # Enter key for new line
                    text_input += "\n"
                elif event.unicode.isprintable():  # Accept alphanumeric characters
                    text_input += event.unicode

        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        screen.fill("black")

        if round == 0:
            for i in range(4):
                current_cards = pygame.Rect(0, i*65, 400, 50)
                card_text = "You have " + str(p[i]) + card_name[i]
                dbwt(screen, current_cards, card_text, 65, "white", "black", "left", 10)
                
                card_count_button = pygame.Rect(screen_width // 2 - 575 + i * 300, screen_height // 2 + 150, 200, 100)
                card_increase_button = pygame.Rect(screen_width // 2 - 375 + i * 300, screen_height // 2 + 150, 50, 50)
                card_decrease_button = pygame.Rect(screen_width // 2 - 375 + i * 300, screen_height // 2 + 200, 50, 50)
                send_queen_text = "Send " + str(send[i]) + card_name[i] + " out"

                dbwt(screen, card_count_button, send_queen_text, 30, "black", "gray69", "centre", 10)

                if p[i] > 0 and send[0]+send[1]+send[2]+send[3] < 3:
                    if card_increase_button.collidepoint(mouse_pos) and mouse_click[0]:
                        send[i] += 1
                        p[i] -= 1
                        textbox_active = False
                    elif card_increase_button.collidepoint(mouse_pos):
                        dbwt(screen, card_increase_button, "+1", 30, "black", "gray69", "centre", 10)
                    else:
                        dbwt(screen, card_increase_button, "+1", 30, "black", "white", "centre", 10)
                else:
                    dbwt(screen, card_increase_button, "+1", 30, "black", "gray69", "centre", 10)

                if send[i] > 0:
                    if card_decrease_button.collidepoint(mouse_pos) and mouse_click[0]:
                        send[i] -= 1
                        p[i] += 1
                        textbox_active = False
                    elif card_decrease_button.collidepoint(mouse_pos):
                        dbwt(screen, card_decrease_button, "-1", 30, "black", "gray69", "centre", 10)
                    else:
                        dbwt(screen, card_decrease_button, "-1", 30, "black", "white", "centre", 10)
                else:
                    dbwt(screen, card_decrease_button, "-1", 30, "black", "gray69", "centre", 10)
                
            textbox_frame = pygame.Rect(screen_width-800, 0, 800, 260)
            textbox = pygame.Rect(screen_width-790, 10, 780, 240)
            send_button = pygame.Rect(screen_width-800, 260, 800, 50)
            dbwt(screen, textbox_frame, "", 0, "black", "white", "left", 0)
            dbwt(screen, textbox, text_input, 30, "white", "black", "left", 10, multiline=True)
            if text_input != "":
                if send_button.collidepoint(mouse_pos) and mouse_click[0]:
                    round = 1
                    textbox_active = False
                elif send_button.collidepoint(mouse_pos):
                    dbwt(screen, send_button, "Send", 30, "black", "gray69", "centre", 10)
                else:
                    dbwt(screen, send_button, "Send", 30, "black", "white", "centre", 10)
            else:
                dbwt(screen, send_button, "Send", 30, "black", "gray69", "centre", 10)
            if textbox.collidepoint(mouse_pos) and mouse_click[0]:
                textbox_active = True

        else:
            round = round  # @kiu

        pygame.display.flip()
        dt = clock.tick(60) / 1000

main()

pygame.quit()
