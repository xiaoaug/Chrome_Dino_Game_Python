#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/31 10:09
# @Author  : xiao
# @File    : dino.py
# @Software: PyCharm
# @Desc    :

import os
import sys
import random
import pygame
from typing import Sequence

pygame.init()  # 初始化 pygame
CLOCK = pygame.time.Clock()  # 游戏时钟

SCREEN_HEIGHT = 600  # 游戏窗口高度
SCREEN_WIDTH = 1100  # 游戏窗口宽度
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chrome Dino Runner")  # 设置游戏标题
pygame.display.set_icon(pygame.image.load(f"{os.getcwd()}/assets/DinoIco.png"))  # 设置游戏图标

# 导入恐龙的图片
RUNNING = [
    pygame.image.load(os.path.join(f"{os.getcwd()}/assets/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join(f"{os.getcwd()}/assets/Dino", "DinoRun2.png")),
]
JUMPING = pygame.image.load(os.path.join(f"{os.getcwd()}/assets/Dino", "DinoJump.png"))
DUCKING = [
    pygame.image.load(os.path.join(f"{os.getcwd()}/assets/Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join(f"{os.getcwd()}/assets/Dino", "DinoDuck2.png")),
]

# 导入仙人掌图片
SMALL_CACTUS = [
    pygame.image.load(os.path.join(f"{os.getcwd()}/assets/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join(f"{os.getcwd()}/assets/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join(f"{os.getcwd()}/assets/Cactus", "SmallCactus3.png")),
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join(f"{os.getcwd()}/assets/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join(f"{os.getcwd()}/assets/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join(f"{os.getcwd()}/assets/Cactus", "LargeCactus3.png")),
]

# 导入小鸟的图片
BIRD = [
    pygame.image.load(os.path.join(f"{os.getcwd()}/assets/Bird", "Bird1.png")),
    pygame.image.load(os.path.join(f"{os.getcwd()}/assets/Bird", "Bird2.png")),
]

# 导入云朵和地面的图片
CLOUD = pygame.image.load(os.path.join(f"{os.getcwd()}/assets/Other", "Cloud.png"))  # 云朵
FLOOR = pygame.image.load(os.path.join(f"{os.getcwd()}/assets/Other", "Track.png"))  # 地面

# 字体和背景颜色参数
FONT_COLOR = (0, 0, 0)      # 字体颜色
BG_COLOR = (247, 247, 247)  # 游戏初始背景颜色
BG_CHANGE = False           # 是否改变背景颜色
BLACK_BG = False            # 背景颜色为黑色
WHITE_BG = True             # 背景颜色为白色
BG_CHANGE_INDEX = 0         # 改变背景颜色的索引，用于颜色的渐变顺序


class Dinosaur:
    X_POS = 80        # 恐龙 x 坐标
    Y_POS = 310       # 恐龙 y 坐标
    Y_POS_DUCK = 340  # 恐龙弯腰的时候 y 坐标
    JUMP_VEL = 8.5    # 恐龙跳跃的初始速度

    def __init__(self):
        """生成一只恐龙"""
        self.duck_img = DUCKING  # 恐龙弯腰的图片
        self.run_img = RUNNING   # 恐龙跑起来的图片
        self.jump_img = JUMPING  # 恐龙跳跃的图片

        self.dino_duck = False   # 恐龙是否弯腰
        self.dino_run = True     # 恐龙是否跑起来
        self.dino_jump = False   # 恐龙是否跳跃

        self.step_index = 0  # 恐龙步数，该标志位用于按顺序切换恐龙图片
        self.jump_vel = self.JUMP_VEL  # 恐龙跳跃的速度
        self.image = self.run_img[0]   # 游戏第一帧的图像
        self.dino_rect = self.image.get_rect()  # 获取恐龙图片的尺寸
        self.dino_rect.x = self.X_POS  # 设定恐龙 x 坐标位置
        self.dino_rect.y = self.Y_POS  # 设定恐龙 y 坐标位置

    def update(self, user_input: Sequence[bool]) -> None:
        """更新恐龙的下一步操作

        :param user_input: 用户指令
        """
        # 如果步数大于 10，则需要重置步数标志位
        if self.step_index >= 10:
            self.step_index = 0

        # 恐龙跳跃指令
        if (user_input[pygame.K_UP] or user_input[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        # 恐龙弯腰指令
        elif user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        # 没有任何指令则恐龙跑起来
        elif not (self.dino_jump or user_input[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

        # 执行指令
        if self.dino_duck:  # 如果恐龙需要弯腰
            self.duck()     # 恐龙弯腰
        if self.dino_run:   # 如果恐龙需要跑起来
            self.run()      # 恐龙跑起来
        if self.dino_jump:  # 如果恐龙需要跳跃
            self.jump()     # 恐龙跳跃

    def duck(self) -> None:
        """恐龙弯腰"""
        self.image = self.duck_img[self.step_index // 5]  # 恐龙弯腰图像
        self.dino_rect = self.image.get_rect()  # 获取图片尺寸
        self.dino_rect.x = self.X_POS       # 设定恐龙 x 坐标位置
        self.dino_rect.y = self.Y_POS_DUCK  # 设定恐龙 y 坐标位置
        self.step_index += 1  # 步数 +1

    def run(self) -> None:
        """恐龙跑起来"""
        self.image = self.run_img[self.step_index // 5]  # 恐龙跑起来图像
        self.dino_rect = self.image.get_rect()  # 获取图片尺寸
        self.dino_rect.x = self.X_POS  # 设定恐龙 x 坐标位置
        self.dino_rect.y = self.Y_POS  # 设定恐龙 y 坐标位置
        self.step_index += 1  # 步数 +1

    def jump(self) -> None:
        """恐龙跳跃"""
        self.image = self.jump_img  # 恐龙跳跃图像
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4  # 改变恐龙 y 轴坐标
            self.jump_vel -= 0.8  # 跳跃速度逐渐减小
        if self.jump_vel < -self.JUMP_VEL and self.dino_rect.y >= 314:  # 跳跃速度达到最小值
            self.dino_rect.y = 314
            self.dino_jump = False  # 跳跃结束
            self.jump_vel = self.JUMP_VEL  # 还原到跳跃的初始速度

    def draw(self, screen: pygame.Surface) -> None:
        """绘制恐龙

        :param screen: pygame 游戏界面
        """
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        """生成一朵云"""
        self.x = SCREEN_WIDTH + random.randint(800, 1000)  # 随机 x 位置
        self.y = random.randint(50, 100)  # 随机 y 位置
        self.image = CLOUD  # 云朵图片
        self.width = self.image.get_width()  # 获取图片的宽度

    def update(self, game_speed: int) -> None:
        """更新云朵位置

        :param game_speed: 游戏当前速度
        """
        self.x -= game_speed  # 云朵不断往左移
        if self.x < -self.width:  # 如果云朵已经消失在屏幕中
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)  # 随机改变云朵的x位置
            self.y = random.randint(50, 100)  # 随机改变云朵的 y 位置

    def draw(self, screen: pygame.Surface) -> None:
        """绘制云朵

        :param screen: pygame 游戏界面
        """
        screen.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image: list[pygame.Surface], index: int):
        """生成一个障碍物

        :param image: 障碍物图片集
        :param index: 合集里的第几张图片索引
        """
        self.image = image      # 障碍物图片合集
        self.image_idx = index  # 第几张障碍物图片
        self.rect = self.image[self.image_idx].get_rect()  # 获取该图片的尺寸
        self.rect.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH+500)  # 障碍物的初始 x 位置

    def update(self, obstacles: list, game_speed: int) -> list:
        """更新障碍物的位置

        :param obstacles: 生成的所有障碍物
        :param game_speed: 游戏当前速度
        :return: obstacles: 所有的障碍物
        """
        self.rect.x -= game_speed  # 障碍物不断的左移
        if self.rect.x < -self.rect.width:  # 如果障碍物消失在了屏幕中，则删除掉
            obstacles.pop()  # 删除该障碍物
        return obstacles

    def draw(self, screen: pygame.Surface) -> None:
        """绘制障碍物

        :param screen: pygame 游戏界面
        """
        screen.blit(self.image[self.image_idx], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image: list[pygame.Surface]):
        """小障碍物

        :param image: 所有小障碍物图片
        """
        self.index = random.randint(0, 2)    # 随机选择一个小障碍物
        super().__init__(image, self.index)  # 继承父类
        self.rect.y = 325  # 设定小障碍物的y坐标


class LargeCactus(Obstacle):
    def __init__(self, image: list[pygame.Surface]):
        """大障碍物

        :param image: 所有大障碍物图片
        """
        self.index = random.randint(0, 2)  # 随机选择一个大障碍物
        super().__init__(image, self.index)  # 集成父类
        self.rect.y = 300  # 设定大障碍物的y坐标


class Bird(Obstacle):
    BIRD_HEIGHTS = [250, 290, 320]  # 小鸟的高度，三者随机取一

    def __init__(self, image: list[pygame.Surface]):
        """创建一只小鸟

        :param image: 所有的小鸟图片
        """
        self.index = 0  # 选择第一张小鸟图片
        super().__init__(image, self.index)  # 集成父类
        self.rect.y = random.choice(self.BIRD_HEIGHTS)  # 随机选择一个小鸟飞行的高度

    def draw(self, screen: pygame.Surface) -> None:
        """绘制小鸟

        :param screen: pygame 游戏界面
        """
        if self.index >= 9:  # 用于切换小鸟图片
            self.index = 0
        screen.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def calc_score(score: int, game_speed: int) -> tuple[int, int]:
    """计算游戏分数及游戏速度

    :param score: 游戏当前分数
    :param game_speed: 游戏当前速度
    :return: score: 游戏分数，game_speed: 游戏速度
    """
    score += 1  # 游戏分数 +1
    # 每 100 分，游戏速度 +1
    if score % 100 == 0:
        game_speed += 1
    return score, game_speed


def floor_update(x_pos_floor: int, y_pos_floor: int, game_speed: int) -> tuple[int, int]:
    """动态地板

    :param x_pos_floor: 地板图片 x 坐标
    :param y_pos_floor: 地板图片 y 坐标
    :param game_speed: 游戏当前速度
    :return: x_pos_floor: 地板图 x 坐标, y_pos_floor: 地板图 y 坐标
    """
    image_width = FLOOR.get_width()  # 获取地板图片的尺寸
    SCREEN.blit(FLOOR, (x_pos_floor, y_pos_floor))   # 显示地板
    SCREEN.blit(FLOOR, (image_width + x_pos_floor, y_pos_floor))  # 再显示一个，防止地板图片移动到最左边，背景出现空白的情况
    if x_pos_floor <= -image_width:
        x_pos_floor = 0
    x_pos_floor -= game_speed
    return x_pos_floor, y_pos_floor


def paused() -> None:
    """暂停游戏"""
    font_name = pygame.font.match_font('SimHei')  # 获得字体文件
    font = pygame.font.Font(font_name, 30)  # 设置字体大小
    text = font.render("游戏已暂停，按 u 继续游戏", True, FONT_COLOR)
    text_rect = text.get_rect()  # 获取文字尺寸
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)  # 文字的中心位置
    SCREEN.blit(text, text_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 按下 u 键继续游戏
            if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                return


def blend_color(color1: tuple[int, int, int], color2: tuple[int, int, int],
                blend_factor: float) -> tuple[int, int, int]:
    """用于转换颜色，实现颜色渐变效果

    :param color1: 最初的颜色
    :param color2: 最终的颜色
    :param blend_factor: 转换因子 [0~1]
    :return: 生成的颜色 RGB
    """
    # 用线性插值 (linear interpolation) 的方法来线性转换颜色。
    # 为了找到两种颜色的中间色，将两种颜色的差乘以一个 0~1 之间的小数，然后再加上第一种颜色。
    # 如果这个数为 0，那么结果就是第一种颜色。
    # 如果这个 0~1 之间的值，则生成的颜色会皆有两者的特色。
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r = r1 + (r2 - r1) * blend_factor
    g = g1 + (g2 - g1) * blend_factor
    b = b1 + (b2 - b1) * blend_factor

    return int(r), int(g), int(b)


def background_update(score: int) -> None:
    """根据分数切换游戏背景颜色（白天和黑天）

    :param score: 当前游戏分数
    """
    global FONT_COLOR, BG_COLOR, BG_CHANGE
    global BLACK_BG, WHITE_BG, BG_CHANGE_INDEX

    # 每积累 1000 分，则变换一次背景
    if score != 0 and score % 1000 == 0:
        BLACK_BG = ~BLACK_BG
        WHITE_BG = ~WHITE_BG
        BG_CHANGE = True
    # 把背景渐变成黑色，字体渐变成白色
    if BG_CHANGE and BLACK_BG:
        BG_CHANGE_INDEX += 1
        BG_COLOR = blend_color((247, 247, 247), (0, 0, 0), BG_CHANGE_INDEX/15)
        FONT_COLOR = blend_color((0, 0, 0), (247, 247, 247), BG_CHANGE_INDEX/15)
        # 渐变完成后，还原各种标志位
        if BG_COLOR == (0, 0, 0) and FONT_COLOR == (247, 247, 247):
            BG_CHANGE = False
            BG_CHANGE_INDEX = 0
    # 把背景渐变成白色，字体渐变成黑色
    elif BG_CHANGE and WHITE_BG:
        BG_CHANGE_INDEX += 1
        BG_COLOR = blend_color((0, 0, 0), (247, 247, 247), BG_CHANGE_INDEX / 15)
        FONT_COLOR = blend_color((247, 247, 247), (0, 0, 0), BG_CHANGE_INDEX / 15)
        # 渐变完成后，还原各种标志位
        if BG_COLOR == (247, 247, 247) and FONT_COLOR == (0, 0, 0):
            BG_CHANGE = False
            BG_CHANGE_INDEX = 0


def game() -> None:
    dinosaur = Dinosaur()  # 生成一只恐龙
    cloud = Cloud()    # 生成一朵云
    game_speed = 20    # 游戏初始速度
    x_pos_floor = 0    # 地板图片 x 坐标
    y_pos_floor = 380  # 地板图片 y 坐标
    score = 0          # 游戏分数
    obstacles = []     # 障碍物合集
    font_name = pygame.font.match_font('SimHei')  # 获得字体文件
    font = pygame.font.Font(font_name, 30)  # 设置字体大小

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 暂停
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused()

        SCREEN.fill(BG_COLOR)  # 游戏背景颜色

        user_input = pygame.key.get_pressed()  # 获取用户按键按下的位置
        dinosaur.update(user_input)  # 更新恐龙位置
        dinosaur.draw(SCREEN)        # 绘制恐龙

        # 如果没有障碍物，则生成障碍物
        if len(obstacles) == 0:
            select_obstacle = random.randint(0, 2)  # 随机选择障碍物类型
            if select_obstacle == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))  # 小障碍物
            elif select_obstacle == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))  # 大障碍物
            elif select_obstacle == 2:
                obstacles.append(Bird(BIRD))  # 小鸟障碍物

        for obstacle in obstacles:
            obstacle.draw(SCREEN)  # 绘制障碍物
            obstacles = obstacle.update(obstacles, game_speed)  # 更新障碍物的位置
            # 恐龙撞到了障碍物
            if dinosaur.dino_rect.colliderect(obstacle.rect):
                # 读取分数文件，获取历史最高分
                with open("score.txt", "r") as file:
                    txt_score = (file.read())
                    score_ints = [int(x) for x in txt_score.split()]  # 将分数转成整型
                high_score = max(score_ints)  # 找到历史最高分
                # 如果当前游戏分数大于历史最高分，则修改文件，将当前分数写进文档中
                if high_score < score:
                    with open("score.txt", "w") as file:
                        file.write(str(score))
                pygame.time.delay(500)  # 等待 0.5s，防止用户误按按键导致游戏重开
                menu(False, score)  # 返回到菜单页

        x_pos_floor, y_pos_floor = floor_update(x_pos_floor, y_pos_floor, game_speed)  # 动态地板

        cloud.update(game_speed)  # 更新云朵位置
        cloud.draw(SCREEN)  # 绘制云朵

        score, game_speed = calc_score(score, game_speed)  # 计算游戏分数

        background_update(score)  # 根据分数动态改变游戏背景颜色

        # 显示游戏当前分数
        score_text = font.render(f"分数：{score}", True, FONT_COLOR)
        SCREEN.blit(score_text, (930, 0))  # 显示分数文字

        # 显示游戏速度
        game_speed_text = font.render(f"速度：{game_speed}", True, FONT_COLOR)
        SCREEN.blit(game_speed_text, (930, 30))  # 显示游戏速度文字

        CLOCK.tick(30)  # 游戏帧数
        pygame.display.update()


def menu(first_start: bool, score: int = 0) -> None:
    """菜单页

    :param first_start: 是不是第一次启动游戏
    :param score: 游戏分数，默认为 0
    """
    global FONT_COLOR, BG_COLOR
    while True:
        SCREEN.fill(BG_COLOR)  # 背景颜色
        font_name = pygame.font.match_font('SimHei')  # 获得字体文件
        font = pygame.font.Font(font_name, 30)  # 设置字体大小

        if first_start:  # 如果是第一次启动游戏
            text = font.render("按任意键开始游戏", True, FONT_COLOR)
            text_rect = text.get_rect()  # 获取文字的尺寸
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # 文字的中心位置
            SCREEN.blit(text, text_rect)  # 显示提示文字
            SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 - 140))  # 显示恐龙图片
        else:  # 如果不是第一次启动游戏，即上局游戏死亡了
            text = font.render("按任意键重新开始游戏", True, FONT_COLOR)
            text_rect = text.get_rect()  # 获取文字的尺寸
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # 文字的中心位置
            SCREEN.blit(text, text_rect)  # 显示提示文字
            SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 - 140))  # 显示恐龙图片

            score_text = font.render("你的分数：" + str(score), True, FONT_COLOR)
            score_text_rect = score_text.get_rect()  # 获取游戏分数文字的尺寸
            score_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)  # 分数文字的中心位置
            SCREEN.blit(score_text, score_text_rect)  # 显示分数文字

            with open("score.txt", "r") as file:
                txt_score = (file.read())
                score_ints = [int(x) for x in txt_score.split()]  # 将分数转成整型
            high_score = max(score_ints)  # 找到历史最高分
            high_score_text = font.render(f"历史最高分：{str(high_score)}", True, FONT_COLOR)
            high_score_rect = high_score_text.get_rect()  # 获取最高分文字的尺寸
            high_score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)  # 最高分文字的中心位置
            SCREEN.blit(high_score_text, high_score_rect)  # 显示最高分文字

        background_update(score)  # 根据分数动态改变游戏背景颜色
        CLOCK.tick(30)  # 游戏帧数
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 按下任意按键进入游戏
            if event.type == pygame.KEYDOWN:
                game()


if __name__ == '__main__':
    menu(first_start=True)
