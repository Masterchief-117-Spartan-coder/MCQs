import pygame
import math
import textwrap
import sys
from Automated_MCQ import TESTING
import os
import re

pygame.init()
clock = pygame.time.Clock()
clock.tick(60)
pygame.display.set_caption('MCQs PROJECT [VERSION-0.0.1]')


class Game:
    def __init__(self):
        self.score_modifier = False
        self.question_count = 10
        self.csv_file = ""
        self.database_selection = True
        self.accepted_message = ''
        self.start_ticks = -100
        self.name = "UNKNOWN"  # name and some screen activations ------
        self.intro_screen_bool = True
        self.testing_1_bool = False
        self.score_screen_bool = False
        self.screen = pygame.display.set_mode((700, 600))
        self.loop_count_question = 0
        self.score = 0
        self.questions_wrong = []
        self.button_loc = []
        self.error = False
        self.input_taken = None  # --- question display data ----
        self.answer_taken = None
        self.button_loc_bool = True
        self.data_fetch = True
        self.base_font = pygame.font.Font(None, 32)  # Naming data -----
        self.user_text = ''
        self.user_text2 = ''
        self.input_box_naming2 = pygame.Rect(10, 200, 100, 32)
        self.input_box_naming = pygame.Rect(200, 500, 100, 32)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('chartreuse4')
        self.color = self.color_passive
        self.active = False
        self.color2 = self.color_passive
        self.active2 = False

    def main_screen(self):
        while True:
            mouse_tracker = pygame.mouse.get_pos()
            if self.intro_screen_bool:
                self.title_screen()
            if self.testing_1_bool:
                self.tesing_1_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.intro_screen_bool:
                        if self.input_box_naming.collidepoint(event.pos):
                            self.active = True

                        else:
                            self.active = False
                    if self.testing_1_bool:
                        if self.database_selection:
                            if self.input_box_naming2.collidepoint(event.pos):
                                self.active2 = True

                        else:
                            self.active2 = False
                if event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            self.user_text += event.unicode
                        if event.key == pygame.K_ESCAPE:
                            if len(self.user_text) > 3:
                                self.name = self.user_text[:-1]
                                self.profiler()
                                self.user_text = ''
                                self.accepted_message = 'ACCEPTED NAME'
                                self.error = True
                            else:
                                self.error = True
                                self.user_text = ""
                                self.accepted_message = 'UNACCEPTABLE FORMAT'
                    if self.active2:
                        if self.testing_1_bool:
                            if event.key == pygame.K_ESCAPE:
                                print(len(self.scanner_databases()))
                                if len(self.scanner_databases()) == 1:
                                    self.csv_file = self.scanner_databases()[0]
                                    print("jj")
                                    self.user_text2 = ''
                                    self.accepted_message = 'ACCEPTED NAME'
                                    self.error = True
                                    self.database_selection = False  # TODO: EXCEPTION TACKLE
                                    self.button_loc_bool = True
                                else:
                                    self.error = True
                                    self.user_text2 = ""
                                    self.accepted_message = 'UNACCEPTABLE FORMAT!'
                            if event.key == pygame.K_BACKSPACE:
                                self.user_text2 = self.user_text2[:-1]
                            else:
                                self.user_text2 += event.unicode
                    if event.key == pygame.K_q:
                        if self.testing_1_bool:
                            for i in range(len(self.button_loc)):
                                if self.question_count == self.loop_count_question:
                                    if self.button_loc[i][1] < mouse_tracker[1] < (self.button_loc[i][2]):
                                        if self.button_loc[i][0] < mouse_tracker[0] < (self.button_loc[i][3]):
                                            self.loop_count_question += 1
                            if not self.database_selection:
                                if self.loop_count_question < self.question_count:
                                    answer_keys = ['a', 'b', 'c', 'd']
                                    for i in range(0, 4):
                                        # print(self.button_loc)
                                        if self.button_loc[i][1] < mouse_tracker[1] < (self.button_loc[i][2]):
                                            if self.button_loc[i][0] < mouse_tracker[0] < (self.button_loc[i][3]):
                                                self.loop_count_question += 1
                                                self.button_loc_bool = True
                                                print(self.loop_count_question)
                                                if self.answer_taken[-1] == answer_keys[i]:
                                                    # print('true')
                                                    self.score += 1
                        print(mouse_tracker)
                        if self.intro_screen_bool:
                            if self.button_loc[0][1] < mouse_tracker[1] < (self.button_loc[0][2]):
                                if self.button_loc[0][0] < mouse_tracker[0] < (self.button_loc[0][3]):
                                    self.testing_1_bool = True
                                    self.intro_screen_bool = False
                                    self.button_loc_bool = True
                            if self.button_loc[1][1] < mouse_tracker[1] < (self.button_loc[1][2]):
                                if self.button_loc[1][0] < mouse_tracker[0] < (self.button_loc[1][3]):
                                    print("hiel2.0")
            if self.loop_count_question >= self.question_count + 1:
                self.testing_1_bool = False
                self.intro_screen_bool = True
                self.button_loc_bool = True
                self.database_selection = True
                self.data_fetch = True
                self.error = False
                self.loop_count_question = 0
                self.score_modifier = True
                # self.question_count = 0
            pygame.display.update()

    def title_screen(self):
        if self.active:
            self.color = self.color_active
        else:
            self.color = self.color_passive
        texts = ["MCQs Bank", "TRAINING", "OVERALL SCORE"]
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font('freesansbold.ttf', 32)
        if self.button_loc_bool:
            if len(self.button_loc) > 0:
                self.button_loc.clear()
            self.button_loc.append(self.continue_calculator(textwrap.fill(texts[1], width=71), 100, loc=True,
                                                            x_axis=240, separator=100,
                                   pre_text=math.ceil(len(texts[0])/71), custom_position=True))
            self.button_loc.append(self.continue_calculator(textwrap.fill(texts[2], width=71), 100, loc=True,
                                                            x_axis=240, separator=150,
                                   pre_text=math.ceil(len(texts[1])/71), custom_position=True))
            self.button_loc_bool = False
        self.continue_calculator(textwrap.fill(texts[0], width=71), 100, loc=False, x_axis=240,
                                 custom_position=True, separator=30, button=False, font2=pygame.font.Font
                                 ('freesansbold.ttf', 32))
        self.continue_calculator(textwrap.fill(texts[1], width=71), 100, loc=False, x_axis=240, separator=100,
                                 pre_text=math.ceil(len(texts[0])/71), custom_position=True)
        self.continue_calculator(textwrap.fill(texts[2], width=71), 100, loc=False, x_axis=240, separator=150,
                                 pre_text=math.ceil(len(texts[1])/71), custom_position=True)
        self.continue_calculator(textwrap.fill("NAME: ", width=71), 0, loc=False, x_axis=80,
                                 custom_position=True, separator=500, button=False, font2=pygame.font.Font
                                 ('freesansbold.ttf', 28))
        self.continue_calculator(textwrap.fill(f"USER: {self.name}", width=71), 0, loc=False, x_axis=10,
                                 custom_position=True, separator=10, button=False, font2=pygame.font.Font
                                 ('freesansbold.ttf', 20))
        if self.error:
            if self.start_ticks < 0:
                self.continue_calculator(textwrap.fill(self.accepted_message, width=71), 0, loc=False, x_axis=10,
                                         custom_position=True, separator=550, button=False, font2=pygame.font.Font
                                         ('freesansbold.ttf', 14))
            else:
                self.start_ticks = -100
                self.error = False
            self.start_ticks += 1

        pygame.draw.rect(self.screen, self.color, self.input_box_naming)
        text_surface = self.base_font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_box_naming.x + 5, self.input_box_naming.y + 5))
        self.input_box_naming.w = max(100, text_surface.get_width() + 10)
        if self.score_modifier:
            pass  # TODO: this type plus sql type...

    def success(self):
        if self.button_loc_bool:
            if len(self.button_loc) > 0:
                self.button_loc.clear()
            self.button_loc.append(self.continue_calculator(textwrap.fill("Back to title screen", width=71), 100,
                                                            loc=True, x_axis=240, separator=300, custom_position=True))
            self.button_loc_bool = False
        self.continue_calculator(textwrap.fill(F"YOU SCORE: {self.score}", width=71), 100, loc=False, x_axis=200,
                                 custom_position=True, separator=100, button=False, font2=pygame.font.Font
                                 ('freesansbold.ttf', 32))
        self.continue_calculator(textwrap.fill("Back to title screen", width=71), 100, loc=False, x_axis=240,
                                 custom_position=True, separator=300, button=False, font2=pygame.font.Font
                                 ('freesansbold.ttf', 20))

    def tesing_1_screen(self):
        global data, fonty
        if self.active:
            self.active = False
            self.user_text = ''
        self.screen.fill((0, 0, 0))
        if self.database_selection:
            if self.button_loc_bool:
                if len(self.button_loc) > 0:
                    self.button_loc.clear()
                self.button_loc.append(self.continue_calculator(textwrap.fill("databases available: ", width=71),
                                                                100, loc=True, x_axis=200, separator=100,
                                                                custom_position=True))
                self.button_loc_bool = False

            if self.active2:
                self.color2 = self.color_active
            else:
                self.color2 = self.color_passive
            self.continue_calculator(textwrap.fill("databases available: ", width=71), 100, loc=False, x_axis=200,
                                     separator=100, custom_position=True)
            self.continue_calculator(textwrap.fill("Name the database in the box: ", width=71), 0, loc=False, x_axis=10,
                                     custom_position=True, separator=500, button=False, font2=pygame.font.Font
                                     ('freesansbold.ttf', 28))

            pygame.draw.rect(self.screen, self.color2, self.input_box_naming2)
            text_surface = self.base_font.render(self.user_text2, True, (255, 255, 255))
            self.screen.blit(text_surface, (self.input_box_naming2.x + 5, self.input_box_naming2.y + 5))
            self.input_box_naming2.w = max(100, text_surface.get_width() + 10)
            if self.error:
                if self.start_ticks < 0:
                    self.continue_calculator(textwrap.fill(self.accepted_message, width=71), 0, loc=False, x_axis=10,
                                             custom_position=True, separator=100, button=False, font2=pygame.font.Font
                                             ('freesansbold.ttf', 14))
                else:
                    self.start_ticks = -100
                    self.error = False
                self.start_ticks += 1
            if len(self.scanner_databases()) > 0:
                for i in range(len(self.scanner_databases())):
                    self.continue_calculator(textwrap.fill(self.scanner_databases()[i], width=71), 0, loc=False,
                                             x_axis=200, custom_position=True, separator=126 + i*12,
                                             button=False, font2=pygame.font.Font('freesansbold.ttf', 10))
            else:
                self.continue_calculator(textwrap.fill("EMPTY", width=71), 0, loc=False, x_axis=200,
                                         custom_position=True, separator=126, button=False,
                                         font2=pygame.font.Font('freesansbold.ttf', 10))

        if not self.database_selection:
            if self.active2:
                self.active2 = False
                self.user_text2 = ''
            if self.data_fetch:
                fonty = pygame.font.Font('freesansbold.ttf', 14)
                # self.csv_file = "databases/full_biology_v-3.1.csv"
                section_2 = TESTING("hello_world", self.csv_file)
                data = section_2.GUI_trainer(self.question_count)
                self.data_fetch = False
                print(f"how much : {data}")
            for i in range(len(data)):
                if i == self.loop_count_question:
                    self.answer_taken = data[i]['Answer']
                    data2 = str(i+1) + str(". ") + str(data[i]['question'][3:])
                    self.continue_calculator(textwrap.fill(data2, width=71, tabsize=10), 0, loc=False, x_axis=30,
                                             separator=10, pre_text=math.ceil(len(data[i]['question']) / 71),
                                             custom_position=True, button=False, font2=pygame.font.Font
                                             ('freesansbold.ttf', 16))
                    if self.button_loc_bool:
                        if len(self.button_loc) > 0:
                            self.button_loc.clear()
                        self.button_loc.append(self.continue_calculator(textwrap.fill(data[i]['A'], width=71), 100,
                                               loc=True, x_axis=30,
                                               separator=90, pre_text=math.ceil(len(data[i]['question']) / 71),
                                               custom_position=True, x=30, font=fonty))
                        self.button_loc.append(self.continue_calculator(textwrap.fill(data[i]['B'], width=71), 100,
                                                                        loc=True, x_axis=30, font=fonty,
                                               separator=160, pre_text=math.ceil(len(data[i]['question']) / 71),
                                               custom_position=True, x=30))
                        self.button_loc.append(self.continue_calculator(textwrap.fill(data[i]['C'], width=71), 100,
                                                                        loc=True, x_axis=30, font=fonty,
                                               separator=230, pre_text=math.ceil(len(data[i]['question']) / 71),
                                               custom_position=True, x=30))
                        self.button_loc.append(self.continue_calculator(textwrap.fill(data[i]['D'], width=71), 100,
                                                                        loc=True, x_axis=30, font=fonty,
                                               separator=300, pre_text=math.ceil(len(data[i]['question']) / 71),
                                               custom_position=True, x=30))
                        self.button_loc_bool = False
                    self.continue_calculator(textwrap.fill(data[i]['A'], width=71), 100, loc=False, x_axis=30,
                                             separator=90, pre_text=math.ceil(len(data[i]['question']) / 71),
                                             custom_position=True, x=30, font=fonty)
                    self.continue_calculator(textwrap.fill(data[i]['B'], width=71), 100, loc=False, x_axis=30,
                                             separator=160, pre_text=math.ceil(len(data[i]['question']) / 71),
                                             custom_position=True, x=30, font=fonty)
                    self.continue_calculator(textwrap.fill(data[i]['C'], width=71), 100, loc=False, x_axis=30,
                                             separator=230, pre_text=math.ceil(len(data[i]['question']) / 71),
                                             custom_position=True, x=30, font=fonty)
                    self.continue_calculator(textwrap.fill(data[i]['D'], width=71), 100, loc=False, x_axis=30,
                                             separator=300, pre_text=math.ceil(len(data[i]['question']) / 71),
                                             custom_position=True, x=30, font=fonty)
            if self.loop_count_question == self.question_count:
                self.success()
            # TODO: testing... (almost done!)

    def testing_type2(self):
        pass

    def scanner_databases(self):
        list_of_databases = []
        identified = []
        dir_path = os.path.dirname(os.path.realpath(__file__))

        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith('v-3.1.csv'):
                    list_of_databases.append(root + '/' + str(file))
        for i in range(len(list_of_databases)):
            # print(re.search(self.user_text2, i))
            if re.search(self.user_text2, list_of_databases[i]) is not None:
                identified.append(list_of_databases[i])
        return identified

    def profiler(self):
        path = os.getcwd()
        try:
            os.mkdir(path + f"/profiles")
        except OSError:
            pass
        finally:
            try:
                os.mkdir(path + f"/profiles" + f"/{self.name}")
            except OSError:
                pass

    def sql_profiler(self):
        pass

    def score_screen(self):
        # TODO: save score on text.dat file...
        pass

    def continue_calculator(self, text, color, loc=False, separator=20, x_axis=50, green=5, font=pygame.font.Font
                            ('freesansbold.ttf', 18), custom_position=False, pre_text=1, button=True, x=100,
                            font2=pygame.font.Font('freesansbold.ttf', 16)):
        val = 0
        if custom_position:
            val += separator
            if loc:
                return [x, val, val+20 * math.sqrt(len(text.splitlines())), x+400]
            else:
                color1 = (0, 200, 100)
                if button:
                    text = text.splitlines()
                    for i in range(len(text)):
                        pygame.draw.rect(self.screen, color1, pygame.Rect(x, val, 475, 35 * (len(text)/2)))
                        self.screen.blit(font.render(f" {text[i]} ", True, (0, 239, 239), (0, green, color)),
                                         (x_axis, val))
                        val += 35/2
                else:
                    text = text.splitlines()
                    for i in range(len(text)):
                        self.screen.blit(font2.render(f" {text[i]} ", True, (239, 239, 90), (0, green, color)), (x_axis,
                                                                                                                 val))
                        val += separator + (5 * math.sqrt(pre_text))


game_1 = Game()
game_1.main_screen()
