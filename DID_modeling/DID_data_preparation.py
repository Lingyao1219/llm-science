import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update(
    {'font.size': 13, 'font.family': "serif", 'mathtext.fontset': 'dejavuserif', 'xtick.direction': 'in',
     'xtick.major.size': 0.5, 'grid.linestyle': "--", 'axes.grid': True, "grid.alpha": 1, "grid.color": "#cccccc",
     'xtick.minor.size': 1.5, 'xtick.minor.width': 0.5, 'xtick.minor.visible': True, 'xtick.top': True,
     'ytick.direction': 'in', 'ytick.major.size': 0.5, 'ytick.minor.size': 1.5, 'ytick.minor.width': 0.5,
     'ytick.minor.visible': True, 'ytick.right': True, 'axes.linewidth': 0.5, 'grid.linewidth': 0.5,
     'lines.linewidth': 1.5, 'legend.frameon': False, 'savefig.bbox': 'tight', 'savefig.pad_inches': 0.05})

needs = ['Computer Science', 'Medicine', 'Social Sciences', 'Engineering', 'Decision Sciences', 
         'Psychology', 'Biochemistry, Genetics and Molecular Biology', 'Business, Management and Accounting',
         'Health Professions', 'Arts and Humanities', 'Economics, Econometrics and Finance', 'Neuroscience']

def read_entropy(f_name='llm-information-entropy.csv', agg_t='year_quarter', u_name='llm', plot_t=True, need_fs=needs):
    llm_entropy = pd.read_csv(f_name)
    llm_entropy['datetime'] = pd.to_datetime(llm_entropy['datetime'])
    llm_entropy = llm_entropy.assign(**{'fields': llm_entropy['fields'].str.split('; ')})
    llm_entropy = llm_entropy.explode('fields')
    llm_entropy = llm_entropy[llm_entropy['fields'].isin(need_fs)]
    llm_entropy['year'] = llm_entropy['datetime'].dt.year
    llm_entropy['month'] = llm_entropy['datetime'].dt.month
    llm_entropy['quarter'] = llm_entropy['datetime'].dt.month // 4
    llm_entropy['year_month'] = pd.to_datetime(
        llm_entropy['year'].astype(str) + '-' + llm_entropy['month'].astype(str) + '-01')
    llm_entropy['year_quarter'] = pd.to_datetime(
        llm_entropy['year'].astype(str) + '-' + (llm_entropy['quarter'] * 3 + 3).astype(str) + '-01')
    desc_df = llm_entropy.groupby([agg_t, 'fields']).agg(
        {'doi': 'count', 'institutions_entropy': 'mean', 'departments_entropy': 'mean'}).reset_index()
    desc_df.columns = ['year', 'fields', 'count', 'entropy_inst', 'entropy_dep']
    desc_df['type'] = u_name

    if plot_t:
        desc_df = desc_df[desc_df['year'].dt.year >= 2019]
        fig, ax = plt.subplots(nrows=3, ncols=4, figsize=(16, 9))
        axs = ax.ravel()
        for kk in range(0, 12):
            desc_dfs = desc_df[desc_df['fields'] == need_fs[kk]].reset_index(drop=True)
            axs[kk].plot(desc_dfs['year'], desc_dfs['entropy_inst'], '-o')
            axs[kk].plot([pd.Timestamp('2022-12-01 00:00:00'), pd.Timestamp('2022-12-01 00:00:00')],
                         [desc_dfs['entropy_inst'].min(), desc_dfs['entropy_inst'].max()], '--')
            axs[kk].set_title(need_fs[kk])
        plt.tight_layout()
        plt.show()

    return desc_df

entropy_llm = read_entropy(f_name='llm-information-entropy.csv', agg_t='year_quarter', u_name='llm')
entropy_nonllm = read_entropy(f_name='non-llm-information-entropy.csv', agg_t='year_quarter', u_name='nonllm')
entropy_ml = read_entropy(f_name='ml-information-entropy.csv', agg_t='year_quarter', u_name='ml')

desc_df = pd.concat([entropy_llm, entropy_nonllm, entropy_ml])
desc_df = desc_df.fillna(0)
desc_df = desc_df.sort_values(by=['type', 'fields', 'year']).reset_index(drop=True)

# Process did results from R
namesv = ['ML, Institution', 'ML, Department', 'Non-LLM/ML, Institution', 'Non-LLM/ML, Department']
cct = 0
all_did = pd.DataFrame()
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(8, 8), sharex=True, sharey=True)
axs = ax.ravel()

# Define the desired order for plotting
plot_order = ['Computer Science', 'Medicine', 'Social Science', 'Engineering', 'Decision Science',
              'Psychology', 'Bio, Gen & Mol', 'Bus,Mgmt & Acct', 'Health Professions',
              'Arts & Humanities', 'Econ, Econom & Fin', 'Neuroscience']
plot_order = plot_order[::-1]

for kk in ['did_mlentropy_inst.csv', 'did_mlentropy_dep.csv', 'did_nonllmentropy_inst.csv', 'did_nonllmentropy_dep.csv']:
    temp = pd.read_csv(kk)
    temp = temp[temp['Est'] == 'did']
    temp['type'] = namesv[cct]
    temp['Name'] = temp['Name'].replace({'Biochemistry, Genetics and Molecular Biology': 'Bio, Gen & Mol',
                                         'Business, Management and Accounting': 'Bus,Mgmt & Acct',
                                         'Economics, Econometrics and Finance': 'Econ, Econom & Fin',
                                         'Arts and Humanities': 'Arts & Humanities',
                                         'Social Sciences': 'Social Science',
                                         'Decision Sciences': 'Decision Science'})
    temp = temp[temp['Name'] != 'Materials Science']
    
    # Reorder the dataframe according to the desired order
    temp['Name'] = pd.Categorical(temp['Name'], categories=plot_order, ordered=True)
    temp = temp.sort_values('Name')
    
    all_did = pd.concat([all_did, temp])
    
    # Use errorbar with horizontal orientation
    axs[cct].errorbar(temp['Estimate'], range(len(temp['Name'])), 
                     xerr=temp['Std. Error'], 
                     fmt='o',
                     markersize=8,  # Increase marker size
                     markerfacecolor='#1f77b4',  # Fill color
                     markeredgecolor='#1f77b4',  # Edge color
                     markeredgewidth=2,  # Make edge bolder
                     ecolor='#1f77b4',  # Make error bars same color as markers
                     elinewidth=2,  # Make error bars thicker
                     #capsize=5,  # Add cap to error bars
                     #capthick=2,  # Make caps thicker
                     linestyle='None')
    
    if cct == 0:  # Only add 'a.' once for the top row
        axs[cct].text(-0.9, 12, 'a.', fontsize=16, fontweight='bold')
    elif cct == 2:  # Only add 'b.' once for the bottom row
        axs[cct].text(-0.9, 12, 'b.', fontsize=16, fontweight='bold')
    
    # Add vertical line at x=0
    axs[cct].axvline(x=0, color='#ff7f0e', linestyle='--')
    axs[cct].set_xlim(-0.5, 0.5)
    
    # Set the y-ticks and labels
    axs[cct].set_yticks(range(len(temp['Name'])))
    axs[cct].set_yticklabels(temp['Name'])
    
    axs[cct].set_title(namesv[cct])
    
    # Add grid lines
    axs[cct].grid(True, axis='x')
    axs[cct].grid(False, axis='y')
    
    cct += 1

# Adjust layout to prevent label cutoff
plt.tight_layout()
plt.savefig(r'DiD_10.pdf', bbox_inches='tight')
