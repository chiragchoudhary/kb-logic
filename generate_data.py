import os
import random
import copy


class Relation:
    def __init__(self, id=1, entities=None):
        self.id = id
        self.name = "R" + str(self.id)
        self.entities = entities


class Entity:
    def __init__(self, id=1, type='a'):
        self.id = id
        self.type = type


def generate_data(entities, relations=None, type="symmetry", relation_prob=0.1):

    num_relations = len(relations)
    if relations is None or num_relations < 2:
        print("Number of relations specified < 2, exiting...")
        return
    else:
        print("Number of relations: {}".format(num_relations))

    num_entities = len(entities)
    print("Number of entities: {}".format(num_entities))

    training_facts = set()
    test_facts = set()

    entity_types = []
    i = 0
    for relation in relations:
        for entity in relation.entities:
            if entity.type not in entity_types:
                entity_types.append(entity.type)
                i += 1

    num_entity_types = len(entity_types)
    num_entities_per_type = num_entities/num_entity_types
    print("Number of entity types: {}".format(num_entity_types))

    entity_paths = []
    mp = {}
    # generate training data
    for i, relation in enumerate(relations[:-1]):
        es1_s = entity_types.index(relation.entities[0].type)*num_entities_per_type
        es2_s = entity_types.index(relation.entities[1].type)*num_entities_per_type

        es1 = entities[es1_s:es1_s + num_entities_per_type]
        es2 = entities[es2_s:es2_s + num_entities_per_type]

        entity_tuples = [(e1, e2) for e1 in es1 for e2 in es2 if e1 != e2]

        # print len(entity_tuples)

        rel = relation.name
        for (e1, e2) in entity_tuples:
            if (e1, rel, e2) not in training_facts and (e2, rel, e1) not in training_facts:
                p = random.random()
                if p < relation_prob:
                    training_facts.add((e1, rel, e2))
                    if (e1, rel) not in mp:
                        mp[(e1, rel)] = [e2]
                    else:
                        mp[(e1, rel)].append(e2)

                    if (rel, e2) not in mp:
                        mp[(rel, e2)] = [e1]
                    else:
                        mp[(rel, e2)].append(e1)

        e1_id = relation.entities[0].id
        e2_id = relation.entities[1].id

        # print e1_id, e2_id
        if i == 0:
            for (e1, r, e2) in training_facts:
                entity_paths.append({e1_id: e1, e2_id: e2})
        else:
            entity_paths_tmp = []
            for j, path in enumerate(entity_paths):
                if e1_id in path and e2_id in path:
                    if (path[e1_id], rel, path[e2_id]) in training_facts:
                        new_path = copy.deepcopy(path)
                        entity_paths_tmp.append(new_path)
                elif e1_id in path:
                    e1 = path[e1_id]
                    if (e1, rel) in mp:
                        for e2 in mp[(e1, rel)]:
                            new_path = copy.deepcopy(path)
                            new_path[e2_id] = e2
                            entity_paths_tmp.append(new_path)
                elif e2_id in path:
                    e2 = path[e2_id]
                    if (rel, e2) in mp:
                        for e1 in mp[(rel, e2)]:
                            new_path = copy.deepcopy(path)
                            new_path[e1_id] = e1
                            entity_paths_tmp.append(new_path)
                else:
                    for (e1, r, e2) in training_facts:
                        if r == rel:
                            new_path = copy.deepcopy(path)
                            new_path[e1_id] = e1
                            new_path[e2_id] = e2
                            entity_paths_tmp.append(new_path)

            #if len(entity_paths_tmp) > 0:
            entity_paths = copy.deepcopy(entity_paths_tmp)
            del entity_paths_tmp

        # print training_facts
        # print(entity_paths)
        # print

    # print
    # print "######## Map ###########"
    # print mp
    # print
    # generate test data, based on training data
    head_rel = relations[-1].name
    e1_id = relations[-1].entities[0].id
    e2_id = relations[-1].entities[1].id

    print "sample entity paths"
    print entity_paths[:3]
    print
    for path in entity_paths:
        if e1_id in path and e2_id in path:
            e1 = path[e1_id]
            e2 = path[e2_id]
            test_facts.add((e1, head_rel, e2))
            if type == "implication":
                # add negative facts also
                es1_s = entity_types.index(relations[-1].entities[0].type) * num_entities_per_type
                es2_s = entity_types.index(relations[-1].entities[1].type) * num_entities_per_type

                es1 = entities[es1_s:es1_s + num_entities_per_type]
                es2 = entities[es2_s:es2_s + num_entities_per_type]
                ie = random.choice(es1)
                while (ie, head_rel, e2) in test_facts:
                    ie = random.choice(es1)
                test_facts.add((ie, head_rel, e2))

                ie = random.choice(es2)
                while (e1, head_rel, ie) in test_facts:
                    ie = random.choice(es2)
                test_facts.add((e1, head_rel, ie))

    return list(training_facts), list(test_facts)


# fetch list of entities
with open(os.path.join(os.getcwd(), "data", "entities.txt")) as f:
    entities = f.read().splitlines()

a = Entity(id=1, type='a')
b = Entity(id=2, type='b')
c = Entity(id=3, type='c')
d = Entity(id=4, type='d')

rel1 = Relation(id=1, entities=[a, b])
rel2 = Relation(id=2, entities=[a, b])
rel3 = Relation(id=3, entities=[a, c])
rel4 = Relation(id=4, entities=[a, d])

training_facts, test_facts = generate_data(entities[:20], [rel1, rel2], relation_prob=0.1, type="symmetry")
# print "training facts"
print "Number of training facts: {}".format(len(training_facts))
training_file = os.path.join(os.getcwd(), "data", "train.txt")
random.shuffle(training_facts)
with open(training_file, 'w+') as f:
    for e in training_facts:
        f.write("{}\n".format('\t'.join(e)))
f.close()
# print
# print "test facts"
# print test_facts
print "Number of test facts: {}".format(len(test_facts))
test_file = os.path.join(os.getcwd(), "data", "test.txt")
random.shuffle(test_facts)
with open(test_file, 'w+') as f:
    for e in test_facts:
        f.write("{}\n".format('\t'.join(e)))
f.close()


