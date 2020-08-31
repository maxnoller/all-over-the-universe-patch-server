from django.db import models
import filecmp
import os
import decimal

# Create your models here.
class Build(models.Model):
    version = models.DecimalField(max_digits=4, decimal_places=2)

    def get_location(self):
        return "/builds/{}/".format(self.version)
    
    def get_new_files(self, prev_version):
        if prev_version == decimal.Decimal(0):
            return self.get_build_files()
        prev_build = Build.objects.get(version=prev_version)
        return self.compare_builds(prev_build)

    def compare_builds(self, other_build):
        current_files = self.get_build_files()
        other_build_files = other_build.get_build_files()
        different_files = [filename for filename in current_files if filename not in other_build_files]
        common_files = [filename for filename in current_files if filename in other_build_files]
        current_files = self.convert_to_version_paths(common_files)
        other_build_files = other_build.convert_to_version_paths(common_files)
        for (new_file, old_file) in zip(current_files, other_build_files):
            if not filecmp.cmp(new_file, old_file):
                different_files.append(new_file)

    def convert_to_version_paths(self, files):
        return [str(self.version)+"/"+filename for filename in files]

    def get_build_files(self):
        ret = []
        path = "/var/www/html/all-over-the-universe/builds/{}/".format(str(self.version))
        for root, _, files in os.walk(path):
            for name in files:
                ret.append(os.path.relpath(os.path.join(root, name), start=path))
        return ret

    def __str__(self):
        return "Version: {}".format(self.version)