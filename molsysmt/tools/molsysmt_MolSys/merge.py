def merge(item_1, item_2, check_form=True):

    tmp_item = extract(item_1)
    tmp_item.add(item_2)

    return tmp_item

