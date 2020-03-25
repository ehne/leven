# leven animation library written by DARCY LUGT-FALK
# a pretty basic tweening system, combined with a task runner.

import math

#### THE TWEEN FUNCTIONS
# each one has a normal, and an "out" version,
# the out version exists because of how python handles ranges
####
# the basic linear function
def linear(x):
    return x


def linearout(x):
    return 1 - x


# ooo, a fun quadratic function
def quad(x):
    return x * x


def quadout(x):
    return 1 - quad(x)


# now, a fancy cubic
def cubic(x):
    return x * x * x


def cubicout(x):
    return 1 - cubic(x)


# but wait, there's 4!
def quint(x):
    return x * x * x * x


def quintout(x):
    return 1 - quint(x)


# the dictionary that converts between string and function
f = {
    "linear": linear,
    "linearout": linearout,
    "quad": quad,
    "quadout": quadout,
    "cubic": cubic,
    "cubicout": cubicout,
    "quint": quint,
    "quintout": quintout,
}

# a function to generate a tween list
# yes, i know i called it an array, im used to JS okay
def generateArray(startValue, endValue, elemNo=60, function="linear"):
    # creates a list to hold the values
    array = []
    # loops from zero to the elemno
    for i in range(elemNo + 1):
        # adds the tweened value into the array.
        array.append(f[function](i / elemNo))
    # creates another array, for the Actual Values
    actualValueArray = []

    print(array)  # should print something like [0,...,1]
    # loops over the first array, the one that goes from 0 to 1
    for i in array:
        # appends the actual values to the actual values array.
        actualValueArray.append(startValue + (i * (endValue - startValue)))
        # it takes the start value, adds (i (between 0 and 1) times by the difference between the end and the start)
    # returns the actual value array
    return actualValueArray


# the tweener class
class Tweener:
    # takes the input of an animation dictionary, and the object it is changing values of
    def __init__(self, tweenDict, _object):
        # tweendict = the one given
        self.tweenDict = tweenDict
        # sets the current animation to be start
        self.currentAnim = "start"
        # sets the tweens to not run from the begining
        self.tweenRunning = False
        # sets the position in the counter to be 0
        self.tweenCount = 0
        # object = the object given
        self.object = _object
        # loops over the keys in the tween dictionary
        for i in tweenDict:
            # creates an empty list in the generated list key of the key "i"
            self.tweenDict[i]["generated list"] = []
        # loops over the keys in the tween dictionary
        for i in tweenDict:
            # loops over the "v", values to adjust, getting the index of them as well
            for index, elem in enumerate(tweenDict[i]["v"]):
                # i is just the key
                # creates the tweened array, and saves it to a new list
                cooleList = generateArray(
                    startValue=tweenDict[i]["sv"][index],
                    endValue=tweenDict[i]["ev"][index],
                    elemNo=tweenDict[i]["t"],
                    function=tweenDict[i]["a"][index],
                )
                # adds a "end" value to the list
                cooleList.append("end")
                # saves this list to the other list
                self.tweenDict[i]["generated list"].append(cooleList)
        # prints the entirety of the dictionary.
        print(self.tweenDict)

    # the update method
    def update(self):
        # checks if the animation is running
        if self.tweenRunning:
            # checks if the current animation isn't "end"
            if self.currentAnim != "end":
                # checks if, in the current animation's generated list, we are not at the "end" value
                if (
                    self.tweenDict[self.currentAnim]["generated list"][0][
                        self.tweenCount
                    ]
                    != "end"
                ):
                    # loops over the current animation's generated list
                    # , taking the index and element of
                    for index, element in enumerate(
                        self.tweenDict[self.currentAnim]["generated list"]
                    ):
                        # creates a string,
                        # basically, this just sets the object's value to be equal to the value at the current position in the current animation's generated list for that specific value
                        execStr = f"self.object.{self.tweenDict[self.currentAnim]['v'][index]} = self.tweenDict[self.currentAnim]['generated list'][index][self.tweenCount]"
                        # then it actually runs that code.
                        exec(execStr)

                        # yes, i'm aware that this is extremely gross,
                        # i was very sleep deprived when i wrote it.
                    # increases the counter's position
                    self.tweenCount += 1
                else:
                    # if it is at the "end" section of the generated list
                    print("tween section end")
                    # set the counter to be 0
                    self.tweenCount = 0
                    # set the current animation to be whatever the user said they wanted it to be.
                    self.currentAnim = self.tweenDict[self.currentAnim]["->"]

            else:
                # if the current animation is "end"
                # sets the tween running to be false
                self.tweenRunning = False
                print("animation sequence finished")
                return "done"

    # the reset method
    def reset(self):
        # sets the current animation to be start
        self.currentAnim = "start"
        # set sthe counter to be 0
        self.tweenCount = 0

    # the set isRunning method
    def setIsRunning(self, _value):
        # tries to set the tweenRunning variable to whatever the _value is
        try:
            self.tweenRunning = bool(_value)
        except:
            pass

    # the start function
    def start(self):
        # resets the animation
        self.reset()
        # sets running to be true
        self.setIsRunning(True)
