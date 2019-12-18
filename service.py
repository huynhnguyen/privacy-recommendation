from flask import Flask, jsonify, request
import json
import argparse
import torch

save_model = torch.load('./preserving_75_percent_model.model')

with open('./movies.json','r') as f:
    all_movies = json.load(f)

app = Flask(__name__)

@app.route('/')
def health():
    return 'recommendation demo'

@app.route('/movies')
def movies():
    return jsonify(all_movies)

@app.route('/recommend', methods=['GET'])
def recommend():
    interacts = request.args.get('interacts', None)
    print( interacts )
    if interacts is None:
        return jsonify({'message': 'please submit interacts as a list of movie ids'})
    else:
        interacts = [int(i) for i in json.loads(interacts)]
        all_scores = save_model.predict(interacts)
        return jsonify({'recommend': all_movies[str(all_scores.argmax())],
            'bestScore':  str(all_scores.max()),
            'interacts': [all_movies[str(id)] for id in interacts] })



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='starting action server')
    parser.add_argument('--port', dest='port', default=5055, help='default port is 5055')
    args = parser.parse_args()    
    port = int(args.port)
    app.run(host='0.0.0.0', port=port, debug=True)