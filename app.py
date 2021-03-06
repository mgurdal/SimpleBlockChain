from Blockchain import Blockchain
from flask import Flask, jsonify, request
from textwrap import dedent
from uuid import uuid4
app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()

@app.route("/", methods=['GET'])
def index():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route("/transactions/new", methods=['POST', 'OPTIONS'])
def new_transaction():

    values = request.form
    print(values)
    required = ["sender", "recipient", "amount"]
    if not all([req in values for req in required]):
        return "Hata, Eksik parametre girdin. Adam gibi parametre gir", 405

    index = blockchain.new_transaction(
        values['sender'], values['recipient'], values['amount']
    )
    response = { "message": "Transaction {}. bloka eklendi.".format(index)}
    return jsonify(response), 201

@app.route("/nodes/register", methods=['POST'])
def register_nodes():
    values = request.form
    nodes = values['nodes']

    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400
    blockchain.register_node(nodes)

    response = {
        'message': 'Yeni node eklendi.',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201

@app.route("/blockchain", methods=['GET'])
def getblockchain():

    return jsonify(list(blockchain.nodes)), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        response = {
            'message': 'Chain değiştirildi.',
            'new_chain': blockchain.chain
        }
    else:
         response = {
            'message': 'Doğru chain.',
            'chain': blockchain.chain
        }
    return jsonify(response), 200

@app.route("/mine", methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.PoW(last_proof) # uzun sürüyor

    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transaction'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)


"""
C
-------------------
M <-> M <-> M   -> D

N N N N N N N N N

A A A A A A A A A
"""
