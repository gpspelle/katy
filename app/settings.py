import os
# Production variables
#ENV = "production"
#DATA_FOLDER = "/data/majelan_data"
#APP_FOLDER = "majelandash"
#prefix_source = ENV
#DASHBOARD_FOLDER = os.path.join(DATA_FOLDER, prefix_source, APP_FOLDER)

# Dev variables
ENV = "dev"
DATA_FOLDER = "/data/majelan_data"
APP_FOLDER = "majelandash"
prefix_source = ENV
DASHBOARD_FOLDER = os.path.join(DATA_FOLDER, prefix_source, APP_FOLDER)
