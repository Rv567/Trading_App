#Import library
from tvDatafeed import TvDatafeed, Interval
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mplfinance as mpf
import random
import pickle
from functools import reduce
from statsmodels.tsa.seasonal import STL
from collections import Counter
import time
from xgboost import XGBRegressor, plot_importance,XGBClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, learning_curve, StratifiedKFold, cross_val_score
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error, f1_score,accuracy_score,classification_report, roc_auc_score,precision_recall_curve,roc_curve, confusion_matrix
from sklearn.preprocessing import StandardScaler
import optuna
import shap
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import statsmodels.api as sm

from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG, SMA


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from IPython.display import display
import warnings
warnings.filterwarnings("ignore")


import requests
import os
import sys
import subprocess

# check if the library folder already exists, to avoid building everytime you load the pahe
if not os.path.isdir("/tmp/ta-lib"):

    # Download ta-lib to disk
    with open("/tmp/ta-lib-0.4.0-src.tar.gz", "wb") as file:
        response = requests.get(
            "http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz"
        )
        file.write(response.content)
    # get our current dir, to configure it back again. Just house keeping
    default_cwd = os.getcwd()
    os.chdir("/tmp")
    # untar
    os.system("tar -zxvf ta-lib-0.4.0-src.tar.gz")
    os.chdir("/tmp/ta-lib")
    # build
    os.system("./configure --prefix=/home/appuser/venv/")
    os.system("make")
    # install
    os.system("mkdir -p /home/appuser/venv/")
    os.system("make install")
    os.system("ls -la /home/appuser/venv/")
    # back to the cwd
    os.chdir(default_cwd)
    sys.stdout.flush()

# add the library to our current environment
from ctypes import *

lib = CDLL("/home/appuser/venv/lib/libta_lib.so.0.0.0")
# import library
try:
    import talib
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--global-option=build_ext", "--global-option=-L/home/appuser/venv/lib/", "--global-option=-I/home/appuser/venv/include/", "ta-lib==0.4.24"])
finally:
    import talib as ta