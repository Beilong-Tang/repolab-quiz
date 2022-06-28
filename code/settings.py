# This is not from Django -- Loe
import os
import json

def main():
    DEFAULT_CONFIG_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../config/" # just in case some one what to modify this
    
    check_and_create_dir(DEFAULT_CONFIG_DIR)
    env_vars = read_from_config_file(DEFAULT_CONFIG_DIR)
    default_env_vars = generate_default_values(DEFAULT_CONFIG_DIR)

    if not env_vars: # No file was found, use default one
        env_vars = default_env_vars
    else: # If found, use the found one, and check them
        env_vars = env_list_intergity_check(default_env_vars,env_vars)
    
    save_to_config_file(DEFAULT_CONFIG_DIR,env_vars) # Save change to config
    apply_env_from_list(env_vars)
    return

# subprocess

def generate_default_values(DEFAULT_CONFIG_DIR):
    # generate default value and write to file
    env_vars = {}

    env_vars["ROOT_DIR"] = os.path.dirname(os.path.realpath(__file__)) + "/../"  # Rott means the repo root
    env_vars["DATA_DIR"] = os.path.join(env_vars["ROOT_DIR"],"data/")
    env_vars["CONFIG_DIR"] = DEFAULT_CONFIG_DIR
    env_vars["DEBUG"] = "True"
    env_vars["ALLOWED_HOSTS"] = "*" # This should be a space-seperated list
    env_vars["DATABASE"] = "sqlite"
    # Only applied to MongoDB
    env_vars["DB_NAME"] = "SSO"
    env_vars["ENFORCE_SCHEMA"] = "True"
    env_vars["HOST"] = ""
    env_vars["PORT"] = "27017"
    env_vars["USERNAME"] = "SSO"
    env_vars["PASSWORD"] = "SSO"
    env_vars["AUTH_SOURCE"] = "admin"
    env_vars["AUTH_MECHANISM"] = "SCRAM-SHA-1"

    # env_vars["ROOT_DIR"] = 

    return env_vars

def read_from_config_file(CONFIG_DIR):
    # read values from files and apply
    print("[INFO] Settings: Reading from file.")
    env_vars = {}
    try:
        with open(os.path.join(CONFIG_DIR,"config.json"),"r",encoding="utf8") as the_file:
            env_vars = json.loads(the_file.read())
    except FileNotFoundError:
        print("[WARNING] Settings: Config file not found. Generating a default one.")
    return env_vars

def apply_env_from_list(env_var_list):
    print("[INFO] Settings: Apply environment variable.")
    for key, value in env_var_list.items():
        os.environ[key] = value
        print("[INFO] Settings: %s - %s"%(key,value))
    return

def env_list_intergity_check(source,sus):
    # check the intergity of the list. Add the missing variables with default values.
    print("[INFO] Settings: Performing intergity check.")
    checked = sus.copy()
    missing = source.copy()
    for source_var in source:
        for sus_var in sus:
            if source_var == sus_var:
                missing.pop(source_var)
    
    if missing:
        for missing_var in missing:
            checked[missing_var] = missing[missing_var]
            print("[WARNING] Settings: Missing environment variable, %s, using default value, %s, will save to file."%(missing_var,missing[missing_var]))

    return checked

def save_to_config_file(DIR, CONTENT):
    with open(os.path.join(DIR,"config.json"),"w",encoding="utf8") as the_file:
        json.dump(CONTENT, the_file, indent=2)
        print("[INFO] Settings: New config file generated.")
    return

# helper

def check_and_create_dir(DIR):
    isExist = os.path.exists(DIR)
    if not isExist:
        print(
            "[WARNNING] Settings: Diractory %s does not exist. It is created now." % DIR)
        try:
            os.mkdir(DIR)
        except FileNotFoundError:
            print("[ERROR] Settings: Intermediate folders in Dir %s does not exist. Please check settings and config." % DIR)
            raise FileNotFoundError
    else:
        print("[INFO] Settings: Folder already exists in Dir %s, skipping creation." % DIR)

    return
