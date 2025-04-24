# https://www.entertainment14.net/blog/post/110995335-%e9%a8%99%e5%ad%90%e9%85%92%e5%90%a7-liars-bar-%e6%96%b0%e6%89%8b%e9%81%8a%e7%8e%a9%e6%8c%87%e5%8d%97

# Modules
from func import dbwt
from random import randint
import pygame
import time

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

    card_name = ["Queen", "King", "Ace", "Joker"]
    cq, ck, ca, cj = 6, 6, 6, 2 # No. of cards in deck

    p = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]] # No. of cards of each type for every player
    send = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    status = [1, 1, 1, 1, 1]
    bullet = [randint(0, 5), randint(0, 5), randint(0, 5), randint(0, 5)]
    bullet_used = [0, 0, 0, 0]
    claim = [0, 0, 0, 0]

    round_card = card_name[randint(0, 3)]

    # Generate Cards
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

    last_button_time = 0
    running = True
    debug_output = True
    
    # During Round
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
            claim[0] = 0
            if debug_output:
                if round == 0:
                    print("No previous cards!")
                else:
                    print(send[(round - 1) % 4])
                debug_output = False
                
            for i in range(4):
                current_cards = pygame.Rect(0, i * 65, 400, 50)
                card_text = f"You have {str(p[0][i])} {card_name[i]}"
                dbwt(screen, current_cards, card_text, 65, "white", "black", 10, align="left")
                
                card_count_button = pygame.Rect(screen_width // 2 - 575 + i * 300, screen_height // 2 + 150, 200, 100)
                card_increase_button = pygame.Rect(screen_width // 2 - 375 + i * 300, screen_height // 2 + 150, 50, 50)
                card_decrease_button = pygame.Rect(screen_width // 2 - 375 + i * 300, screen_height // 2 + 200, 50, 50)

                send_card_text = f"Send {send[0][i]} {card_name[i]} out"
                dbwt(screen, card_count_button, send_card_text, 30, "black", "gray69", 10)

                prev_round_text = "This is the first round"
                if round != 0:
                    prev_round_text = f"Previous player sent {sum(send[3])} cards, claimed {claim[3]} to be {round_card}"

                prev_cards = pygame.Rect(screen_width - 800, 150, 300, 45)
                dbwt(screen, prev_cards, prev_round_text, 45, "white", "black", 10, align="left")

                
                if p[0][i] > 0 and sum(send[0]) < 3:
                    if card_increase_button.collidepoint(mouse_pos) and mouse_click[0] and current_time - last_button_time > 167:
                        send[0][i] += 1
                        p[0][i] -= 1
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
                        last_button_time = current_time
                    elif card_decrease_button.collidepoint(mouse_pos):
                        dbwt(screen, card_decrease_button, "-1", 30, "black", "gray69", 10)
                    else:
                        dbwt(screen, card_decrease_button, "-1", 30, "black", "white", 10)
                else:
                    dbwt(screen, card_decrease_button, "-1", 30, "black", "gray55", 10)
                
            send_button = pygame.Rect(screen_width - 800, 60, 800, 50)

            if send_button.collidepoint(mouse_pos) and mouse_click[0] and sum(send[0]) > 0:
                send[0] = [0, 0, 0, 0] # Reset
                round += 1
            elif send_button.collidepoint(mouse_pos):
                dbwt(screen, send_button, "Send", 30, "black", "gray69", 10)
            else:
                dbwt(screen, send_button, "Send", 30, "black", "white", 10)
            
        else:
            debug_output = True
            print(send[(round - 1) % 4])
            round += 1

        pygame.display.flip()
        dt = clock.tick(60) / 1000

main()

pygame.quit()