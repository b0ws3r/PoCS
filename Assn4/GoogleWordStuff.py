import pandas
import pandas as pd  # To read data
import scipy

from Monktools import statstools, plottools
import numpy


def ccdf(df, y):
    # PDF
    df['pdf'] = df[y] / sum(df[y])

    # CDF
    df['cdf'] = df['pdf'].cumsum()
    df = df.reset_index()
    df['ccdf'] = numpy.ones(len(df['cdf'])) - df['cdf']
    return df


def Q1_Q2():
    ## QUESTION 1
    # Get data from CSV
    dataframe = statstools.get_dataframe('Data/vocab_cs_mod.csv')

    dataframe = dataframe.sort_values(by=['k'])

    # dataframe['ccdf'] = arr.tolist()
    # NEW CCDF attempt
    dataframe = ccdf(dataframe, 'N')

    loggified_df = statstools.get_logs_2axes(dataframe, 'k', 'ccdf')
    plottools.plot_results(loggified_df, 'k_log', 'ccdf_log', 'CCDF of Word Frequencies')
    #################################################################################################
    ## QUESTION 2
    # Measure gamma-1 where gamma is the exponent of the underlying dist.
    threshold = 6.8
    # k_log <
    filter_lt = statstools.get_filter_lt(loggified_df, 'k_log', threshold)
    linear_reg_items_1 = statstools.get_linear_regression(filter_lt, 'k_log', 'ccdf_log')
    plottools.plot_results_with_fit(filter_lt, 'k_log', 'ccdf_log', 'log_10(k)<' + str(threshold), linear_reg_items_1[0])


    print('coef for less than ' + str(threshold) + '-> ' + str(linear_reg_items_1[2]))
    g_1 = -1 * linear_reg_items_1[2]

    # k_log >
    filter_gt = statstools.get_filter_gt(loggified_df, 'k_log', threshold)
    linear_reg_items_2 = statstools.get_linear_regression(filter_gt, 'k_log', 'ccdf_log')
    plottools.plot_results_with_fit(filter_gt, 'k_log', 'ccdf_log', 'log_10(k)>' + str(threshold), linear_reg_items_2[0])
    print('coef for greater than ' + str(threshold) + '-> ' + str(linear_reg_items_2[2]))
    g_2 = -1 * linear_reg_items_2[2]

    ## TODO report 95% confidence interval!
    return g_1, g_2


#################################################################################################
## QUESTION 3
def Q3_Q4_Q5():
    gammas = Q1_Q2()

    raw_dataframe = statstools.get_dataframe('Data/rawwwordfreqs.csv')
    raw_dataframe['rank'] = raw_dataframe.index.tolist()
    samplerange = numpy.arange(0, 7, 0.001)
    subsample = set(numpy.around((10**samplerange)))
    raw_dataframe = statstools.get_filter_in(raw_dataframe, 'rank', subsample)
    loggy = statstools.get_logs_2axes(raw_dataframe, 'rank', 'k')
    plottools.plot_results(loggy, 'rank_log', 'k_log', 'Zipf plot of word frequencies')

    ## rank < 10 fit
    threshold = 10
    filter_lt = statstools.get_filter_lt(loggy, 'rank', threshold)
    linear_reg_items_1 = statstools.get_linear_regression(filter_lt, 'rank_log', 'k_log')
    plottools.plot_results_with_fit(filter_lt, 'rank_log', 'k_log', 'log_10(k)<' + str(threshold), linear_reg_items_1[0])
    print('coef for less than 10' + str(threshold) + '-> ' + str(linear_reg_items_1[2]))
    a_1 = -1 * linear_reg_items_1[2]
    ## rank > 10 fit
    filter_gt = statstools.get_filter_gt(loggy, 'rank', threshold)
    linear_reg_items_2 = statstools.get_linear_regression(filter_gt, 'rank_log', 'k_log')
    plottools.plot_results_with_fit(filter_gt, 'rank_log', 'k_log', 'log_10(k)>' + str(threshold), linear_reg_items_2[0])
    print('coef for greater than ' + str(threshold) + ' -> ' + str(linear_reg_items_2[2]))
    ## TODO report 95% confidence interval!
    a_2 = -1 * linear_reg_items_2[2]

    print('transformed_gamma_1: ' + str(1/(gammas[0]-1)) + '\nexpected alpha: ' + str(a_1))
    print('transformed_gamma_2: ' + str(1/(gammas[1]-1)) + '\nexpected alpha: ' + str(a_2))


#################################################################################################
## QUESTION 6

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * numpy.array(data)
    n = len(a)
    m, se = numpy.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h


def zipf(dataframe, yvalue, title):
    dataframe['rank'] = dataframe[yvalue].rank(ascending=False)
    loggified_df = statstools.get_logs_1axis(dataframe, 'rank')
    plottools.plot_results(loggified_df, 'rank_log', yvalue + '_log', 'Zipf plot for' + title)
    return loggified_df


def get_name_ccdf_and_zipf_data(path, title):
    # for ccdf, x is times it appeared, N is number of names appearing those times
    dataframe = statstools.get_dataframe(path)
    kNamesAppearingNTimes = dataframe['Frequency'].value_counts(sort=True)
    k_vs_n = kNamesAppearingNTimes.rename_axis('k').reset_index(name='N')
    k_vs_n = statstools.get_logs_2axes(k_vs_n, 'k', 'N')
    k_vs_n = k_vs_n.sort_values(by=['k'])
    ccdfed = ccdf(k_vs_n, 'N')
    statstools.get_logs_1axis(ccdfed, 'ccdf')
    plottools.plot_results(ccdfed, 'k_log', 'ccdf_log', 'CCDF: ' + title)

    dataframe = statstools.get_logs_1axis(dataframe, 'Frequency')
    zipfed = zipf(dataframe, 'Frequency', title)
    return ccdfed, zipfed

def get_and_plot_fit_for_threshold(df, x, y, title, threshold):
    filter_lt = statstools.get_filter_lt(df, x, threshold)
    linear_reg_items_1 = statstools.get_linear_regression(filter_lt, x, y)
    plottools.plot_results_with_fit(filter_lt, x, y, title + ': ' + x + '<' + str(threshold),
                                    linear_reg_items_1[0])
    print('coef for less than ' + str(threshold) + '-> ' + str(linear_reg_items_1[2]))
    g_1 = -1 * linear_reg_items_1[2]

    #TODO
    # confidence_interval = mean_confidence_interval(filter_lt['ccdf_log'], 0.95)
    # print(confidence_interval)

    # k_log >
    filter_gt = statstools.get_filter_gt(df, x, threshold)
    linear_reg_items_2 = statstools.get_linear_regression(filter_gt, x, y)
    plottools.plot_results_with_fit(filter_gt, x, y, title + ': ' + x + '>' + str(threshold),
                                    linear_reg_items_2[0])
    print('coef for greater than ' + str(threshold) + '-> ' + str(linear_reg_items_2[2]))
    g_2 = -1 * linear_reg_items_2[2]
    return g_1, g_2

def compare_gammas_to_alphas(gammas, alphas, title):
    print('###################################################################')
    print(title)
    print('transformed_gamma_1: ' + str(1/(gammas[0]-1)) + '\nexpected alpha: ' + str(alphas[0]))
    print('transformed_gamma_2: ' + str(1/(gammas[1]-1)) + '\nexpected alpha: ' + str(alphas[1]))
    print('###################################################################')


Q3_Q4_Q5()
title = 'Girl''s names in 1952'
g1952 = get_name_ccdf_and_zipf_data('Data/names-girls1952.csv', title)
ccdffit = get_and_plot_fit_for_threshold(g1952[0], 'k_log', 'N_log', "CCDF: " + title, 4.2)
zipffit = get_and_plot_fit_for_threshold(g1952[1], 'rank_log', 'Frequency_log', "Zipf: " + title, 1.25)
compare_gammas_to_alphas(ccdffit, zipffit, title)

title = 'Boy''s names in 1952'
b1952 = get_name_ccdf_and_zipf_data('Data/names-boys1952.csv', title)
ccdffit = get_and_plot_fit_for_threshold(b1952[0], 'k_log', 'N_log', title, 4.2)
zipffit = get_and_plot_fit_for_threshold(b1952[1], 'rank_log', 'Frequency_log', title, 1)
compare_gammas_to_alphas(ccdffit, zipffit, title)

title = 'Girl''s names in 2002'
g2002 = get_name_ccdf_and_zipf_data('Data/names-girls2002.csv', title)
ccdffit = get_and_plot_fit_for_threshold(g2002[0], 'k_log', 'N_log', title, 3.7)
zipffit = get_and_plot_fit_for_threshold(g2002[1], 'rank_log', 'Frequency_log', title, 1.2)
compare_gammas_to_alphas(ccdffit, zipffit, title)

title = 'Boy''s names in 2002'
b2002 = get_name_ccdf_and_zipf_data('Data/names-boys2002.csv', title)
ccdffit = get_and_plot_fit_for_threshold(b2002[0], 'k_log', 'N_log', title, 4.2)
zipffit = get_and_plot_fit_for_threshold(b2002[1], 'rank', 'Frequency', title, 1.3)
compare_gammas_to_alphas(ccdffit, zipffit, title)

