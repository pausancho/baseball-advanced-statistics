#!/usr/bin/env python
# coding: utf-8

# ## Hitting Formulas

# In[2]:


# woba weights - using D3 weights from 2019
bb_w = 0.78
hbp_w = 0.81
h_w = 0.97
do_w = 1.39
tr_w = 1.69
hr_w = 2.02


# woba scale
woba_scale = ((bb_w+hbp_w+h_w+do_w+tr_w+hr_w)/6)

# league runs per plate appearance function
def league_runs_pa(df):
    league_runs = round(df.r/df.ab,3)
    return league_runs

# league woba function
def league_woba(df): 
    l_woba = round((((df.bb*bb_w) + (df.hbp*hbp_w) + (df.h*h_w) + (df["2b"]*do_w) + (df["3b"]*tr_w) + (df.hr*hr_w)) / (df.ab + df.bb + df.sf + df.hbp)),3)
    return l_woba

# individual woba

def individual_woba(df):
    i_woba = round((((df.bb*bb_w) + (df.hbp*hbp_w) + (df.h*h_w) + (df["2b"]*do_w) + (df["3b"]*tr_w) + (df.hr*hr_w)) / (df.ab + df.bb + df.sf + df.hbp)),3)
    return i_woba
    
# wRAA
def wraa_col(df, league_woba, woba_scale):
    wraa = round(((df.wOBA-league_woba)/woba_scale)*df.ab,1)
    return wraa

# wRC
def wrc_col(df, league_woba, woba_scale, league_runs):
    wrc = round((((df.wOBA - league_woba)/woba_scale)+league_runs)*df.ab)
    return wrc

# OPS
def ops_col(df):
    ops = round(((df.h+df.bb+df.hbp)/(df.ab+df.bb+df.sf+df.hbp)) + (((1*df.h)+(2*df["2b"])+(3*df["3b"])+(4*df.hr)) / df.ab),3)
    return ops

# ISO
def iso_col(df):
    iso = round((((df["2b"])+(2*df["3b"])+(3*df.hr))/df.ab),3)
    return iso

# BABIP
def babip_col(df):
    babip = round(((df.h+df["2b"]+df["3b"])-df.hr)/(df.ab-df.so-df.hr+df.sf),3)
    return babip


# ## Pitching Formulas

# In[3]:


# FIP constant
def fip_constant(df):
    C = df.era - (((13*df.hr)+(3*(df.bb+df.hbp))-(2*df.so))/df.ip)
    return C

# FIP
def fip_col(df):
    fip = round((((13*df.hr)+3*(df.bb+df.hbp)-(2*df.so))/df.ip+4.94),2)
    return fip

# DICE
def dice_col(df):
    dice = 3+(13*df.hr+ 3*(df.bb+df.hbp) -2*df.so/df.ip)
    return dice

# Pitcher BABIP
def pitch_babip_col(df):
    pitch_babip = round(((df.h+df["2b"]+df["3b"])-df.hr)/(df.ab-df.so-df.hr),3)
    return pitch_babip
    
# SO/9
def so_9(df):
    so9 = round((df.so/9),2)
    return so9

# BB/9
def bb_9(df):
    bb9 = round((df.bb/9),2)
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
    hr9 = round((df.hr/9),2)
    return hr9

# K%
def k_percentage(df):
    k_percent = round(((df.so/df.ab)*100), 1)
    return k_percent

# BB%
def bb_percentage(df):
    bb_percent = round(((df.bb/df.ab)*100),1)
    return bb_percent
    
# WHIP

def walk_hit(df):
    whip = round(((df.bb+df.h)/df.ip),2)
    return whip

# In[ ]:


#K%-BB% (Strikeout Percentage minus Walk Percentage): The percentage differential between K% and BB%, often a better indicator of performance than K/BB, which can be skewed by very low walk rates.
    

