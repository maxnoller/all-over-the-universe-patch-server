from django.db import models

# Create your models here.
class Build(models.Model):
    version = models.DecimalField(max_digits=4, decimal_places=2)

    def get_location(self):
        return "/builds/{}/".format(version)
    
    def get_new_files(self, prev_version):
        files = self.get_all_build_files()
        prev_build = Build.objects.get(version=prev_version)
        prev_build_files = prev_build.get_all_build_files

    def get_all_build_files(self):
        return ["a"]