from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MultiLabelBinarizer
import sklearn.metrics as metricas
param_grid = [{
    'hidden_layer_sizes': [(10,8),(6,4),(8,2),(6,2)],
    'activation': ['identity', 'logistic', 'tanh', 'relu'],
    'solver': ['lbfgs','sgd','adam'],
    'alpha':[0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000],
    'learning_rate':['constant', 'invscaling', 'adaptive']
}]



def rodarGridCV(X, Y):
    mlb = MultiLabelBinarizer()
    Ybin = mlb.fit_transform(Y)
    x_train, x_test, y_train, y_test = train_test_split(X, Ybin, test_size=0.33)
    reg = GridSearchCV(MLPClassifier(),param_grid, cv=5, n_jobs=4, refit='accuracy')
    reg.fit(x_train,y_train)
    scores_list = []
    #for params, mean_score, scores in reg.grid_scores:
    #    scores_list.append({'Média de Score': mean_score, 'Desvio Score': scores.std, 'Params': params})
    return {'Melhores parâmetros': reg.best_params_,
                'Melhor Score': reg.best_score_,
            'Resultados':reg.cv_results_}

