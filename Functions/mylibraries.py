#Import library
from tvDatafeed import TvDatafeed, Interval
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mplfinance as mpf
import pandas_ta as ta
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
from sklearn.model_selection import ParameterGrid
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

