import os
import shutil
from urllib.parse import unquote, urlparse

import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import get_file_name
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)
        fsize = get_file_size(local_path)
        with tqdm(desc=f"Downloading '{file_name_with_ext}' to buffer..", total=fsize) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = get_file_size(local_path)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer {local_path}...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_jpg_files(folder_path):
    count = 0

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".jpg"):
                count += 1

    return count


# https://zenodo.org/record/6530106

import os
import xml.etree.ElementTree as ET

import numpy as np
import supervisely as sly
from dotenv import load_dotenv
from supervisely.io.fs import (
    dir_exists,
    file_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)

# if sly.is_development():
# load_dotenv("local.env")
# load_dotenv(os.path.expanduser("~/supervisely.env"))

# api = sly.Api.from_env()
# team_id = sly.env.team_id()
# workspace_id = sly.env.workspace_id()

# project_name = "Detection of Small Size Construction Tools"
teamfiles_dir = "/4import/original_format/detection-small-size-construction-tools/"
# dataset_path = download_dataset(teamfiles_dir)  # for large datasets stored on instance
# dataset_path = os.path.join(sly.app.get_data_dir(), "ninja-repo-updater/649/")
dataset_path = sly.app.get_data_dir()

batch_size = 30
images_ext = ".jpg"
bboxes_ext = ".txt"
ds_name = "ds"


def create_ann(image_path, meta):
    labels = []

    image_np = sly.imaging.image.read(image_path)[:, :, 0]
    img_height = image_np.shape[0]
    img_wight = image_np.shape[1]

    item_name = get_file_name(image_path) + bboxes_ext
    bbox_path = os.path.join(os.path.dirname(image_path), item_name)

    if file_exists(bbox_path):
        with open(bbox_path) as f:
            content = f.read().split("\n")

            for curr_data in content:
                if len(curr_data) != 0:
                    curr_data = curr_data.split(",")
                    try:
                        class_name, tag_name = curr_data[4].split("_")
                    except:
                        continue
                    if tag_name == "train1":
                        tag_name = "train"
                    if tag_name.endswith("."):
                        tag_name = tag_name.rstrip(".")
                    if tag_name.endswith("1"):
                        tag_name = tag_name.rstrip("1")
                    tag = sly.Tag(meta.get_tag_meta(tag_name))
                    obj_class = meta.get_obj_class(class_name)
                    left = int(curr_data[0])  # - int(curr_data[2]) / 4
                    right = int(curr_data[0]) + int(curr_data[2])
                    top = int(curr_data[1])  # - int(curr_data[3]) / 4
                    bottom = int(curr_data[1]) + int(curr_data[3])

                    rectangle = sly.Rectangle(top=top, left=left, bottom=bottom, right=right)
                    label = sly.Label(rectangle, obj_class, tags=[tag])
                    labels.append(label)

    return sly.Annotation(img_size=(img_height, img_wight), labels=labels)


obj_class_bucket = sly.ObjClass("bucket", sly.Rectangle)
obj_class_cutter = sly.ObjClass("cutter", sly.Rectangle)
obj_class_drill = sly.ObjClass("drill", sly.Rectangle)
obj_class_grinder = sly.ObjClass("grinder", sly.Rectangle)
obj_class_hammer = sly.ObjClass("hammer", sly.Rectangle)
obj_class_knife = sly.ObjClass("knife", sly.Rectangle)
obj_class_saw = sly.ObjClass("saw", sly.Rectangle)
obj_class_shovel = sly.ObjClass("shovel", sly.Rectangle)
obj_class_spanner = sly.ObjClass("spanner", sly.Rectangle)
obj_class_tacker = sly.ObjClass("tacker", sly.Rectangle)
obj_class_trowel = sly.ObjClass("trowel", sly.Rectangle)
obj_class_wrench = sly.ObjClass("wrench", sly.Rectangle)

tag_train = sly.TagMeta("train", sly.TagValueType.NONE)
tag_test = sly.TagMeta("test", sly.TagValueType.NONE)


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)

    meta = sly.ProjectMeta(
        obj_classes=[
            obj_class_bucket,
            obj_class_cutter,
            obj_class_drill,
            obj_class_grinder,
            obj_class_hammer,
            obj_class_knife,
            obj_class_saw,
            obj_class_shovel,
            obj_class_spanner,
            obj_class_tacker,
            obj_class_trowel,
            obj_class_wrench,
        ],
        tag_metas=[tag_train, tag_test],
    )

    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    jpg_count = count_jpg_files(dataset_path)
    progress = sly.Progress("Create dataset '{}'".format(ds_name), jpg_count)

    for folderpath in [
        "DATA3/DATA3",
        "DATA4/DATA4",
        "DATA1/DATA1",
        "DATA2/DATA2",
    ]:
        curpath = os.path.join(dataset_path, folderpath)

        print(folderpath)

        images_names = [
            im_name for im_name in os.listdir(curpath) if get_file_ext(im_name) == images_ext
        ]

        for images_names_batch in sly.batched(images_names, batch_size=batch_size):
            images_pathes_batch = [
                os.path.join(curpath, image_name) for image_name in images_names_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, images_names_batch, images_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = [create_ann(image_path, meta) for image_path in images_pathes_batch]
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(images_names_batch))

    return project
