import os
import subprocess
from typing import List

from config import settings


def get_all_fbx_files(dir_path: str) -> List[str]:
    fbx_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(".fbx")]
    return fbx_files


def log_subprocess_output(subproces_result: subprocess.CompletedProcess, encoding='utf-8'):
    for line in subproces_result.stdout.splitlines():
        print(str(line, encoding))  # feel free changing to logging.log()


if __name__ == "__main__":
    source_files = get_all_fbx_files(settings.source_fbx_directory_path)

    if len(source_files) == 0:
        print("No source fbx files!")
    for file in source_files:
        command = ['Blender', '--background', '--python', settings.core_path, "--", str(settings.import_scale),
                   file, settings.export_directory_path, settings.export_suffix, str(settings.start_frame),
                   str(settings.end_frame), str(settings.last_key_frames_ahead), settings.better_fbx_install_global_path]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                cwd=os.path.dirname(os.path.realpath(__file__)))
        log_subprocess_output(result)
