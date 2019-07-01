from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/game')
def game():
    quad = 'quad'
    fact = 'fact'
    clue4 = 'clue #4'
    clue3 = 'clue #3'
    clue2 = 'clue #2'
    clue1 = 'clue #1'
    return render_template('game.html', quad = quad, fact = fact, clue4 = clue4,
    clue3 = clue3, clue2 = clue2, clue1 = clue1)



if __name__ == "__main__":
    app.run(port=5002)
