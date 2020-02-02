from flask import Flask, render_template, url_for, redirect
import re
import random
import html
import os



app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')



descriptionDict = {}
collectionDict = {}
# load in all collection files

from quadegories.beginner import *
descriptionDict['Beginner'], collectionDict['Beginner'] = beginnerTup
from quadegories.expert import *
descriptionDict['Expert'], collectionDict['Expert'] = expertTup
from quadegories.harryPotter import *
descriptionDict['Harry Potter'], collectionDict['Harry Potter'] = harryPotterTup




@app.route('/choose-collection')
def choose():
    global collectionDict
    return render_template('choose-collection.html', collectionDict=collectionDict)


@app.route('/transition')
@app.route('/transition/<string:collection>')
def transition(collection):
    return render_template('transition.html', collection=collection)


@app.route('/game')
def auto():
    return redirect('/game/beginner/0')


@app.route('/collection/<string:collection>')
def collectionInfo(collection):
    global descriptionDict
    description = descriptionDict[collection]
    global collectionDict
    quadegories = collectionDict[collection]
    return render_template('collection-info.html', collection=collection,
                                                   description=description,
                                                   max=len(quadegories) - 1)

@app.route('/game/<string:collection>')
def chooseRand(collection):
    global collectionDict
    quadegories = collectionDict[collection]
    return redirect(f'/game/{collection}/' + str(random.randint(0,len(quadegories)-1)))



@app.route('/game/<string:collection>/<int:choice>')
def game(collection, choice):
    global collectionDict
    quadegories = collectionDict[collection]
    [clue4, clue3, clue2, clue1, quad, fact] = quadegories[choice]
    return render_template('game.html', collection = collection, quad = quad,
                                        choice = choice, fact = fact,
                                        clue4 = clue4, clue3 = clue3,
                                        clue2 = clue2, clue1 = clue1,
                                        max = len(quadegories) - 1)


if __name__ == "__main__":
    app.run(port=2005)
