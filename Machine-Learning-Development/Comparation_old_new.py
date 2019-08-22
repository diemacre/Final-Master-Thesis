import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#old_results = pd.read_csv('./Datasets/ML_trained/Building_31/floor_1.0/results/database_test_parametric_equations.csv')

#linear_1_not_filter = pd.read_csv('./Datasets/ML_trained/Building_31/floor_1.0/results/results_linear_1_no_filter.csv')

GB_1_not_filter = pd.read_csv('./Datasets/ML_trained/Building_31/floor_1.0/results/results_GB_1_no_filter.csv')
GB_1_not_filter_optim_param = pd.read_csv('./Datasets/ML_trained/Building_31/floor_1.0/results/results_GB_1_no_filter_optimized_param.csv')

RF_1_not_filter = pd.read_csv('./Datasets/ML_trained/Building_31/floor_1.0/results/results_RF_1_no_filter.csv')
RF_1_not_filter_optim_param = pd.read_csv('./Datasets/ML_trained/Building_31/floor_1.0/results/results_RF_1_no_filter_optimized_param.csv')

outliers_parametric_eq = pd.read_csv('./Datasets/ML_trained/Building_31/floor_1.0/results/EXTRA_database_test_parametric_equations.csv')
outliers_GBR = pd.read_csv('./Datasets/ML_trained/Building_31/floor_1.0/results/EXTRA_results_GB_1_no_filter_optimized_param.csv')


'''
print('Max error old:', old_results['xy_error'].max())
print('Mean error old:', old_results['xy_error'].mean())
print('Description old:', old_results['xy_error'].describe(
    percentiles=[.5, .75, .9]))
'''


print('--------------------------------')

print('Max error GB_1_not_filter:', GB_1_not_filter['error'].max())
print('Mean error GB_1_not_filter:', GB_1_not_filter['error'].mean())
print('Description GB_1_not_filter:',GB_1_not_filter['error'].describe(percentiles=[.5, .75, .9]))

print('--------------------------------')

print('Max error GB_1_not_filter optimized:', GB_1_not_filter_optim_param['error'].max())
print('Mean error GB_1_not_filter optimized:',GB_1_not_filter_optim_param['error'].mean())
print('Description GB_1_not_filter optimized:',GB_1_not_filter_optim_param['error'].describe(percentiles=[.5, .75, .9]))

print('--------------------------------')

print('Max error RF_1_not_filter:', RF_1_not_filter['error'].max())
print('Mean error RF_1_not_filter:', RF_1_not_filter['error'].mean())
print('Description RF_1_not_filter:',RF_1_not_filter['error'].describe(percentiles=[.5, .75, .9]))

print('--------------------------------')

print('Max error RF_1_not_filter optimized:',RF_1_not_filter_optim_param['error'].max())
print('Mean error RF_1_not_filter optimized:',RF_1_not_filter_optim_param['error'].mean())
print('Description RF_1_not_filter optimized:', RF_1_not_filter_optim_param['error'].describe(percentiles=[.5, .75, .9]))


print('--------------------------------')

print('Max error Outliers Param EQ:', outliers_parametric_eq['xy_error'].max())
print('Mean error Outliers Param EQ:',outliers_parametric_eq['xy_error'].mean())
print('Description Outliers Param EQ:',outliers_parametric_eq['xy_error'].describe(percentiles=[.5, .75, .9]))

print('--------------------------------')

print('Max error Outliers GBR:',outliers_GBR['error'].max())
print('Mean error Outliers GBR:', outliers_GBR['error'].mean())
print('Description Outliers GBR:',outliers_GBR['error'].describe(percentiles=[.5, .75, .9]))


plt.subplot(2,2,1)
plt.hist(np.array(GB_1_not_filter['error']), bins=20)
plt.ylabel('Number of tests')
plt.xlabel('Error in meters')
plt.title('Error distribution - Gradient Boosting (no opt)')

plt.subplot(2, 2, 2)
plt.hist(np.array(GB_1_not_filter_optim_param['error']), bins=20)
plt.ylabel('Number of tests')
plt.xlabel('Error in meters')
plt.title('Error distribution - Gradient Boosting (opt)')

plt.subplot(2, 2, 3)
plt.hist(np.array(RF_1_not_filter['error']), bins=20)
plt.ylabel('Number of tests')
plt.xlabel('Error in meters')
plt.title('Error distribution - Random Forest (no opt)')

plt.subplot(2, 2, 4)
plt.hist(np.array(RF_1_not_filter_optim_param['error']), bins=20)
plt.ylabel('Number of tests')
plt.xlabel('Error in meters')
plt.title('Error distribution - Random Forest (opt)')

plt.tight_layout()
plt.show()

