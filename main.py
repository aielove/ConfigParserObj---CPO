class Section:
    def __init__(self):
        pass

    def toDict(self):
        return self.__dict__


class SubSection:
    def __init__(self):
        pass

    def toDict(self):
        return self.__dict__


class ConfigParser:
    def __init__(self, file):
        self.fileName = file
        self.configFile = self._openFile(self.fileName)
        self.rawParsedSections = {}
        self.sectionList = []
        self._rawParse()
        self._parse()

    def _openFile(self, file: str):
        try:
            with open(file, mode="r", encoding="utf-8") as confifReadFile:
                return [line.rstrip("\n") for line in confifReadFile]

        except:
            raise Exception(f"Cannot open file {file}")

    def _rawParse(self):
        for line in range(len(self.configFile)):
            if self.configFile[line].startswith("["):
                sectionName = self._parseSectionHeader(self.configFile[line])
                self.rawParsedSections[sectionName] = []
                for sectionComp in self.configFile[line + 1 :]:
                    if not sectionComp.startswith("["):
                        if len(sectionComp) != 0:
                            self.rawParsedSections[sectionName].append(sectionComp)
                    else:
                        break

    def _parse(self):
        for section in self.rawParsedSections:
            if ":" not in section:
                sectionObj = Section()
                setattr(sectionObj, "__name__", section)
                for param in self.rawParsedSections[section]:
                    parsedParam = self._parseParam(param)
                    setattr(sectionObj, parsedParam[0], parsedParam[1])
                setattr(self, section, sectionObj)
                self.sectionList.append(sectionObj)
            else:
                parsedSubSectionHeader = self._parseSubSectionHeader(section)
                parentSectionObj = getattr(self, parsedSubSectionHeader[0], None)

                if parentSectionObj is not None:
                    subSectionObj = SubSection()
                    setattr(subSectionObj, "__name__", section)
                    for param in self.rawParsedSections[section]:
                        parsedParam = self._parseParam(param)
                        setattr(subSectionObj, parsedParam[0], parsedParam[1])

                    setattr(parentSectionObj, parsedSubSectionHeader[1], subSectionObj)

    def _parseParam(self, input: str) -> tuple:

        b = input[input.index("=") + 1 :].split(" ")
        f = filter(lambda x: x != "", b)
        x = "".join(f"{i} " for i in list(f))[:-1]

        paramName = input.replace(" ", "").split("=")[0]
        paramVal = self._detectType(x)
        return (paramName, paramVal)

    def _parseSectionHeader(self, input: str) -> str:
        return input.strip("[").strip("]")

    def _parseSubSectionHeader(self, input: str) -> tuple:
        subSection = input.split(":")
        parentSection = subSection[0]
        subSectionName = subSection[1]
        return (parentSection, subSectionName)

    def _detectType(self, input: str):
        if input.lower() == "true" or input.lower() == "false":
            return self._convertBool(input)

        if input.startswith('"') and input.endswith('"'):
            return input.replace('"', "")

        try:
            return int(input)
        except ValueError:
            pass

        try:
            return float(input)
        except ValueError:
            pass

        return input

    def _convertBool(self, input: str) -> bool:
        return bool(input)

    def update(self):
        with open(self.fileName, mode="w") as configWrite:
            for section in self.sectionList:
                configWrite.write(f"\n[{section.__name__}]\n")
                section = section.toDict()
                for param in section:
                    if param != "__name__":
                        if not isinstance(section[param], SubSection):
                            if isinstance(section[param], str):
                                configWrite.write(f'{param} = "{section[param]}"\n')
                            else:
                                configWrite.write(f"{param} = {section[param]}\n")
                        else:
                            configWrite.write(f"\n[{section[param].__name__}]\n")
                            param = section[param].toDict()
                            for SubSectionParam in param:
                                if SubSectionParam != "__name__":
                                    configWrite.write(f"{SubSectionParam} = {param[SubSectionParam]}\n")
