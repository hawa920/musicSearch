import base64
from flask import Flask, request, send_from_directory, send_file, make_response, render_template

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def main():
  if request.method == 'POST':
    return 'Bad Request.'
  return render_template('index.html')


@app.route('/js/mp3Worker.js', methods = ['GET'])
def mp3Worker():
  return app.send_static_file('js/mp3Worker.js')


@app.route('/js/recorderWorker.js', methods = ['GET'])
def recordWorker():
  return app.send_static_file('js/recorderWorker.js')

@app.route('/js/libmp3lame.min.js', methods = ['GET'])
def libmp3lame():
  return app.send_static_file('js/libmp3lame.min.js')

@app.route('/<path:dummy>', methods = ['GET', 'POST'])
def fallback(dummy):
  return 'bro......'

@app.route('/upload.php', methods = ['POST'])
def musicSearch():
  mp3signals = request.form['data']
  pos = mp3signals.find(',')
  mp3signals = base64.b64decode(mp3signals[pos:])
  with open('./test.mp3', 'wb') as fp:
    fp.write(mp3signals)

  return '1'
  #return base64.b64decode(mp3signals)


if __name__ == "__main__":
  app.run(port=5005, debug=True)
  # Comment the line above and use the line below if you launch on your own server
  # app.run(host='0.0.0.0', port=5005, debug = False)
