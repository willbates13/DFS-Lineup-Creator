from flask import Flask, flash, redirect, render_template, request, session, jsonify
import pandas as pd
import os
from cs50 import SQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# file path for csv data file
local_file_path = 'projections.csv'
db = SQL("sqlite:///lineups.db")

@app.route('/', methods=['GET', 'POST'])
def index():
    if os.path.exists(local_file_path):
        df = pd.read_csv(local_file_path)
        headers = df.columns.tolist()
        rows = df.values.tolist()
        return render_template('index.html', headers=headers, rows=rows)

    return render_template('index.html')


@app.route('/lineups', methods=['POST'])
def add_lineup():
    if request.method == "POST":

        if os.path.exists(local_file_path):
            df = pd.read_csv(local_file_path)
        selected_lineup = request.form['selectedLineup']

        player_names = selected_lineup.split(',')
        print(player_names)

        player_ids = []
        salary = 0
        for player in player_names:
            idx = df[df.Name == player].ID.item()
            salary +=  df[df.Name == player].Salary.item()
            player_ids.append(idx)

        if (len(player_names) < 9) or (any(not name.strip() for name in player_names)):
            return "error: Lineup must have at least 9 players. Please select more players."

        if salary > 50000:
            return "error: Lineup exceeded salary limit."


        if not db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='lineup_list'"):
            db.execute("CREATE TABLE lineup_list ( \
                id INTEGER PRIMARY KEY, \
                qb INTEGER NOT NULL, \
                rb1 INTEGER NOT NULL, \
                rb2 INTEGER NOT NULL, \
                wr1 INTEGER NOT NULL, \
                wr2 INTEGER NOT NULL, \
                wr3 INTEGER NOT NULL, \
                te INTEGER NOT NULL, \
                flex INTEGER NOT NULL, \
                dst INTEGER NOT NULL \
            )")

        db.execute("INSERT INTO lineup_list (qb, rb1, rb2, wr1, wr2, wr3, te, flex, dst) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", player_names[0], player_names[1], player_names[2], player_names[3], player_names[4], player_names[5], player_names[6], player_names[7], player_names[8])

        if not db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='lineup_list_ids'"):
            db.execute("CREATE TABLE lineup_list_ids ( \
                id INTEGER PRIMARY KEY, \
                qb INTEGER NOT NULL, \
                rb1 INTEGER NOT NULL, \
                rb2 INTEGER NOT NULL, \
                wr1 INTEGER NOT NULL, \
                wr2 INTEGER NOT NULL, \
                wr3 INTEGER NOT NULL, \
                te INTEGER NOT NULL, \
                flex INTEGER NOT NULL, \
                dst INTEGER NOT NULL \
            )")

        db.execute("INSERT INTO lineup_list_ids (qb, rb1, rb2, wr1, wr2, wr3, te, flex, dst) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", player_ids[0], player_ids[1], player_ids[2], player_ids[3], player_ids[4], player_ids[5], player_ids[6], player_ids[7], player_ids[8])

        return redirect("/")

@app.route('/database')
def history():
    database = db.execute("SELECT * FROM lineup_list")
    ids = db.execute("SELECT * FROM lineup_list_ids")
    if database:
        return render_template("database.html", database=database, ids = ids)
    else:
        return render_template("no_database.html")

@app.route('/remove_lineup/<int:lineup_id>', methods=['DELETE'])
def remove_lineup(lineup_id):
    try:
        # Remove the lineup from the SQL database using the ID from the URL parameters
        db.execute("DELETE FROM lineup_list WHERE id = ?", (lineup_id,))
        db.execute("DELETE FROM lineup_list_ids WHERE id = ?", (lineup_id,))

        return jsonify({'message': 'Lineup removed successfully'})
    except Exception as e:
        # Handle any database errors
        return jsonify({'error': f'Database error: {str(e)}'}), 500


@app.route('/remove_all', methods=['POST'])
def remove_all():
    try:
        # Remove the lineup from the SQL database using the ID from the URL parameters
        db.execute("DELETE FROM lineup_list")
        db.execute("DELETE FROM lineup_list_ids")

        return redirect("/")

    except Exception as e:
        # Handle any database errors
        return jsonify({'error': f'Database error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
