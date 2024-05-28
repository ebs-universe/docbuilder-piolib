import json
import os

# Define the mapping of Doxygen variables to JSON paths
lib_var_map = {
    "PROJECT_NAME": ["name"],
    "PROJECT_VERSION": ["version"],
    "PROJECT_BRIEF": ["description"],
}

doxygen_var_map = {
    "INCLUDE_PATH": ["include_path"],
}

def get_nested_value(data, keys):
    """Fetches a value from a nested dictionary using a list of keys."""
    for key in keys:
        data = data.get(key)
        if data is None:
            return ""
    return data

def generate_doxyfile():
    # Load the library.json file
    with open('../library.json', 'r') as lib_file:
        data = json.load(lib_file)

    with open('../doxygen.json', 'r') as doxygen_file:
        doxygen_data = json.load(doxygen_file)

    # Read the Doxyfile.in template
    with open('Doxyfile.in', 'r') as template_file:
        doxyfile_content = template_file.read()

    for var, json_path in lib_var_map.items():
        value = get_nested_value(data, json_path)
        placeholder = f'@{var}@'
        doxyfile_content = doxyfile_content.replace(placeholder, value)

    for var, json_path in doxygen_var_map.items():
        value = get_nested_value(doxygen_data, json_path)
        placeholder = f'@{var}@'
        doxyfile_content = doxyfile_content.replace(placeholder, value)

    doxyfile_content.replace("@BASE_PATH@", os.path.abspath(os.path.join(os.getcwd(), os.pardir)))

    # Write the generated Doxyfile
    with open('Doxyfile', 'w') as doxyfile:
        doxyfile.write(doxyfile_content)

    print('Doxyfile generated successfully.')

if __name__ == "__main__":
    generate_doxyfile()