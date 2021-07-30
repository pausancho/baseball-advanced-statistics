#!/usr/bin/env python
# coding: utf-8

# ## Hitting Formulas

# In[2]:


# woba weights - using D3 weights from 2019
bb_w = 0.78
hbp_w = 0.81
s_w = 0.97 # single
do_w = 1.39 # double
tr_w = 1.69 # triple
hr_w = 2.02 # homerun


# woba scale
woba_scale = ((bb_w+hbp_w+s_w+do_w+tr_w+hr_w)/6)

# league runs per plate appearance function
def league_runs_pa(df):
    league_runs = round(df.r/df.pa,3)
    return league_runs

# league woba function
def league_woba(df): 
    l_woba = round((((df.bb*bb_w) + (df.hbp*hbp_w) + (df["1b"]*s_w) + (df["2b"]*do_w) + (df["3b"]*tr_w) + (df.hr*hr_w)) / (df.ab + df.bb + df.sf + df.hbp)),3)
    return l_woba

# individual woba

def individual_woba(df):
    try:
        i_woba = round((((df.bb*bb_w) + (df.hbp*hbp_w) + (df["1b"]*s_w) + (df["2b"]*do_w) + (df["3b"]*tr_w) + (df.hr*hr_w)) / (df.ab + df.bb + df.sf + df.hbp)),3)
    except ZeroDivisionError:
        i_woba = 0.0
    return i_woba
    
# wRAA
def wraa_col(df, league_woba, woba_scale):
    try:
        wraa = round(((df.wOBA-league_woba)/woba_scale)*df.ab,1)
    except ZeroDivisionError:
        wraa = 0.0
    return wraa

# wRC
def wrc_col(df, league_woba, woba_scale, league_runs):
    try:
        wrc = round((((df.wOBA - league_woba)/woba_scale)+league_runs)*df.ab)
    except ZeroDivisionError:
        wrc = 0.0
    return wrc

# OPS
def ops_col(df):
    try:
        ops = round(((df.h+df.bb+df.hbp)/(df.ab+df.bb+df.sf+df.hbp)) + (((1*df["1b"])+(2*df["2b"])+(3*df["3b"])+(4*df.hr)) / df.ab),3)
    except ZeroDivisionError:
        ops = 0.0
    return ops

# ISO
def iso_col(df):
    try:
        iso = round((((df["2b"])+(2*df["3b"])+(3*df.hr))/df.ab),3)
    except ZeroDivisionError:
        iso = 0.0
    return iso

# BABIP
def babip_col(df):
    try:
        babip = round(((df.h)-df.hr)/((df.ab-df.so-df.hr)+df.sf),3)
    except ZeroDivisionError: 
        babip = 0.0    
    return babip

# ## Pitching Formulas

# In[3]:


# FIP constant
def fip_constant(df):
    try:
        C = df.era - (((13*df.hr)+(3*(df.bb+df.hbp))-(2*df.so))/df.ip)
    except ZeroDivisionError:
         C = 0.0
    return C

# FIP
def fip_col(total_df, df):
    C = total_df.era - (((13*total_df.hr)+(3*(total_df.bb+total_df.hbp))-(2*total_df.so))/total_df.ip)
    try:
        fip = round((((13*df.hr)+3*(df.bb+df.hbp)-(2*df.so))/df.ip+C),2)
    except ZeroDivisionError:
        fip = 0.0
    return fip

# DICE
def dice_col(df):
    try:
        dice = 3+(13*df.hr+ 3*(df.bb+df.hbp) -2*df.so/df.ip)
    except ZeroDivisionError:
        dice = 0.0
    return dice

# Pitcher BABIP
def pitch_babip_col(df):
    try:
        pitch_babip = round(((df["1b"]+df["2b"]+df["3b"])-df.hr)/(df.ab-df.so-df.hr),3)
    except ZeroDivisionError:
        pitch_babip = 0.0
    return pitch_babip
    
# SO/9 - divide strikeout totals by his innings pitched total and multiplying the result by nine
def so_9(df):
    try:
        so9 = round((df.so/df.ip)*9,2)
    except ZeroDivisionError:
        so9 = 0.0
    return so9

# BB/9
def bb_9(df):
    try:
        bb9 = round((df.bb/df.ip)*9,2)
    except ZeroDivisionError:
        bb9 = 0.0
    return bb9

# K/BB
def k_bb(df):
    try:
        kbb = round((df.so/df.bb),2)
    except ZeroDivisionError:
        kbb = 0.0
    return kbb

# HR/9
def hr_9(df):
    try:
        hr9 = round((df.hr/df.ip)*9,2)
    except ZeroDivisionError:
        hr9 = 0.0
    return hr9

# K% 
def k_percentage(df):
    try:
        k_percent = round(((df.so/df.pa)*100), 1)
    except ZeroDivisionError:
        k_percent = 0.0
    return k_percent

# BB%
def bb_percentage(df):
    try:
        bb_percent = round(((df.bb/df.pa)*100),1)
    except ZeroDivisionError:
        bb_percent = 0.0
    return bb_percent
    
# WHIP

def walk_hit(df):
    try:
        whip = round(((df.bb+df.h)/df.ip),2)
    except ZeroDivisionError:
        whip = 0.0
    return whip

# In[ ]:


#K%-BB% (Strikeout Percentage minus Walk Percentage): The percentage differential between K% and BB%, often a better indicator of performance than K/BB, which can be skewed by very low walk rates.
    

