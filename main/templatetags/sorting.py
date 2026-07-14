from django import template


register = template.Library()


@register.inclusion_tag("main/includes/sortable_header.html", takes_context=True)
def sortable_header(context, label, sort_key):
    current_key = context.get("sort_key")
    current_direction = context.get("sort_direction", "asc")
    is_active = current_key == sort_key
    next_direction = "desc" if is_active and current_direction == "asc" else "asc"

    query = context["request"].GET.copy()
    query["sort"] = sort_key
    query["direction"] = next_direction

    return {
        "label": label,
        "is_active": is_active,
        "current_direction": current_direction,
        "next_direction": next_direction,
        "query_string": query.urlencode(),
    }
