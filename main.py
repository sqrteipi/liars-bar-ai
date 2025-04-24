# https://www.entertainment14.net/blog/post/110995335-%e9%a8%99%e5%ad%90%e9%85%92%e5%90%a7-liars-bar-%e6%96%b0%e6%89%8b%e9%81%8a%e7%8e%a9%e6%8c%87%e5%8d%97

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

# Drawing button with text (modified to handle leading newlines)
def dbwt(screen, button_rect, text, font_size, text_color, button_color, border, align="center", multiline=False, char_spacing=0):
    font = pygame.font.Font(None, font_size)
    pygame.draw.rect(screen, button_color, button_rect)
    
    if multiline:
        lines = []
        max_width = button_rect.width - 2 * border
        
        # Split text into raw lines, preserving empty lines
        raw_lines = text.split("\n")
        
        for raw_line in raw_lines:
            current_line = ""
            current_words = raw_line.split(" ") if raw_line else [""]
            
            for word in current_words:
                word_with_space = word + " " if word else ""
                word_width = sum(font.render(char, True, text_color).get_width() + char_spacing for char in word_with_space) - char_spacing if word else 0
                if font.render(current_line, True, text_color).get_width() + word_width <= max_width:
                    current_line += word_with_space
                else:
                    if current_line:
                        lines.append(current_line.strip())
                        current_line = ""
                    
                    temp_line = current_line
                    for i, char in enumerate(word):
                        char_surface = font.render(char, True, text_color)
                        char_width = char_surface.get_width() + char_spacing
                        if font.render(temp_line, True, text_color).get_width() + char_width <= max_width:
                            temp_line += char
                        else:
                            if temp_line:
                                lines.append(temp_line)
                            temp_line = char
                    current_line = temp_line
                    if word_with_space and word_with_space[-1] == " " and font.render(current_line + " ", True, text_color).get_width() + char_spacing <= max_width:
                        current_line += " "
            
            # Always append the current line, even if empty
            lines.append(current_line.strip() if current_line else "")
        
        # Render each line, including empty ones
        for i, line in enumerate(lines):
            if char_spacing == 0:
                text_surface = font.render(line, True, text_color)
                text_rect = text_surface.get_rect()
                if align == "left":
                    text_rect.topleft = (button_rect.left + border, button_rect.top + border + i * font_size)
                else:
                    text_rect.center = (button_rect.centerx, button_rect.top + border + i * font_size)
                screen.blit(text_surface, text_rect)
            else:
                x_pos = button_rect.left + border if align == "left" else button_rect.centerx - sum(font.render(c, True, text_color).get_width() + char_spacing for c in line)/2 + char_spacing/2
                y_pos = button_rect.top + border + i * font_size
                for char in line:
                    char_surface = font.render(char, True, text_color)
                    screen.blit(char_surface, (x_pos, y_pos))
                    x_pos += char_surface.get_width() + char_spacing
    else:
        if char_spacing == 0:
            text_surface = font.render(text, True, text_color)
            text_rect = text_surface.get_rect()
            if align == "left":
                text_rect.topleft = (button_rect.left + border, button_rect.top + border)
            else:
                text_rect.center = button_rect.center
            screen.blit(text_surface, text_rect)
        else:
            x_pos = button_rect.left + border if align == "left" else button_rect.centerx - sum(font.render(c, True, text_color).get_width() + char_spacing for c in text)/2 + char_spacing/2
            y_pos = button_rect.top + border if align == "left" else button_rect.centery - font.get_height()/2
            for char in text:
                char_surface = font.render(char, True, text_color)
                screen.blit(char_surface, (x_pos, y_pos))
                x_pos += char_surface.get_width() + char_spacing

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
    round_card = card_name[randint(0, 3)]
    prev_sent_amount = 0
    prev_claim_amount = 0

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
            elif textbox_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    text_input = text_input[:cursor_pos] + " " + text_input[cursor_pos:]
                    cursor_pos += 1
                elif event.key == pygame.K_BACKSPACE:
                    # Prevent backspace detect as printable character
                    if cursor_pos > 0:
                        if text_input[cursor_pos - 1] == "\n":
                            line_count -= 1
                            cursor_y -= 30
                        text_input = text_input[:cursor_pos-1] + text_input[cursor_pos:]
                        cursor_pos -= 1
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    text_input = text_input[:cursor_pos] + "\n" + text_input[cursor_pos:]
                    cursor_pos += 1
                    line_count += 1
                    cursor_y += 30
                    cursor_x = textbox.left + 10  # Reset to start of new line
                elif event.key == pygame.K_LEFT and cursor_pos > 0:
                    cursor_pos -= 1
                    if cursor_pos == 0:
                        # At the start of text, reset to first line
                        line_count = 0
                        cursor_y = textbox.top + 10
                        cursor_x = textbox.left + 10
                    elif text_input[cursor_pos] == "\n":
                        # Moving left across a newline
                        line_count -= 1
                        cursor_y -= 30
                        # Calculate x position on the previous line
                        text_before_newline = text_input[:cursor_pos]
                        prev_lines = text_before_newline.split("\n")
                        last_line = prev_lines[-1] if prev_lines else ""
                        x_pos = 0
                        for char in last_line:
                            x_pos += font.render(char, True, "white").get_width()
                        cursor_x = textbox.left + 10 + x_pos
                elif event.key == pygame.K_DELETE:
                    # Delete character to the right of the cursor
                    if cursor_pos < len(text_input):
                        text_input = text_input[:cursor_pos] + text_input[cursor_pos + 1:]
                elif event.key == pygame.K_RIGHT and cursor_pos < len(text_input):
                    cursor_pos += 1
                    if text_input[cursor_pos - 1] == "\n":
                        line_count += 1
                        cursor_y += 30
                        cursor_x = textbox.left + 10
                elif len(event.unicode) > 0:
                    text_input = text_input[:cursor_pos] + event.unicode + text_input[cursor_pos:]
                    cursor_pos += 1

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
                send_card_text = "Send " + str(send[0][i]) + card_name[i] + " out"
                prev_round_text = "This is the first round"
                if round != 0:
                    prev_round_text = f"Previous player sent {prev_sent_amount} cards, claimed {prev_claim_amount} to be {round_card}"

                dbwt(screen, card_count_button, send_card_text, 30, "black", "gray69", 10)

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