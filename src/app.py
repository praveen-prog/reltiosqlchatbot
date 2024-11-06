
from flask import Flask, render_template, jsonify, request
from helper import TableListClass     
import os
from logger import logging
import time

os.chdir("src/")
app = Flask(__name__)

obj = TableListClass()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = obj.full_chain_call(input)
    logging.info(f"Response value is : {response}")
    print("Response : ", response)
    return str(response)

def generate_stream():
    def generate():
        for row in chat():
            yield f"{','.join(row)}\n"
            time.sleep(0.01)  # Simulate some delay in processing
    return app.response_class(generate(), mimetype='text/html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)

    