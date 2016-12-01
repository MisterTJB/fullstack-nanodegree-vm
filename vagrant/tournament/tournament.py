#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def read(query, params=()):
    """
    Wraps a generic read query (i.e. one in which the entire results set should
    be returned to the caller) with calls to open and close a connection and
    cursor.

    Args:
        query: The SQL query to execute
        params: A tuple of arguments to interpolate the query

    Returns:
        An array of tuples representing rows in the result
    """

    conn = connect()
    cur = conn.cursor()
    cur.execute(query, params)
    result = cur.fetchall()
    return result


def write(query, params=()):
    """
    Wraps a generic write query (i.e. one in which the query should be executed
    and committed) with calls to open and close a connection and cursor, and
    commit the transaction.

    Args:
        query: The SQL query to execute
        params: A tuple of arguments to interpolate the query
    """

    conn = connect()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    cur.close()
    conn.close()


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    write("DELETE FROM Matches;")


def deletePlayers():
    """Remove all the player records from the database."""
    write("DELETE FROM Players;")


def countPlayers():
    """Returns the number of players currently registered."""
    return read("SELECT COUNT(*) FROM Players;")[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    write("INSERT INTO Players (name) VALUES (%s);", (name,))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    return read("SELECT id, name, wins, wins+losses as matches FROM standings")


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    write("INSERT INTO Matches (winner, loser) VALUES (%s, %s);",
          (winner, loser,))
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    return read("SELECT id1, name1, id2, name2 FROM next_round");