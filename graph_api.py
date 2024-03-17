# develop flask application that exposes apis to get data from redis graph
import json
import os
import yaml
import redis
import argparse
from flask import Flask, jsonify, request
from redisgraph import Graph
from openai import AzureOpenAI

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
graph = Graph('ancenstory_wiki', r)
deployment_name = 'us-datascience-text-davinci-003'
with open('secrets.yaml', 'r') as f:
    secrets = yaml.safe_load(f)
    os.environ['AZURE_OPENAI_API_KEY'] = secrets.get('openai').get('api_key')
    os.environ['AZURE_OPENAI_ENDPOINT'] = secrets.get('openai').get('api_base')
    # create an instance of the openai client
    llm_client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=secrets.get('openai').get('api_version'),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )


@app.route('/api/v1/model', methods=['GET'])
def get_model():
    model_id = request.args.get('id')
    # get the model from the graph using opencypher and redis graph query
    query = "MATCH (m) RETURN m limit 10"
    result = graph.query(query)
    nodes = []
    for n in result.result_set:
        nodes.append(n[0].properties)
    return jsonify(nodes)


# api to get a natural language and convert it to a cypher query
@app.route('/api/v1/query', methods=['GET'])
def get_query():
    query = request.args.get('query')
    if not llm_client:
        # error out and return 412
        return jsonify({'error': 'language model not initialized'}), 412
    prompt = f"""
        Assume the following graph model is available in a graph database and you are expected to take in a natural 
        language query and convert it to a an opencypher query. 
        If your unable to convert it to a query, please provide a response that indicates that the query is not valid.
        Do not make any assumptions about the graph model, and use the natural language query as is. If the query is 
        empty or not provided, please provide a response that indicates that the query is not valid.
        
        Graph model:
        
        1. Nodes: Model, Dataset, and Tag
        2. Relationships: Model trained_on Dataset, Model tagged_as Tag
        
        Properties for Model nodes are: created_at(time), downloads(int), id(str), library_name(str), likes(int),
         modelId(str), pipeline_tag(list), private(boolean), tags(list)
        Properties for Dataset nodes are: tag(list), id(str), last_updated(time), sha(str), likes(long), 
        downloads(long), author(str)
        Properties for Tag nodes are: tag(str)
        
        Natural Language Query: {query}
        
        Only return a json response with the opencypher query and a boolean flag status that indicates if the query was 
        translated successfully or not. Sample response:
         {{
            "query": "MATCH (m:Model)-[:trained_on]->(d:Dataset) WHERE m.id = '1234' RETURN m, d",
            "status": true
         }}
         Sample failed response:
         {{
            "query": "The query is not valid",
            "status": false
        }}
    """
    response = llm_client.completions.create(model='us-datascience-text-davinci-003', prompt=prompt, max_tokens=150,
                                             temperature=0.7,
                                             top_p=1.0)
    result = json.loads(response.choices[0].text.strip())
    if result and type(result) == dict:
        if result.get('status') == 'false':
            return jsonify({'query': 'The query is not valid', 'status': False})
        else:
            cypher = result.get('query')
            g_response = graph.query(cypher)

            return



# use arg parse to get the redis details as parameter for starting the server and also the namespace/graph name
if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Start the graph api to serve model information')
    argparser.add_argument('--host', type=str, help='redis host', required=True)
    argparser.add_argument('--port', type=int, help='redis port', required=True)
    argparser.add_argument('--graph', type=str, help='graph name', required=True)
    args = argparser.parse_args()
