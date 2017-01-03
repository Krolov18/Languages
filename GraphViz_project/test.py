import sqlite3

with sqlite3.connect("database.sqlt3") as input:
	curseur = input.cursor()

curseur.executescript("""
	CREATE TABLE IF NOT EXISTS labels (
		id INTEGER PRIMARY KEY,
		label STRING UNIQUE
		);

	CREATE TABLE IF NOT EXISTS traits (
		id INTEGER PRIMARY KEY,
		feature STRING UNIQUE,
		value INTEGER
		);

	CREATE TABLE IF NOT EXISTS valeurs (
		id INTEGER PRIMARY KEY,
		value INTEGER
		);

	CREATE TABLE IF NOT EXISTS mots (
		id INTEGER PRIMARY KEY,
		mot STRING UNIQUE
		);

	CREATE TABLE mot_feats(
		id INTEGER PRIMARY KEY,
		mot_id INTEGER,
		feat_id INTEGER,
		FOREIGN KEY(mot_id) REFERENCES mots(id),
		FOREIGN KEY(feat_id) REFERENCES features(id)
	);

	CREATE TABLE IF NOT EXISTS weights_features (
		id INTEGER PRIMARY KEY,
		labels_id INTEGER,
		features_id INTEGER,
		values_id INTEGER,
		FOREIGN KEY(labels_id) REFERENCES labels(id),
		FOREIGN KEY(features_id) REFERENCES features(id),
		FOREIGN KEY(values_id) REFERENCES valeurs(id)
		);

""")
    i = 0
    j = 0
    for label in perceptron.weights:
        print(label)
        if i == 1:
            break
        perceptron.curseur.execute("INSERT INTO labels VALUES (NULL, ?)", (label,))
        w = perceptron.curseur.execute("SELECT id FROM labels WHERE label=?", (label,)).fetchone()[0]
        print(len(perceptron.weights[label]))
        for feat in perceptron.weights[label]:
            j += 1
            print(j)
            perceptron.curseur.execute("INSERT INTO features VALUES (NULL, ?)", (feat,))
            r = perceptron.curseur.execute("SELECT id FROM features WHERE feature=?", (feat,)).fetchone()[0]
            perceptron.curseur.execute("INSERT INTO valeurs  VALUES (NULL, ?)", (perceptron.weights[label][feat],))
            x = perceptron.curseur.execute("SELECT id FROM valeurs WHERE value=?", (perceptron.weights[label][feat],)).fetchone()[0]
            perceptron.curseur.execute("INSERT INTO weights VALUES (NULL, ?, ?, ?)", (w, r, x))
        i+=1
        print(i)
    perceptron.sortie.commit()
    perceptron.sortie.close()
