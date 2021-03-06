import pandas as pd
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline
from  regression_model.config import config # i need to import config while making sure it doesnt disrupt the folders
from regression_model.config import logging_config
from regression_model import __version__ as _version


_logger = logging_config.get_logger()



def load_dataset(*, file_name: str) -> pd.DataFrame:
    data_path = config.DATASET_DIR / file_name
    data = pd.read_csv(filepath_or_buffer= config.DATASET_DIR/data_path)
    return data



def save_pipeline(*, pipeline_to_persist) -> None:
    #saves the versioned model, and overwrites the previous saved models
    #This ensures that when the package is published, there is only one trained
    #model that can be called, and we know exactly how it was built.



    #prepare versioned save file name
    save_file_name = f"{config.PIPELINE_SAVE_FILE}{_version}.pkl"
    save_path = config.TRAINED_MODEL_DIR / save_file_name
    remove_old_pipelines(files_to_keep=save_file_name)
    joblib.dump(pipeline_to_persist, save_path)
    _logger.info(f"saved pipeline: {save_file_name}")

    



def load_pipeline(*, file_name: str) -> Pipeline:
    file_path = config.TRAINED_MODEL_DIR / file_name
    trained_model = joblib.load(filename=file_path)
    return trained_model



def remove_old_pipelines(*, files_to_keep) -> None:
    
    #Removes old model pipelines
    #This is to ensure that there is a simple one-to-one
    #mapping between the package version and the model version
    #to be imported and used by other application

    for model_file in config.TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in [files_to_keep, "__init__.py"]:
            model_file.unlink()