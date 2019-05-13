import json


### DEFAULT METHODS ###


_default_methods = {}
def _add_fuction_to_methods_dict(name):
    def decorator(function):
        _default_methods[name] = function
    return decorator


@_add_fuction_to_methods_dict('undefinedMethod')
def _undefinedMethod(method_name):
    return json.dumps({
        'error':"Method '{}' doesn't exist.".format(method_name)})

@_add_fuction_to_methods_dict('missedArgument')
def _missedArgument(method_name, argument_name):
    return json.dumps({
        'error': "Method '{}' missing required argument: '{}'.".format(
            method_name, argument_name)})

@_add_fuction_to_methods_dict('wrongValueType')
def _wrongValueType(method_name, arg_name, arg, right_arg_type):
    return json.dumps({
        'error': "Argument '{}' in method '{}' mast be {}.".format(
            arg_name, method_name, right_arg_type),
        'data': {arg_name: arg} })

@_add_fuction_to_methods_dict('wrongAccessCode')
def _wrongAccessCode( method_name, target_access_code):
    return json.dumps({
        'error': "Method '{}' requiers access code {}.".format(
            method_name, target_access_code) })


### MAIN ###


class ApiExeptionHelper(Exception):
    def __init__(self, name, *args, **kwargs):
        super().__init__('ApiExeptionHelper {} rised.'.format(name))
        self.name = name
        self.args = args
        self.kwargs = kwargs


class ApiExeptions:
    def __init__(self):
        self.methods = _default_methods
    
    def method(self, name):  # decorator
        def decorator(function):
            def wrapper(*args, **kwargs):
                response = function(*args, **kwargs)
                return response
            self.methods[name] = wrapper
        return decorator

    def get(self, method_name):
        return self.methods[method_name]

