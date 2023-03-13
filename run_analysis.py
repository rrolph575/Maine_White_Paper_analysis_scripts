"""Primary analysis script."""

__author__ = "Matt Shields"
__copyright__ = "Copyright 2022, National Renewable Energy Laboratory"
__maintainer__ = "Matt Shields"
__email__ = "matt.shields@nrel.gov"

import pandas as pd
import datetime as dt
import pprint

from ORBIT import load_config
from ORBIT import ProjectManager
from ORBIT.core.library import initialize_library

import os
if 'DATA_LIBRARY' in os.environ:
    del os.environ['DATA_LIBRARY']

# set relative paths (alternatively, set absolute paths)
custom_library = "library"
custom_configs  = ['configs/scenario_1_for_1GW.yaml', 'configs/scenario_2_for_1GW.yaml', 'configs/scenario_3_for_1GW.yaml', 'configs/scenario_4_for_5GW.yaml']
custom_weather = "data/swh_ws100m_maine_2010_thru_2022.csv"


if __name__ == '__main__':
    # Point ORBIT to the custom data libraries in the anlaysis repo
    initialize_library(custom_library)

    # Load in the input configuration YAML
    for custom_config in custom_configs:
        config = load_config(custom_config)
    
        # Print out the required information for input config
        phases = ['ArraySystemDesign',
                    'ElectricalDesign',
                    'SemiSubmersibleDesign',
                    #'SemiTautMooringSystemDesign',
                    'MooringSystemDesign',
                    'ArrayCableInstallation',
                    'ExportCableInstallation',
                    'MooringSystemInstallation',
                    'FloatingSubstationInstallation',
                    'MooredSubInstallation']
        #expected_config = ProjectManager.compile_input_dict(phases)
        pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(expected_config)
    
        # Initialize and run project
        weather = pd.read_csv(custom_weather).set_index("datetime")  # Project installation begins at start of weather file unless other wise specified in install_phase in input config
        project = ProjectManager(config, weather=weather)
        project.run()
    
        # Print some output results
        pp.pprint(project.capex_breakdown_per_kw)
        
        # save the capex breakdown_per_kw
        capex_brkdwn_per_kw_series = pd.Series(project.capex_breakdown_per_kw)
        capex_brkdwn_per_kw_series.to_pickle('output/capex_breakdown_per_kw_' + custom_config[8:-5] + '.pkl')
    
        #print(f"Total CapEx per kW")
        print(f"Installation CapEx: {project.installation_capex/1e6:.0f} M")
        print(f"System CapEx: {project.system_capex/1e6:.0f} M")
        print(f"Turbine CapEx: {project.turbine_capex/1e6:.0f} M")
        print(f"Soft CapEx: {project.soft_capex/1e6:.0f} M")
        print(f"Total CapEx: {project.total_capex/1e6:.0f} M")
    
        print(f"\nInstallation Time: {project.installation_time:.0f} h")
    
        # Should add a method here to report the start/end dates of each phase and maybe plot a Gantt chart or similar
