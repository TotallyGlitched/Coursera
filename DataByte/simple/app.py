from flask import Flask, render_template, request
import pickle
import numpy as np

model = pickle.load(open('iriss.pkl', 'rb'))

app=Flask(__name__, template_folder='template', static_folder='static')

@app.route('/')

def main():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def home():
    if request.method == 'POST':
    
        sepalL = request.form['sepal_length']
        sepalW = request.form['sepal_width']
        petalL = request.form['petal_length']
        petalW = request.form['petal_width']

        array_iris = np.array([[sepalL, sepalW, petalL, petalW]])
        prediction_value = model.predict(array_iris)
        
        setosa = 'The flower is classified as Setosa'
        versicolor = 'The flower is classified as Versicolor'
        virginica = 'The flower is classified as Virginica'
        
        if prediction_value == 0:
            return render_template('index.html', setosa=setosa)
        elif prediction_value == 1:
            return render_template('index.html', versicolor=versicolor)
        else:
            return render_template('index.html', virginica=virginica) 
    
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
    