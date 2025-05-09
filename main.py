# https://www.entertainment14.net/blog/post/110995335-%e9%a8%99%e5%ad%90%e9%85%92%e5%90%a7-liars-bar-%e6%96%b0%e6%89%8b%e9%81%8a%e7%8e%a9%e6%8c%87%e5%8d%97

# Modules
from func import *
from random import shuffle
import math
import os
import pygame
import time

# Initialization
pygame.init()
display_info = pygame.display.Info()
screen_width = display_info.current_w
screen_height = display_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
current_state = "main"
pygame.display.set_caption("Liar's Bar (v0.1r)")
easter_egg = False

# Start Screen
max_bullet = 6
def start():

    global max_bullet
    last_button_time = 0

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
        
        current_time = pygame.time.get_ticks()

        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        screen.fill("black")

        start_button = pygame.Rect(screen_width // 2 - 200, screen_height // 2 - 250, 400, 100)
        if start_button.collidepoint(mouse_pos) and mouse_click[0]:
            return None
        elif start_button.collidepoint(mouse_pos):
            dbwt(screen, start_button, "Start", 65, "black", "gray69", 10)
        else:
            dbwt(screen, start_button, "Start", 65, "black", "white", 10)
        
        bullet_count_button = pygame.Rect(screen_width // 2 - 175, screen_height // 2 + 150, 300, 100)
        bullet_increase_button = pygame.Rect(screen_width // 2 + 125, screen_height // 2 + 150, 50, 50)
        bullet_decrease_button = pygame.Rect(screen_width // 2 + 125, screen_height // 2 + 200, 50, 50)

        send_card_text = f"shoot {max_bullet} bullets to lose"
        dbwt(screen, bullet_count_button, send_card_text, 30, "black", "gray69", 10)

        if max_bullet < 9:
            if bullet_increase_button.collidepoint(mouse_pos) and mouse_click[0] and current_time - last_button_time > 167:
                max_bullet += 1
                last_button_time = current_time
            elif bullet_increase_button.collidepoint(mouse_pos):
                dbwt(screen, bullet_increase_button, "+1", 30, "black", "gray69", 10)
            else:
                dbwt(screen, bullet_increase_button, "+1", 30, "black", "white", 10)
        else:
            dbwt(screen, bullet_increase_button, "+1", 30, "black", "gray55", 10)

        if max_bullet > 1:
            if bullet_decrease_button.collidepoint(mouse_pos) and mouse_click[0] and current_time - last_button_time > 167:
                max_bullet -= 1
                last_button_time = current_time
            elif bullet_decrease_button.collidepoint(mouse_pos):
                dbwt(screen, bullet_decrease_button, "-1", 30, "black", "gray69", 10)
            else:
                dbwt(screen, bullet_decrease_button, "-1", 30, "black", "white", 10)
        else:
            dbwt(screen, bullet_decrease_button, "-1", 30, "black", "gray55", 10)
    
        pygame.display.flip()

# Main Program

def main():
    global easter_egg, bullet, bullet_used, alive, max_bullet

    easter_egg = False
    bullet = [randint(0, max_bullet), randint(0, max_bullet), randint(0, max_bullet), randint(0, max_bullet)]
    bullet_used = [0, 0, 0, 0]
    alive = [1, 1, 1, 1]

    start()

    while alive.count(1) > 1:
        game()
        for i in range(4):
            if alive[i] == 0:
                alive[i] = 1

# Main game
def game():
    global prv_send, prv_player, cur_send, cur_player, round_idx, round_card
    global lgun_img, rgun_img
    
    pygame.key.set_repeat(200, 30)

    round = 0

    card_name = ["Queen", "King", "Ace", "Joker"]
    cq, ck, ca, cj = 6, 6, 6, 2 # No. of cards in deck

    p = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]] # No. of cards of each type for every player
    prv_send = [-1, -1, -1, -1]
    prv_player = -1
    cur_send = [0, 0, 0, 0]
    cur_player = 0

    queen_img = pygame.image.load(os.path.join("assets", "img-queen.png"))
    king_img = pygame.image.load(os.path.join("assets", "img-king.png"))
    ace_img = pygame.image.load(os.path.join("assets", "img-ace.png"))
    joker_img = pygame.image.load(os.path.join("assets", "img-joker.png"))
    lgun_img = pygame.image.load(os.path.join("assets", "img-gun-left.png"))
    rgun_img = pygame.image.load(os.path.join("assets", "img-gun-right.png"))

    img_arr = [queen_img, king_img, ace_img, joker_img]

    round_idx = randint(0, 2)
    round_card = card_name[round_idx]

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
    debug_output = True
    
    # During Round
    while True:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()

        # keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        screen.fill("black")
        
        if round % 4 == 0:
            if debug_output:
                print(prv_send, (prv_send[round_idx] + prv_send[3] != sum(prv_send)))
                debug_output = False
            
            round_card_button = pygame.Rect(0, 350, 400, 50)
            round_card_text = f"Current Round Card: {round_card}"
            dbwt(screen, round_card_button, round_card_text, 65, "white", "black", 10, align="left")
            
            ################################################################################################

            for i in range(4):
                screen.blit(img_arr[i], (10 + 210 * (i % 2), 10 + 155 * (i // 2)))

                current_cards = pygame.Rect(130 + 210 * (i % 2), 45 + 155 * (i // 2), 80, 65)
                card_text = f"x{str(p[0][i])}"
                dbwt(screen, current_cards, card_text, 65, "white", "black", 10, align="left")

                card_count_button = pygame.Rect(screen_width // 2 - 575 + i * 300, screen_height // 2 + 150, 200, 100)
                card_increase_button = pygame.Rect(screen_width // 2 - 375 + i * 300, screen_height // 2 + 150, 50, 50)
                card_decrease_button = pygame.Rect(screen_width // 2 - 375 + i * 300, screen_height // 2 + 200, 50, 50)

                send_card_text = f"Send {cur_send[i]} {card_name[i]} out"
                dbwt(screen, card_count_button, send_card_text, 30, "black", "gray69", 10)
                
                if p[0][i] > 0 and sum(cur_send) < 3:
                    if card_increase_button.collidepoint(mouse_pos) and mouse_click[0] and current_time - last_button_time > 167:
                        cur_send[i] += 1
                        p[0][i] -= 1
                        last_button_time = current_time
                    elif card_increase_button.collidepoint(mouse_pos):
                        dbwt(screen, card_increase_button, "+1", 30, "black", "gray69", 10)
                    else:
                        dbwt(screen, card_increase_button, "+1", 30, "black", "white", 10)
                else:
                    dbwt(screen, card_increase_button, "+1", 30, "black", "gray55", 10)

                if cur_send[i] > 0:
                    if card_decrease_button.collidepoint(mouse_pos) and mouse_click[0] and current_time - last_button_time > 167:
                        cur_send[i] -= 1
                        p[0][i] += 1
                        last_button_time = current_time
                    elif card_decrease_button.collidepoint(mouse_pos):
                        dbwt(screen, card_decrease_button, "-1", 30, "black", "gray69", 10)
                    else:
                        dbwt(screen, card_decrease_button, "-1", 30, "black", "white", 10)
                else:
                    dbwt(screen, card_decrease_button, "-1", 30, "black", "gray55", 10)
            
            ################################################################################################

            cur_player = round % 4

            prev_round_text = "This is the first round"
            if round != 0:
                prev_round_text = f"Player {prv_player+1} sent {sum(prv_send)} cards that claimed to be {round_card}"

            prev_cards = pygame.Rect(screen_width - 800, 150, 300, 45)
            dbwt(screen, prev_cards, prev_round_text, 40, "white", "black", 10, align="left")
            
            send_button = pygame.Rect(screen_width - 800, 60, 300, 80)

            if send_button.collidepoint(mouse_pos) and mouse_click[0] and sum(cur_send) > 0:

                screen.fill("black")

                sub = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 22.5, 300, 45)
                cur_round_text = f"You sent {sum(cur_send)} cards that claimed to be {round_card}"
                dbwt(screen, sub, cur_round_text, 60, "white", "black", 10, align="center")
                pygame.display.flip()
                time.sleep(1)

                prv_send = cur_send.copy() 
                cur_send = [0, 0, 0, 0] # Reset
                prv_player = round % 4

                round += 1
                
            elif send_button.collidepoint(mouse_pos):
                dbwt(screen, send_button, "Send", 30, "black", "gray69", 10)
            else:
                dbwt(screen, send_button, "Send", 30, "black", "white", 10)
                
            liar_button = pygame.Rect(screen_width - 400, 60, 300, 80)

            if liar_button.collidepoint(mouse_pos) and mouse_click[0] and round != 0:
                challenge()
                return None

            elif liar_button.collidepoint(mouse_pos) and round != 0:
                dbwt(screen, liar_button, "Liar!", 30, "black", "gray69", 10)
            elif round != 0:
                dbwt(screen, liar_button, "Liar!", 30, "black", "white", 10)
            else:
                dbwt(screen, liar_button, "Liar!", 30, "black", "gray55", 10)
        
        ####################################################################################################

        else:
            cur_player = round % 4

            debug_output = True

            if alive[cur_player] == -1:
                cur_round_text = f"Player {cur_player + 1} is dead"
            elif alive[cur_player] == 0:
                cur_round_text = f"Player {cur_player + 1} sent all his cards already"
            else :
                rem = [i for i, count in enumerate(p[round % 4]) for _ in range(count)]
                shuffle(rem)
                obt = randint(1, min(3, len(rem)))
                for i in range(obt):
                    cur_send[rem[i]] += 1
                    p[round % 4][rem[i]] -= 1
                
                cur_round_text = f"Player {cur_player + 1} sent {sum(cur_send)} cards that claimed to be {round_card}"

            sub = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 22.5, 300, 45)
            dbwt(screen, sub, cur_round_text, 60, "white", "black", 10, align="center")
            pygame.display.flip()
            
            if sum(p[round % 4]) == 0:
                alive[round % 4] = 0
            
            prv_send = cur_send.copy() 
            cur_send = [0, 0, 0, 0] # Reset
            prv_player = round % 4

            time.sleep(1)
            round += 1
        
        pygame.display.flip()

def challenge():

    screen.fill("black")

    b, a = prv_player, cur_player
    challenge_title = "Challenged"
    challenge_title_box = pygame.Rect(screen_width // 2 - 250, 0, 500, 85)
    dbwt(screen, challenge_title_box, challenge_title, 65, "white", "black", 10, align="center")
    challenge_player = f"Player {a + 1}"
    challenged_player = f"Player {b + 1}"

    if a == 0:
        challenge_player = "You"
    if b == 0:
        challenged_player = "You"
    
    challenge_player_box = pygame.Rect(screen_width // 2 - 550, 0, 300, 85)
    challenged_player_box = pygame.Rect(screen_width // 2 + 250, 0, 300, 85)
    dbwt(screen, challenge_player_box, challenge_player, 65, "white", "black", 10, align="left")
    dbwt(screen, challenged_player_box, challenged_player, 65, "white", "black", 10, align="right")

    dare_text_box = pygame.Rect(screen_width // 2 - 550, screen_height // 2 - 43, 300, 85)
    dbwt(screen, dare_text_box, "Dare!", 65, "white", "black", 10, align="left")
    dare_text_box = pygame.Rect(screen_width // 2 + 150, screen_height // 2 - 43, 400, 85)
    dbwt(screen, dare_text_box, f"They claimed that they sent {sum(prv_send)} {round_card}", 65, "white", "black", 10, align="right")
    
    pygame.display.flip()
    time.sleep(2)

    challenge_success = (prv_send[round_idx] + prv_send[3] != sum(prv_send))
    
    if challenge_success:
        win_text_box = pygame.Rect(screen_width // 2 - 200, screen_height // 2 + 215, 400, 70)
        dbwt(screen, win_text_box, f"Player {b+1} is a liar!", 70, "white", "black", 10, align="center")
        screen.blit(rgun_img, (screen_width // 2 + 300, screen_height // 2 + 100))
        bullet_used[b] += 1
        pygame.display.flip()
        time.sleep(1)
        if bullet_used[b] == bullet[b]:
            player_dead_box = pygame.Rect(screen_width // 2 + 200, screen_height // 2 + 215, 400, 70)
            dbwt(screen, player_dead_box, f"Player {b+1} took a headshot!", 70, "white", "black", 10, align="center")
            alive[b] = -1
            pygame.display.flip()
            time.sleep(1)
    else:
        lose_text_box = pygame.Rect(screen_width // 2 - 200, screen_height // 2 + 215, 400, 70)
        dbwt(screen, lose_text_box, f"Player {b+1} is not a liar!", 70, "white", "black", 10, align="center")
        screen.blit(lgun_img, (screen_width // 2 - 400, screen_height // 2 + 100))
        bullet_used[a] += 1
        pygame.display.flip()
        time.sleep(1)

    return None

main()

pygame.quit()