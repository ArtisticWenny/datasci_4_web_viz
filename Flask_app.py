# import packages
from io import BytesIO
import base64
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import pandas as pd

#import file
df = pd.read_csv('/content/drive/MyDrive/HHS_Provider_Relief_Fund.csv')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        state = request.form['state']

        df_filtered = df[df['state'] == state]

        fig, ax = plt.subplots()
        ax.bar(df_filtered['measure'], df_filtered['value'])
        ax.set_title('Measure Values by State')

        buf = BytesIO()
        plt.savefig(buf, format='png')

        image_data = base64.b64encode(buf.getvalue()).decode('utf-8')

        return render_template('index.html', image_data=image_data)
    else:
        return render_template('index.html', image_data=None)

# HTML 
<!DOCTYPE html>
<html>
<head>
    <title>HHS_Provider_Relief_Fund</title>
</head>
<body>
    <h1>HHS_Provider_Relief_Fund</h1>

    <form action="/" method="post">
        <select name="state">
            <option value="NY">New York</option>
            <option value="TX">Texas</option>
            <option value="CA">California</option>
        </select>

        <input type="submit" value="Submit">
    </form>

    <img src="data:image/png;base64,{{ image_data }}" alt="Measure Values by State">
</body>
</html>


app.run(debug=True)

