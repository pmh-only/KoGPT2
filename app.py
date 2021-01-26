import os
import torch
import platform
import sentencepiece
from kogpt2.utils import get_tokenizer
from kogpt2.pytorch_kogpt2 import get_pytorch_kogpt2_model
from flask import Flask, request, jsonify, __version__ as flaskver

tok_path = get_tokenizer(cachedir='./bin/')
model, vocab = get_pytorch_kogpt2_model(cachedir='./bin/')
tok = sentencepiece.SentencePieceProcessor(tok_path)

app = Flask(__name__)
port = int(os.getenv('port', '8080'))

@app.route('/', methods=['GET'])
def root():
  env = { 'python': platform.python_version(), 'flask': flaskver, 'pytorch': torch.__version__ }
  urls = { 'original': 'https://github.com/SKT-AI/KoGPT2', 'fork': 'https://github.com/pmh-only/KoGPT2' }
  usage = 'GET /job?query=<sentence>[&loop=<loopLimit>]'
  return jsonify(label='kogpt2', urls=urls, env=env, usage=usage)

@app.route('/job', methods=['GET'])
def job():
  query = request.args.get('query')
  loop = request.args.get('loop', -1, type=int)
  if query == None:
    return jsonify(success=False, result='')

  if loop < 0:
    result = gpt2(query)
    result.reverse()
    return jsonify(success=True, result=result)
  else:
    result = query
    while loop > 0:
      if result.endswith('</s>'):
        break

      loop -= 1
      result += list(gpt2(result))[-1]
    return jsonify(success=True, result=result)

def gpt2 (sent):
  toked = tok.Encode(sent, alpha=0, nbest_size=0, out_type=str)
  input_ids = torch.tensor([vocab[vocab.bos_token],]  + vocab[toked]).unsqueeze(0)
  pred = model(input_ids)[0]
  gen = vocab.to_tokens(torch.argmax(pred, axis=-1).squeeze().tolist())
  return gen

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=port)
