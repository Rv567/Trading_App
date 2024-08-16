#Import library
from tvDatafeed import TvDatafeed, Interval
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
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
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, GridSearchCV, learning_curve, StratifiedKFold, cross_val_score
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error, f1_score,accuracy_score,classification_report, roc_auc_score,precision_recall_curve,roc_curve, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import ParameterGrid
import shap
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import statsmodels.api as sm

from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG, SMA

import quantstats as qs

from datetime import date

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from IPython.display import display
import warnings
warnings.filterwarnings("ignore")

from tradingview_screener import Query, Column
import yaml
from yaml.loader import SafeLoader
import re

import requests
import os
import sys
import subprocess

