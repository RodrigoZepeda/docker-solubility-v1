# -*- coding: utf-8 -*-
"""
Functions for predicting expected solubility
Rodrigo Zepeda

Adapted from:
https://github.com/PatWalters/solubility/blob/master/solubility_comparison.py
"""

import pandas as pd
import sys
import warnings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' #Hide tensorflow warnings

#Importing deepchem throws a numpy warning
sys.stderr = None            # suppress deprecation warning
import deepchem as dc
sys.stderr = sys.__stderr__  # restore stderr

from deepchem.models import GraphConvModel
from deepchem.utils.save import load_from_disk
from rdkit import Chem

def load_model(modelname, model_file):
    #Read model file
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore",category=UserWarning)
            model = modelname.load_from_dir(model_file)
    except:
        sys.exit('Unable to find' + modelname + ' at ' + model_file)
    return model

def load_data(dataset_file, smiles_column = "Smiles"):
    #Read dataset to predict
    try:
        newsmiles = pd.read_csv(dataset_file)
    except:
        sys.exit('Unable to read ' + dataset_file + 'from "/data" directory')

    #Search for smiles column
    try:
        mols = [Chem.MolFromSmiles(s) for s in newsmiles.loc[:,smiles_column]]
    except:
        sys.exit('Unable to read ' + smiles_column + ' column from ' + dataset_file)

    return newsmiles, mols

def predict_from_mols(featurizer, transformers, mols, model, molnames):

    #Featurize data
    ftdata = featurizer.featurize(mols)

    #Predict data
    #TODO add transfoemrs
    predicted_solubility = model.predict_on_batch(ftdata)

    #Convert to dataframe
    mydf = pd.concat([molnames, pd.DataFrame(predicted_solubility)], axis = 1)
    mydf.columns = ["Smile","Predicted Solubility"]

    return mydf

def write_to_csv(fname, mydir, mydf):

    #Write dataset
    try:
        mydf.to_csv(mydir + fname, index=False)
        print('Model saved as "' + fname + '" on "' + mydir + '" directory')
    except:
        sys.exit('Unable to save "' + fname + '" on "' + mydir + '" directory')

    return 0

def predict_csv_from_model(featurizer, transformers, modelname, model_file, dataset_file, fname, smiles_column = 'Smiles', mydir = '/data/'):

    #Load model
    model = load_model(modelname, model_file)

    #Load data
    newsmiles, mols = load_data(dataset_file, smiles_column)

    #Predict dataset
    predict_df = predict_from_mols(featurizer, transformers, mols, model, newsmiles)

    #Write to csv
    write_to_csv(fname, mydir, predict_df)

    return 0