# https://www.entertainment14.net/blog/post/110995335-%e9%a8%99%e5%ad%90%e9%85%92%e5%90%a7-liars-bar-%e6%96%b0%e6%89%8b%e9%81%8a%e7%8e%a9%e6%8c%87%e5%8d%97

from func import dbwt
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
        dt = clock.tick(60) / 1000

# Main game
def game():
    pygame.key.set_repeat(200, 30)

    round = 0
    p = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    card_name = [" Queen", " King ", " Ace  ", " Joker"]
    cq = 6
    ck = 6
    ca = 6
    cj = 2
    send = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    status = [1, 1, 1, 1, 1]
    
    for i in range(20):
        r = randint(0, 19 - i)
        if r < cq and cq > 0:
            cq -= 1
            p[i//5][0] += 1   
        elif r < cq + ck and ck > 0:
            ck -= 1
            p[i//5][1] += 1
        elif r < cq + ck + ca and ca > 0:
            ca -= 1
            p[i//5][2] += 1
        else:
            cj -= 1
            p[i//5][3] += 1

    textbox_active = False
    text_input = ""
    cursor_pos = 0
    last_button_time = 0
    cursor_x = 0
    cursor_y = 0
    line_count = 0  # Track number of lines before cursor
    running = True
    debug_output = True
    
    while running:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        screen.fill("black")
        
        if round % 4 == 0:
            if debug_output:
                if round == 0:
                    print("No previous cards!")
                else:
                    print(send[(round - 1) % 4])
                debug_output = False
            for i in range(4):
                current_cards = pygame.Rect(0, i * 65, 400, 50)
                card_text = "You have " + str(p[0][i]) + card_name[i]
                dbwt(screen, current_cards, card_text, 65, "white", "black", 10, align="left")
                
                card_count_button = pygame.Rect(screen_width // 2 - 575 + i * 300, screen_height // 2 + 150, 200, 100)
                card_increase_button = pygame.Rect(screen_width // 2 - 375 + i * 300, screen_height // 2 + 150, 50, 50)
                card_decrease_button = pygame.Rect(screen_width // 2 - 375 + i * 300, screen_height // 2 + 200, 50, 50)
                send_queen_text = "Send " + str(send[0][i]) + card_name[i] + " out"

                dbwt(screen, card_count_button, send_queen_text, 30, "black", "gray69", 10)

                if p[0][i] > 0 and sum(send[0]) < 3:
                    if card_increase_button.collidepoint(mouse_pos) and mouse_click[0] and current_time - last_button_time > 167:
                        send[0][i] += 1
                        p[0][i] -= 1
                        textbox_active = False
                        last_button_time = current_time
                    elif card_increase_button.collidepoint(mouse_pos):
                        dbwt(screen, card_increase_button, "+1", 30, "black", "gray69", 10)
                    else:
                        dbwt(screen, card_increase_button, "+1", 30, "black", "white", 10)
                else:
                    dbwt(screen, card_increase_button, "+1", 30, "black", "gray55", 10)

                if send[0][i] > 0:
                    if card_decrease_button.collidepoint(mouse_pos) and mouse_click[0] and current_time - last_button_time > 167:
                        send[0][i] -= 1
                        p[0][i] += 1
                        textbox_active = False
                        last_button_time = current_time
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
            
            # Calculate cursor position
            font = pygame.font.Font(None, 30)
            char_spacing = 0
            text_before_cursor = text_input[:cursor_pos] if text_input else ""
            lines = []
            max_width = textbox.width - 20
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
            last_line = lines[-1] if lines else ""
            x_pos = 0
            for char in last_line:
                x_pos += font.render(char, True, "white").get_width() + char_spacing
            
            # Set cursor position
            cursor_y = textbox.top + 10 + line_count * 30
            if not text_input or cursor_pos == 0:
                cursor_x = textbox.left + 10
            elif text_input[cursor_pos - 1] == "\n":
                cursor_x = textbox.left + 10  # Start of new line after \n
            else:
                cursor_x = textbox.left + 10 + x_pos  # Position after last character

            if text_input != "":
                dbwt(screen, textbox, text_input, 30, "white", "black", 10, align="left", multiline=True, char_spacing=0)
                if textbox_active:
                    if pygame.time.get_ticks() % 1000 < 500:
                        cursor_surface = font.render("|", True, "white")
                    else:
                        cursor_surface = font.render("|", True, "gray69")
                    screen.blit(cursor_surface, (cursor_x, cursor_y))
            else:
                dbwt(screen, textbox, "Input Text Here", 30, "gray69", "black", 10, align="left", multiline=True, char_spacing=0)
                if textbox_active:
                    if pygame.time.get_ticks() % 1000 < 500:
                        cursor_surface = font.render("|", True, "gray69")
                        screen.blit(cursor_surface, (cursor_x, cursor_y))

            if send_button.collidepoint(mouse_pos) and mouse_click[0]:
                round += 1
                textbox_active = False
            elif send_button.collidepoint(mouse_pos):
                dbwt(screen, send_button, "Send", 30, "black", "gray69", 10)
            else:
                dbwt(screen, send_button, "Send", 30, "black", "white", 10)

            if textbox.collidepoint(mouse_pos) and mouse_click[0]:
                textbox_active = True
            
        else:
            debug_output = True
            print(send[(round - 1) % 4])
            round += 1

        pygame.display.flip()
        dt = clock.tick(60) / 1000

main()

pygame.quit()