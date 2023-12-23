from flask import Flask, request
from quotation.OrderBooks import OrderBooks

app = Flask(__name__)


@app.route('/quotation/orderBooks', methods=["post"])
def drape_order():
    data = request.json
    return OrderBooks.drape_order_book(**data)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
