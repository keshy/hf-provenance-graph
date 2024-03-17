import argparse
import json
import random
import re
from copy import deepcopy

from huggingface_hub import HfApi, list_models, get_model_tags
from redisgraph import Graph, Node
import redis
import requests
import argparse


class ModelCard:
    def __init__(self, model):
        _id = model.id
        author = model.author


class ModelCrawler:
    def __init__(self, host='localhost', port=6379, label='model_metadata'):
        self.redis_connection = redis.Redis(host=host, port=port)
        self.graph = Graph('ancenstory_wiki', self.redis_connection)
        self.hf_api = HfApi()

    def crawl(self, label='model', depth=1000, parent=None):
        # iterate through all models upto the limit.
        models = self.hf_api.list_models()
        for model in models:
            model_d = model.__dict__
            # persist model
            datasets = []
            for tag in model.tags:
                if tag.startswith('dataset:'):
                    datasets.append(tag)
            siblings = model_d.get('siblings', '')
            spaces = model_d.get('spaces', '')
            model_d['created_at'] = str(model.created_at)
            if siblings != '':
                model_d.pop('siblings')
            if spaces != '':
                model_d.pop('spaces')
            final_d = deepcopy(model_d)
            for k, v in model_d.items():
                if v is None:
                    final_d.pop(k)
            if not model.tags or model.tags == []:
                continue
            self.graph.query("MERGE (n: %s%s)" % ('Model',
                                                  Node(node_id=model.id, label='Model',
                                                       properties=final_d).toString()))
            for dataset in datasets:
                if dataset.startswith('dataset:'):
                    r_d = re.sub('dataset:', '', dataset)
                try:
                    d_info = self.hf_api.dataset_info(repo_id=r_d, files_metadata=True)
                    d_i = {
                        'tag': d_info.tags,
                        'id': d_info.id,
                        'last_updated': str(d_info.lastModified),
                        'sha': d_info.sha,
                        'likes': d_info.likes,
                        'downloads': d_info.downloads,
                        'author': d_info.author
                    }
                    d_d_i = deepcopy(d_i)
                    for k, v in d_i.items():
                        if v is None:
                            d_d_i.pop(k)
                    self.graph.query("MERGE (n: %s%s)" % ('Dataset',
                                                          Node(node_id=d_info.id, label='Dataset',
                                                               properties=d_d_i).toString()))
                    # create the edge
                    self.graph.query(
                        "MATCH (u: %s {id: \"%s\"}), (u2: %s {id: \"%s\"}) MERGE (u)-[r: %s]->(u2)" % ('Model',
                                                                                                       model.id,
                                                                                                       'Dataset',
                                                                                                       d_info.id,
                                                                                                       'trained_on'))
                except Exception as e:
                    print(f'could not fetch dataset: {dataset} due to {e}')
                    pass
            # remove datasets from tags and create nodes and edges for each tag that is not a dataset
            for tag in model.tags:
                # add try cattch block to handle exceptions
                try:
                    if not tag.startswith('dataset:'):
                        self.graph.query("MERGE (n: %s%s)" % ('Tag',
                                                              Node(node_id=tag, label='Tag',
                                                                   properties={'tag': tag}).toString()))
                        self.graph.query(
                            "MATCH (u: %s {id: \"%s\"}), (u2: %s {tag: \"%s\"}) MERGE (u)-[r: %s]->(u2)" % ('Model',
                                                                                                            model.id,
                                                                                                            'Tag',
                                                                                                            tag,
                                                                                                            'tagged_as'))
                except Exception as e:
                    print(f'could not fetch tag: {tag} due to {e}')
                    pass


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-s', '--tag', required=False, type=str,
                            help="Starting model URL to crawl from")
    arg_parser.add_argument('-l', '--label', default='model_metadata', type=str,
                            help="Default label model_metadata but can be overridden")
    arg_parser.add_argument('-d', '--depth', default=1000, type=int,
                            help="Default limit on depth of crawl at each level")
    args = arg_parser.parse_args()
    ac = ModelCrawler(label=args.label)
    ac.crawl(label=args.label, depth=args.depth)
