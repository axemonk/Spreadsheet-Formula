APP_SUFFIXES = [
    'excel',
    'google',
    'libre',
]

class SpreadsheetFunction(object):
    """Metadata about a function for a spreadsheet application"""

    def __init__(self, name: str, description: str = None, family: str = None,
                 required_args: list[str] = None,
                 optional_args: list[str] = None,
                 has_ellipsis: bool = False):
        super(SpreadsheetFunction, self).__init__()
        self.name = name
        self.description = description
        self.family = family
        self.required_args = required_args
        self.optional_args = optional_args
        self.has_ellipsis = has_ellipsis

    @staticmethod
    def from_json(json_obj):
        """This is the temporary transfer format"""
        return SpreadsheetFunction(
            json_obj.get('func_name'),
            description = json_obj.get('func_desc', None),
            family = json_obj.get('func_cat', None),
            required_args = json_obj.get('req_param', None),
            optional_args = json_obj.get('opt_param', None),
            has_ellipsis = json_obj.get('ellipsis', False),
        )

    def to_json(self) -> str:
        """This is the temporary transfer format"""
        output = dict(
            func_name = self.name,
            func_cat = self.family,
            func_desc = self.description,
            is_nullary = not (self.required_args or self.optional_args),
            comp_str = self.to_completion_arg_string(),
            req_param = self.required_args,
            opt_param = self.optional_args,
            ellipsis = self.has_ellipsis,
        )
        return {k:output[k] for k in output if output[k] is not None}

    def to_arg_list(self) -> list[str]:
        args = []
        if self.required_args:
            args += self.required_args
        if self.optional_args:
            args += [f'[{a}]' for a in self.optional_args]
        if self.has_ellipsis:
            args += ['...']
        return args

    def to_arg_string(self) -> str:
        return ', '.join(self.to_arg_list())

    def to_completion_arg_string(self) -> str:
        completions = []
        param_id = 0

        if self.required_args:
            for req in self.required_args:
                param_id += 1

                if param_id > 1:
                    completions.append(',')
                    completions.append(f'${{{param_id}: {req}}}')
                else:
                    completions.append(f'${{{param_id}:{req}}}')

        if self.optional_args:
            num_opt_param = len(self.optional_args)
            num_param = num_opt_param + len(self.required_args or [])

            # Wrap optional arguments in an extra tabstop
            param_id += 1
            completions.append(f'${{{param_id}:')

            for opt in self.optional_args:
                param_id += 1

                if param_id == num_param + 1 and self.has_ellipsis:
                    completions.append(f',${{{param_id}: [{opt}], ...}}')
                else:
                    completions.append(f',${{{param_id}: [{opt}]}}')

            completions.append('}')

        return f'{self.name}({"".join(completions)})'

    def to_sublime_word_completion(self) -> dict[str,str]:
        return {
            "trigger": self.name,
            "contents": self.name,
            "annotation": self.family,
            "details": self.description,
            "kind": "function",
        }

    def to_sublime_snippet_completion(self) -> dict[str,str]:
        return {
            "trigger": self.name,
            "contents": self.to_completion_arg_string(),
            "annotation": self.family,
            "details": self.description,
            "kind": "snippet",
        }
