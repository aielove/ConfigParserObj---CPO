from main import ConfigParser

cfg = ConfigParser("config.cfg")
print(cfg.sectionList[0].toDict())
cfg.abc.dfeg.int = "dfgfrhg"
print(cfg.abc.toDict())
cfg.update()
