#----------------------------------------------------------------------------------------------
# This bash will automatically install the dependency for the sso_webserver and download the latest data from gitee. Feel Free to run this.
# The bash will install a virtual environment. To activate it, you should run "source /env/bin/activate" at the root dirctory of the webserver. To deactivate the virtual environemnt, "deactivate" will do the job.
#----------------------------------------------------------------------------------------------
#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path" && cd ..

echo "Installing venv"
pip install virtualenv
cd "$parent_path" && cd ..
python3 -m venv env

echo "Starting python environment"
cd "$parent_path" && cd ..
source env/bin/activate

echo "Installing package according to requirement"
cd "$parent_path"
cat requirements.txt | xargs -n 1 pip install