from review_agents.structure_reviewer import build_structure_agent
from review_agents.base import review


BAD_STRUCTURE_CODE = """
def process_order(order):
    validate_order(order)
    calculate_price(order)
    save_order(order)
    send_email(order)
    update_inventory(order)
    generate_invoice(order)
    log_order(order)
    notify_customer(order)
"""


BAD_STRUCTURE_CODE_2 = """
def register_user(user):
    validate_email(user.email)
    hash_password(user.password)
    save_to_database(user)
    send_welcome_email(user.email)
    create_user_profile(user)
    write_audit_log(user)
"""


CLEAN_STRUCTURE_CODE = """
def calculate_total(prices, tax_rate):
    subtotal = sum(prices)
    return subtotal * (1 + tax_rate)


def save_order(order, database):
    database.save(order)


def notify_customer(customer, message):
    customer.send(message)
"""


agent = build_structure_agent()

print("=== Bad structure snippet ===")
result1 = review(agent, BAD_STRUCTURE_CODE, "structure")
print(result1.model_dump_json(indent=2))


print("\n=== Bad structure snippet 2 ===")
result2 = review(agent, BAD_STRUCTURE_CODE_2, "structure")
print(result2.model_dump_json(indent=2))


print("\n=== Clean structure snippet ===")
result3 = review(agent, CLEAN_STRUCTURE_CODE, "structure")
print(result3.model_dump_json(indent=2))