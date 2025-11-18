from django import template

register = template.Library()


@register.filter(name='add_class')
def add_class(field, css_class):
    """Ajoute une classe CSS à un champ de formulaire."""
    if hasattr(field, 'field') and hasattr(field.field, 'widget'):
        attrs = field.field.widget.attrs.copy()
        classes = attrs.get('class', '').split()
        if css_class not in classes:
            classes.append(css_class)
        attrs['class'] = ' '.join(classes)
        field.field.widget.attrs = attrs
    return field

