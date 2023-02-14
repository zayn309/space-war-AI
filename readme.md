
# award class:

the class that specify the affect of the reward that you gain during playing (increase bullets speed, increase bullet max number, increase the health by 1)
designed in starategy design pattern to be easy to add more types of awards.

# spaceship class

a super class that encapsulate the common aspects of a spaceship and has 2 supclasses which is the left and right handside ship.

# Game class

it's like the interface that you deal with to control the game via simple methods like loop that run the game for one iteration and draw that draw the game for you and all the comlex stuff is happening behind the scenes.

# AI class 

it's the class that encapsulate the methods to deal with the AI like test_AI that takes a genome and test it against a human player and train_AI that trains all the neural networks of all the genomes

# training approch

the approch that i'm currently using is training all genomes against each others,
as the game is multiplayer game so the performance of your AI depends on your oponent so you need a perfect player to train you AI on but this your main goal in the first place, you can make the AI playes against him self but this is gonna result in an AI that won't do much with anybody but itself, so making every genome playes with every other genome is convenient to get  us a good AI, it's gonna take long time to train but it's gonna give a pretty good AI.