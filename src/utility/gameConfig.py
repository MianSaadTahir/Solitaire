import pickle
import os
default_settings = {'draw_three': False}

def store_preferences(settings):
    data = settings

    file_path = os.path.join("prefereData", "setup.data")
    file = open(file_path, "wb")

    pickle.dump(data, file)
    file.close()

def retrieve_preferences():
    try:
        file_path = os.path.join("prefereData", "setup.data")
        file = open(file_path, "rb")
    except FileNotFoundError:
        store_preferences(default_settings)
        return default_settings
    else:
        settings = pickle.load(file)
        file.close()
        return settings
