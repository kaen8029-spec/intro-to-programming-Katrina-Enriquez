# Katrina Enriquez Choose YOur Own Adventure

greetings = ["Howdy ", "Adios"]

intro= """


You are a cowboy in the wild west in charge of a small 
heard of cows and the land they reside on. It's a tough job, and it doesn't much make $$$ but 
it's honest work.
"""

prompt = """Your farm hand woke up early and finish the morning tasks.
You finally have extra time! How do you want to spend your morning?
1-take your trusty steed out for a walk 
2-relax on the farm 
"""


levelOne = """You saddle up ol'Trigger and hit the trail. You've havent been out in awhile, 
this place is unfamiliar. Are you going right or left? 
1 - right
2 - left
"""

levelTwo = """Going right has taken you on an amazing tour of America's vast wilderness.
Oddly enough, you see an old man slumped over and waving at you for help. What should you do?
1 - go towards him
2 - avoid him and find another route.
"""

levelThree = """As you slowly approach, you gather that this old man is Mayor John. He is stuck under a big fallen log.
Mayor John tells you that his horse got spooked and bucked him off the saddle. You move the log and free his leg. 
He tell you to call him John from now on and invites you to come into town so he can buy you a drink to thank you. 
1 - go toward town with John
2 - continue on you solo ride with Trigger
"""

levelFour = """You start towards town. There is no space on Trigger's 
back for John because the supplies you packed but walk slow so he can keep up. 
A couple miles pass. Tired, and very angry that he can't find his horse. John
reaches for a weapon from you supply pack. He points it at you, fires, and takes Ol'Trigger.
This is the wild west after all. Game over. 
"""

firstChoice = "2"


print(greetings[0])
print(intro)


while (firstChoice != "1"):
    firstChoice =input(prompt)

    if(firstChoice == "1"): 
        secondChoice= "2"
        
    elif(firstChoice == "2"):
        print("You relax at home.Game over.")
        run = False
        break
    else:
        print("please enter 1 or 2")

while (secondChoice != "1"):
    secondChoice = input(levelOne) #second decision point
    
    if(secondChoice == "1"): 
       thirdChoice = "2"
       
    elif(secondChoice == "2"):
        print("Ahhhhh! You are still reorienting yourself to the area. You fall off a hidden cliff! Game over.")
        run = False
        break
    else:
        print("please enter 1 or 2")


while (thirdChoice != "1"):
    thirdChoice = input(levelTwo) # third decision point
    
    if(thirdChoice == "1"): 
       fourthChoice = "2"

    elif(thirdChoice == "2"):
        print("Ahhhhh! You are still reorienting yorself to the area. You fall off a hidden cliff! Game over.")
        run = False
        break
    else:
        print("please enter 1 or 2")


while (fourthChoice != "1"):
    fourthChoice = input(levelThree) #final decision point

    if(fourthChoice == "1"): 
        print(levelFour)
        run = False
    elif(fourthChoice == "2"):
        print("Ahhhhh! You are still reorienting yorself to the area. Ahhh! You fall off a hidden cliff! Game over.")
        run = False
        break
    else:
        print("please enter 1 or 2")

print(greetings[1])

