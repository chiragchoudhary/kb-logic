import os
import math
import random


def generate_entities(num_entities=100):
    """generate num_entities random entities for synthetic knowledge graph."""
    i = 0
    entity_list = []
    hex_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    len = int(math.log(num_entities, 16)+1)
    while i < num_entities:
        entity = "/entity_{}".format(''.join(random.sample(hex_chars, len)))
        if entity not in entity_list:
            entity_list.append(entity)
            i += 1
    return entity_list


N = 200

entities = generate_entities(N)
print entities
entity_file = os.path.join(os.getcwd(), "data", "entities.txt")
f = open(entity_file, 'w+')
with open(entity_file, 'w+') as f:
    for e in entities:
        f.write("{}\n".format(e))

f.close()
