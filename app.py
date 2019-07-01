from flask import Flask, render_template, url_for
import re
import random


app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')


# load in quadegoties.txt
text_file = open("quadegories.txt", "r")
lines = text_file.readlines()

text = ''.join(line if line[0]=='\\' else '' for line in open("quadegories.txt", "r").readlines())
quadegories = re.split('\\\\listP', text)[1:]
for i in range(len(quadegories)):
    # Split into quads and clues
    quadegories[i] = re.split('\\n\\\\ansP', quadegories[i])
    # remove braces
    quadegories[i] = [re.split('}{', quadegories[i][0][1:-1]), re.split('}{', quadegories[i][1][1:-2])]
    # replace `` and reformat to single lines
    quadegories[i] = [re.sub('``', '&#8220', string) for string in quadegories[i][0] + quadegories[i][1]]
    # replace '
    quadegories[i] = [re.sub('`', '&#39', string) for string in quadegories[i]]
    # replace bold statements    \\textbf{string} --> <strong>string</strong>

    # replace italics statements    \\textit{string} --> <i>string</i>

    # replace sc statements       \\textsc{string} --> <span style="font-variant:small-caps;">string</span>

    # delete extra newlines \\
    quadegories[i] = [re.sub('\\\\', '', string) for string in quadegories[i]]

text_file.close()


@app.route('/game')
def game():
    [[clue4, clue3, clue2, clue1], [quad, fact]] = quadegories[random.randint(0,len(quadegories))]
    return render_template('game.html', quad = quad, fact = fact, clue4 = clue4,
    clue3 = clue3, clue2 = clue2, clue1 = clue1)




if __name__ == "__main__":
    app.run(port=5002)
