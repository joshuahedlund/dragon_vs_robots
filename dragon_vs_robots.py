import sys
from time import sleep

import pygame

from models.sprites.bullet import Bullet
from models.sprites.player import Player
from models.sprites.robot import Robot
from models.sprites.robot_boss import RobotBoss
from models.sprites.super_bullet import SuperBullet

from models.components.button import Button

from models.data.game_stats import GameStats
from models.data.scoreboard import Scoreboard
from models.data.settings import Settings

class DragonVsRobots:
    def __init__(self):
        """ Initialize the game """
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Robot Invasion")

        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        self.player = Player(self)
        self.boss = RobotBoss(self)
        self.robots = pygame.sprite.Group()
        self.fired_bullets = pygame.sprite.Group()
        self.collectible_bullets = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game """
        while True:
            #Watch for keyboard and mouse events
            self._check_events()
            if self.stats.game_active:
                # Update sprite positions
                self.player.update()
                self._update_bullets()
                self._update_robots()
                # Check for collisions
                self._check_collect_bullet()
                self._check_player_hit()
                self._check_enemy_hit()
                self._check_boss_hit()
                # Check for edges
                self._check_robots_edge()
                self._check_bullets_edge()
                # Check for game
                self._check_boss_time()
            self._update_screen()

    def _create_fleet(self):
        # Determine robots per row
        robot = Robot(self)
        robot_width, robot_height = robot.rect.size
        available_space_x = self.settings.screen_width - (7 * robot_width)
        number_robots_x = 3 #available_space_x // (2 * robot_width)

        # Determine number of rows
        available_space_y = (self.settings.screen_height - (1 * robot_height))
        number_rows = available_space_y // (2 * robot_height)

        # Create the fleet of robots
        for row_number in range(number_rows):
            for robot_number in range(number_robots_x):
                self._create_robot(robot_number, row_number)

        # Create boss
        self._create_boss(robot_width, robot_number + 1)

    def _create_robot(self, robot_number, row_number):
        robot = Robot(self)
        robot_width, robot_height = robot.rect.size
        robot.x = (7 * robot_width) + (2 * robot_width * robot_number)
        robot.x_orig = robot.x
        robot.rect.x = robot.x
        robot.y = self.settings.margin + (2 * robot.rect.height * row_number)
        robot.rect.y = robot.y
        self.robots.add(robot)

    def _create_boss(self, robot_width, column_number):
        boss_x = (7 * robot_width) + (2 * robot_width * column_number)
        self.boss.set_init_position(boss_x)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.player.moving_x = self.settings.player_speed
        elif event.key == pygame.K_LEFT:
            self.player.moving_x = -1 * self.settings.player_speed
        elif event.key == pygame.K_UP:
            self.player.moving_y = -1 * self.settings.player_speed
        elif event.key == pygame.K_DOWN:
            self.player.moving_y = self.settings.player_speed
        elif event.key == pygame.K_SPACE:
            if not self.stats.game_started:
                self._start_game()
            else:
                self._fire_bullet()
        elif event.key == pygame.K_p:
            self._toggle_game()
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            self.player.moving_x = 0
        elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            self.player.moving_y = 0

    def _check_play_button(self, mouse_pos):
        if not self.stats.game_active and self.play_button.rect.collidepoint(mouse_pos):
            self._start_game()

    def _toggle_game(self):
        if not self.stats.game_started:
            self._start_game()
        else: #pause or unpause
            self.stats.game_active = not self.stats.game_active

    def _start_game(self):
        self.stats.game_started = True
        self.stats.game_active = True
        self.stats.set_game()
        self._reset_board()

    def _update_screen(self):
        #Redraw the screen during each pass
        self.screen.fill(self.settings.bg_color)

        self.player.draw()
        self.fired_bullets.draw(self.screen)
        self.collectible_bullets.draw(self.screen)
        self.robots.draw(self.screen)
        self.boss.draw()
        self.scoreboard.draw()

        if not self.stats.game_active:
            self.play_button.draw_button()

        #Make the most recently drawn screen visible
        pygame.display.flip()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if not self.stats.game_active:
            return

        if self.player.inv_super_bullets > 0:
            self._fire_super_bullet()
        elif len(self.fired_bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            new_bullet.set_pos_from_player(self.player.rect)
            self.fired_bullets.add(new_bullet)

    def _make_super_bullet(self):
        new_super_bullet = SuperBullet(self)
        new_super_bullet.set_pos_random(self.player.rect.x)
        self.collectible_bullets.add(new_super_bullet)

    def _collect_super_bullet(self, super_bullet):
        self.collectible_bullets.remove(super_bullet)
        self.player.inv_super_bullets += 1

    def _fire_super_bullet(self):
        if self.stats.game_active and self.player.inv_super_bullets > 0:
            fired_super_bullet = SuperBullet(self)
            fired_super_bullet.set_pos_from_player(self.player.rect)
            self.fired_bullets.add(fired_super_bullet)
            self.player.inv_super_bullets -= 1

    def _update_bullets(self):
        #Update bullet positions
        self.fired_bullets.update()
        self.collectible_bullets.update()

    def _update_robots(self):
        self.settings.fleet_cur_shift_cycles += 1
        self._check_fleet_edges()
        self.robots.update()
        self.boss.update()

    def _check_fleet_edges(self):
        should_change = False
        if self.settings.is_at_max_shift_cycles():
            should_change = True
        else:
            for robot in self.robots.sprites():
                if robot.is_at_edge():
                    should_change = True
                    break

        if should_change:
            self._change_fleet_direction()

    def _change_fleet_direction(self):
        """ Shift the fleet and change direction """
        for robot in self.robots.sprites():
            robot.rect.x -= self.settings.fleet_drop_speed
        self.settings.update_fleet_direction()

    def _check_collect_bullet(self):
        collected_bullet = pygame.sprite.spritecollideany(self.player, self.collectible_bullets)
        if collected_bullet and not collected_bullet.is_moving: # don't collect fired bullets
            self._collect_super_bullet(collected_bullet)

    def _check_player_hit(self):
        if pygame.sprite.spritecollideany(self.player, self.robots):
            self._lose_life()

    def _check_enemy_hit(self):
        # Remove any collided robots and bullets
        collisions = pygame.sprite.groupcollide(self.fired_bullets, self.robots, True, True)
        if collisions:
            robots_hit_cnt = 0
            for robots_hit in collisions.values():
                robots_hit_cnt += len(robots_hit)
            self.scoreboard.update_score(robots_hit_cnt * self.settings.hit_points)

    def _check_boss_hit(self):
        fired_bullet = pygame.sprite.spritecollideany(self.boss, self.fired_bullets)
        if fired_bullet and type(fired_bullet) == SuperBullet:
            self.scoreboard.update_score(self.settings.boss_hit_points)
            self.fired_bullets.remove(fired_bullet)
            self.stats.boss_life_left -= 1
            if self.stats.boss_life_left <= 0:
                self._win_game()

    def _check_robots_edge(self):
        screen_rect = self.screen.get_rect()
        for robot in self.robots.sprites():
            if robot.rect.left <= screen_rect.left:
                self._lose_life()
                break

    def _check_bullets_edge(self):
        #Get rid of bullets past the screen
        for bullet in self.fired_bullets.copy():
            if bullet.rect.right > self.settings.screen_width:
                self.fired_bullets.remove(bullet)
                self.scoreboard.update_score(self.settings.miss_points)

    def _check_boss_time(self):
        if len(self.robots) == 0 and len(self.collectible_bullets) == 0:
            self._make_super_bullet()

    def _win_game(self):
        self.play_button = Button(self, "You Win! Play Again")
        self.stats.game_started = False
        self.stats.game_active = False

    def _lose_game(self):
        self.play_button = Button(self, "You Lose! Play Again")
        self.stats.game_started = False
        self.stats.game_active = False

    def _lose_life(self):
        self.stats.player_life_left -= 1
        self.scoreboard.render_lives()

        if self.stats.player_life_left <= 0:
            self._lose_game()
            return

        self.fired_bullets.empty()
        self.collectible_bullets.empty()
        self._reset_enemy_x()

        self.player.center()

        sleep(0.5)

    def _reset_board(self):
        self.robots.empty()
        self.fired_bullets.empty()
        self.scoreboard.reset_score()
        self.scoreboard.draw()

        # New fleet
        self._create_fleet()
        self.player.center()

    def _reset_enemy_x(self):
        """ Return robots to original horizontal position """
        for robot in self.robots.sprites():
            robot.rect.x = robot.x_orig

if __name__ == '__main__':
    game = DragonVsRobots()
    game.run_game()