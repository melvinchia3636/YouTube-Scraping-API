import re
from itertools import chain

class Cipher:
    def __init__(self, js):
        self.transform_plan = self.get_transform_plan(js)
        var, _ = self.transform_plan[0].split(".")
        self.transform_map = self.get_transform_map(js, var)
        self.js_func_regex = re.compile(r"\w+\.(\w+)\(\w,(\d+)\)")

    def get_signature(self, ciphered_signature):
        signature = list(ciphered_signature)

        for js_func in self.transform_plan:
            name, argument = self.parse_function(js_func)  # type: ignore
            signature = self.transform_map[name](signature, argument)
        return "".join(signature)

    def parse_function(self, js_func: str):
        parse_match = self.js_func_regex.search(js_func)
        if not parse_match:
            raise Exception
        fn_name, fn_arg = parse_match.groups()
        return fn_name, int(fn_arg)

    def regex_search(self, pattern, string, group):
        regex = re.compile(pattern)
        results = regex.search(string)
        if not results:
            raise Exception
        return results.group(group)

    def get_initial_function_name(self, js):
        function_patterns = [
            r"\b[cs]\s*&&\s*[adf]\.set\([^,]+\s*,\s*encodeURIComponent\s*\(\s*(?P<sig>[a-zA-Z0-9$]+)\(",  # noqa: E501
            r"\b[a-zA-Z0-9]+\s*&&\s*[a-zA-Z0-9]+\.set\([^,]+\s*,\s*encodeURIComponent\s*\(\s*(?P<sig>[a-zA-Z0-9$]+)\(",  # noqa: E501
            r'(?:\b|[^a-zA-Z0-9$])(?P<sig>[a-zA-Z0-9$]{2})\s*=\s*function\(\s*a\s*\)\s*{\s*a\s*=\s*a\.split\(\s*""\s*\)',  # noqa: E501
            r'(?P<sig>[a-zA-Z0-9$]+)\s*=\s*function\(\s*a\s*\)\s*{\s*a\s*=\s*a\.split\(\s*""\s*\)',  # noqa: E501
            r'(["\'])signature\1\s*,\s*(?P<sig>[a-zA-Z0-9$]+)\(',
            r"\.sig\|\|(?P<sig>[a-zA-Z0-9$]+)\(",
            r"yt\.akamaized\.net/\)\s*\|\|\s*.*?\s*[cs]\s*&&\s*[adf]\.set\([^,]+\s*,\s*(?:encodeURIComponent\s*\()?\s*(?P<sig>[a-zA-Z0-9$]+)\(",  # noqa: E501
            r"\b[cs]\s*&&\s*[adf]\.set\([^,]+\s*,\s*(?P<sig>[a-zA-Z0-9$]+)\(",  # noqa: E501
            r"\b[a-zA-Z0-9]+\s*&&\s*[a-zA-Z0-9]+\.set\([^,]+\s*,\s*(?P<sig>[a-zA-Z0-9$]+)\(",  # noqa: E501
            r"\bc\s*&&\s*a\.set\([^,]+\s*,\s*\([^)]*\)\s*\(\s*(?P<sig>[a-zA-Z0-9$]+)\(",  # noqa: E501
            r"\bc\s*&&\s*[a-zA-Z0-9]+\.set\([^,]+\s*,\s*\([^)]*\)\s*\(\s*(?P<sig>[a-zA-Z0-9$]+)\(",  # noqa: E501
            r"\bc\s*&&\s*[a-zA-Z0-9]+\.set\([^,]+\s*,\s*\([^)]*\)\s*\(\s*(?P<sig>[a-zA-Z0-9$]+)\(",  # noqa: E501
        ]
        for pattern in function_patterns:
            regex = re.compile(pattern)
            function_match = regex.search(js)
            if function_match:
                return function_match.group(1)
        raise Exception

    def get_transform_plan(self, js):
        name = re.escape(self.get_initial_function_name(js))
        pattern = r"%s=function\(\w\){[a-z=\.\(\"\)]*;(.*);(?:.+)}" % name
        return self.regex_search(pattern, js, group=1).split(";")

    def get_transform_object(self, js, var):
        pattern = r"var %s={(.*?)};" % re.escape(var)
        regex = re.compile(pattern, flags=re.DOTALL)
        transform_match = regex.search(js)
        if not transform_match:
            raise Exception
        return transform_match.group(1).replace("\n", " ").split(", ")

    def get_transform_map(self, js, var):
        transform_object = self.get_transform_object(js, var)
        mapper = {}
        for obj in transform_object:
            # AJ:function(a){a.reverse()} => AJ, function(a){a.reverse()}
            name, function = obj.split(":", 1)
            fn = self.map_functions(function)
            mapper[name] = fn
        return mapper

    def reverse(self, arr, _):
        return arr[::-1]

    def splice(self, arr, b):
        return arr[b:]

    def swap(self, arr, b):
        r = b % len(arr)
        return list(chain([arr[r]], arr[1:r], [arr[0]], arr[r + 1 :]))

    def map_functions(self, js_func):
        mapper = (
            # function(a){a.reverse()}
            (r"{\w\.reverse\(\)}", self.reverse),
            # function(a,b){a.splice(0,b)}
            (r"{\w\.splice\(0,\w\)}", self.splice),
            # function(a,b){var c=a[0];a[0]=a[b%a.length];a[b]=c}
            (r"{var\s\w=\w\[0\];\w\[0\]=\w\[\w\%\w.length\];\w\[\w\]=\w}", self.swap),
            # function(a,b){var c=a[0];a[0]=a[b%a.length];a[b%a.length]=c}
            (
                r"{var\s\w=\w\[0\];\w\[0\]=\w\[\w\%\w.length\];\w\[\w\%\w.length\]=\w}",
                self.swap,
            ),
        )

        for pattern, fn in mapper:
            if re.search(pattern, js_func):
                return fn

        raise Exception
