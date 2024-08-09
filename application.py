from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import random
from datetime import datetime
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, SECRET_KEY, DEBUG

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['DEBUG'] = DEBUG
def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
@app.route('/')
def index():
    return render_template('index.html')
# Sign up function
@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = connect_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO players (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            return "User signed up successfully!"
        except mysql.connector.errors.IntegrityError:
            return "Username already exists. Please choose a different username."
        finally:
            cursor.close()
            conn.close()
    
    return render_template('Signup.html')

# Log in function
@app.route('/login', methods=['GET', 'POST'])
def log_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, password FROM players WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user and password == user[1]:
            cursor.close()
            conn.close()
            return redirect(url_for('welcome_menu', player_id=user[0]))
        else:
            return "Invalid username or password."
    
    return render_template('Login.html')

# Store game result
def store_result(player_id, player_score, dealer_score, result):
    conn = connect_db()
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute(
        "INSERT INTO results (player_id, player_score, dealer_score, result, timestamp) VALUES (%s, %s, %s, %s, %s)",
        (player_id, player_score, dealer_score, result, timestamp)
    )
    conn.commit()
    
    cursor.close()
    conn.close()

# View player scores
def view_scores(player_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT player_score, dealer_score, result, timestamp FROM results WHERE player_id = %s", (player_id,))
    results = cursor.fetchall()
    
    scores = []
    for row in results:
        timestamp = row[3].strftime('%d/%m/%Y %H:%M:%S')
        scores.append({
            'player_score': row[0],
            'dealer_score': row[1],
            'result': row[2],
            'timestamp': timestamp
        })
    
    cursor.close()
    conn.close()
    
    return render_template('View_Scores.html', scores=scores)

# Calculate the value of a hand
def calculate_hand_value(hand):
    value = 0
    ace_count = 0
    
    for card in hand:
        if card == 'A':
            ace_count += 1
            value += 11
        elif card in ['J', 'Q', 'K']:
            value += 10
        else:
            value += int(card)
    
    while value > 21 and ace_count:
        value -= 10
        ace_count -= 1
    
    return value

# Main game loop
@app.route('/play_game/<int:player_id>', methods=['GET', 'POST'])
def play_game(player_id):
    if request.method == 'GET':
        deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4
        random.shuffle(deck)
        
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]
        
        player_score = calculate_hand_value(player_hand)
        dealer_score = calculate_hand_value(dealer_hand)
        
        store_result(player_id, player_score, dealer_score, 'playing')
        
        return render_template('play_game.html', player_hand=player_hand, dealer_hand=dealer_hand[0])
    elif request.method == 'POST':
        move = request.form['move']
        
        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT player_score, dealer_score FROM results WHERE player_id = %s AND result = 'playing' ORDER BY timestamp DESC LIMIT 1", (player_id,))
        result = cursor.fetchone()
        
        player_hand = result[0].split(',')
        dealer_hand = result[1].split(',')
        
        if move == 'hit':
            player_hand.append(deck.pop())
            player_score = calculate_hand_value(player_hand)
            
            if player_score > 21:
                store_result(player_id, player_score, dealer_score, 'loss')
                return "You busted! Dealer wins."
            
            cursor.execute("UPDATE results SET player_score = %s WHERE player_id = %s AND result = 'playing' ORDER BY timestamp DESC LIMIT 1", (','.join(player_hand), player_id))
            conn.commit()
            
            return render_template('play_game.html', player_hand=player_hand, dealer_hand=dealer_hand[0])
        elif move == 'stand':
            while dealer_score < 17:
                dealer_hand.append(deck.pop())
                dealer_score = calculate_hand_value(dealer_hand)
            
            if dealer_score > 21 or player_score > dealer_score:
                store_result(player_id, player_score, dealer_score, 'win')
                return "You win!"
            elif player_score == dealer_score:
                store_result(player_id, player_score, dealer_score, 'tie')
                return "It's a tie!"
            else:
                store_result(player_id, player_score, dealer_score, 'loss')
                return "Dealer wins!"

# Welcome menu
@app.route('/welcome_menu/<int:player_id>')
def welcome_menu(player_id):
    return render_template('Welcome_note.html', player_id=player_id)

# Main function
def new_func(__name__, app):
    if __name__ == '__main__':
        try:
            app.run()
        except SystemExit:
            pass

new_func(__name__, app)