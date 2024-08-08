import datetime
import pandas as pd
from ast import literal_eval
import matplotlib.pyplot as plt

dep_entropy = pd.read_csv(r'D:\Short_Research\LLM_SoS\institution_entropy(3).csv')
dep_entropy['created_date'] = pd.to_datetime(dep_entropy['created_date'])
dep_entropy.fields = dep_entropy.fields.apply(literal_eval)
dep_entropy = dep_entropy.explode('fields')
needs = dep_entropy['fields'].value_counts().head(12).index
dep_entropy = dep_entropy[dep_entropy['fields'].isin(needs)]
dep_entropy['year'] = dep_entropy['created_date'].dt.year
dep_entropy['month'] = dep_entropy['created_date'].dt.month
dep_entropy['quarter'] = dep_entropy['created_date'].dt.month // 4
dep_entropy['year_month'] = pd.to_datetime(
    dep_entropy['year'].astype(str) + '-' + dep_entropy['month'].astype(str) + '-01')
dep_entropy['year_quarter'] = dep_entropy['year'].astype(str) + '-' + dep_entropy['quarter'].astype(str)
desc_df = dep_entropy.groupby(['year_month', 'fields']).agg({'doi': 'count', 'entropy': 'mean'}).reset_index()
desc_df.columns = ['year', 'fields', 'doi', 'entropy_inst']

# fig, ax = plt.subplots(nrows=3, ncols=4, figsize=(16, 9))
# axs = ax.ravel()
# for kk in range(0, 12):
#     desc_dfs = desc_df[desc_df['fields'] == needs[kk]].reset_index(drop=True)
#     axs[kk].plot(desc_dfs['year_month'], desc_dfs['entropy_inst'], '-o')
#     axs[kk].plot([pd.Timestamp('2022-12-01 00:00:00'), pd.Timestamp('2022-12-01 00:00:00')],
#                  [desc_dfs['entropy_inst'].min(), desc_dfs['entropy_inst'].max()], '--')
#     axs[kk].set_title(needs[kk])
# plt.tight_layout()
# plt.show()

dep_entropy = pd.read_csv(r'D:\Short_Research\LLM_SoS\department_entropy(3).csv')
dep_entropy['created_date'] = pd.to_datetime(dep_entropy['created_date'])
dep_entropy.fields = dep_entropy.fields.apply(literal_eval)
dep_entropy = dep_entropy.explode('fields')
needs = dep_entropy['fields'].value_counts().head(12).index
dep_entropy = dep_entropy[dep_entropy['fields'].isin(needs)]
dep_entropy['year'] = dep_entropy['created_date'].dt.year
dep_entropy['month'] = dep_entropy['created_date'].dt.month
dep_entropy['quarter'] = dep_entropy['created_date'].dt.month // 4
dep_entropy['year_month'] = pd.to_datetime(
    dep_entropy['year'].astype(str) + '-' + dep_entropy['month'].astype(str) + '-01')
dep_entropy['year_quarter'] = dep_entropy['year'].astype(str) + '-' + dep_entropy['quarter'].astype(str)
desc_df1 = dep_entropy.groupby(['year_month', 'fields']).agg({'doi': 'count', 'entropy': 'mean'}).reset_index()
desc_df1.columns = ['year', 'fields', 'doi', 'entropy_dep']

desc_df1 = desc_df1.merge(desc_df, on=['year', 'fields'], how='outer')
desc_df1 = desc_df1.fillna(0)
desc_df1 = desc_df1.sort_values(by=['fields', 'year']).reset_index(drop=True)
desc_df1.to_csv(r'D:\Short_Research\LLM_SoS\desc_df3.csv')
