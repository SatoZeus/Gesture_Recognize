#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
宝藏冒险游戏 (Treasure Adventure Game)
一个简单而有趣的文字冒险游戏，用于展示Python的基础编程概念
包含：条件语句、循环结构、异常处理、函数定义等
"""

import random
import time
import sys
import os

def print_slow(text):
    """
    缓慢打印文本，营造游戏氛围
    参数:
        text: 需要打印的文本
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)  # 调整此值可改变打印速度
    print()

def clear_screen():
    """
    清空屏幕，使界面更整洁（跨平台实现）
    """
    print("\n" * 50)

def get_valid_input(prompt, valid_options):
    """
    获取并验证用户输入
    参数:
        prompt: 提示用户的文本
        valid_options: 有效选项列表
    返回:
        用户输入的有效选项
    """
    while True:
        try:
            # 显示提示并获取用户输入
            print_slow(prompt)
            choice = input("请输入您的选择: ").strip().upper()
            
            # 检查输入是否在有效选项中
            if choice in valid_options:
                return choice
            else:
                print_slow(f"无效选择！请输入: {', '.join(valid_options)}")
        except KeyboardInterrupt:
            # 处理Ctrl+C终止程序的异常
            print_slow("\n游戏被中断。再见！")
            sys.exit(0)
        except Exception as e:
            # 处理其他可能的异常
            print_slow(f"发生错误: {e}")
            print_slow("请重试。")
# 添加颜色支持（增强像素艺术效果）
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

# ASCII艺术图案
ASCII_ART = {
    "title": f"""{Colors.CYAN}
    ╔═══════════════════════════════════════════════════╗
    ║             {Colors.YELLOW}神 秘 岛 屿 寻 宝 记{Colors.CYAN}              ║
    ║                                                   ║
    ║    {Colors.WHITE}/|{Colors.CYAN}          {Colors.BLUE}~~~{Colors.CYAN}          {Colors.GREEN}/\\{Colors.CYAN}      {Colors.YELLOW}☼{Colors.CYAN}        ║
    ║   {Colors.WHITE}/ |{Colors.CYAN}         {Colors.BLUE}~~~~~{Colors.CYAN}       {Colors.GREEN}/  \\{Colors.CYAN}              ║
    ║  {Colors.WHITE}/__|______{Colors.CYAN}   {Colors.BLUE}~~~~~~~{Colors.CYAN}    {Colors.GREEN}/    \\{Colors.CYAN}             ║
    ║  {Colors.YELLOW}|  |==== |{Colors.CYAN}  {Colors.BLUE}~{Colors.CYAN}   {Colors.BLUE}~{Colors.CYAN}   {Colors.GREEN}/      \\{Colors.CYAN}     {Colors.RED}△{Colors.CYAN}       ║
    ║  {Colors.YELLOW}|  |     |{Colors.CYAN} {Colors.BLUE}~~~~~~~~~{Colors.CYAN} {Colors.GREEN}/________\\{Colors.CYAN}            ║
    ║{Colors.GREEN}^^^^^^^^^^^^^^{Colors.BLUE}~~~~~~~~~~~~~~~~~~~~~{Colors.GREEN}^^^^^^^^^^^^{Colors.CYAN}║
    ╚═══════════════════════════════════════════════════╝{Colors.RESET}
    """,
    "beach": f"""{Colors.CYAN}
    {Colors.YELLOW}☼{Colors.CYAN}                                         
       {Colors.BLUE}~~~~~{Colors.CYAN}                                     
      {Colors.BLUE}~~~~~~~{Colors.CYAN}                {Colors.GREEN}/\\{Colors.CYAN}                  
     {Colors.BLUE}~~~~~~~~~{Colors.CYAN}              {Colors.GREEN}/  \\{Colors.CYAN}                 
    {Colors.BLUE}~~~~~~~~~~~{Colors.CYAN}            {Colors.GREEN}/    \\{Colors.CYAN}                
   {Colors.BLUE}~~~~~~~~~~~~~{Colors.CYAN}          {Colors.GREEN}/      \\{Colors.CYAN}               
  {Colors.BLUE}~~~~~~~~~~~~~~~{Colors.CYAN}        {Colors.GREEN}/________\\{Colors.CYAN}              
 {Colors.YELLOW}...{Colors.BLUE}~~~~~~~~~~~~~~~{Colors.YELLOW}...{Colors.GREEN}^^^^^^^^^^^^^^^{Colors.YELLOW}...{Colors.CYAN}
{Colors.YELLOW} ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈{Colors.RESET}
    """,
    "cave": f"""{Colors.WHITE}
    ______________________________________________
   /                                              \\
  /                                                \\
 /     {Colors.YELLOW}*{Colors.WHITE}                         {Colors.YELLOW}*{Colors.WHITE}               \\
|                {Colors.YELLOW}*{Colors.WHITE}                                 |
|        {Colors.PURPLE}▓{Colors.WHITE}                                       |
|       {Colors.PURPLE}▓▓▓{Colors.WHITE}                                      |
|      {Colors.PURPLE}▓▓▓▓▓{Colors.WHITE}                   {Colors.YELLOW}^{Colors.WHITE}                |
|  {Colors.BLUE}~{Colors.WHITE}  {Colors.PURPLE}▓▓▓▓▓{Colors.WHITE}                  {Colors.YELLOW}/|\\{Colors.WHITE}               |
|{Colors.BLUE}~~~{Colors.WHITE}       {Colors.YELLOW}*{Colors.WHITE}                  {Colors.YELLOW}/ | \\{Colors.WHITE}              |
 \\__{Colors.BLUE}~{Colors.WHITE}_________________________________________/
    {Colors.RESET}
    """,
    "temple": f"""{Colors.YELLOW}
          ╔═════════════════╗
          ║                 ║
    ╔═════╩═════════════════╩═════╗
    ║        {Colors.RED}▲ ▲ ▲ ▲ ▲{Colors.YELLOW}        ║
    ║        {Colors.RED}║ ║ ║ ║ ║{Colors.YELLOW}        ║
    ║     {Colors.GREEN}╔═╧═╧═╧═╧═╧═╗{Colors.YELLOW}     ║
    ║     {Colors.GREEN}║         ║{Colors.YELLOW}     ║
    ║     {Colors.GREEN}║    □    ║{Colors.YELLOW}     ║
    ║     {Colors.GREEN}║         ║{Colors.YELLOW}     ║
    ╚═════╦═══════════════╦═════╝
          ║               ║
         {Colors.WHITE}▓▓▓{Colors.YELLOW}             {Colors.WHITE}▓▓▓{Colors.YELLOW}
        {Colors.WHITE}▓▓▓▓▓{Colors.YELLOW}           {Colors.WHITE}▓▓▓▓▓{Colors.YELLOW}
       {Colors.WHITE}▓▓▓▓▓▓▓{Colors.YELLOW}         {Colors.WHITE}▓▓▓▓▓▓▓{Colors.YELLOW}
      {Colors.WHITE}▓▓▓▓▓▓▓▓▓{Colors.YELLOW}       {Colors.WHITE}▓▓▓▓▓▓▓▓▓{Colors.RESET}
    """,
    "treasure": f"""{Colors.YELLOW}
        {Colors.YELLOW}★{Colors.RESET}          {Colors.WHITE}✦{Colors.RESET}           {Colors.YELLOW}★{Colors.RESET}
      
     {Colors.YELLOW}╔═════════════════════════╗
     ║  {Colors.WHITE}○{Colors.YELLOW} {Colors.RED}◆{Colors.YELLOW} {Colors.WHITE}○{Colors.YELLOW} {Colors.GREEN}❖{Colors.YELLOW} {Colors.WHITE}○{Colors.YELLOW} {Colors.BLUE}◇{Colors.YELLOW} {Colors.WHITE}○{Colors.YELLOW}  ║
     ║ {Colors.WHITE}○{Colors.YELLOW}   {Colors.RED}╭───╮{Colors.YELLOW}   {Colors.WHITE}○{Colors.YELLOW} ║
     ║{Colors.WHITE}○{Colors.YELLOW} {Colors.RED}╱│{Colors.YELLOW}     {Colors.RED}│╲{Colors.YELLOW} {Colors.WHITE}○{Colors.YELLOW}║
     ║{Colors.RED}╱ │{Colors.YELLOW}  {Colors.WHITE}✦{Colors.YELLOW}  {Colors.RED}│ ╲{Colors.YELLOW}║
     ║{Colors.RED}│  ╰───╯  │{Colors.YELLOW}║
     ║{Colors.RED}╲         ╱{Colors.YELLOW}║
     ║ {Colors.RED}╲_______╱{Colors.YELLOW} ║
     ╚═════════════════════════╝
     {Colors.WHITE}○{Colors.RESET} {Colors.YELLOW}●{Colors.RESET}  {Colors.RED}◆{Colors.RESET}   {Colors.GREEN}❖{Colors.RESET}  {Colors.BLUE}◇{Colors.RESET}   {Colors.WHITE}○{Colors.RESET} {Colors.YELLOW}●{Colors.RESET}
    {Colors.RESET}""",
    "puzzle": f"""{Colors.CYAN}
     ╭───────────────────────────────╮
     │  {Colors.YELLOW}■{Colors.CYAN}   {Colors.RED}▲{Colors.CYAN}   {Colors.GREEN}★{Colors.CYAN}   {Colors.BLUE}●{Colors.CYAN}   {Colors.PURPLE}◆{Colors.CYAN}  │
     │                               │
     │  {Colors.WHITE}┌───┬───┬───┬───┬───┐{Colors.CYAN}  │
     │  {Colors.WHITE}│   │   │   │   │   │{Colors.CYAN}  │
     │  {Colors.WHITE}├───┼───┼───┼───┼───┤{Colors.CYAN}  │
     │  {Colors.WHITE}│   │   │   │   │   │{Colors.CYAN}  │
     │  {Colors.WHITE}└───┴───┴───┴───┴───┘{Colors.CYAN}  │
     │                               │
     │   {Colors.YELLOW}?{Colors.CYAN} {Colors.WHITE}解开谜题获得宝藏之匙{Colors.CYAN} {Colors.YELLOW}?{Colors.CYAN}   │
     ╰───────────────────────────────╯{Colors.RESET}
    """
}

# 显示ASCII图案的函数
def display_art(art_name):
    """显示预定义的ASCII艺术图案"""
    if art_name in ASCII_ART:
        print(ASCII_ART[art_name])
    else:
        print(f"未找到名为 {art_name} 的艺术图案")

# 骰子功能，用于某些谜题的随机性
def roll_dice(sides):
    """掷骰子，返回随机数"""
    return random.randint(1, sides)


def intro():
    """游戏介绍和背景故事"""
    clear_screen()
    display_art("title")  # 显示游戏标题图案
    print_slow(f"{Colors.YELLOW}=" * 60 + Colors.RESET)
    print_slow(f"{Colors.CYAN}《神秘岛屿寻宝记》{Colors.RESET}")
    print_slow(f"{Colors.YELLOW}=" * 60 + Colors.RESET)
    print_slow(f"欢迎来到{Colors.GREEN}神秘岛屿{Colors.RESET}！")
    print_slow(f"传说这座岛上隐藏着一件{Colors.YELLOW}失落的宝藏{Colors.RESET}...")
    print_slow(f"作为一名勇敢的{Colors.CYAN}探险家{Colors.RESET}，你决定踏上寻宝之旅。")
    print_slow(f"你的选择将决定你的{Colors.RED}命运{Colors.RESET}，也将决定宝藏的归属。")
    print_slow(f"{Colors.YELLOW}祝你好运！{Colors.RESET}")
    print_slow(f"{Colors.YELLOW}=" * 60 + Colors.RESET)
    input("按回车键开始冒险...")

# 添加游戏道具系统
class Item:
    def __init__(self, name, description, value=0):
        self.name = name
        self.description = description
        self.value = value  # 物品价值或能力提升

# 添加玩家类
class Player:
    def __init__(self):
        self.inventory = []
        self.health = 100
        self.riddles_solved = 0  # 解决的谜题数

    def add_item(self, item):
        self.inventory.append(item)
        print_slow(f"{Colors.GREEN}你获得了物品: {item.name}{Colors.RESET}")
        print_slow(f"{Colors.CYAN}描述: {item.description}{Colors.RESET}")

    def has_item(self, item_name):
        return any(item.name == item_name for item in self.inventory)

# 创建全局玩家对象
player = Player()

# 显示玩家状态
def show_status():
    """显示玩家状态和物品栏"""
    print_slow(f"{Colors.YELLOW}=" * 40 + Colors.RESET)
    print_slow(f"{Colors.CYAN}玩家状态:{Colors.RESET}")
    print_slow(f"{Colors.GREEN}健康: {player.health}%{Colors.RESET}")
    print_slow(f"{Colors.PURPLE}解决谜题: {player.riddles_solved}{Colors.RESET}")
    
    if player.inventory:
        print_slow(f"{Colors.CYAN}物品栏:{Colors.RESET}")
        for item in player.inventory:
            print_slow(f"{Colors.YELLOW}・{item.name}: {Colors.WHITE}{item.description}{Colors.RESET}")
    print_slow(f"{Colors.YELLOW}=" * 40 + Colors.RESET)

def game_over(message, is_win=False):
    """游戏结束时显示信息"""
    print_slow("\n" + f"{Colors.YELLOW}=" * 60 + Colors.RESET)
    
    if is_win:
        print_slow(f"{Colors.GREEN}{message}{Colors.RESET}")
    else:
        print_slow(f"{Colors.RED}{message}{Colors.RESET}")
    
    print_slow(f"{Colors.YELLOW}=" * 60 + Colors.RESET)

def beach_scene():
    """海滩场景，游戏的起始点"""
    clear_screen()
    display_art("beach")  # 显示海滩图案
    print_slow("你站在沙滩上，面前是茂密的丛林。")
    print_slow("你可以看到三条小路延伸进丛林深处。")
    
    # 显示玩家状态
    show_status()
    
    # 多分支选择的条件判断示例
    choice = get_valid_input(
        f"你选择哪条路？\n"
        f"A - {Colors.GREEN}左边的小路{Colors.RESET}，看起来比较平坦\n"
        f"B - {Colors.YELLOW}中间的小路{Colors.RESET}，有些杂草\n"
        f"C - {Colors.RED}右边的小路{Colors.RESET}，显得很陡峭",
        ["A", "B", "C"]
    )
    
    # 根据用户选择确定下一个场景
    if choice == "A":
        print_slow("你选择了左边的小路，开始向丛林深处走去...")
        return jungle_scene
    elif choice == "B":
        print_slow("你选择了中间的小路，小心翼翼地穿过杂草...")
        return cave_entrance_scene
    else:  # choice == "C"
        print_slow("你选择了右边陡峭的小路，开始攀爬...")
        return mountain_scene


def jungle_scene():
    """
    丛林场景
    返回:
        下一个场景的函数引用或None表示游戏结束
    """
    clear_screen()
    print_slow("你来到了茂密的丛林中，四周都是高大的树木和奇怪的声音。")
    print_slow("突然，你看到地上有一个闪闪发光的物体。")
    
    choice = get_valid_input(
        "你想要做什么？\nA - 捡起发光的物体\nB - 忽略它，继续前进",
        ["A", "B"]
    )
    
    if choice == "A":
        # 随机事件示例
        if random.random() < 0.5:  # 50%的概率
            print_slow("你捡起了一个古老的指南针！它似乎指向某个特定的方向。")
            print_slow("跟随指南针，你找到了一条隐藏的小路...")
            return hidden_path_scene
        else:
            print_slow("当你伸手去捡发光的物体时，突然从地下窜出一条毒蛇！")
            print_slow("你被咬了一口，剧毒迅速蔓延...")
            game_over("你因毒蛇的毒液而丧生。游戏结束！")
            return None
    else:
        print_slow("你决定不冒险，继续沿着小路前进。")
        print_slow("走了一段时间后，你来到了一个山洞入口...")
        return cave_entrance_scene

def mountain_scene():
    """
    山脉场景
    返回:
        下一个场景的函数引用或None表示游戏结束
    """
    clear_screen()
    print_slow("你爬上陡峭的山路，能够俯瞰整个岛屿。")
    print_slow("在远处，你看到一座古老的神庙矗立在山顶。")
    
    # 让用户做出决策
    choice = get_valid_input(
        "你想怎么做？\nA - 继续向山顶的神庙前进\nB - 沿着山路下到另一侧的山谷",
        ["A", "B"]
    )
    
    if choice == "A":
        print_slow("你决定继续向山顶前进，朝着神庙的方向走去...")
        return temple_scene
    else:
        print_slow("你选择下山，朝着山谷前进...")
        
        # 随机事件处理
        if random.random() < 0.3:  # 30%的概率发生意外
            print_slow("下山的路非常湿滑，你不慎踩空...")
            print_slow("你从高处摔下，失去了意识...")
            game_over("你因坠落而重伤。游戏结束！")
            return None
        else:
            print_slow("你小心翼翼地下到了山谷...")
            return valley_scene

def cave_entrance_scene():
    """
    洞穴入口场景
    返回:
        下一个场景的函数引用
    """
    clear_screen()
    print_slow("你站在一个黑暗洞穴的入口前。")
    print_slow("洞穴内漆黑一片，但似乎有微弱的光从深处传来。")
    
    # 用户决策点
    choice = get_valid_input(
        "你要怎么做？\nA - 进入洞穴探索\nB - 寻找另一条路",
        ["A", "B"]
    )
    
    if choice == "A":
        # 额外的挑战：需要工具
        print_slow("你决定进入洞穴，但里面太黑了，需要光源...")
        
        # 要求玩家输入数字，演示异常处理
        while True:
            try:
                print_slow("你在背包中搜寻火柴。请输入1-10之间的数字来尝试找到火柴:")
                num = int(input().strip())
                
                # 验证输入是否在有效范围内
                if 1 <= num <= 10:
                    # 随机决定是否找到火柴
                    if num == random.randint(1, 10):
                        print_slow("太幸运了！你找到了火柴，点燃了一根火把。")
                        print_slow("借着火光，你深入洞穴...")
                        return deep_cave_scene
                    else:
                        print_slow("你没有找到火柴，无法在黑暗中前进。")
                        print_slow("你决定寻找另一条路...")
                        return valley_scene
                else:
                    print_slow("请输入1-10之间的数字！")
            except ValueError:
                # 处理输入非数字的情况
                print_slow("请输入有效的数字！")
            except Exception as e:
                # 处理其他可能的异常
                print_slow(f"发生错误: {e}")
                print_slow("请重试。")
    else:
        print_slow("你决定不冒险进入黑暗的洞穴，转而寻找另一条路...")
        return valley_scene

def deep_cave_scene():
    clear_screen()
    display_art("cave")
    print_slow("借着火把的光，你小心翼翼地在洞穴中前进。")
    print_slow("洞壁上刻着奇怪的符号，地上散落着古老的骨头。")
    print_slow("突然，你看到前方有个宝箱！")
    
    choice = get_valid_input(
        f"你要怎么做？\n"
        f"A - {Colors.RED}立刻打开宝箱{Colors.RESET}\n"
        f"B - {Colors.GREEN}仔细检查宝箱是否有陷阱{Colors.RESET}",
        ["A", "B"]
    )
    
    if choice == "A":
        # 直接打开宝箱的后果
        print_slow("你迫不及待地打开宝箱...")
        print_slow("砰！一团毒气从宝箱中喷出！")
        game_over("你中毒身亡。贪婪害死了你！游戏结束！")
        return None
    else:
        # 谨慎检查的结果
        print_slow("你仔细检查宝箱，发现了一个隐藏的机关。")
        print_slow("你小心地解除了机关，然后安全地打开了宝箱。")
        print_slow(f"宝箱里有一把{Colors.YELLOW}奇怪的钥匙{Colors.RESET}和一张{Colors.CYAN}地图{Colors.RESET}！")
        player.add_item(Item("古老的钥匙", "一把看起来非常古老的钥匙，不知道能打开什么", 10))
        
        print_slow(f"你注意到洞穴深处还有一条{Colors.CYAN}隐秘的通道{Colors.RESET}...")
        choice = get_valid_input(
            f"你要继续探索吗？\n"
            f"A - {Colors.GREEN}继续深入洞穴{Colors.RESET}\n"
            f"B - {Colors.YELLOW}按照地图离开洞穴{Colors.RESET}",
            ["A", "B"]
        )
        
        if choice == "A":
            print_slow(f"你决定继续探索洞穴深处的{Colors.CYAN}秘密{Colors.RESET}...")
            return cave_puzzle_scene  # 前往石板谜题场景
        else:
            print_slow("你决定按照地图指示的方向继续前进...")
            return temple_scene
    
def cave_puzzle_scene():
    """洞穴中的石板谜题"""
    clear_screen()
    display_art("puzzle")
    print_slow(f"在洞穴深处，你发现了一块古老的{Colors.YELLOW}石板{Colors.RESET}。")
    print_slow(f"石板上雕刻着{Colors.CYAN}五个符号{Colors.RESET}，每个符号下方都有一个凹槽，似乎需要按特定顺序放入某些物品。")
    print_slow(f"石板旁的墙壁上刻着一段文字：'{Colors.GREEN}天、地、水、火、风，创世之力需按自然之序排列。{Colors.RESET}'")
    
    show_status()
    
    attempts = 3
    while attempts > 0:
        print_slow(f"你需要确定五个元素的正确顺序。({attempts}次机会)")
        sequence = input("请输入五个元素的正确顺序(例如：地水火风天): ").strip()
        
        # 正确答案是"天地水火风"或"空地水火风"
        if sequence in ["天地水火风", "空地水火风"]:
            print_slow(f"{Colors.GREEN}石板上的符号开始发光！{Colors.RESET}")
            print_slow(f"随着最后一个符号被点亮，石板缓缓移开，露出了一条{Colors.CYAN}隐藏的通道{Colors.RESET}。")
            player.riddles_solved += 1
            player.add_item(Item("元素之钥", "一把由五行元素力量形成的钥匙", 20))
            print_slow(f"恭喜你解开了{Colors.YELLOW}洞穴石板谜题{Colors.RESET}！")
            return treasure_room_scene
        else:
            attempts -= 1
            if attempts > 0:
                print_slow(f"{Colors.RED}顺序似乎不对，石板上的符号闪烁了一下，又恢复了原样。{Colors.RESET}")
                print_slow(f"再仔细思考一下... 也许是按照{Colors.YELLOW}自然创世的顺序{Colors.RESET}？")
            else:
                print_slow(f"{Colors.RED}你尝试了所有可能的组合，但石板纹丝不动。{Colors.RESET}")
                print_slow(f"就在你准备放弃时，墙壁上突然出现一个{Colors.GREEN}小通道{Colors.RESET}。")
                print_slow(f"虽然你没解开谜题，但至少找到了{Colors.YELLOW}继续前进的路{Colors.RESET}。")
                return mountain_scene
    
    return mountain_scene


def valley_scene():
    """
    山谷场景
    返回:
        下一个场景的函数引用
    """
    clear_screen()
    print_slow("你来到一个美丽的山谷，这里有一条清澈的小溪和茂密的树林。")
    print_slow("你注意到溪边有一位老人正在钓鱼。")
    
    choice = get_valid_input(
        "你要怎么做？\nA - 上前与老人交谈\nB - 悄悄绕过老人继续前进",
        ["A", "B"]
    )
    
    if choice == "A":
        # 与NPC互动
        print_slow("你走向老人，礼貌地打招呼。")
        print_slow("'啊，又一位寻宝人。'老人微笑着说。")
        print_slow("'如果你想找到真正的宝藏，就去山顶的神庙吧。不过要小心，路上有许多危险。'")
        print_slow("老人给了你一根魔法手杖，说它会在危险时保护你。")
        print_slow("你感谢老人，继续你的旅程，朝着山顶前进...")
        return temple_scene
    else:
        print_slow("你选择不打扰老人，悄悄地绕过他继续前进。")
        print_slow("你发现一条小路通向山脉的更深处...")
        return mountain_scene

def temple_scene():
    clear_screen()
    display_art("temple")
    print_slow("你来到了山顶的古老神庙前。")
    print_slow("神庙外墙刻满了神秘的符文，大门上有一个奇怪的锁。")
    
    # 简单的谜题示例
    print_slow("门上刻着一个谜语：'我有山，但没有岩石；我有河，但没有水；我有城市，但没有建筑。我是什么？'")
    
    # 循环尝试解谜
    attempts = 3
    while attempts > 0:
        try:
            answer = input("请输入你的答案: ").strip().lower()
            
            if answer == "地图" or answer == "map":
                print_slow(f"{Colors.GREEN}正确！神庙的大门缓缓打开了...{Colors.RESET}")
                return temple_interior_scene  # 修改为进入神庙内部场景
            else:
                attempts -= 1
                if attempts > 0:
                    print_slow(f"{Colors.RED}答案错误！你还有{attempts}次尝试机会。{Colors.RESET}")
                else:
                    print_slow(f"{Colors.RED}答案错误！地面开始震动...{Colors.RESET}")
                    print_slow("突然，你脚下的地板塌陷，你掉进了一个深坑！")
                    game_over("你坠入陷阱，无法脱身。游戏结束！")
                    return None
        except Exception as e:
            print_slow(f"发生错误: {e}")
            print_slow("请重试。")


def temple_interior_scene():
    """神庙内部的祭坛谜题"""
    clear_screen()
    display_art("temple")
    print_slow(f"你进入神庙后，发现自己站在一个{Colors.YELLOW}宏伟的大厅{Colors.RESET}中。")
    print_slow(f"大厅的中央是一个古老的{Colors.CYAN}祭坛{Colors.RESET}，三条走廊分别通向不同的方向。")
    print_slow(f"祭坛上刻着文字：'{Colors.GREEN}只有通过智慧、勇气和选择的试炼，才能找到真正的宝藏。{Colors.RESET}'")
    
    show_status()
    
    hall_choice = get_valid_input(
        f"你选择走哪条走廊？\n"
        f"A - {Colors.CYAN}左边的走廊{Colors.RESET}（智慧之路）\n"
        f"B - {Colors.GREEN}中间的走廊{Colors.RESET}（勇气之路）\n"
        f"C - {Colors.BLUE}右边的走廊{Colors.RESET}（选择之路）",
        ["A", "B", "C"]
    )
    
    # 记录通过的试炼数量
    trials_passed = 0
    
    # 第一个试炼：智慧
    if hall_choice == "A":
        print_slow(f"你选择了{Colors.CYAN}智慧之路{Colors.RESET}，走进左边的走廊...")
        print_slow(f"走廊尽头是一个{Colors.BLUE}圆形房间{Colors.RESET}，中央有一张桌子。")
        print_slow(f"桌子上有一个{Colors.YELLOW}古老的棋盘{Colors.RESET}和一个{Colors.RED}沙漏{Colors.RESET}。")
        print_slow(f"墙上写着：'{Colors.GREEN}解开智慧的谜题，将获得前进的权利。{Colors.RESET}'")
        
        riddle_choice = get_valid_input(
            f"桌上有三个谜语卷轴，你选择打开哪一个？\n"
            f"A - {Colors.RED}红色卷轴{Colors.RESET}\n"
            f"B - {Colors.BLUE}蓝色卷轴{Colors.RESET}\n"
            f"C - {Colors.GREEN}绿色卷轴{Colors.RESET}",
            ["A", "B", "C"]
        )
        
        if riddle_choice == "A":
            print_slow(f"你打开了{Colors.RED}红色卷轴{Colors.RESET}...")
            print_slow(f"上面写着：'{Colors.YELLOW}我有眼睛却看不见，有嘴巴却不能言语，有双手却不能掐掐你，有双脚却不能走路。我是谁？{Colors.RESET}'")
            
            riddle_answer = input("请输入你的答案: ").strip().lower()
            if riddle_answer in ["娃娃", "洋娃娃", "人偶", "玩偶", "doll"]:
                print_slow(f"{Colors.GREEN}正确！{Colors.RESET}墙上的一块石板移开，露出了一条通道。")
                player.riddles_solved += 1
                trials_passed += 1
            else:
                print_slow(f"{Colors.RED}回答错误。{Colors.RESET}沙漏的沙子流完了，桌子上的棋盘发出一阵光芒。")
                print_slow(f"一条通道打开了，但你感到{Colors.YELLOW}自己错过了什么重要的东西{Colors.RESET}。")
        
        elif riddle_choice == "B":
            print_slow(f"你打开了{Colors.BLUE}蓝色卷轴{Colors.RESET}...")
            print_slow(f"上面写着：'{Colors.YELLOW}什么东西能穿越窗户却不打破玻璃？{Colors.RESET}'")
            
            riddle_answer = input("请输入你的答案: ").strip().lower()
            if riddle_answer in ["阳光", "光", "光线", "太阳光", "light", "sunlight"]:
                print_slow(f"{Colors.GREEN}正确！{Colors.RESET}墙上的一块石板移开，露出了一条通道。")
                player.riddles_solved += 1
                trials_passed += 1
            else:
                print_slow(f"{Colors.RED}回答错误。{Colors.RESET}沙漏的沙子流完了，桌子上的棋盘发出一阵光芒。")
                print_slow(f"一条通道打开了，但你感到{Colors.YELLOW}自己错过了什么重要的东西{Colors.RESET}。")
        
        else:  # riddle_choice == "C"
            print_slow(f"你打开了{Colors.GREEN}绿色卷轴{Colors.RESET}...")
            print_slow(f"上面写着：'{Colors.YELLOW}我被你踩在脚下，但你却永远无法打败我。我是谁？{Colors.RESET}'")
            
            riddle_answer = input("请输入你的答案: ").strip().lower()
            if riddle_answer in ["影子", "影", "shadow"]:
                print_slow(f"{Colors.GREEN}正确！{Colors.RESET}墙上的一块石板移开，露出了一条通道。")
                player.riddles_solved += 1
                trials_passed += 1
            else:
                print_slow(f"{Colors.RED}回答错误。{Colors.RESET}沙漏的沙子流完了，桌子上的棋盘发出一阵光芒。")
                print_slow(f"一条通道打开了，但你感到{Colors.YELLOW}自己错过了什么重要的东西{Colors.RESET}。")
                
    # 第二个试炼：勇气（已实现部分内容）
    elif hall_choice == "B":
        print_slow(f"你选择了{Colors.GREEN}勇气之路{Colors.RESET}，走进中间的走廊...")
        print_slow(f"走廊越来越窄，最后通向一个{Colors.RED}宽阔的房间{Colors.RESET}。")
        print_slow(f"房间中央是一个{Colors.CYAN}深不见底的深渊{Colors.RESET}，只有一座摇摇欲坠的吊桥连接两端。")
        
        courage_choice = get_valid_input(
            "你要怎么过去？\n"
            f"A - {Colors.RED}尝试走过吊桥{Colors.RESET}\n"
            f"B - {Colors.CYAN}寻找其他路径{Colors.RESET}\n"
            f"C - {Colors.YELLOW}检查吊桥的结构{Colors.RESET}",
            ["A", "B", "C"]
        )
        
        # 实现勇气试炼的具体内容
        if courage_choice == "A":
            print_slow(f"你深吸一口气，开始{Colors.RED}小心翼翼地走过吊桥{Colors.RESET}...")
            print_slow(f"吊桥在你脚下{Colors.YELLOW}摇晃不已{Colors.RESET}，几块木板突然断裂掉入深渊！")
            
            # 勇气检查
            courage_check = roll_dice(20)
            if courage_check > 12:
                print_slow(f"你鼓起勇气，{Colors.GREEN}坚定地一步步向前{Colors.RESET}...")
                print_slow(f"终于，你安全地到达了对岸！")
                print_slow(f"你成功通过了{Colors.YELLOW}勇气的试炼{Colors.RESET}！")
                trials_passed += 1
            else:
                print_slow(f"{Colors.RED}一块木板突然断裂{Colors.RESET}！你失去平衡...")
                print_slow(f"你勉强抓住了吊桥的绳索，但{Colors.RED}受了伤{Colors.RESET}。")
                player.health -= 15
                print_slow(f"{Colors.RED}你的健康值下降了15点！当前健康值：{player.health}%{Colors.RESET}")
                
                if player.health <= 0:
                    game_over("你从吊桥上坠落，消失在黑暗的深渊中...")
                    return None
                
                print_slow(f"尽管受伤，你还是{Colors.GREEN}设法爬到了对岸{Colors.RESET}。")
                print_slow(f"你通过了勇气的试炼，但付出了代价。")
                trials_passed += 1
        elif courage_choice == "B":
            # 寻找其他路径
            print_slow(f"你决定{Colors.CYAN}寻找其他可能的路径{Colors.RESET}...")
            # 这里可以实现相应的逻辑
            trials_passed += 1  # 假设通过了试炼
        else:  # courage_choice == "C"
            # 检查吊桥结构
            print_slow(f"你仔细{Colors.YELLOW}检查吊桥的结构{Colors.RESET}...")
            # 这里可以实现相应的逻辑
            trials_passed += 1  # 假设通过了试炼
            
    # 第三个试炼：选择
    else:  # hall_choice == "C"
        print_slow(f"你选择了{Colors.BLUE}选择之路{Colors.RESET}，走进右边的走廊...")
        print_slow(f"走廊尽头是一个{Colors.CYAN}六角形的房间{Colors.RESET}，中央是一个祭坛。")
        print_slow(f"祭坛上放着{Colors.YELLOW}两件宝物{Colors.RESET}：一个金光闪闪的王冠和一本古老的书籍。")
        print_slow(f"墙上的铭文写道：'{Colors.RED}选择一件，但要明智。贪婪者将一无所获，而慷慨者将得到真正的宝藏。{Colors.RESET}'")
        
        # 实现选择试炼的具体内容
        choice_selection = get_valid_input(
            "你要选择什么？\n"
            f"A - {Colors.YELLOW}拿取金光闪闪的王冠{Colors.RESET}\n"
            f"B - {Colors.GREEN}拿取古老的书籍{Colors.RESET}\n"
            f"C - {Colors.CYAN}两样都不拿{Colors.RESET}\n"
            f"D - {Colors.RED}尝试两样都拿{Colors.RESET}",
            ["A", "B", "C", "D"]
        )
        
        # 处理不同的选择
        if choice_selection in ["B", "C"]:
            # B和C都视为通过试炼
            trials_passed += 1
            if choice_selection == "B":
                player.add_item(Item("智慧之书", "一本包含古代智慧的书籍", 50))
            else:  # choice_selection == "C"
                print_slow(f"你选择什么都不拿，突然出现了一个{Colors.CYAN}小型水晶球{Colors.RESET}...")
                player.add_item(Item("平静水晶", "一个能带来内心平静的水晶", 40))
                player.health = 100  # 恢复健康
                print_slow(f"{Colors.GREEN}你的健康值完全恢复了！当前健康值：100%{Colors.RESET}")
    
    # 前往最终宝藏室
    print_slow(f"通过了{trials_passed}个试炼后，你来到了一个{Colors.RED}金色的大门{Colors.RESET}前。")
    
    if trials_passed >= 1:
        print_slow(f"由于你通过了试炼，{Colors.YELLOW}大门自动打开{Colors.RESET}，欢迎你进入。")
        # 添加第三个谜题：宝藏守护者谜题
        return guardian_puzzle_scene
    else:
        print_slow(f"大门纹丝不动。墙上的文字显示：'{Colors.RED}只有通过至少一个试炼的勇者才能进入。{Colors.RESET}'")
        print_slow(f"你需要{Colors.YELLOW}重新尝试其他试炼{Colors.RESET}。")
        return temple_interior_scene

def guardian_puzzle_scene():
    """宝藏守护者谜题场景"""
    clear_screen()
    display_art("puzzle")
    print_slow(f"你面前站着一位{Colors.PURPLE}古老的守护者{Colors.RESET}，它的眼睛闪烁着智慧的光芒。")
    print_slow(f"'{Colors.YELLOW}想要获得宝藏，你必须通过我的考验。{Colors.RESET}'守护者说道。")
    print_slow(f"'{Colors.GREEN}我会问你三个谜语，每回答正确一个，就能获得一把通往宝藏的钥匙。{Colors.RESET}'")
    
    show_status()
    
    # 准备三个谜语及其答案
    riddles = [
        {
            "question": "我无形无色却能填满任何容器，我对生命至关重要但却能带来死亡，我是什么？",
            "answers": ["空气", "气", "air"]
        },
        {
            "question": "我能够在一天内环游世界，却始终留在角落里。我是什么？",
            "answers": ["邮票", "stamp"]
        },
        {
            "question": "我被发明出来就是为了打败现在的我。我是什么？",
            "answers": ["谜语", "谜题", "puzzle", "riddle"]
        }
    ]
    
    keys_obtained = 0
    attempts_remain = True
    
    # 打乱谜语顺序
    random.shuffle(riddles)
    
    for i, riddle in enumerate(riddles[:min(3, len(riddles))]):
        if not attempts_remain:
            break
            
        print_slow(f"\n{Colors.CYAN}谜语 {i+1}:{Colors.RESET}")
        print_slow(f"{Colors.YELLOW}{riddle['question']}{Colors.RESET}")
        
        # 每个谜语有2次尝试机会
        for attempt in range(2):
            user_answer = input("你的答案是: ").strip().lower()
            
            if user_answer in riddle["answers"]:
                print_slow(f"{Colors.GREEN}守护者点了点头：'回答正确。'{Colors.RESET}")
                keys_obtained += 1
                player.riddles_solved += 1
                player.add_item(Item(f"宝藏钥匙{keys_obtained}", f"开启宝藏室的第{keys_obtained}把钥匙", 30))
                break
            else:
                if attempt == 0:
                    print_slow(f"{Colors.RED}守护者摇了摇头：'思考更深入些。'{Colors.RESET}")
                else:
                    print_slow(f"{Colors.RED}守护者叹了口气：'可惜，答案是 {riddle['answers'][0]}。'{Colors.RESET}")
                    # 第二次机会用完，但仍继续下一个谜语
    
    print_slow(f"\n{Colors.YELLOW}你获得了 {keys_obtained} 把宝藏钥匙！{Colors.RESET}")
    
    if keys_obtained > 0:
        print_slow(f"守护者让开了道路：'{Colors.GREEN}你可以继续前进了，但记住，钥匙越多，宝藏就越丰厚。{Colors.RESET}'")
        # 将钥匙数量传递给宝藏室场景
        return lambda: treasure_room_scene(keys_obtained)
    else:
        print_slow(f"守护者摇头道：'{Colors.RED}你没有获得任何钥匙，但我会给你一次机会。{Colors.RESET}'")
        print_slow(f"守护者从袍子里取出一把{Colors.YELLOW}简陋的铜钥匙{Colors.RESET}：'{Colors.CYAN}这只能打开最基本的宝藏。{Colors.RESET}'")
        player.add_item(Item("铜钥匙", "一把简陋的钥匙，似乎只能打开基本的宝藏", 5))
        return lambda: treasure_room_scene(1)


def hidden_path_scene():
    """
    隐藏小路场景
    返回:
        下一个场景的函数引用
    """
    clear_screen()
    print_slow("你沿着隐藏的小路前进，穿过茂密的丛林。")
    print_slow("这条路似乎很少有人走过，但非常平坦。")
    print_slow("不久，你发现前方有一个分岔口。")
    
    choice = get_valid_input(
        "你选择哪条路？\nA - 左边，通向山谷\nB - 右边，通向山顶",
        ["A", "B"]
    )
    
    if choice == "A":
        print_slow("你选择了左边的路，向山谷方向前进...")
        return valley_scene
    else:
        print_slow("你选择了右边的路，向山顶方向前进...")
        return temple_scene

def treasure_room_scene(keys=0):
    """
    宝藏室场景 - 游戏终点
    参数:
        keys: 获得的钥匙数量
    返回:
        None表示游戏结束
    """
    clear_screen()
    display_art("treasure")
    print_slow("你进入了一个宏伟的宝藏室，到处都是金币、宝石和珍贵的文物！")
    print_slow("在房间中央，有一个金色的宝箱，发出耀眼的光芒。")
    
    show_status()
    
    # 根据钥匙数量决定结局
    if keys == 3:
        print_slow(f"你拿出{Colors.YELLOW}所有三把钥匙{Colors.RESET}，它们在空中自动组合成了一把华丽的金钥匙！")
        print_slow(f"你用这把{Colors.YELLOW}终极钥匙{Colors.RESET}打开了宝箱...")
        print_slow(f"宝箱里是一颗{Colors.CYAN}前所未见的宝石{Colors.RESET}，传说中的'{Colors.GREEN}海洋之心{Colors.RESET}'！")
        print_slow(f"当你触碰它时，一股奇妙的力量流遍全身，你仿佛{Colors.YELLOW}理解了整个世界的奥秘{Colors.RESET}。")
        game_over("你找到了真正的宝藏，不仅是物质财富，还有无价的智慧！你成为了传奇探险家！", is_win=True)
    elif keys == 2:
        print_slow(f"你拿出{Colors.YELLOW}两把钥匙{Colors.RESET}，它们在宝箱的锁孔中闪烁着光芒。")
        print_slow(f"宝箱打开了，里面有一堆{Colors.YELLOW}金币和宝石{Colors.RESET}，以及一张古老的地图！")
        print_slow(f"这张地图指向了{Colors.GREEN}更多宝藏的位置{Colors.RESET}，为你的未来探险铺平了道路。")
        game_over("你找到了珍贵的宝藏和新的冒险线索！你的探险生涯才刚刚开始！", is_win=True)
    elif keys == 1:
        print_slow(f"你拿出{Colors.YELLOW}唯一的钥匙{Colors.RESET}，小心地打开了宝箱。")
        print_slow(f"宝箱里有一些{Colors.YELLOW}金币和一件精美的饰品{Colors.RESET}，虽不是传说中的宝藏，但也相当珍贵。")
        game_over("你找到了一些宝藏！虽然不是最珍贵的，但也足以让你满载而归！", is_win=True)
    else:
        choice = get_valid_input(
            f"你没有钥匙！你要怎么做？\n"
            f"A - {Colors.RED}尝试强行撬开宝箱{Colors.RESET}\n"
            f"B - {Colors.GREEN}寻找其他打开宝箱的方法{Colors.RESET}",
            ["A", "B"]
        )
        
        if choice == "A":
            print_slow(f"你尝试强行撬开宝箱，但触发了{Colors.RED}防护机关{Colors.RESET}！")
            print_slow(f"一阵刺眼的{Colors.YELLOW}强光{Colors.RESET}闪过，你失去了知觉...")
            game_over("你被宝箱的防护机关击昏，醒来时发现自己已被传送回海滩，两手空空。", is_win=False)
        else:
            print_slow(f"你仔细检查宝藏室，发现墙上有一个{Colors.CYAN}小型机关{Colors.RESET}。")
            print_slow(f"激活机关后，宝箱的侧面打开了一个小隔间，里面有一个{Colors.YELLOW}小袋金币{Colors.RESET}。")
            print_slow(f"虽然没有得到传说中的宝藏，但这些金币也足以让你的旅途没有白费。")
            game_over("你找到了一小部分宝藏！下次冒险也许能发现更多！", is_win=True)
    
    return None

def main():
    """
    游戏主函数，控制游戏流程
    """
    try:
        # 显示游戏介绍
        intro()
        
        # 开始游戏，从第一个场景开始
        current_scene = beach_scene
        
        # 主游戏循环，持续到某个场景返回None（游戏结束）
        while current_scene is not None:
            # 执行当前场景函数，获取下一个场景
            next_scene = current_scene()
            current_scene = next_scene
        
        # 询问是否重新开始游戏
        restart = get_valid_input("想再玩一次吗？\nY - 是\nN - 否", ["Y", "N"])
        if restart == "Y":
            main()  # 递归调用实现游戏重新开始
        else:
            print_slow("感谢您的游玩！再见！")
    
    except KeyboardInterrupt:
        # 处理Ctrl+C终止程序的情况
        print_slow("\n\n游戏被中断。感谢您的游玩！")
    except Exception as e:
        # 处理其他未预料到的异常
        print_slow(f"\n哎呀！游戏出现了意外错误: {e}")
        print_slow("请尝试重新启动游戏。")

# 当程序直接运行而非被导入时执行游戏
if __name__ == "__main__":
    main()