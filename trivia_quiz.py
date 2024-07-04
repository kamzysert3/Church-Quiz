import pygame
import pygame.locals

pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Trivia Quiz')

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
grey = (128, 128, 128)

# Message variables
message = ""
message_color = black
message_timer = 0
message_duration = 2000  # Duration in milliseconds

# Load font
font = pygame.font.Font(None, 36)

# Define questions
questions_data = [
    [
        [
            {"question": "What is the capital of Nigeria?", "options": ["(A) Enugu", "(B) Imo", "(C) Kaduna", "(D) Abuja"], "answer": "(D) Abuja"},
            {"question": "What is the color of the Nigerian Flag", "options": ["(A) Green White Green", "(B) Green Blue Green", "(C) Green Yellow Green", "(D) Green Purple Green"], "answer": "(A) Green White Green"},
            {"question": "Who is the president of Nigeria", "options": ["(A) Peter", "(B) Buhari", "(C) Tinubu", "(D) Goodluck"], "answer": "(C) Tinubu"},
            {"question": "Nigeria is in what continent", "options": ["(A) Europe", "(B) Mars", "(C) Africa", "(D) Asia"], "answer": "(C) Africa"},
            {"question": "Which is not a major Tribe in Nigeria", "options": ["(A) Tiv", "(B) Igbo", "(C) Yoruba", "(D) Hausa"], "answer": "(A) Tiv"},
        ],
        [
            {"question": "What is the capital of Nigeria?", "options": ["(A) Enugu", "(B) Imo", "(C) Kaduna", "(D) Abuja"], "answer": "(D) Abuja"},
            {"question": "What is the color of the Nigerian Flag", "options": ["(A) Green White Green", "(B) Green Blue Green", "(C) Green Yellow Green", "(D) Green Purple Green"], "answer": "(A) Green White Green"},
            {"question": "Who is the president of Nigeria", "options": ["(A) Peter", "(B) Buhari", "(C) Tinubu", "(D) Goodluck"], "answer": "(C) Tinubu"},
            {"question": "Nigeria is in what continent", "options": ["(A) Europe", "(B) Mars", "(C) Africa", "(D) Asia"], "answer": "(C) Africa"},
            {"question": "Which is not a major Tribe in Nigeria", "options": ["(A) Tiv", "(B) Igbo", "(C) Yoruba", "(D) Hausa"], "answer": "(A) Tiv"},
        ]
    ],
    [
        [
            {"question": "What is the capital of Nigeria?", "options": ["(A) Enugu", "(B) Imo", "(C) Kaduna", "(D) Abuja"], "answer": "(D) Abuja"},
            {"question": "What is the color of the Nigerian Flag", "options": ["(A) Green White Green", "(B) Green Blue Green", "(C) Green Yellow Green", "(D) Green Purple Green"], "answer": "(A) Green White Green"},
            {"question": "Who is the president of Nigeria", "options": ["(A) Peter", "(B) Buhari", "(C) Tinubu", "(D) Goodluck"], "answer": "(C) Tinubu"},
            {"question": "Nigeria is in what continent", "options": ["(A) Europe", "(B) Mars", "(C) Africa", "(D) Asia"], "answer": "(C) Africa"},
            {"question": "Which is not a major Tribe in Nigeria", "options": ["(A) Tiv", "(B) Igbo", "(C) Yoruba", "(D) Hausa"], "answer": "(A) Tiv"},
        ]
    ]
]

section_names = [
    ["Section A.1", "Section A.2"],
    ["Section B"]
]

# Track clicked question numbers
clicked_questions = set()

# Score variables
scores = [0] * 11
score_input = ""
score_added = False
teams = ["Team " + str(i+1) for i in range(11)]
current_team = 0

# Screen state
screen_state = 'selection'  # Can be 'selection', 'question', 'answer', 'scores'

def draw_question_buttons():
    vertical_offset = 50  # Start drawing from this vertical position
    for j, section in enumerate(questions_data):
        for k, subsection in enumerate(section):
            # Display the section/subsection name
            section_name = font.render(f"{section_names[j][k]}", True, black)
            screen.blit(section_name, (50, vertical_offset))
            vertical_offset += 40  # Increase vertical offset for the questions
            
            # Draw buttons for each question in the subsection
            for i in range(1, len(subsection) + 1):
                x = 50 + ((i - 1) % 10) * 70  # Arrange buttons in 10 columns
                y = vertical_offset + ((i - 1) // 10) * 50  # Adjust vertical position based on the number of questions
                color = grey if (j, k, i) in clicked_questions else black
                pygame.draw.rect(screen, color, (x, y, 60, 40))
                num_text = font.render(str(i), True, white)
                screen.blit(num_text, (x + 20, y + 10))
            
            vertical_offset += 50 + ((len(subsection) - 1) // 10) * 50  # Adjust vertical offset for the next section/subsection

    # Draw the score button at the bottom
    score_button_rect = pygame.Rect(screen_width - 150, screen_height - 100, 140, 40)
    pygame.draw.rect(screen, black, score_button_rect)
    score_text = font.render("Scores", True, white)
    screen.blit(score_text, (screen_width - 145, screen_height - 90))

def check_question_button_click(pos):
    vertical_offset = 50
    for j, section in enumerate(questions_data):
        for k, subsection in enumerate(section):
            vertical_offset += 40  # Account for the section/subsection name
            for i in range(1, len(subsection) + 1):
                x = 50 + ((i - 1) % 10) * 70
                y = vertical_offset + ((i - 1) // 10) * 50
                button_rect = pygame.Rect(x, y, 60, 40)
                if button_rect.collidepoint(pos) and (j, k, i) not in clicked_questions:
                    global current_question, screen_state, current_questions
                    current_question = i - 1  # Adjust for 0-based index
                    current_questions = subsection  # Set the current questions to the clicked subsection
                    clicked_questions.add((j, k, i))  # Track clicked question
                    screen_state = 'question'  # Switch to question screen
                    return True
            vertical_offset += 50 + ((len(subsection) - 1) // 10) * 50  # Adjust vertical offset for the next section/subsection
    return False

def check_score_button_click(pos):
    button_rect = pygame.Rect(screen_width - 150, screen_height - 100, 140, 40)
    if button_rect.collidepoint(pos):
        global screen_state
        screen_state = 'scores'
        return True
    return False
    
def check_back_button_click(pos):
    button_rect = pygame.Rect(screen_width - 150, screen_height - 100, 140, 40)
    if button_rect.collidepoint(pos):
        global screen_state
        screen_state = 'selection'
        return True
    return False

def draw_question_screen():
    question = current_questions[current_question]
    question_text = font.render(question["question"], True, black)
    screen.blit(question_text, (50, 100))  # Adjusted for visibility
    for i, option in enumerate(question["options"]):
        option_text = font.render(option, True, black)
        screen.blit(option_text, (50, 150 + i * 40))

def draw_answer_screen():
    global message
    question = current_questions[current_question]
    answer = question["answer"]
    caption = font.render("Correct answer is:", True, black)
    screen.blit(caption, (100, 100))
    answer_text = font.render(answer, True, black)
    screen.blit(answer_text, (200, 200))
    score_input_text = font.render("Score: ", True, black)
    screen.blit(score_input_text, (100, 300))

    input_box_x = 180
    input_box_y = 300
    input_box_width = 200
    input_box_height = 40
    input_box_color = grey
    pygame.draw.rect(screen, input_box_color, (input_box_x, input_box_y, input_box_width, input_box_height))

    # Render real-time score input
    input_text = font.render(score_input, True, black)
    screen.blit(input_text, (input_box_x + 10, input_box_y + 10))

    if message and pygame.time.get_ticks() - message_timer < message_duration:
        message_text = font.render(message, True, message_color)
        screen.blit(message_text, (50, 500))
    else:
        message = ""

def draw_scores_screen():
    # Create a list of (team number, score) tuples
    scored_teams = [(i + 1, score) for i, score in enumerate(scores)]
    # Sort the list in descending order by score
    scored_teams.sort(key=lambda x: x[1], reverse=True)
    
    # Display the sorted scores
    for i, (team_num, score) in enumerate(scored_teams):
        score_text = font.render(f"{i + 1}) {teams[team_num - 1]}: {score}", True, black)
        screen.blit(score_text, (50, 50 + i * 40))
    
    # Draw the back button
    back_button_rect = pygame.Rect(screen_width - 150, screen_height - 100, 140, 40)
    pygame.draw.rect(screen, black, back_button_rect)
    back_text = font.render("Back", True, white)
    screen.blit(back_text, (screen_width - 145, screen_height - 90))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = event.pos
            if screen_state == 'selection':
                if not check_question_button_click(mouse_pos):
                    check_score_button_click(mouse_pos)
            elif screen_state == 'question':
                screen_state = 'answer'
            elif screen_state == 'answer' and score_added:
                current_team = (current_team + 1) % len(teams)
                screen_state = 'selection'
                score_added = False
            elif screen_state == 'scores':
                check_back_button_click(mouse_pos)
        elif event.type == pygame.KEYDOWN and screen_state == 'answer' and not score_added:
            if event.key in range(pygame.K_0, pygame.K_9 + 1):
                score_input += str(event.key - pygame.K_0)
            elif event.key == pygame.K_BACKSPACE:
                score_input = score_input[:-1]
            elif event.key == pygame.K_RETURN:
                message = "Added"
                message_color = green
                message_timer = pygame.time.get_ticks()
                scores[current_team] += int(score_input)
                score_input = ""
                score_added = True
                
    screen.fill(white)
    if screen_state == 'selection':
        draw_question_buttons()
    elif screen_state == 'question':
        draw_question_screen()
    elif screen_state == 'answer':
        draw_answer_screen()
    elif screen_state == 'scores':
        draw_scores_screen()

    pygame.display.flip()

pygame.quit()
