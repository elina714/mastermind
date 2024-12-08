import random, pygame, sys
from backcode import MasterMindSolver

#global variable
SQUARE_SIZE = 50
abs_white = (194, 188, 187)
WHITE = (255, 255, 255)
GRASS = (96,255,128)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
attempts = 10
num_pieces = 4
BOARDING = 20
piece_im = {
       "red": "assets/red_button_46x46.png",
       "yellow": "assets/yellow_button_46x46.png",
       "green": "assets/green_button_46x46.png",
       "blue": "assets/blue_button_46x46.png",
     }
COLORS = list(piece_im.keys())

width = SQUARE_SIZE * num_pieces * 2 + SQUARE_SIZE
height = SQUARE_SIZE * attempts + SQUARE_SIZE
screen = pygame.display.set_mode((width + 2 * BOARDING, height + 2 * BOARDING))
side_bar_x = (width - SQUARE_SIZE + BOARDING)
pygame.font.init()
font = pygame.font.Font(None, 48)
smallfont = pygame.font.Font(None, 28)


def Img(Img, x, y):
  #drawing pegs or images on the specific coordinates
  screen.blit(Img, (x, y))

def game_setup():
  #Initiailize the pygame
  pygame.init()

  #Title and Icon
  pygame.display.set_caption("MasterMind")

  #Screen background
  screen.fill(WHITE)

  def grid1():
    #draw grid for the codebreacker input and codemaker output
    #c - column, r - row
    for c in range(num_pieces):
        for r in range(attempts):
            pygame.draw.circle(screen, abs_white,
                           ((c + 1 / 2) * SQUARE_SIZE + BOARDING, (r + 1.5) * SQUARE_SIZE + BOARDING),
                           (SQUARE_SIZE-5) / 2, 2)
  grid1()
  def grid2():
    #draw grid for the hidden row
    for c in range(num_pieces):
      pygame.draw.circle(screen, abs_white,
                         ((c + 1 / 2) * SQUARE_SIZE + BOARDING, BOARDING + 1/2 * SQUARE_SIZE),
                         (SQUARE_SIZE - 5) / 2, 2)
  grid2()

  #draw the side bar:
  location = height - SQUARE_SIZE + BOARDING
  y_positions = [location, location - SQUARE_SIZE, location - 2 * SQUARE_SIZE, location - 3 * SQUARE_SIZE]
  for y, color in zip(y_positions, COLORS):
      image = pygame.image.load(piece_im[color])
      Img(image,side_bar_x,y)



  #draw reset
  rel = pygame.image.load('assets/reload.png')
  rel_x = (8 * SQUARE_SIZE) + BOARDING
  rel_y = BOARDING
  Img(rel, rel_x, rel_y)



  #draw AI button
  button_text = font.render("AI", True, GRASS)  # Render the text
  aibuttonx = (7 * SQUARE_SIZE) + BOARDING
  aibuttony = BOARDING + SQUARE_SIZE / 2
  circle_center_x = aibuttonx + (1 / 2 * SQUARE_SIZE)
  circle_center_y = aibuttony

  # Draw the circle
  pygame.draw.circle(screen, abs_white, (circle_center_x, circle_center_y), SQUARE_SIZE / 2-2, 2)

  # Center the text in the circle
  text_rect = button_text.get_rect(center=(circle_center_x, circle_center_y))
  screen.blit(button_text, text_rect)

  pygame.display.update()


def color_pieces(im_piece, i, row):
  choiceX = (i*SQUARE_SIZE + BOARDING)
  choiceY = (height - (11-row)*SQUARE_SIZE + BOARDING)
  Img(im_piece, choiceX, choiceY)
  pygame.display.update()


def select_random_piece():

  selected_one = random.sample(COLORS, 4)
  print(f"Secrete colors: {selected_one}")
  return selected_one

def reload(a, b, c, d, event):
  if a < event.pos[0] < b and c < event.pos[1]< d:
    attempts = 10
    game_setup()
    game(attempts)

def show_hidden_row(selected_one):
  for index, val in enumerate(selected_one):
    im_piece = pygame.image.load(piece_im[val])
    color_pieces(im_piece, index, 0)

def game_over_screen(selected_one):
    show_hidden_row(selected_one)
    EndImg = pygame.image.load('assets/game_over.png')
    Img(EndImg, 0, 0)
    pygame.display.update()



def draw_output_box(message, screen, smallfont):
    """
    Draws an output box with the AI suggestion at a fixed location
    """
    box_width, box_height = 3 * SQUARE_SIZE - 10, SQUARE_SIZE
    # box_x = location  # Center horizontally
    # box_y = BOARDING +SQUARE_SIZE
    box_x = 4.5 * SQUARE_SIZE  # Example position (use a fixed value for debugging)
    box_y = BOARDING  # Example position

    # Draw the rectangle (gray box) on the screen
    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height))  # Main rectangle
    pygame.draw.rect(screen, GRAY, (box_x, box_y, box_width, box_height), 2)  # Border

    # Render message text
    input_text = message
    text_surface = smallfont.render(input_text, True, GRASS)
    text_rect = text_surface.get_rect(topleft=(box_x + 10, box_y + 10))
    screen.blit(text_surface, text_rect)

    pygame.display.update()

def game(attempts):
    # Creating codemaker row
    selected_one = select_random_piece()
    # Ai solver
    aisolver = MasterMindSolver(COLORS)
    game_is_on = True
    codebreaker_row = [] # Initialize outside the main loop
    awaiting_input = False  # Track if waiting for codebreaker input
    i = 0
    # Game Loop
    while game_is_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # AI button
                aibuttonx = (7 * SQUARE_SIZE) + BOARDING
                aibuttony = BOARDING + SQUARE_SIZE / 2
                circle_center_x = aibuttonx + (1 / 2 * SQUARE_SIZE)
                circle_center_y = aibuttony

                airan = pygame.Rect(
                    aibuttonx,
                    aibuttony - SQUARE_SIZE // 2,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                )

                # Handle AI Button Click
                if airan.collidepoint(x, y):
                    print("AI Button Clicked")  # Debug print
                    print("Current codebreaker_row:", codebreaker_row)  # Debug print

                    secret_space = aisolver.refine_secret_space()
                    message = aisolver.choose_best_guess(secret_space)
                    ms = [color[0] for color in message]
                    message = ", ".join(ms)  # Convert tuple to string
                    draw_output_box(message, screen, smallfont)

                # Handle Reset Button Click
                # Reset button
                reset_x = (8 * SQUARE_SIZE) + BOARDING
                reset_y = BOARDING
                resetan = pygame.Rect(reset_x, reset_y, SQUARE_SIZE, SQUARE_SIZE)

                if resetan.collidepoint(x, y):
                    print("reset Button Clicked")
                    codebreaker_row = []  # Reset row on game reset
                    i = 0
                    reload(100, 350, 250, 300, event)
                    aisolver = MasterMindSolver(COLORS)
                    continue

                #the input for try region:
                if 2 * SQUARE_SIZE + BOARDING <= y <= height:
                    if (side_bar_x - SQUARE_SIZE / 2) < x < (side_bar_x + SQUARE_SIZE / 2):
                        if 500 < y < 550:
                            selected_color = "red"
                        elif 450 < y < 500:
                            selected_color = "yellow"
                        elif 400 < y < 450:
                            selected_color = "green"
                        elif 350 < y < 400:
                            selected_color = "blue"
                        codebreaker_row.append(selected_color)
                        im_piece = pygame.image.load(piece_im[selected_color])
                        color_pieces(im_piece, i, attempts)
                        i += 1
                        if i == num_pieces:
                            print("Codebreaker Row Complete:", codebreaker_row)
                            print("selected_one:", selected_one)
                            selected_one_copy = selected_one[:]
                            codebreaker_row_copy = codebreaker_row[:]
                            codemaker_response = []
                            count = 0
                            for index1, val1 in enumerate(codebreaker_row_copy):
                                for index2, val2 in enumerate(selected_one_copy):
                                    if index1 == index2 and val1 == val2:
                                        codemaker_response.append("black")
                                        count += 1
                                        # Update AI knowledgebase
                                        print("count:", count)
                                        print("select:", selected_one_copy)
                                        print("guess:", codebreaker_row_copy)

                            aisolver.update_knowledge_base(codebreaker_row_copy, count)
                            aisolver.refine_secret_space()
                            print(aisolver.refine_secret_space())

                            message = str(count)
                            new_screen_text = font.render(message, True, (0, 0, 0))
                            respond_x = (1 + num_pieces + 1 / 2) * SQUARE_SIZE + BOARDING
                            respond_y = (height - (11 - attempts) * SQUARE_SIZE + BOARDING + 10)
                            screen.blit(new_screen_text, (respond_x, respond_y))
                            pygame.display.update()

                            print(f"the response of the code :\n{codemaker_response}")
                            attempts = attempts - 1
                            i = 0
                            codebreaker_row = []
                            print("attempts:",attempts)
                            # Win/lose check
                            if attempts >= 0 and codemaker_response == ["black", "black", "black", "black"]:
                                WinImg = pygame.image.load('assets/you_win.png')
                                Img(WinImg, 200, 0)
                                print("Win!")
                                game_over_screen(selected_one)
                                game_is_on = False
                                break
                            elif attempts < 0 and codemaker_response != ["black", "black", "black", "black"]:
                                LoseImg = pygame.image.load('assets/you_lose.png')
                                Img(LoseImg, 200, 0)
                                print("lost")
                                game_over_screen(selected_one)
                                game_is_on = False
                                break

game_setup()
game(attempts)









