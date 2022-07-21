from pymongo import MongoClient

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    new_list = []
    client = MongoClient()
    db = client.variables
    variables = db.variables
    cursor = variables.find({})
    # print(variables)
    for doc in cursor:
        message = ''
        symbol = doc['symbol']
        fiveMinSuccess =  doc['values']["5MIN"]['success']
        fiveMinBlackX =  doc['values']["5MIN"]['black_x']
        fiveMinPrice =  doc['values']["5MIN"]['price']
        fiveMinMa =  doc['values']["5MIN"]['ma']
         
        fifteenMinSuccess = doc['values']["15MIN"]['success']
        fifteenMinBlackX = doc['values']["15MIN"]['black_x']
        fifteenMinPrice =  doc['values']["15MIN"]['price']
        fifteenMinMa =  doc['values']["15MIN"]['ma']

        oneHourSuccess = doc['values']["1HRS"]['success']
        oneHourBlackX = doc['values']["1HRS"]['black_x']
        oneHourPrice =  doc['values']["1HRS"]['price']
        oneHourMa =  doc['values']["1HRS"]['ma']

        fourHourSuccess = doc['values']["4HRS"]['success']
        fourHourBlackX = doc['values']["4HRS"]['black_x']
        fourHourPrice =  doc['values']["4HRS"]['price']
        fourHourMa =  doc['values']["4HRS"]['ma']

        oneDaySuccess = doc['values']["1DAY"]['success']
        oneDayBlackX = doc['values']["1DAY"]['black_x']
        oneDayPrice =  doc['values']["1DAY"]['price']
        oneDayMa =  doc['values']["1DAY"]['ma']
        
        new_dict = {"symbol": symbol, "fiveMin": f"{fiveMinSuccess}/{fiveMinBlackX}     {calculate_difference(fiveMinPrice, fiveMinMa)}", "fifteenMin": f"{fifteenMinSuccess}/{fifteenMinBlackX}  {calculate_difference(fifteenMinPrice, fifteenMinMa)}", "oneHour": f"{oneHourSuccess}/{oneHourBlackX}    {calculate_difference(oneHourPrice, oneHourMa)}", "fourHour": f"{fourHourSuccess}/{fourHourBlackX}   {calculate_difference(fourHourPrice, fourHourMa)}", "oneDay": f"{oneDaySuccess}/{oneDayBlackX}    {calculate_difference(oneDayPrice, oneDayMa)}"}
        new_list.append(new_dict)
        print(new_list)
    return jsonify(new_list)


def calculate_difference(price, ma) -> str:
    up = '↗'
    down = '↘'
    if price > ma:
        return up
    return down


app.run(debug=True)
