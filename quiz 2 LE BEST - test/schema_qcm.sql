DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS options;

CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    qcm INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);

CREATE TABLE options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER,
    option TEXT NOT NULL,
    FOREIGN KEY(question_id) REFERENCES questions(id)
);
