import os
import math
import random
import argparse


def generate_entities(num_entities=100):
    """generate num_entities random entities for synthetic knowledge graph."""
    i = 0
    entity_list = []
    hex_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    l = int(math.log(num_entities, 18)+1)
    # print l
    while i < num_entities:
        entity = "/entity_{}".format(''.join(random.sample(hex_chars, l)))
        if entity not in entity_list:
            entity_list.append(entity)
            i += 1
    return entity_list


parser = argparse.ArgumentParser()
parser.add_argument("--N", type=int)
args = parser.parse_args()
N = args.N

print N

entities = generate_entities(N)
entity_file = os.path.join(os.getcwd(), "data", "fake-420", "entities.txt")
f = open(entity_file, 'w+')
with open(entity_file, 'w+') as f:
    for e in entities:
        f.write("{}\n".format(e))

f.close()
