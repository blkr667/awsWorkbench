from cf import template_factory


def generate_template_json():
    template = template_factory.create_template()
    return template.to_yaml()
