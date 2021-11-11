from flask import Flask,request,render_template
import pickle
import pandas as pd

model = pickle.load(open('DT_car.pkl','rb'))

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')



@app.route('/predict',methods=['GET','POST'])
def result():
    if (request.method=="POST"):
        present_price=request.form['presentprice']
        km_driven=request.form['kmdriven']
        make_year=request.form['purchaseyear']
        age_of_car=2021-int(make_year)
        fuel_type=request.form['fueltype']
        transmission_type=request.form['transmissiontype']
        seller_type=request.form['sellertype']

        if seller_type == 'Dealer':
            seller_individual = 0
        else:
            seller_individual = 1

        if transmission_type == 'Manual':
            trans_manual = 1
        else:
            trans_manual = 0

        if fuel_type == 'Petrol':
            fuel_type_petrol = 1
            fuel_type_diesel = 0

        elif fuel_type == 'Diesel':
            fuel_type_petrol = 0
            fuel_type_diesel = 1

        else:
            fuel_type_petrol = 0
            fuel_type_diesel = 0

        prediction = model.predict(pd.DataFrame([present_price, km_driven, age_of_car, fuel_type_diesel, fuel_type_petrol, seller_individual,trans_manual]).T.values)
        result=round(prediction[0])

        return render_template('results.html',result=result)


if __name__ == '__main__':
    app.run(debug=True)