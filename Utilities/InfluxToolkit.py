import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

localToken = os.environ.get("INFLUX_TOKEN")
orgId = os.environ.get("INFLUX_ORG_ID_LOCAL")

headers = {
    "Authorization": f"Token {localToken}",
    "Content-Type": "application/vnd.flux",
}
params = {
    'orgID': f'{orgId}',
}


def make_influx_query(startDate, endDate, tags, vehicle_id):
    query_template = 'r["_field"] == "{}"'
    
    tag_queries = [query_template.format(tag) for tag in tags]
    tag_query_str = " or ".join(tag_queries)
    
    influx_query = f"""
    from(bucket: "digitaltwin")
      |> range(start: {startDate}T00:00:00Z, stop: {endDate}T00:00:00Z)
      |> filter(fn: (r) => r["_measurement"] == "telemetry")
      |> filter(fn: (r) => {tag_query_str})
      |> filter(fn: (r) => r["id"] == "{vehicle_id}")
      |> aggregateWindow(every: 1s, fn: mean, createEmpty: false)
      |> yield(name: "mean")
    """
    
    return influx_query


def makeDataframe(response):
    data = response.text
    rows = data.strip().split('\r\n')
    values = [row.split(',') for row in rows]
    df = pd.DataFrame(values[1:], columns=values[0])
    df = df[['_time', '_field', '_value']]
    df = df.pivot(index='_time', columns='_field', values='_value').reset_index()
    df['_time'] = pd.to_datetime(df['_time'])
    df.set_index('_time', inplace=True, drop=True)
    
    for c in list(df.columns):
        df[c] = df[c].apply(lambda x:float(x))
    return df

def queryInflux(startDate, endDate, vehicle_id, tags):
    influx_query = make_influx_query(startDate, endDate,tags, vehicle_id)
    
    response = requests.post("http://localhost:8086/api/v2/query", params=params, headers=headers, data=influx_query)
    
    dfi = makeDataframe(response).dropna()
    
    return dfi


def plotCorrelationMatrix(df):
    correlation_matrix = df.corr()
    plt.figure(figsize=(6, 4))  # Set the figure size (optional)
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.show()

def trainModel(df):
    tags = list(df.columns)
    features = [t for t in tags if t != 'EngineLoad']
    X = df[features]
    y = df['EngineLoad']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    coefficients = model.coef_
    c_d = {key: value for key, value in zip(features, coefficients)}

    model_result = {
        "Scores":{"MSE":mse,"R2":r2},
        "Intercept":model.intercept_,
        "Coefficients":c_d
    }
    
    return model_result