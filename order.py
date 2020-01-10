class Files:
    name = ""
    page_count = ""


class Order:

    uid = ""
    status = ""
    number = ""
    subject = ""
    copies = ""
    duplex = ""
    collation = ""
    stapling = ""
    drilling = ""
    folding = ""
    cutting = ""
    front_cover = ""
    back_cover = ""
    slipsheets = ""
    special_instructions = ""

    paper = ""
    paper_size = ""
    paper_color = ""
    paper_weight = ""

    date = ""
    first_name = ""
    last_name = ""
    email = ""
    bill_to = ""
    deliver_to_name = ""
    deliver_to_address = ""

    page_counts = ""
    files = [Files()]


orders = Order()
orders.files[0].page_count
