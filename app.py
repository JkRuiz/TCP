from flask import Flask, request, flash
import json


app = Flask(__name__)


@app.route('/metrics', methods=['POST'])
def register():
    reqJson = json.loads(request.json)
    with open("metrics.txt", "a") as metrics:
        ip = str(reqJson['ipClient'])
        receivedBytes = str(reqJson['bytes'])
        time = str(reqJson['time'])
        metrics.write('Cliente - ' + ip + ': \n')
        metrics.write('Bytes recibidos - ' + receivedBytes + '\n')
        metrics.write('Fecha - ' + time + '\n')
        metrics.write('--------------------------------------------------' + '\n')
    return('', 204)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(host='157.253.205.122')
