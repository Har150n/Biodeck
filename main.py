import pygame
import sys
from unit import Unit
from player import Player
import random
from images import *


# Setting constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 700



def main():
    global SCREEN, CLOCK, board, player_one, player_two, deck, player_one_units_on_board, player_two_units_on_board, p1_hand, p2_hand
    turn = 0
     # creating a varaible that changes player's turns
    pygame.init()
    pygame.font.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    font = pygame.font.SysFont('Comic Sans MS', 19)
    # clock is used to control how fast the screen updates
    CLOCK = pygame.time.Clock()
    # running is used to check if game is still going
    running = True

    # Creating the 3x7 board in an array
    rows, cols = (3, 7)
    board = [[None for i in range(cols)] for j in range(rows)]

    # Set title
    pygame.display.set_caption("BioDeck")
    
    # Creating the deck of all units

    
    deck = [
        Unit("Merlin", 5, 4, 4, merlin_image),
        Unit("Whomp", 10, 3, 1, whomp_image),
        Unit("Assasin", 1, 2, 1, talon_image),
        Unit("Mega-Man", 2, 3, 4, megaman_image),
        Unit("King Arthur", 8, 4, 3, arthur_image),
        Unit("Yoda", 1, 2, 3, yoda_image),
        Unit("Laura-Croft", 6, 3, 3, lora_image),
        Unit("St.Jean Paul", 2, 2, 1, saint_image)
        ]

    # Creating the hand of p1 and p2
    p1_hand = []
    p2_hand = []
    max_cards = 5
    print("Player one hand")
    for i in range(max_cards):
        p1_hand.append(random.choice(deck))
        print(p1_hand[i].name)
        p1_hand[i].x_pos = i + 1

    for unit in p1_hand:
        unit.side = 1

    print("\nPlayer two hand")
    for i in range(max_cards):
        p2_hand.append(random.choice(deck))
        print(p2_hand[i].name)
        p2_hand[i].x_pos = i + 1

    for unit in p2_hand:
        unit.side = 2





      
    player_one_units_on_board = [] #player 1 list of units in play
    player_two_units_on_board = [] #player 2 list of units in play

    # Loading the player images
    # scaling the image
    # p1_image = pygame.transform.scale(first_image, (70, 70))
    # p2_image = pygame.transform.scale(second_image, (85, 85))
    
    # # placements of player sprite
    p1_x, p1_y = 0, 100
    p2_x, p2_y = 600, 100
    
    # initializes the two players
    player_one = Player(True, 10, 10, p1_hand, p1_image, p1_x, p1_y)
    player_two = Player(False, 10, 10, p2_hand, p2_image, p2_x, p2_y)

    # setting background to be white
    SCREEN.fill(WHITE)

    #initializes the starting player

    # ----------Main Program Loop--------------
    while running:

         #refreshes 60 times a second
        CLOCK.tick(60)
        # --- Main Event Loop
        # drawing the grid
        drawGrid()
        #drawing user interface under game board ex-hand, end turn and ff
        rect = pygame.Rect((0,300), (700, 100))
        pygame.draw.rect(SCREEN,WHITE,rect,0)

        # displaying the players 
        SCREEN.blit(player_one.image, (player_one.x, player_one.y))
        SCREEN.blit(player_two.image, (player_two.x, player_two.y))

        #creating all the text for display
        p1_hp_text = font.render(f'hp: {player_one.player_hp}/10',False,(0,0,0))
        p1_mana_text = font.render(f'mp: {player_one.player_mana}/10',False,(0,0,0))
        p2_hp_text = font.render(f'hp: {player_two.player_hp}/10',False,(0,0,0))
        p2_mana_text = font.render(f'mp: {player_two.player_mana}/10', False, (0,0,0))

        #displaying player stats
        SCREEN.blit(p1_hp_text, (5,0))
        SCREEN.blit(p1_mana_text,(5,31))
        SCREEN.blit(p2_hp_text, (605,0))
        SCREEN.blit(p2_mana_text,(605,31))
        
        #display player's hand
        hand_x, hand_y = 100,300
        if turn == 0:
            for unit in p1_hand:
                SCREEN.blit(unit.image,(hand_x,hand_y))
                hand_x += 100
        elif turn == 1:
            for unit in p2_hand:
                SCREEN.blit(unit.image,(hand_x,hand_y))
                hand_x += 100

        pygame.display.update()

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # if the user clicked close
                pygame.quit()
                sys.exit()
            # handle MOUSEBUTTONDOWN
            if event.type == pygame.MOUSEBUTTONDOWN:

                pos = pygame.mouse.get_pos()
                #checks all player one unit's on board
                if turn == 0:
                    clicked_units = [s for s in player_one_units_on_board if s.rect.collidepoint(pos)]
                    for unit in clicked_units:
                        if unit.x_pos == 5:
                            print("attempted attack")
                            attack(turn, unit)
                        elif board[unit.y_pos][unit.x_pos+1] is not None:
                            print("attempted attack")
                            attack(turn, unit)
                        else:
                            print("attempted move")
                            move(turn, unit)


                    
                elif turn == 1:
                    clicked_units = [s for s in player_two_units_on_board if s.rect.collidepoint(pos)]
                    for unit in clicked_units:
                        if unit.x_pos == 1:
                            print("attempted attack")
                            attack(turn, unit)
                        elif board[unit.y_pos][unit.x_pos-1] is not None:
                            print("attempted attack")
                            attack(turn, unit)
                        else:
                            print("attempted move")
                            move(turn, unit)
                        

            #handle number key input
            if event.type == pygame.KEYDOWN:

                pos = pygame.mouse.get_pos()
                
                if turn == 0: #player one's turn
                    
                    #if number key clicked, places the unit that the mouse is hovering over
                    if event.key == pygame.K_1:
                        if pos[1] >= 300:
                            place(turn, pos[0] // 100, 0)

                    elif event.key == pygame.K_2:
                        if pos[1] >= 300:
                            place(turn, pos[0] // 100, 1)
                    elif event.key == pygame.K_3:
                        if pos[1] >= 300:
                            place(turn, pos[0] // 100, 2)
                    elif event.key == pygame.K_RETURN: #next turn
                        turn = (turn + 1) % 2
                    
                        
                    

                elif turn == 1:
                    
                    if event.key == pygame.K_1:
                        if pos[1] >= 300:
                            place(turn, pos[0] // 100, 0)
                    elif event.key == pygame.K_2:
                        if pos[1] >= 300:
                            place(turn, pos[0] // 100, 1)
                    elif event.key == pygame.K_3:
                        if pos[1] >= 300:
                            place(turn, pos[0] // 100, 2)
                    elif event.key == pygame.K_RETURN: #next turn
                        turn = (turn + 1) % 2


        # putting players into the board
        board[1][0] = "Player One"
        board[1][6] = "Player Two"






#---places unit on board if there is valid spot x-coordinate will always either be 1 or 5 depending on team
def place(turn: int, index: int, y_coordinate):
    #check which side the unit is on
    index -= 1
    if turn == 0:
      #check if the starting bench is full
        if board[0][1] is not None and board[1][1] is not None and board[2][1] is not None:
            print("Starting Bench is Full")
      #check if y_coordinate is valid
        elif board[y_coordinate][1] is not None:
            print("Please Choose a different spot")
        else:
            player_one_units_on_board.append(p1_hand[index]) #adds to player one's total units
            board[y_coordinate][1] = p1_hand[index]
            board[y_coordinate][1].x_pos, board[y_coordinate][1].y_pos = 1, y_coordinate
            SCREEN.blit(board[y_coordinate][1].image, (board[y_coordinate][1].x_pos * 100, board[y_coordinate][1].y_pos * 100))
            board[y_coordinate][1].rect.update(board[y_coordinate][1].x_pos * 100, board[y_coordinate][1].y_pos * 100, 100, 100)
            p1_hand.pop(index)
    #check which side the unit is on
    elif turn == 1:
      #check if the starting bench is full
        if board[0][5] is not None and board[1][5] is not None and board[2][5] is not None:
            print("Starting Bench is Full")
      #check if y_coordinate is valid
        elif board[y_coordinate][5] is not None:
            print("Please Choose a different spot")
        else:
            player_two_units_on_board.append(p2_hand[index]) #adds to player one's total units
            board[y_coordinate][5] = p2_hand[index]
            board[y_coordinate][5].x_pos, board[y_coordinate][5].y_pos = 5,  y_coordinate
            SCREEN.blit(board[y_coordinate][5].image,(board[y_coordinate][5].x_pos * 100, board[y_coordinate][5].y_pos * 100))
            board[y_coordinate][5].rect.update(board[y_coordinate][5].x_pos * 100, board[y_coordinate][5].y_pos * 100, 100, 100)
            p2_hand.pop(index)

def drawGrid():
    blockSize = 100  # Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)


# checks if a player has won , returns True if someone has won, False if not
# displays "win" text pop-up
def check_winner(p1: Player, p2: Player) -> None:
    if p1.player_hp <= 0:
        print("Player Two wins!")  # replace with text pop-up
    elif p2.player_hp <= 0:
        print("Player One wins!")  # replace with text pop-up

    pass


# ---moves the unit forward a number of spaces
# changes the unit's x_pos if the unit is movable
def move(turn: int, unit: Unit) -> None:
    if turn == 0 :  # player one's turn
        if unit.x_pos < len(board[0]) - 2:  # if not at end of board
            if board[unit.y_pos][unit.x_pos + 1] is None:  # if the space on the right of unit is empty
                y = ((unit.y_pos * 100) - 100) if (unit.y_pos != 0) else 0
                x = ((unit.x_pos * 100) - 100) if (unit.x_pos != 0) else 0  #setting the orignal position (block) to be white
                rect = pygame.Rect((x,y), (100, 100)) 
                pygame.draw.rect(SCREEN,WHITE,rect,1) 
                board[unit.y_pos][unit.x_pos + 1] = unit  # sets next space on board to unit
                board[unit.y_pos][unit.x_pos] = None  # sets current space on board to 0
                SCREEN.blit(white_image, (unit.x_pos * 100, unit.y_pos * 100))
                unit.x_pos += 1
                SCREEN.blit(unit.image,(unit.x_pos * 100, unit.y_pos * 100))
                cur_unit = board[unit.y_pos][unit.x_pos]
                cur_unit.rect.update(cur_unit.x_pos * 100, cur_unit.y_pos * 100, 100, 100)
            else:
                print("no space in front of unit")
        else:
            print("unit at end of board")  # replace with pop-up text
    elif turn == 1:  # player one's turn
        if unit.x_pos - 1 > 0:  # if not at end of board
            if board[unit.y_pos][unit.x_pos - 1] is None:  # if the space on the left of unit is empty
                y = ((unit.y_pos * 100) - 100) if (unit.y_pos != 0) else 0
                x = ((unit.x_pos * 100) - 100) if (unit.x_pos != 0) else 0  #setting the orignal position (block) to be white
                rect = pygame.Rect((x,y), (100, 100)) 
                pygame.draw.rect(SCREEN,WHITE,rect,1) 
                board[unit.y_pos][unit.x_pos - 1] = unit  # sets next space on board to unit
                board[unit.y_pos][unit.x_pos] = None  # sets current space on board to 0
                SCREEN.blit(white_image, (unit.x_pos * 100, unit.y_pos * 100)   )
                unit.x_pos -= 1
                SCREEN.blit(unit.image,(unit.x_pos * 100, unit.y_pos * 100))
                cur_unit = board[unit.y_pos][unit.x_pos]
                cur_unit.rect.update(cur_unit.x_pos * 100, cur_unit.y_pos * 100, 100, 100)
            else:
                print("no space in front of unit")
        else:
            print("unit at end of board")  # replace with pop-up text


# ---checks if enemy unit is in front of a unit, only works if unit is not in front of other player
def enemy_in_front(unit):
    if unit.side == 1:
        if board[unit.y_pos][unit.x_pos + 1].side == 2:
            return True
    if unit.side == 2:
        if board[unit.y_pos][unit.x_pos - 1].side == 1:
            return True
    return False


#---allows units to attack thing in front of it
#---if thing in front of unit is another unit then it deals damage to that unit
#---if thing in front of the unit is a player, the unit deals damage to the player
def attack(turn, unit):
    #check if unit belongs to player 1
    if turn == 0:
        #check to see if unit is in front of player 2
        if unit.x_pos == 5:
            player_two.player_hp -= unit.att
            check_winner(player_one, player_two)
        #check to see if unit is in front of enemy unit
        elif enemy_in_front(unit):
            #enemy unit loses hp equal to units attack
            board[unit.y_pos][unit.x_pos + 1].hp -= unit.att
            #if enemy unit takes enough damage to kill it, the board will set that space to None
            if board[unit.y_pos][unit.x_pos + 1].hp <= 0:
                board[unit.y][unit.x_pos +1] = None
        else:
            return 
    #check if unit belongs to player 2
    elif turn == 1:
        #check to see if unit is in front of player 1
        if unit.x_pos == 1:
            player_one.player_hp -= unit.att
            check_winner(player_one, player_two)
        #check to see if unit is in front of enemy unit
        elif enemy_in_front(unit):
            #enemy unit loses hp equal to units attack
            board[unit.y_pos][unit.x_pos - 1].hp -= unit.att
            #if enemy unit takes enough damage to kill it, the board will set that space to None
            if board[unit.y_pos][unit.x_pos -1].hp <= 0:
                board[unit.y_pos][unit.x_pos -1] = None
        else:
            return

#Adds a random card from the deck to a players hand
def draw(player_hand):
    player_hand.append(random.choice(deck))






main()