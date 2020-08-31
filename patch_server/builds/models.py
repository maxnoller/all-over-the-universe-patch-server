from django.db import models
import filecmp
import os
import decimal

# Create your models here.
class Build(models.Model):
    version = models.DecimalField(max_digits=4, decimal_places=2)

    def get_location(self):
        return "/var/www/html/all-over-the-universe/builds/{}/".format(str(self.version))
    
    def get_new_files(self, prev_version):
        if prev_version == decimal.Decimal(0):
            return self.convert_to_version_paths(self.get_build_files())
        prev_build = Build.objects.get(version=prev_version)
        return self.compare_builds(prev_build)
    
    def get_destination_dict(self, files):
        ret_dict = dict()
        path = self.get_location()
        for file in files:
            ret_dict[os.path.relpath(file, start=path)] = os.path.relpath(file, start="/var/www/html/")
        return ret_dict

    def compare_builds(self, other_build):
        current_files = self.get_build_files()
        other_build_files = other_build.get_build_files()
        different_files = [filename for filename in current_files if filename not in other_build_files]
        different_files = self.convert_to_version_paths(different_files)
        common_files = [filename for filename in current_files if filename in other_build_files]
        current_files = self.convert_to_version_paths(common_files)
        other_build_files = other_build.convert_to_version_paths(common_files)
        for (new_file, old_file) in zip(current_files, other_build_files):
            if not filecmp.cmp(new_file, old_file):
                different_files.append(new_file)

    def convert_to_version_paths(self, files):
        version_path = self.get_location()
        return [version_path+filename for filename in files]

    def get_build_files(self):
        ret = []
        path = self.get_location()
        for root, _, files in os.walk(path):
            for name in files:
                ret.append(os.path.relpath(os.path.join(root, name), start=path))
        return ret

    def __str__(self):
        return "Version: {}".format(self.version)
