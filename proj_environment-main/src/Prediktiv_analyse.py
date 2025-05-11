from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def predictive_modeling(df, pollutant_name):
    df["Time Interval"] = pd.to_datetime(df["Time Interval"])
    df = df.set_index("Time Interval").sort_index()

    # Månedlig gjennomsnitt
    monthly = df["Value"].resample("MS").mean().interpolate("time")

    # Konverter dato til numerisk verdi (år + desimal)
    x_years = monthly.index.year + (monthly.index.dayofyear / 365.25)
    X = x_years.reshape(-1, 1)  # Skalert input
    y = monthly.values

    # Split data (valgfritt – f.eks. siste 12 måneder som test)
    split_index = -12
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    # Modell
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Prediksjon og evaluering
    y_pred = model.predict(X_test)

    print(f"--- {pollutant_name} ---")
    print(f"R² score: {r2_score(y_test, y_pred):.3f}")
    print(f"MAE: {mean_absolute_error(y_test, y_pred):.3f}")
    print(f"MSE: {mean_squared_error(y_test, y_pred):.3f}")

    # Fremtidig prediksjon (neste 24 måneder)
    future_years = np.arange(x_years[-1], x_years[-1] + 2, 1/12).reshape(-1, 1)
    future_preds = model.predict(future_years)

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(x_years, y, label='Observations', alpha=0.6)
    plt.plot(X_test.flatten(), y_pred, label='Test Prediction', linestyle='--', color='deeppink')
    plt.plot(future_years.flatten(), future_preds, label='Future Prediction', linestyle='--', color='green')
    plt.xlabel("Year")
    plt.ylabel("Pollutant measure [µg/m^3]")
    plt.title(f"Linear Prediction for {pollutant_name} (sklearn)")
    plt.legend()
    plt.grid()
    plt.show()

    return model, future_years, future_preds

predictive_modeling(NO2, 'NO2')
predictive_modeling(PM25, 'PM2.5')
predictive_modeling(PM10, 'PM10')