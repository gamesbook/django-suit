from django.apps import apps
from suit.apps import DjangoSuitConfig


def get_config_instance(app_name=None):
    """
    :rtype: DjangoSuitConfig()
    """
    try:
        return apps.get_app_config(app_name or 'suit')
    except LookupError:
        return apps.get_app_config('suit')


#: :type: DjangoSuitConfig()
suit_config_cls = DjangoSuitConfig

def get_config(param=None, app_name=None):
    suit_config = get_config_instance(app_name)
    if param:
        value = getattr(suit_config, param, None)
        if value is None:
            value = getattr(suit_config_cls, param, None)
        return value

    return suit_config


def set_config_value(name, value):
    config = get_config()
    # Store previous value to reset later if needed
    prev_value_key = '_%s' % name
    if not hasattr(config, prev_value_key):
        setattr(config, prev_value_key, getattr(config, name))
        setattr(config, name, value)


def reset_config_value(name):
    config = get_config()
    prev_value_key = '_%s' % name
    if hasattr(config, prev_value_key):
        setattr(config, name, getattr(config, prev_value_key))
        del config.__dict__[prev_value_key]
