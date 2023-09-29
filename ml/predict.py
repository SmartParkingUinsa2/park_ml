import pandas as pd

# to do machine learning
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# import warnings filter
from warnings import simplefilter

def predict(hari, jam, area):

    # ignore all future warnings
    simplefilter(action='ignore', category=FutureWarning)

    data = pd.read_csv('dummyParkir.csv')

    # One-hot encode the categorical features
    encoder = OneHotEncoder(sparse=False)
    encoded_features = encoder.fit_transform(data[['hari', 'jam', 'area']])
    feature_names = encoder.get_feature_names_out(input_features=['hari', 'jam', 'area'])

    # Create a DataFrame with the encoded features and label
    encoded_df = pd.DataFrame(encoded_features, columns=feature_names)
    data_encoded = pd.concat([encoded_df, data['jumlah']], axis=1)

    # split to feature (X) and label (y)
    X = data_encoded.drop('jumlah', axis=1)
    y = data_encoded['jumlah']

    # split to train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)

    # build model (linear regression)
    lr = LinearRegression()
    lr.fit(X_train, y_train)

    # # train model
    # y_lr_train_pred = lr.predict(X_train)
    # y_lr_test_pred = lr.predict(X_test)

    # # evaluate model
    # lr_train_mse = mean_squared_error(y_train, y_lr_train_pred)
    # lr_train_r2 = r2_score(y_train, y_lr_train_pred)

    # lr_test_mse = mean_squared_error(y_test, y_lr_test_pred)
    # lr_test_r2 = r2_score(y_test, y_lr_test_pred)

    # result = pd.DataFrame(["Linear Regression", lr_train_mse, lr_train_r2, lr_test_mse, lr_test_r2]).transpose()
    # result.columns = ["Method", "Training MSE", "Training R2", "Test MSE", "Test R2"]
    # result

    # Predict new value
    new_example = pd.DataFrame({'hari_jumat': [0], 'hari_kamis': [0], 'hari_rabu': [0], 'hari_selasa': [0], 'hari_senin': [0],
                                'jam_7.0': [0], 'jam_12.0': [0], 'jam_16.0': [0],
                                'area_Danau': [0], 'area_FISIP': [0], 'area_FPK': [0], 'area_FST': [0], 'area_Masjid': [0]})
    
    # Set the corresponding feature to 1 based on user input
    new_example['hari_' + hari] = 1
    new_example['jam_' + jam] = 1
    new_example['area_' + area] = 1
    
    predicted = lr.predict(new_example)
    final = int(predicted[0])
    return final
    # print(f'Prediksi jumlah: {predicted_price[0]:.2f}')