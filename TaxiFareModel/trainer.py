
from TaxiFareModel.utils import compute_rmse
from TaxiFareModel.data import get_data
from TaxiFareModel.data import clean_data

from TaxiFareModel.encoders import DistanceTransformer
from TaxiFareModel.encoders import TimeFeaturesEncoder


from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler



from sklearn.model_selection import train_test_split



# implement set_pipeline() function
def set_pipeline():
    '''returns a pipelined model'''
    dist_pipe = Pipeline([
        ('dist_trans', DistanceTransformer()),
        ('stdscaler', StandardScaler())
    ])
    time_pipe = Pipeline([
        ('time_enc', TimeFeaturesEncoder('pickup_datetime')),
        ('ohe', OneHotEncoder(handle_unknown='ignore'))
    ])
    preproc_pipe = ColumnTransformer([
        ('distance', dist_pipe, ["pickup_latitude", "pickup_longitude", 'dropoff_latitude', 'dropoff_longitude']),
        ('time', time_pipe, ['pickup_datetime'])
    ], remainder="drop")
    pipe = Pipeline([
        ('preproc', preproc_pipe),
        ('linear_model', LinearRegression())
    ])
    return pipe


# implement train() function
def train(X_train, y_train, pipeline):
    '''returns a trained pipelined model'''
    pipeline.fit(X_train, y_train)
    return pipeline


# implement evaluate() function
def evaluate(X_test, y_test, pipeline):
    '''returns the value of the RMSE'''
    y_pred = pipeline.predict(X_test)
    rmse = compute_rmse(y_pred, y_test)
    print(rmse)
    return rmse



class Trainer():

    def __init__(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

    def set_pipeline(self):
        """build pipeline"""
        self.pipeline = set_pipeline()
        return self

    def run(self):
        """train the pipeline"""
        self.set_pipeline()
        train(self.X_train, self.y_train, self.pipeline)
        return self

    def evaluate(self, X_test, y_test):
        return evaluate(X_test, y_test, self.pipeline)


if __name__ == '__main__':
    N = 10_000
    df = get_data(nrows=N)
    df = clean_data(df)
    y = df["fare_amount"]
    X = df.drop("fare_amount", axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    trainer = Trainer(X_train, y_train)
    trainer.run()
    trainer.evaluate(X_test, y_test)
