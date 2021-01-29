from flask import Flask, render_template, request
from sklearn.datasets import load_iris
import model
app = Flask(__name__, template_folder='template', static_folder='static')

@app.route('/', methods=['GET', 'POST'])

def basic():
    if request.method == 'POST':
        sepallength = request.form['sepal_length']
        sepalwidth = request.form['petal_width']
        petallength = request.form['petal_length']
        petalwidth = request.form['petal_width']
        y_pred = [[sepallength, sepalwidth, petallength, petalwidth]]
        trained_model = model.training_model()
        prediction_value = trained_model.predict(y_pred)
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

if __name__ == '__main__':
    app.run(debug=True)