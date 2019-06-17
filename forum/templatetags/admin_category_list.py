from django.contrib.admin.templatetags.admin_list import (
    ResultList, register, items_for_result,
    result_hidden_fields, result_headers,
    )


def show_children(res):
    for child in res.children.all():
        yield child
        if child.children.all():
            yield from show_children(child)


def results(cl):
    if cl.formset:
        for res, form in zip(cl.result_list, cl.formset.forms):
            if not res.parent:
                yield ResultList(form, items_for_result(cl, res, form))
                if res.children.all():
                    results_children = show_children(res)
                    for child in results_children:
                        yield ResultList(form, items_for_result(cl, child, form))
    else:
        for res in cl.result_list:
            if not res.parent:
                yield ResultList(None, items_for_result(cl, res, None))
                if res.children.all():
                    results_children = show_children(res)
                    for child in results_children:
                        yield ResultList(None, items_for_result(cl, child, None))


def admin_category_list(cl):
    """
    Display the headers and data list together.
    """
    headers = list(result_headers(cl))
    num_sorted_fields = 0
    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1
    return {
        'cl': cl,
        'result_hidden_fields': list(result_hidden_fields(cl)),
        'result_headers': headers,
        'num_sorted_fields': num_sorted_fields,
        'results': list(results(cl)),
    }


register.inclusion_tag('admin/category_list_results.html')(admin_category_list)
