# print('install splotlight if needed')
#!pip install  git+https://github.com/maciejkula/spotlight.git@master#egg=spotlight


# # movielense data
# - Download the 100k version from https://grouplens.org/datasets/movielens/
# - extract to folder './ml-100k/'

import numpy as np
from spotlight.interactions import Interactions
from spotlight.cross_validation import random_train_test_split
user_ids, item_ids, ratings, timestamps = zip(*[i.strip().split('\t') for i in open("./ml-100k/u.data").readlines()])
user_ids = np.array([int(u) for u in list(user_ids)])
item_ids = np.array([int(i) for i in list(item_ids)])
timestamps = np.array([int(s) for s in list(timestamps)])
interactions = Interactions(user_ids=user_ids, item_ids=item_ids, timestamps=timestamps)
train, test = random_train_test_split(interactions)


# Create random noise


import random
preserving_25_percent_items = []
preserving_50_percent_items = []
preserving_75_percent_items = []
vmin = train.item_ids.min()
vmax = train.item_ids.max()
for real_item_idx in train.item_ids:
    random_item_idx = random.randint(vmin, vmax)
    sampling_threshold = random.random()
    if sampling_threshold < .25:
        preserving_25_percent_items.append(real_item_idx)
    else:
        preserving_25_percent_items.append(random_item_idx)
    if sampling_threshold < .5:
        preserving_50_percent_items.append(real_item_idx)
    else:
        preserving_50_percent_items.append(random_item_idx)
    if sampling_threshold < .75:
        preserving_75_percent_items.append(real_item_idx)
    else:
        preserving_75_percent_items.append(random_item_idx)


# Create train data


user_ids = train.user_ids
timestamps = train.timestamps
preserving_25_percent_train = Interactions(user_ids=user_ids,
                                  item_ids=np.asarray(preserving_25_percent_items),
                                  timestamps=timestamps)
preserving_50_percent_train = Interactions(user_ids=user_ids,
                                  item_ids=np.asarray(preserving_50_percent_items),
                                  timestamps=timestamps)
preserving_75_percent_train = Interactions(user_ids=user_ids,
                                  item_ids=np.asarray(preserving_75_percent_items),
                                  timestamps=timestamps)


# visulize train data


# from matplotlib import pyplot
# plt = pyplot.figure(figsize=(16,10))
# pyplot.subplot(221)
# pyplot.hist(item_ids, bins=50, alpha=0.7, label='100% item preserving', color='red')
# pyplot.legend(loc='upper right')
# pyplot.subplot(222)
# pyplot.hist(preserving_25_percent_items, bins=50, alpha=0.7, color='green', 
#             label='25% item preserving, 75% random noise' )
# pyplot.legend(loc='upper right')
# pyplot.subplot(223)
# pyplot.hist(preserving_50_percent_items, bins=50, alpha=0.7, color='blue', 
#             label= '50% item preserving, 50% random noise')
# pyplot.legend(loc='upper right')
# pyplot.subplot(224)
# pyplot.hist(preserving_75_percent_items, bins=50, alpha=0.7, 
#             label='75% item preserving, 25% random noise')
# pyplot.legend(loc='upper right')
# pyplot.show()


# create train models


from spotlight.sequence.implicit import ImplicitSequenceModel
model = ImplicitSequenceModel(embedding_dim=128)
preserving_25_percent_model = ImplicitSequenceModel(embedding_dim=128)
preserving_50_percent_model = ImplicitSequenceModel(embedding_dim=128)
preserving_75_percent_model = ImplicitSequenceModel(embedding_dim=128)


# fit models


model.fit(train.to_sequence(), verbose=True)
preserving_25_percent_model.fit(preserving_25_percent_train.to_sequence(), verbose=True)
preserving_50_percent_model.fit(preserving_50_percent_train.to_sequence(), verbose=True)
preserving_75_percent_model.fit(preserving_75_percent_train.to_sequence(), verbose=True)

import torch
torch.save(preserving_25_percent_model, './preserving_25_percent_model.model')
torch.save(preserving_50_percent_model, './preserving_50_percent_model.model')
torch.save(preserving_75_percent_model, './preserving_75_percent_model.model')
# result evaluation

from spotlight.evaluation import mrr_score
train_mrrs = mrr_score(model, train)
preserving_25_train_mrrs = mrr_score(preserving_25_percent_model, preserving_25_percent_train)
preserving_50_train_mrrs = mrr_score(preserving_50_percent_model, preserving_50_percent_train)
preserving_75_train_mrrs = mrr_score(preserving_75_percent_model, preserving_75_percent_train)

test_mrrs = mrr_score(model, test)
preserving_25_test_mrrs = mrr_score(preserving_25_percent_model, test)
preserving_50_test_mrrs = mrr_score(preserving_50_percent_model, test)
preserving_75_test_mrrs = mrr_score(preserving_75_percent_model, test)

print('For 100% preserving items')
print('Train MRRS {:.3f}, test MRRS {:.3f}'.format(train_mrrs.sum(), test_mrrs.sum()))
print('For 25% preserving items')
print('Train MRRS {:.3f}, test MRRS {:.3f}'.format(preserving_25_train_mrrs.sum(), preserving_25_test_mrrs.sum()))
print('For 50% preserving items')
print('Train MRRS {:.3f}, test MRRS {:.3f}'.format(preserving_50_train_mrrs.sum(), preserving_50_test_mrrs.sum()))
print('For 75% preserving items')
print('Train MRRS {:.3f}, test MRRS {:.3f}'.format(preserving_75_train_mrrs.sum(), preserving_75_test_mrrs.sum()))