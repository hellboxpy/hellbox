import atexit
import os
import shlex
import shutil
import subprocess
import tempfile
from collections import namedtuple
from shutil import copyfile


TEMPORARY_DIRECTORIES = []


@atexit.register
def _cleanup():
    for directory in TEMPORARY_DIRECTORIES:
        if os.path.exists(directory):
            shutil.rmtree(directory)


class SourceFile(namedtuple("SourceFile", ["original_path", "content_path"])):

    def copy(self, basename=None):
        # TODO: Should copy directories as well

        if basename is None:
            basename = self.basename

        directory = self._create_temporary_directory()
        destination = os.path.join(directory, basename)
        copyfile(self.content_path, destination)

        return SourceFile(self.original_path, destination)

    def transform(self, command_template, extension=None):
        if extension is None:
            extension = self.extension

        filename = f"{self.root}.{extension}"

        if "{output}" in command_template:
            input_path = self.content_path
            output_path = os.path.join(
                self._create_temporary_directory(),
                filename
            )
        else:
            copy = self.copy()
            input_path = copy.content_path
            output_path = os.path.join(copy.directory, filename)

        command = command_template.format(input=input_path, output=output_path)

        subprocess.run(
            shlex.split(command),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )

        return SourceFile(self.original_path, output_path)

    def write(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)

        destination = os.path.join(path, self.basename)
        copyfile(self.content_path, destination)

        return SourceFile(self.original_path, destination)

    @property
    def basename(self):
        return os.path.basename(self.content_path)

    @property
    def directory(self):
        return os.path.dirname(self.content_path)

    @property
    def extension(self):
        return os.path.splitext(self.basename)[1][1:]

    @property
    def root(self):
        return os.path.splitext(self.basename)[0]

    def _create_temporary_directory(self):
        directory = tempfile.mkdtemp()
        TEMPORARY_DIRECTORIES.append(directory)
        return directory
