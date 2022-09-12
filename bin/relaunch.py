#!/usr/bin/env python3

# This script is an example of how to relaunch a workflow
# using a difference compute environment, but it doesn't
# always work. Related work is being tracked here:
# https://git.seqera.io/sage/nf-support/issues/33

# TODO: Create a proper CLI if this script ends up working

# Import standard packages
import importlib

# Import functions from Tower configuration script
tw = importlib.import_module("configure-tower-projects")

# Define parameters
run_id = "5qL0rezU2psz7H"
params = {"workspaceId": "212046960530683"}
target_ce = "TjHwqdo7aKa1FWOrINk3n"

# Initialize Tower client
client = tw.TowerClient()  # type: ignore

# Retrieve run name
run_info = client.request("GET", f"/workflow/{run_id}", params=params)
run_name = run_info["workflow"]["runName"]

# Retrieve launch info
launch_info = client.request("GET", f"/workflow/{run_id}/launch", params=params)
launch_info = launch_info["launch"]

# Subset run info for relaunch POST request
data = {
    "launch": {
        "computeEnvId": target_ce,
        "runName": f"{run_name}_relaunched",
        "pipeline": launch_info["pipeline"],
        "workDir": launch_info["workDir"],
        "revision": launch_info["revision"],
        "sessionId": launch_info["sessionId"],
        "paramsText": launch_info["paramsText"],
        "configText": launch_info["configText"],
        "configProfiles": launch_info["configProfiles"],
        "preRunScript": launch_info["preRunScript"],
        "resume": True,
    }
}
relaunch_info = client.request("POST", "/workflow/launch", params=params, json=data)
print(relaunch_info)
