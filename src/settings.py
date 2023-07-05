from typing import Dict, List, Optional, Union

from dataset_tools.templates import AnnotationType, CVTask, Industry, License

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "Detection of Small Size Construction Tools"
PROJECT_NAME_FULL: str = "Image Dataset for Object Detection of Small Size Construction Tools"

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.CC_BY_4_0()
INDUSTRIES: List[Industry] = [Industry.Construction()]  # Construction
CV_TASKS: List[CVTask] = [CVTask.ObjectDetection()]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.ObjectDetection()]

RELEASE_YEAR: int = 2023
HOMEPAGE_URL: str = "https://zenodo.org/record/6530106"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 1463142
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/small-size-construction-tools"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = {
    "DATA1.zip": "https://zenodo.org/record/6530106/files/DATA1.zip?download=1",
    "DATA2.zip": "https://zenodo.org/record/6530106/files/DATA2.zip?download=1",
    "DATA3.zip": "https://zenodo.org/record/6530106/files/DATA3.zip?download=1",
    "DATA4.zip": "https://zenodo.org/record/6530106/files/DATA4.zip?download=1",
}
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = {
    "bucket": [255, 0, 0],
    "cutter": [0, 255, 0],
    "drill": [0, 0, 255],
    "grinder": [255, 255, 0],
    "hammer": [0, 255, 255],
    "knife": [255, 0, 255],
    "saw": [255, 128, 0],
    "shovel": [128, 0, 128],
    "spanner": [255, 192, 203],
    "tacker": [165, 42, 42],
    "trowel": [155, 155, 155],
    "wrench": [184, 234, 134],
}
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

PAPER: Optional[str] = "https://link.springer.com/article/10.1007/s12205-023-1011-2"
CITATION_URL: Optional[str] = "https://zenodo.org/record/6530106/export/hx"
ORGANIZATION_NAME: Optional[Union[str, List[str]]] = [
    "Korea Expressway Corporation and Inha University, Korea",
]
ORGANIZATION_URL: Optional[Union[str, List[str]]] = [
    "https://link.springer.com/article/10.1007/s12205-023-1011-2#author-information",
]
TAGS: List[str] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    settings = {
        "project_name": PROJECT_NAME,
        "license": LICENSE,
        "industries": INDUSTRIES,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["project_name_full"] = PROJECT_NAME_FULL or PROJECT_NAME
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["citation_url"] = CITATION_URL
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["tags"] = TAGS if TAGS is not None else []

    return settings
