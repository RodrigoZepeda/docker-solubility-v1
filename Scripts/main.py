# -*- coding: utf-8 -*-
'''
Selects which model files to run
https://github.com/deepchem/deepchem/blob/master/deepchem/models/multitask.py
http://moreisdifferent.com/2017/9/21/DIY-Drug-Discovery-using-molecular-fingerprints-and-machine-learning-for-solubility-prediction/
'''
#TODO transform and undo transforms
import time
import predictchem
import deepchem
from deepchem.models import GraphConvModel
from deepchem.models import WeaveModel
from deepchem.models import MPNNModel
from deepchem.models.sklearn_models import RandomForestRegressor, SklearnModel
import sys

#Docker's working directories
model_dir = "/usr/src/models/"
data_dir = "/data/"
newdir = "model " + time.ctime()

#Models to run are inputed through docker file
models = sys.argv
del models[0] #First argument of list is always the script name
flag_predicted = True   #Flag for running models
print('Running models')

#Predict between different models
if len(models) == 0 or "GraphConv" in models:
    print("-Evaluating Graph Convolution Model")
    predictchem.predict_csv_from_model(
        featurizer = deepchem.feat.ConvMolFeaturizer(),
        transformers = 2,
        modelname = GraphConvModel,
        model_file = model_dir + "graph_convolution",
        dataset_file = '/data/To_predict.csv',
        fname = 'PredictedGraphConvolution.csv',
        parentdir = data_dir,
        newdir = newdir)
    flag_predicted = False;

if len(models) == 0 or "Weave" in models:
    print("-Evaluating Weave Neural Network Model")
    predictchem.predict_csv_from_model(
        featurizer = deepchem.feat.WeaveFeaturizer(),
        transformers = 2,
        modelname = WeaveModel,
        model_file = model_dir + "weave_model",
        dataset_file = data_dir + 'To_predict.csv',
        fname = 'PredictedWeave.csv',
        parentdir = data_dir,
        newdir = newdir)
    flag_predicted = False;

if len(models) == 0 or "DAG" in models:
    print("-Evaluating DAG Model")
    #exec(open("DAGModel.py").read());
    #flag_predicted = False;

if len(models) == 0 or "MPNN" in models:
    print("-Evaluating Message Passing Neural Network Model")
    predictchem.predict_csv_from_model(
        featurizer = deepchem.feat.WeaveFeaturizer(),
        transformers = 2,
        modelname = MPNNModel,
        model_file = model_dir + "mpnn_model",
        dataset_file = data_dir + 'To_predict.csv',
        fname = 'PredictedMPNN.csv',
        parentdir = data_dir,
        newdir = newdir)
    flag_predicted = False;

if len(models) == 0 or "RandomForest" in models:
    print("-Evaluating Random Forest Model")
    predictchem.predict_csv_from_model(
        featurizer = deepchem.feat.CircularFingerprint(size=1024),
        transformers = 2,
        modelname = SklearnModel(model_dir = model_dir + "random_forest"),
        model_file = "", #No need for model_file
        dataset_file = data_dir + 'To_predict.csv',
        fname = 'PredictedForest.csv',
        parentdir = data_dir,
        newdir = newdir,
        modeltype = "sklearn")
    flag_predicted = False;

if len(models) == 0 or "KRR" in models:
    print("-Evaluating Kernel Ridge Regression")
    predictchem.predict_csv_from_model(
        featurizer = deepchem.feat.CircularFingerprint(size=1024),
        transformers = 2,
        modelname = SklearnModel(model_dir = model_dir + "krr_model"),
        model_file = "", #No need for model_file
        dataset_file = data_dir + 'To_predict.csv',
        fname = 'PredictedKRR.csv',
        parentdir = data_dir,
        newdir = newdir,
        modeltype = "sklearn")
    flag_predicted = False;

if flag_predicted:
    sys.exit('ERROR: No adecquate options for models passed to main.py \n' +
    'Please leave empty to run all models:\n' +
    "'docker run --rm -v ~<PATHTODIRECTORY>:/data docker-solubility-v1'" +
    '\nor specify at least one of the following models:' +
    "\n > GraphConv" +
    "\n > Weave" +
    "\n > DAG" +
    "\n > MPNN" +
    "\n > RandomForest"
    "\nand run as:\n"
    "'docker run --rm -v ~<PATHTODIRECTORY>:/data docker-solubility-v1 MODELNAME'")

print('Process finished')
