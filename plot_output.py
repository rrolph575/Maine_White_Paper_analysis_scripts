# Plot the output of ORBIT runs

import pandas as pd
import matplotlib.pyplot as plt


scenario_names = ['scenario_1_for_1GW', 'scenario_2_for_1GW', 'scenario_3_for_1GW', 'scenario_4_for_5GW']


# read ofiles and concatenate them into one df for plotting
df = pd.concat([pd.read_pickle("output/capex_breakdown_per_kw_" + scenario_name + '.pkl') for scenario_name in scenario_names], axis=1, ignore_index=True)

# label the columns based on the scenario
df.columns = scenario_names



##### Calculate lcoe for each scenario

# 1 GW scenarios
project_kW_1GW = 15000*67

# 5 GW scenario
project_kW_5GW = 15000*334

''' for now, we do not calculate LCOE becuase OpEx is not constant -- that is not realistic when comparing different scenarios with different distances to shore.
opex = 118
fcr = .0582
ncf = .459 

df_lcoe = df.sum(axis=0).to_frame().T
df_lcoe = df_lcoe.rename(index={0: 'Total CapEx ($/kW)'})

df_lcoe.loc[len(df_lcoe)] = 1000*(fcr * df_lcoe.iloc[0] + opex)/(ncf * 8760)
df_lcoe = df_lcoe.rename(index={1: 'LCOE ($/kW)'})
'''


### Plot the LCOE (df_lcoe) and CapEx breakdown (df)
# CapEx breakdown
fig = plt.figure(figsize=(6, 4), dpi=200)
ax = fig.add_subplot(111)
df.T.plot(kind='bar',stacked=True,ax=ax).legend(bbox_to_anchor=(1.05, 1))
ax.set_xlabel("")
ax.set_ylabel("CapEx ($/kW)")
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], bbox_to_anchor=(1.05, 1))
plt.xticks([0,1,2,3], ['Scenario 1, 1GW', 'Scenario 2, 1GW', 'Scenario 3, 1GW', 'Scenario 4, 5GW'], rotation=45, ha='right') # remove xticks
plt.savefig('CapEx_breakdown_all_scenarios.png', bbox_inches='tight')






