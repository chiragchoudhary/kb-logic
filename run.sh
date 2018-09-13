#!/usr/bin/env bash
N=100
python2 generate_entities.py --N 500
emb_dim=(2 10 20 60 120 150 200)

for prob in `seq 0.10 0.10 1.0`;
do
    if [ -f "/ConvE/ConvE/data/fake-420/train.txt" ]
    then
        rm /ConvE/ConvE/data/fake-420/*.json
        rm /ConvE/ConvE/data/fake-420/t*.txt
    fi
    python2 generate_data.py --N ${N} --relation_prob ${prob}
    bash preprocess.sh
    for d in ${emb_dim[@]};
    do
        rm /home/chirag/.data/fake-420/* -rf
        CUDA_VISIBLE_DEVICES=0 python3 main.py model DistMult dataset fake-420 input_drop 0.2 hidden_drop 0.3 feat_drop 0.2  lr 0.003 process True embedding_dim ${d}
        sleep 2
    done
done

