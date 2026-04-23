# Platformer  

#### Introduction  

The goal of this coursework is to make a simple platformer game and utilising concepts learnt during lectures, so the 4 OOP pillars design patterns, PEP8 style guidelines and in addition to this git and github as well as work with files.  
My topic for this coursework is a platformer game. In leau of this it has simple platformer features, such as forgiveness on precise jump inputs and input buffering for jumps, a walljump and a dash with some exceptions that function as intentional features.  
The coursework also features a level editor along with the game, to start either one needs to compile the editor.py or game.py files respectively and oh course have python and the pygame library installed in their system. Alternatively one can launch the respective exe files, although it may raise a malware warning due to the library used to compile them being commonly used for viruses.  
The controls for the game are as follows: arrow keys to move horizontaly, jump is z, dash is x and reads arrow keys for dash direction, r resets the character, p prints the current scoreboard in the terminal or console.  
The controls for the editor are as follows: wasd to move the camera, left shift increases the camera move speed, left mouse click places a tile, right click deletes a tile, to select tile group one uses the mouse scrollwheel, to select the variant hold left shift while using the mousewheel. Additionaly to place tiles not on the grid (e.g. large decor tiles), press g, pressing g again will set the tile placement to the grid.

#### Body

Requirements:

> Pillars of object oriented programming

1. Inheritance - Inheritance allows us to define a class that inherits all the methods and properties from another class. In the coursework inheritance is utilised in the Player class that inherits from the PhysicsEntity class. While the PhysicsEntity class is a class to handle basic collisions with tiles and initiate basic variables and could be used to create, for example, an Enemy class or a physics object that could be pushed by the Player, the Player class has unique methods to handle it's own processes. Which leads to the next OOP pillar:
2. Polymorphism - is defined as the capability of different classes interacting with the same method, but having different results. In python the most common occurence of this is an inhereted class (Player) overriding an inhereted method(from PhysicsEntity). In the coursework this is shown specifically by the PhysicsEntity update method, which is vastly larger in the Player class, so in essence the Player class has additional functions and can act differently.
3. Encapsulation - the practice of obscuring data or methods. Using a private variable in a class (denoted by double underscores before the variable and after self: self.__variable) prevents access from outside the class thus "encapsulating" it. To work with the private variable one has to utilise class methods. In this coursework encapsulation can be seen in the scoreboard.py script in which the scoreboard itself is a private dictionary. It loads the scoreboard from a json file, after which it can be printed using the print() method or saved and sorted by using the save() method.
4. Abstraction - the practice of hiding complex logic in functions. It is essentially everywhere in the coursework, but a fine example can once again be the scoreboard script. In it there's a method to sort the scoreboard dictionary and reorder the entries, while from the game program it simply calls the sort() method, the method itself creates a list of entries to be sorted, clears the private scoreboard variable, sorts the temporary list based on score, refills the scoreboard variable with the ordered entries and keys for the dictionaries acting as values and deletes the temporary list. On the end user side nothing is outputed, but a relatively complex process happened in the background.

> Design pattern

A design patern is used to solve a common problem in programing.  
In this coursework the singleton design pattern is used to ensure only one scoreboard is created at a time, since there's no use to have multiple as they would load the same scoreboard, thus avoiding wasted resources in creating multiple ScoreBoard objects.

> Composition and aggregation

Composition creates multiple objects of a different class within itself to make work with it easier, the connection between parent and child object is very close, so when the parent object is deleted, so are to composited objects. Aggregation is more loose, wherein objects are passed in from outside and aren't deleted when the parent object is.  
The coursework by definition contains composition, the best example of which is the Clouds class, which creates multiple random Cloud objects within itself to render in the background.

> Git and Github

This file and the repository are stored in github. There one can check the commit history and verify the creation of the programs.

> Work with files

Work with files is needed when the amount of input or output data is large, as well as when it is desireable to save and load information.  
It is utilised in two places in the coursework, in both dictionaries are stored in a json file. One - saving and loading maps that contain tiles to be rendered and calculate collisions with. Two - saving and loading the scoreboard in which you can see older entries and compare to newer ones and is ordered by score.

> Code style

It is needed for code to be standardised and written in an easily readable way.  
This coursework follows PEP8 style guidelines, e.g. using Pascal case for classes and snake case for methods and variables, limiting the line length in longer commands (mostly when working with positional arguments).

#### Results

- In my personal opinion the program turned out quite well, and physics were implemented in a reasonably satisfactory way
- The functional requirements were met
- A report was written for the program using the markdown format (a bit meta)

#### Conclusions

This coursework taught me a good bit more about python and object oriented programing than the lectures by themselves, for example, seperating out methods and classes into scripts to save linespace on the main program. During this work a platformer game with a level editor was created based on a general python game framework.

Some future prospects that could be easily achieved with some work would be level transitions / switching between levels in the editor, allowing for multiple levels. Using the Physics entity class it would be possible to create moving obstacles or moveable goals and objects as well as potentially an Enemy class that would inherit from it. It'd be possible to add more methods to the ScoreBoard class, such as deleting multiple entries based on passed indecies.

A potentially more difficult future prospect would be creating a general user interface with which one could switch between the editor, the game, and potentially the scoreboard as an entirely separate window.