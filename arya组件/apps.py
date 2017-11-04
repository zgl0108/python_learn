from django.apps import AppConfig


class AryaConfig(AppConfig):
    name = 'arya'

    def ready(self):
        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('arya')        # 在项目启动的时候先在所有的目录下寻找并执行arya.py文件