-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE Players (
  id SERIAL PRIMARY KEY,
  name TEXT
);

CREATE TABLE Matches (
  id SERIAL PRIMARY KEY,
  winner INT REFERENCES Players(id),
  loser INT REFERENCES Players(id)
);

-- Builds a table reporting each player's id, name, and number of wins
--
--  id | name | wins
-- -------+----+------
--      1 |  P1 | 0
--      2 |  P2 | 2
--      3 |  P3 | 2
--      4 |  P4 | 0
CREATE VIEW win_tally AS
  SELECT id, name, coalesce(win_count, 0) as wins FROM
    (SELECT winner as id, count(*) as win_count
     FROM Matches GROUP BY winner) as win_t
  FULL JOIN Players USING (id);


-- Builds a table reporting each player's id, name, and number of losses
--
--  id | name | losses
-- -------+----+------
--      1 |  P1 | 2
--      2 |  P2 | 0
--      3 |  P3 | 0
--      4 |  P4 | 2
CREATE VIEW loss_tally AS
  SELECT id, name, coalesce(loss_count, 0) as losses FROM
    (SELECT loser as id, count(*) as loss_count
     FROM Matches GROUP BY loser) as lose_t
  FULL JOIN Players USING (id);

-- Builds a table reporting each player's id, wins, and number of matches played
-- in descending order of the number of wins
--
--  id | name | wins
-- -------+----+------
--      2 |  P2 | 2
--      3 |  P3 | 2
--      1 |  P1 | 0
--      4 |  P4 | 0
CREATE VIEW standings AS
  SELECT id, win_tally.name, wins, losses
  FROM win_tally FULL JOIN loss_tally using (id)
  ORDER BY wins DESC;


-- Assigns adjacent players (i.e according to the standings view) to a new
-- match
--
--  match | id | wins
-- -------+----+------
--      0 |  2 | P2
--      0 |  3 | P3
--      1 |  1 | P1
--      1 |  4 | P4
CREATE VIEW match_assignments AS
  select (row_number() OVER () - 1) / 2 as match, id, name
  FROM standings;


-- Reports the assignments for the next round of matches
--
--  match | id1 | name1 | id2 | name2
-- -------+-----+-------+-----+-------
--      0 |  2  |   P2  |  3  |  P3
--      1 |  1  |   P1  |  4  |  P4

CREATE VIEW next_round AS
  SELECT a.match AS match, a.id AS id1, a.name as name1, b.id AS id2, b.name as name2
  FROM match_assignments AS a CROSS JOIN match_assignments AS b
  WHERE a.id < b.id and a.match = b.match;