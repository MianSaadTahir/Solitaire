# Solitaire

**Klondike-Solitaire**  is a Python implementation of the classic Solitaire card game, following the traditional Klondike rules. The game allows users to interact with a graphical interface built using Pygame, featuring a fully functional deck of cards, tableau columns, foundation piles, and a stockpile. It implements different data structures including python lists, stacks, queues, linked lists and hash-map.

## Table of Contents
- [Features](#features)
- [Screenshots](#screenshots)
- [Usage](#usage)
- [Documentation](#documentation)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Card Setup**: Implements the standard Klondike card layout with 7 tableau columns and 4 foundation piles.
- **Game Logic**: Card movement between tableau columns, foundation piles, and stockpile, adhering to Klondike rules.
- **Data Structures**: Stack (LIFO) for tableau columns and foundation piles <br>
Queue (FIFO) for the stockpile <br>
Linked List for tableau piles for card manipulation <br>
Dictionary for tracking card positions and states <br>
- **User Interface**:  Built with Pygame, providing an interactive GUI where players can select and drop cards.
- **Win Condition**:  The game ends when all cards are moved to the foundation piles in the correct order.

### Step 2: Install Microsoft Visual Studio

Download Microsoft Visual Studio from the official website:  
[Visual Studio Download](https://visualstudio.microsoft.com/downloads/)

### Step 3: Install .NET Desktop Development

During installation, make sure to select the **.NET desktop development** workload. This will provide all the tools and libraries needed to run the project.

<div align="center">
    ![alt text](image.png)
</div>

### Step 4: Open and Run the Project

1. Open the extracted project folder and locate the `.sln` file.
2. Double-click on the `.sln` file to open it in Visual Studio.
3. Once Visual Studio opens, simply click **Start** or press `F5` to run the game.

Enjoy playing Solitaire!
