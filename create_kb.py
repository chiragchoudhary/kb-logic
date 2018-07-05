import os
import random


def generate_facts(num_facts):
    """Generate tuples of type (e1, R1, e2), (e1, R2, e2) & (e1', R1, e2') for training, and (e1', R2, e2') for testing.

    In total, generates 3*num_facts of first two relation types for training, with R1:R2::1:2.
    For every two R2 tuples, it generates an R1 tuple.

    Generates fixed number of tuples of type (e1', R1, e2') and (e1', R2, e2').
    """
    # fetch list of entities
    with open(os.path.join(os.getcwd(), "data", "entities.txt")) as f:
        entities = f.read().splitlines()

    training_facts_1 = []    # list of all training tuples of type (e1, R1, e2) and (e1, R2, e2)
    training_facts_2 = []  # list of all training tuples of type (e1', R1, e2')
    test_facts = []        # list of all test tuples of type  (e1', R2, e2')
    rel1 = "/rel/relation_1/"
    rel2 = "/rel/relation_2/"
    fact_set = ()  # to ensure that all the generated facts are unique
    i = 0
    while i < 2*num_facts:
        e1, e2 = random.sample(entities, 2)
        if (e1, rel2, e2) not in fact_set and (e2, rel2, e1) not in fact_set:
            training_facts_1.append((e1, rel2, e2))
            if i % 2 == 0:
                training_facts_1.append((e1, rel1, e2))
            i += 1

    i = 0
    while i < 500:
        e1, e2 = random.sample(entities, 2)
        if (e1, rel2, e2) not in fact_set and (e2, rel2, e1) not in fact_set:
            training_facts_2.append((e1, rel1, e2))
            test_facts.append((e1, rel2, e2))
            i += 1

    return training_facts_1, training_facts_2, test_facts


N = 3000
facts1, facts2, facts_test = generate_facts(N)

# write training files with different sizes
ratio = 0.2
while ratio <= 1.0:
    count = int(3*N*ratio)
    facts_file = os.path.join(os.getcwd(), "data", "train_{}.txt".format(count))
    facts = facts1[:count] + facts2
    with open(facts_file, 'w+') as f:
        for e in facts:
            f.write("{}\n".format('\t'.join(e)))
    f.close()
    ratio += 0.2

# write test file
test_file = os.path.join(os.getcwd(), "data", "test.txt")
with open(test_file, 'w+') as f:
    for e in facts_test:
        f.write("{}\n".format('\t'.join(e)))

f.close()
