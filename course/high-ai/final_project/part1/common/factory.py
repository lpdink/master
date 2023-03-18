import sys

from .log import logging


class Factory:
    def __init__(self) -> None:
        self.name2clazz = dict()
        self.clazz2name = dict()
        self.name2obj = dict()
        self.obj2name = dict()

    def __call__(self, name):
        def register(clazz):
            if name not in self.name2clazz:
                self.name2clazz[name] = clazz
            else:
                logging.error(f"class name {name} already registered!")
                sys.exit(-1)
            if clazz not in self.clazz2name:
                self.clazz2name[clazz] = name
            else:
                logging.error(
                    f"class already registered with name {self.clazz2name[clazz]}!"
                )
                sys.exit(-1)
            return clazz

        return register

    def get(self, obj_name):
        return self[obj_name]

    def get_objs(self):
        return self.name2obj.values()

    def __getitem__(self, key):
        return self.name2obj.get(key, None)

    def _create_objs_common(self, config, section):
        if hasattr(config, section):
            for obj_name, obj in config.models.items():
                clazz = self.name2clazz.get(obj.clazz, None)
                if clazz is None:
                    logging.warning(f"can't find clazz {clazz}, instanced failed")
                    continue
                if hasattr(obj, "args") and len(obj.args) > 0:
                    new_model = clazz(**obj.args)
                else:
                    new_model = clazz()
                self.name2obj[obj_name] = new_model
                self.obj2name[new_model] = obj_name
                logging.info(f"created instance with {obj}")
        else:
            logging.warning(f"no {section} in {config}, so {section} not instanced.")

    def create_models_from_config(self, config):
        self._create_objs_common(config, "models")

    def create_datasets_from_config(self, config):
        self._create_objs_common(config, "datasets")

    def create_objs(self, config):
        self.create_models_from_config(config)
        self.create_datasets_from_config(config)
        return self


objfactory = Factory()
