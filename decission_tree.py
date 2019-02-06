from __future__ import print_function

import train_data

## alt-inna restauracja w pobliżu
## sta- miejsce aby poczekać
## day- sobota-0 czy piatek-1(średnia ilosc ludzi na miescie)
## hu - czy jestes bardzo glodny
## peop - ilosc miejsc w restauracji(1 brak(słaba restaruracja),2-srednio,3 duzo)
## rain czy pada
## res - rezerwacja
## time - czas oczekiwania
# dezycja
# [ [1,0],[1,0],[1,0],[1-0],[1-3],[1-0],[1-0],[0-100],[1-0]


#
training_data = [
    # $
    [1, 1, 1, 1, 1, 1, 0, 5, 0],  #
    [1, 0, 0, 0, 2, 0, 1, 5, 1],
    [1, 0, 0, 0, 2, 0, 1, 70, 0],  #
    [0, 0, 1, 1, 3, 1, 0, 35, 0],
    [0, 1, 1, 1, 3, 1, 0, 35, 0],
    [0, 1, 1, 1, 3, 1, 0, 35, 0],
    [1, 1, 0, 0, 2, 0, 1, 5, 1],
    [1, 0, 1, 0, 1, 1, 0, 5, 1],  #
    [0, 1, 0, 1, 2, 0, 0, 5, 1],
    [0, 0, 1, 0, 3, 1, 1, 70, 0],  #
    [1, 1, 1, 1, 3, 0, 0, 5, 1],
    [1, 1, 1, 1, 3, 0, 0, 70, 1],
    [1, 0, 1, 1, 3, 1, 1, 35, 1],
    [0, 1, 1, 0, 3, 0, 1, 70, 0],  #
    [0, 0, 1, 1, 3, 1, 1, 35, 1],  #
    [1, 0, 1, 0, 3, 0, 1, 70, 0],  #
    [0, 1, 1, 1, 3, 0, 1, 35, 1],  #
    [0, 1, 1, 1, 3, 1, 0, 5, 1]
]
header = ["Topi się?", #1,0, szklo, plastik 0
          "Palne?", #1,0 organiczne, papier 1
         "Przeźroczyste?", #1,0 plastik/szklo 2
          "Podlega recyklingowi?", #1,0 oprocz organicznych 3
          "Mokre?",#1,0 oprócz papieru 4
            "Da sie zgniatac?", #1,0 oprócz szkła 5

          "Waga m3"
          ]


def unique_vals(rows, col):
    return set(row[col] for row in rows)


print(unique_vals(train_data.data, 0))


def class_counts(rows):
    counts = {}
    for row in rows:
        label = row[-1]  # label = row[len(row)-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts


print(class_counts(train_data.data))


def is_numeric(value):
    return isinstance(value, int) or isinstance(value, float)


class Question:
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):  # sprawdza czy dane nadaja sie do oczyttu
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        # self.column=str(self.column)
        condition = str(condition)
        try:
            return "Is %s $s $s?" % (header[self.column], condition, str(self.value))
        except:
            return "Is %s?" % str((header[self.column], condition, str(self.value)))


#print(Question(1, 1).match(training_data[5]))


def partition(rows, question):
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows


true_rows, false_rows = partition(training_data, Question(3, 1))
rowes = []
for ss in true_rows:
    rowes.append(str(ss[-0]))


# print(rowes)
# print(true_rows)
def gini(rows):  # szanse na poprawnosć danych
    counts = class_counts(rows)
    impurity = 1  # na początku 100% niepoprawnosci

    for label in counts:
        prob_of_label = counts[label] / float(len(rows))
        impurity -= prob_of_label ** 2
    return impurity


#print(gini(rowes))


def info_gain(left, right, niepewny):  # informacja o wartości informacji
    p = float(len(left) / len(left) + len(right))
    return niepewny - p * gini(left) - (1 - p * gini(right))


niepewnosc = gini(train_data.data)
#print(info_gain(true_rows, false_rows, niepewnosc))


def best_split(rows):  # znajduje najlepsze rozdzielenie danych
    best_gain = 0  # przechowuje najlepsze informacje
    best_question = None  # przechowuje najlepsze pytanie
    niepewnosc = gini(rows)
    n_features = len(rows[0]) - 1  # liczba column

    for col in range(n_features):
        values = set([row[col] for row in rows])

        for val in values:  # dla kazdego wpisu danych
            question = Question(col, val)

            true_rows, false_rows = partition(rows, question)  # dzieli dane

            if len(true_rows) == 0 or len(false_rows) == 0:  # pomin jesli nie dzeli danyc
                continue

            gain = info_gain(true_rows, false_rows, niepewnosc)  # oblicza info z tego rozdzielenia

            if gain >= best_gain:
                best_gain, best_question = gain, question
    return best_gain, best_question


best_gain, best_question = best_split(training_data)


class Leaf:
    # tworzy oddzielne galezie dla drzewa
    def __init__(self, rows):
        self.predictions = class_counts(rows)


class Decision_Node:
    # przechowuje najlepsze pytania i dwie galezie

    def __init__(self,
                 question
                 , true_branch
                 , false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch


def build_tree(rows):
    # tworzy drzewo

    gain, question = best_split(rows)

    if gain == 0:  # gdy nie ma co sprawdzać
        return Leaf(rows)

    # dziele pozostale drzewo, na poczatku cale drzewo
    true_rows, false_rows = partition(rows, question)

    # rekurencyjnie budje poprawną gałąź
    true_branch = build_tree(true_rows)

    # rekurencyjnie budje niepoprawna gałąź
    false_branch = build_tree(false_rows)

    return Decision_Node(question, true_branch, false_branch)


def print_tree(node, spacing=""):  # wypisuje drzewo

    # czy mamy gałąż
    if isinstance(node, Leaf):
        print(spacing + "Predict", node.predictions)
        return
    # wypisz warunek
    print(spacing + str(node.question))
    # tworzy rekurencyjnie true gałąż
    print(spacing + '--> True:')
    print_tree(node.true_branch, spacing + " ")
    # tworzy rekurencyjnie false gałąż
    print(spacing + '--> False:')
    print_tree(node.false_branch, spacing + " ")


def classify(row, node):
    if isinstance(node, Leaf):
        return node.predictions

    # dezycja którą gałęzią podążać
    if node.question.match(row):
        return classify(row, node.true_branch)

    else:
        return classify(row, node.false_branch)


my_tree = build_tree(train_data.data)
#print(classify(train_data.data[0], my_tree))


def print_leaf(counts):
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs


#print_tree(my_tree)
testing_data = [

    ['1', '0', '1', '1', '0', '0', '30', 'szklo']
]




def test_data(test_data):
    for row in test_data:
        return "%s" % (print_leaf(classify(row, my_tree)))

print(test_data(testing_data))