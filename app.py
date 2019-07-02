from flask import Flask, render_template, url_for, redirect
import re
import random
import html


app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


def format(string):
    while re.search("{", string) is not None:
        # find the first { and set the start of the string as the character index after
        start = re.search("{", string).start() + 1
        # find the next } and set the end of the string as that characte index
        end = re.search("}", string).start() - 1
        # while there is a { in between start and end, reset start
        while re.search("{", string[start:end+1]) is not None:
            start += re.search("{", string[start:end+1]).start() + 1
        # replace the 6 characters before start with html and replace } with the closing html
        string = string[:start-7] + {'bf':'<strong>', 'it':'<em>', 'sc':'<span style="font-variant:small-caps;">'}[string[start-3:start-1]] + string[start:end+1] + {'bf':'</strong>', 'it':'</em>', 'sc':'</span>'}[string[start-3:start-1]] + string[end+2:]
    return string


# read in quadegories.txt
text = ''.join(line if line[0]=='\\' else '' for line in open("quadegories.txt", "r").readlines())
quadegories = re.split('\\\\listP', text)[1:]
# format text
for i in range(len(quadegories)):
    # Split into quads and clues
    quadegories[i] = re.split('\\n\\\\ansP', quadegories[i])
    # remove braces
    quadegories[i] = [re.split('}{', quadegories[i][0][1:-1]), re.split('}{', quadegories[i][1][1:-2])]
    # replace `` and reformat to single lines
    quadegories[i] = [re.sub('``', '&#8220;', string) for string in quadegories[i][0] + quadegories[i][1]]
    # replace '
    quadegories[i] = [re.sub('`', '&#39;', string) for string in quadegories[i]]
    # delete \\
    quadegories[i] = [re.sub('\\\\', '', string) for string in quadegories[i]]
    # replace bold statements    textbf{string} --> <strong>string</strong>
    # replace italics statements    textit{string} --> <em>string</em>
    # replace sc statements       textsc{string} --> <span style="font-variant:small-caps;">string</span>
    quadegories[i] = [format(string) for string in quadegories[i]]


@app.route('/play')
def play():
    return redirect('/game/' + str(random.randint(0,len(quadegories))))

@app.route('/game/<int:choice>')
def game(choice):
    [clue4, clue3, clue2, clue1, quad, fact] = quadegories[choice]
    return render_template('game.html', quad = quad, fact = fact, clue4 = clue4,
                                        clue3 = clue3, clue2 = clue2, clue1 = clue1)



if __name__ == "__main__":
    app.run(port=5002)
