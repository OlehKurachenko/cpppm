# 
#   Created by Oleh Kurachenko
#          aka okurache
#   on 2018-05-05T15:37:26Z as a part of c3pm
#   
#   ask me      oleh.kurachenko@gmail.com , I'm ready to help
#   GitHub      https://github.com/OlehKurachenko
#   rate & CV   http://www.linkedin.com/in/oleh-kurachenko-6b025b111
#

from collections import OrderedDict
from colored_print import ColoredPrint as ColorP
import json


class C3PMJSON:
    """
    Represents a c3pm.json file, which stores data about project and
    it's dependencies. Class is being constructed from string representation
    of c3pm.json containment, or from a file directly. If no arguments given,
    a new C3PMJSON is being constructed from users data via CLI. Class allows
    to make changes  and export new version of this file as string or write it
    directly to file.

    property "version" is a version of c3pm.json standard
    property "whatIsC3pm" is a url to c3pm project, which is added to all c3pm.json
    files

    Attributes:
        __c3pm_dict -- an OrderedDict with containment of c3pm.json
    """

    version = 'v0.2'
    whatIsC3pm = "https://github.com/OlehKurachenko/c3pm"

    C3PM_JSON_FILENAME = "c3pm.json"

    def __init__(self, json_str: str = None, load_from_file: bool = False):
        """
        If json_str is not None (default), it is being parsed to get it's representation. In this
        case, load_from_file have to be False (default), otherwise it causes an assertion error.
        If json_str is None and load_from_file if False, it is being constructed with users data
        via CLI.
        If json_str in None and load_from_file if True, containment is being red from file
        self.C3PM_JSON_FILENAME.
        :param json_str: str - containment of c3pm.json
        :param load_from_file: if True, json is being red directly from file

        :raises json.decoder.JSONDecodeError: if json_str is not a valid json
        :raises FileNotFoundError: if self.C3PM_JSON_FILENAME cannot be opened
        :raises C3PMJSON.BadC3PMJSONError: if json is not a valid s3pm project json
        :raises AssertionError: if call parameters are forbidden
        """

        assert not (json_str and load_from_file), "if json_str is not None (default)," \
                                                  "load_from_file have to be False (default)"

        if json_str is not None:
            assert type(json_str) == str, "json_str type must be str"

            self.__c3pm_dict = json.loads(json_str, object_pairs_hook=OrderedDict)
            self.__check_c3pm_dict()
        else:
            if load_from_file:
                with open(self.C3PM_JSON_FILENAME, "r") as c3pm_json_file:
                    self.__c3pm_dict = json.loads(c3pm_json_file.read(), object_pairs_hook=OrderedDict)
                    self.__check_c3pm_dict()
            else:
                self.__c3pm_dict = OrderedDict()
                self.init_new_json()

    def init_new_json(self):
        """
        Initialize new C3PMJSON with data from user via CLI.
        !!! Do not handle wrong input TODO fix
        """

        # Getting name
        while True:
            name = input("Project name>")
            if not C3PMJSON.FieldsChecker.name_is_ok(name):
                ColorP.print("Bad name: " + C3PMJSON.FieldsChecker.problem_with_name(name))
            else:
                self.__c3pm_dict["name"] = name
                break

        self.__c3pm_dict["author"] = input("Author>")
        self.__c3pm_dict["version"] = "0.0.1"
        self.__c3pm_dict["description"] = input("Description>")
        self.__c3pm_dict["url"] = input("Project URL>")
        self.__c3pm_dict["email"] = input("Project e-mail>")
        proj_license = input("License (empty line if not exist)>")
        if proj_license:
            self.__c3pm_dict["license"] = proj_license
        self.__c3pm_dict["dependencies"] = []
        self.__c3pm_dict["c3pm_version"] = self.version
        self.__c3pm_dict["whatIsC3pm"] = self.whatIsC3pm

    @property
    def name(self) -> str:
        return self.__c3pm_dict["name"]

    @name.setter
    def name(self, name: str):
        """
        :param name: new name
        :raises ValueError: if name is not a valid c3pm-project name
        """
        if not C3PMJSON.FieldsChecker.name_is_ok(name):
            raise ValueError(C3PMJSON.FieldsChecker.problem_with_name(name))
        self.__c3pm_dict["name"] = name

    @property
    def json_str(self) -> str:
        """
        :return: json str representation to be written for c3mp.json file
        """
        return json.dumps(self.__c3pm_dict, indent=4)

    def write(self):
        """
        Writes/re-writes c3mp.json
        """
        with open(C3PMJSON.C3PM_JSON_FILENAME, "w+") as c3pm_json_file:
            c3pm_json_file.write(self.json_str)

    def __check_c3pm_dict(self):
        """
        Checks is a self.__s3mp_dict which is parsed from c3pm.json is valid
        :raises C3PMJSON.BadC3PMJSONError: when self.__s3mp_dict is not valid
        """
        # name section
        if "name" not in self.__c3pm_dict:
            raise C3PMJSON.BadC3PMJSONError("no name")
        if not C3PMJSON.FieldsChecker.name_is_ok(self.__c3pm_dict["name"]):
            raise C3PMJSON.BadC3PMJSONError(C3PMJSON.FieldsChecker.
                                            problem_with_name(self.__c3pm_dict["name"]))

    class FieldsChecker:
        """
        Class-envelop for methods, which check value is a proper value for c3pm.json field

        Checkers return true
        """

        ALLOWED_CHARACTERS = "abcdefghijklmnopqrstuvwxyz-_"

        @staticmethod
        def name_is_ok(name: str) -> bool:
            """
            Checks name value
            :param name: value for name field of c3pm.json
            :return: True if all ok, False otherwise
            """
            return not bool(C3PMJSON.FieldsChecker.problem_with_name(name))

        @staticmethod
        def problem_with_name(name: str) -> str:
            """
            Checks name value
            :param name: value for name field of c3pm.json
            :return: empty line if all ok, str with problem text otherwise
            """
            if type(name) != str:
                return "name is not a string"
            if name == "":
                return "name is empty string"
            if len(name) > 100:
                return "length of name is greater than 100"
            for i, character in enumerate(name, start=1):
                if character not in C3PMJSON.FieldsChecker.ALLOWED_CHARACTERS:
                    return "name have bad character '" + character + "' (code " + str(ord(character)) \
                            + ") at position " + str(i)
            if name[0] not in C3PMJSON.FieldsChecker.ALLOWED_CHARACTERS[:-2]:
                return "first character is not a latin letter"
            if name[len(name) - 1] not in C3PMJSON.FieldsChecker.ALLOWED_CHARACTERS[:-2]:
                return "last character is not a latin letter"
            return ""

    class BadC3PMJSONError(Exception):
        """
        Raised when c3pm.json containment, on which class is constructed, is a valid json
        but is not a valid c3pm.json because of bad data

        Attributes:
            problem -- a reason why json is not a valid c3mp.json
        """

        def __init__(self, problem: str):
            self.problem = problem
