import os
import pandas as pd
import valentine
from valentine import valentine_match, valentine_metrics
from valentine.algorithms import Coma
import pprint

def match_ground_truth(df1, df2, ground_truth):
    matcher = Coma(max_n=1, strategy="COMA_OPT_INST", java_xmx="4g")
    matches_coma_inst = valentine_match(df1, df2, matcher)
    
    matcher = Coma(strategy="COMA_OPT", java_xmx="4g")
    matches_coma = valentine_match(df1, df2, matcher)

    matcher = valentine.algorithms.Cupid(th_accept=0.8)
    matches_cupid = valentine_match(df1, df2, matcher)
    
    matcher = valentine.algorithms.DistributionBased()
    matches_distri = valentine_match(df1, df2, matcher)
    
    matcher = valentine.algorithms.JaccardLevenMatcher()
    matches_jaccard = valentine_match(df1, df2, matcher)
    
    matcher = valentine.algorithms.SimilarityFlooding()
    matches_simflooding = valentine_match(df1, df2, matcher)
    
    metrics_coma_inst = valentine_metrics.all_metrics(matches_coma_inst, ground_truth)
    metrics_coma = valentine_metrics.all_metrics(matches_coma, ground_truth)
    metric_cupid = valentine_metrics.all_metrics(matches_cupid, ground_truth)
    metric_distri = valentine_metrics.all_metrics(matches_distri, ground_truth)
    metric_jaccard = valentine_metrics.all_metrics(matches_jaccard, ground_truth)
    metric_simflooding = valentine_metrics.all_metrics(matches_simflooding, ground_truth)
    
    print("These are the scores of the matcher COMA INST:")
    print(metrics_coma_inst)
    
    print("These are the scores of the matcher COMA:")
    print(metrics_coma)
    
    print("These are the scores of the matcher CUPID:")
    print(metric_cupid)
    
    print("These are the scores of the matcher DISTRIBUTION:")
    print(metric_distri)
    
    print("These are the scores of the matcher JACCARD:")
    print(metric_jaccard)
    
    print("These are the scores of the matcher SIMILARITY FLOODING:")
    print(metric_simflooding)
    
def match_schema(df1, schema):
    matcher = Coma(max_n=1, strategy="COMA_OPT_INST", java_xmx="4g")
    matches_coma_inst = valentine_match(df1, schema, matcher)
    
    matcher = Coma(strategy="COMA_OPT", java_xmx="4g")
    matches_coma = valentine_match(df1, schema, matcher)

    print("These are the matches of the matcher COMA INST:")
    print(matches_coma_inst)
    
    print("These are the matches of the matcher COMA:")
    print(matches_coma)
    
def main():
    # mediated schema
    schema_path = os.path.join('', 'training.csv')
    schema = pd.read_csv(schema_path, encoding = "ISO-8859-1")

    # load forbes.com.csv
    d1_path = os.path.join('datasets', 'famcap_germany.csv', )
    df1 = pd.read_csv(d1_path, encoding = "ISO-8859-1")
    
    # Ground truth to let valentine calculate the metrics
    # id,name,code,website,headquarter,country,ceo,founded,employees,
    # market_value,market_cap,annual_revenue,business
    ground_truth = [
                    ("Company", "name"),
                    ("Revenues 2018 $m", "annual_revenue"),
                    ("Employees", "employees"),
                    ("Founded", "founded"),
                    ("Sector", "business"),
                    ("Headquarters", "headquarter"),
                    ("State (abbreviation)", "country"),
                    ("Website", "website")]
    
    print("Matching dataset famcap_germany.csv:")
    match_all(df1, schema, ground_truth)
    #match_schema(df1, schema)
    
if __name__ == '__main__':
    main()