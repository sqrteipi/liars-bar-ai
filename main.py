import pygame
import time
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
def dbwt(screen, button_rect, text, font_size, text_color, button_color, border, align="center", multiline=False):
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
                dbwt(screen, start_button, "Start", 65, "black", "gray69", 10)
            else:
                dbwt(screen, start_button, "Start", 65, "black", "white", 10)
            
        pygame.display.flip()
        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

# Main game
def game():

    # Enable key repeat: 500ms delay, 50ms interval
    pygame.key.set_repeat(500, 50)

    # Round: Now is which player's turn (Player = 0, AI1 = 1, AI2 = 2, AI3 = 3)
    round = 0

    # Card distribution code
    p = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    card_name = [" Queen", " King ", " Ace  ", " Joker"]
    cq = 6
    ck = 6
    ca = 6
    cj = 2
    send = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    for i in range(20):
        r = randint(0, 19 - i)
        if r < cq:
            cq -= 1
            p[i//5][0] += 1
        elif r < cq + ck and ck != 0:
            ck -= 1
            p[i//5][1] += 1
        elif r < cq + ck + ca:
            ca -= 1
            p[i//5][2] += 1
        else:
            cj -= 1
            p[i//5][3] += 1

    textbox_active = False
    text_input = ""
    cursor_pos = 0  # Tracks insertion point in text_input

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif textbox_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    text_input = text_input[:cursor_pos] + " " + text_input[cursor_pos:]
                    cursor_pos += 1
                elif event.key == pygame.K_BACKSPACE and cursor_pos > 0:
                    text_input = text_input[:cursor_pos-1] + text_input[cursor_pos:]
                    cursor_pos -= 1
                elif event.key == pygame.K_RETURN:
                    text_input = text_input[:cursor_pos] + "\n" + text_input[cursor_pos:]
                    cursor_pos += 1
                elif event.key == pygame.K_LEFT and cursor_pos > 0:
                    cursor_pos -= 1
                elif event.key == pygame.K_RIGHT and cursor_pos < len(text_input):
                    cursor_pos += 1
                elif event.unicode.isprintable():
                    text_input = text_input[:cursor_pos] + event.unicode + text_input[cursor_pos:]
                    cursor_pos += 1

        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        screen.fill("black")

        if round == 0:
            for i in range(4):
                current_cards = pygame.Rect(0, i*65, 400, 50)
                card_text = "You have " + str(p[0][i]) + card_name[i]
                dbwt(screen, current_cards, card_text, 65, "white", "black", 10, align="left")
                
                card_count_button = pygame.Rect(screen_width // 2 - 575 + i * 300, screen_height // 2 + 150, 200, 100)
                card_increase_button = pygame.Rect(screen_width // 2 - 375 + i * 300, screen_height // 2 + 150, 50, 50)
                card_decrease_button = pygame.Rect(screen_width // 2 - 375 + i * 300, screen_height // 2 + 200, 50, 50)
                send_queen_text = "Send " + str(send[0][i]) + card_name[i] + " out"

                dbwt(screen, card_count_button, send_queen_text, 30, "black", "gray69", 10)

                if p[0][i] > 0 and sum(send[0]) < 3:
                    if card_increase_button.collidepoint(mouse_pos) and mouse_click[0]:
                        send[0][i] += 1
                        p[0][i] -= 1
                        textbox_active = False
                        time.sleep(0.167)
                    elif card_increase_button.collidepoint(mouse_pos):
                        dbwt(screen, card_increase_button, "+1", 30, "black", "gray69", 10)
                    else:
                        dbwt(screen, card_increase_button, "+1", 30, "black", "white", 10)
                else:
                    dbwt(screen, card_increase_button, "+1", 30, "black", "gray55", 10)

                if send[0][i] > 0:
                    if card_decrease_button.collidepoint(mouse_pos) and mouse_click[0]:
                        send[0][i] -= 1
                        p[0][i] += 1
                        textbox_active = False
                        time.sleep(0.167)
                    elif card_decrease_button.collidepoint(mouse_pos):
                        dbwt(screen, card_decrease_button, "-1", 30, "black", "gray69", 10)
                    else:
                        dbwt(screen, card_decrease_button, "-1", 30, "black", "white", 10)
                else:
                    dbwt(screen, card_decrease_button, "-1", 30, "black", "gray55", 10)
                
            textbox_frame = pygame.Rect(screen_width-800, 0, 800, 260)
            textbox = pygame.Rect(screen_width-790, 10, 780, 240)
            send_button = pygame.Rect(screen_width-800, 260, 800, 50)
            dbwt(screen, textbox_frame, "", 0, "black", "white", 0)

            if text_input != "":
                dbwt(screen, textbox, text_input, 30, "white", "black", 10, align="left", multiline=True)
                if textbox_active:
                    # Render the gray "|" cursor at cursor_pos
                    font = pygame.font.Font(None, 30)
                    # Split text into lines up to cursor_pos
                    text_before_cursor = text_input[:cursor_pos]
                    lines = []
                    max_width = textbox.width - 20  # Match dbwt padding
                    current_line = ""
                    for char in text_before_cursor:
                        test_line = current_line + char
                        if char == "\n":
                            lines.append(current_line)
                            current_line = ""
                        elif font.render(test_line, True, "white").get_width() <= max_width:
                            current_line = test_line
                        else:
                            lines.append(current_line)
                            current_line = char
                    if current_line:
                        lines.append(current_line)
                    # Calculate cursor position
                    last_line = lines[-1] if lines else ""
                    text_surface = font.render(last_line, True, "white")
                    cursor_x = textbox.left + 10 + text_surface.get_width()
                    cursor_y = textbox.top + 10 + (len(lines) - 1) * 30
                    # Blinking cursor
                    if pygame.time.get_ticks() % 1000 < 500:
                        cursor_surface = font.render("|", True, "gray69")
                        screen.blit(cursor_surface, (cursor_x, cursor_y))
                    else:
                        cursor_surface = font.render("|", True, "white")
                        screen.blit(cursor_surface, (cursor_x, cursor_y))
            else:
                dbwt(screen, textbox, "Input Text Here", 30, "gray69", "black", 10, align="left", multiline=True)
                if textbox_active:
                    # Cursor at start
                    if pygame.time.get_ticks() % 1000 < 500:
                        font = pygame.font.Font(None, 30)
                        cursor_surface = font.render("|", True, "gray69")
                        screen.blit(cursor_surface, (textbox.left + 10, textbox.top + 10))

            if send_button.collidepoint(mouse_pos) and mouse_click[0]:
                round = 1
                textbox_active = False
            elif send_button.collidepoint(mouse_pos):
                dbwt(screen, send_button, "Send", 30, "black", "gray69", 10)
            else:
                dbwt(screen, send_button, "Send", 30, "black", "white", 10)

            if textbox.collidepoint(mouse_pos) and mouse_click[0]:
                textbox_active = True

        else:
            round = round  # @kiu

        pygame.display.flip()
        dt = clock.tick(60) / 1000

main()

pygame.quit()
