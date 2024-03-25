import json




def get_response_text(category_name, customer_name):
    """Get response text based on a category name."""
    
    template_map_file = "resources/template_map.json"
    with open(template_map_file, 'r') as file:
        template_map = json.load(file)
    
    template_file_path = template_map.get(category_name)

    if template_file_path:
        try:
            with open(template_file_path, 'r') as template_file:
                template_text = template_file.read()

                if not customer_name:
                    customer_name = "Customer"

                response_text = template_text.replace("[CustomerName]", customer_name)
                return response_text

        except FileNotFoundError:
            print(f"File not found: {template_file_path}")

    else:
        print(f"No template found for category: {category_name}")

    return None
