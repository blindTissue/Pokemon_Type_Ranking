import csv
import math
import copy
INITAL_DEF_RATING = 100
INITAL_OFF_RATING = 100

with open('chart.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)



# Seperate type of ranking for defense and offense. If super effective against type with higher def rating, off rating is better.
# Used dict because of dual typing in future.
def_rating = {}
off_rating = {}
type_list = []

attack_score_increment = {0: 0, 0.25 : 1, 0.5 : 2, 1: 3, 2: 4, 4: 5}
def_score_increment = {0: 5, 0.25 : 4, 0.5 : 3, 1: 2, 2: 1, 4: 0}


# Initialize all types with 100 rating
types = data[0][1:]
for type in types:
    def_rating[type] = INITAL_DEF_RATING
    off_rating[type] = INITAL_OFF_RATING
    type_list.append(type)

def update_ratings(ratio=1):
    def_rating_save = copy.deepcopy(def_rating)
    off_rating_save = copy.deepcopy(off_rating)
    update_off_rating(off_rating_save, def_rating_save, ratio)
    update_def_rating(off_rating_save, def_rating_save, ratio)



def update_off_rating(off_rating_save, def_rating_save, ratio):
    update_list = [0 for i in range(len(types))]
    for key in off_rating_save:
        type_index = type_list.index(key)
        att_effective_list = data[type_index + 1][1:]
        for i in range(len(att_effective_list)):
            update_list[type_index] += def_rating_save[types[i]] * attack_score_increment[float(att_effective_list[i])]
        
    # Normalize so that average is 100
    l_average = sum(update_list) / len(update_list)
    normalize_factor = 100 / l_average
    update_list = [x * normalize_factor for x in update_list]


    # Update off_rating
    for i in range(len(update_list)):
        off_rating[types[i]] = off_rating_save[types[i]] * (1 - ratio) + update_list[i] * ratio

def update_def_rating(off_rating_save, def_rating_save, ratio):
    update_list = [0 for i in range(len(types))]
    print(off_rating_save)
    for key in def_rating_save:
        type_index = type_list.index(key)
        def_effective_list = [data[i][type_index + 1] for i in range(1, len(data))]
        for i in range(len(def_effective_list)):
            update_list[type_index] += off_rating_save[types[i]] * def_score_increment[float(def_effective_list[i])]

    l_average = sum(update_list) / len(update_list)
    normalize_factor = 100 / l_average
    update_list = [x * normalize_factor for x in update_list]

    # Update def_rating
    for i in range(len(update_list)):
        def_rating[types[i]] = def_rating_save[types[i]] * (1 - ratio) + update_list[i] * ratio




def print_ratings():
    # Print out the ratings in order.
    print("Offensive Ratings:")
    for key, value in sorted(off_rating.items(), key=lambda item: item[1], reverse=True):
        print("%s: %s" % (key, value))

    print("\nDefensive Ratings:")
    for key, value in sorted(def_rating.items(), key=lambda item: item[1], reverse=True):
        print("%s: %s" % (key, value))


def print_combined():
    combined_rating = {}
    for key in off_rating:
        combined_rating[key] = off_rating[key] + def_rating[key]
    print("Combined Ratings:")
    for key, value in sorted(combined_rating.items(), key=lambda item: item[1], reverse=True):
        print("%s: %s" % (key, value))

def rank_typing():
    for i in range(100):
        update_ratings(1)
        print_ratings()
        print("\n")
    print_combined()


if __name__ == "__main__":
    rank_typing()



