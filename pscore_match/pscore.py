"""
Implements several propensity score estimation, balance diagnostics for 
group characteristics, average treatment effect on the treated (ATT) estimates, 
and bootstraping to estimate standard errors of the estimated ATT.
"""

from __future__ import division
import numpy as np
import scipy
from scipy.stats import binom, hypergeom, gaussian_kde
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

################################################################################
##################### Base Propensity Score Class ##############################
################################################################################

class PropensityScore(object):
    """
    doc
    """

    def __init__(self, treatment, covariates):
        """
        Parameters
        -----------        
        treatment : array-like
            binary treatment assignment
        covariates : pd.DataFrame
            covariates, one row for each observation
        """
        assert treatment.shape[0]==covariates.shape[0], 'Number of observations in \
            treated and covariates doesnt match'
        self.treatment = treatment
        self.covariates = covariates
        
    def compute(self, method='logistic'):
        """
        Compute propensity score and measures of goodness-of-fit
        
        Parameters
        ----------
        
        """
        ####### Using LogisticRegression from sklearn.linear_model    
        #propensity = LogisticRegression()
        #propensity.fit(predictors, groups)
        #return propensity.predict_proba(predictors)[:,1]
    
        ####### Using sm.GLM
        predictors = sm.add_constant(self.covariates, prepend=False)
        if method == 'logistic':
            model = sm.Logit(self.treatment, predictors).fit(disp=False, warn_convergence=True)
        elif method == 'probit':
            model = sm.Probit(self.treatment, predictors).fit(disp=False, warn_convergence=True)
        else:
            raise ValueError('Unrecognized method')
        return model.predict()

        ####### Using sm.formula.glm with formula call
        #glm_binom = sm.formula.glm(formula = formula, data = data, family = sm.families.Binomial())
        #res = glm_binom.fit()
        #if verbosity:
        #    print res.summary()
        #return res.fittedvalues