import os
import json
from typing import List, Dict, Any

def get_input(prompt: str, default: str = "") -> str:
    """Get user input with an optional default value."""
    if default:
        result = input(f"{prompt} [{default}]: ").strip()
        return result if result else default
    return input(f"{prompt}: ").strip()

def get_list_input(prompt: str) -> List[str]:
    """Get a list of items from user input."""
    print(f"\n{prompt}")
    print("Enter one item per line. Press Enter twice when done.")
    items = []
    while True:
        item = input().strip()
        if not item:
            if items:
                break
            print("Please enter at least one item.")
            continue
        items.append(item)
    return items

def get_bool_input(prompt: str, default: bool = True) -> bool:
    """Get a yes/no response from user input."""
    default_str = "Y/n" if default else "y/N"
    while True:
        response = input(f"{prompt} [{default_str}]: ").strip().lower()
        if not response:
            return default
        if response in ["y", "yes"]:
            return True
        if response in ["n", "no"]:
            return False
        print("Please enter 'y' or 'n'")

def get_int_input(prompt: str, default: int, min_val: int = 1) -> int:
    """Get an integer value from user input."""
    while True:
        try:
            response = input(f"{prompt} [{default}]: ").strip()
            if not response:
                return default
            value = int(response)
            if value < min_val:
                print(f"Please enter a number >= {min_val}")
                continue
            return value
        except ValueError:
            print("Please enter a valid number")

def create_config() -> Dict[str, Any]:
    """Create a new crawler configuration interactively."""
    print("\n🤖 DeepSeek Web Crawler Configuration Generator\n")
    
    # Basic Information
    print("📝 Basic Information")
    print("-" * 50)
    config_name = get_input("Configuration name (e.g., amazon_products)")
    base_url = get_input("Target website URL")
    css_selector = get_input("CSS selector for items (e.g., div.product-card)")

    # Required and Optional Fields
    print("\n🔑 Data Fields")
    print("-" * 50)
    print("Define the fields to extract from each item:")
    required_keys = get_list_input("Enter required fields (e.g., title, price, description):")
    has_optional = get_bool_input("\nDo you want to add optional fields?")
    optional_keys = []
    if has_optional:
        optional_keys = get_list_input("Enter optional fields:")

    # Crawler Settings
    print("\n⚙️ Crawler Settings")
    print("-" * 50)
    multi_page = get_bool_input("Enable multi-page crawling?")
    max_pages = 1
    delay = 2
    if multi_page:
        max_pages = get_int_input("Maximum number of pages to crawl", 5)
        delay = get_int_input("Delay between pages (seconds)", 2)

    headless = get_bool_input("Run in headless mode (no visible browser)?")
    verbose = get_bool_input("Enable verbose logging?")

    # LLM Instructions
    print("\n🧠 LLM Configuration")
    print("-" * 50)
    print("Define extraction instructions for the LLM.")
    print("Default instructions will be generated based on your fields.")
    custom_instructions = get_bool_input("Do you want to provide custom instructions?")
    
    if custom_instructions:
        print("\nEnter your custom instructions. Press Enter twice when done:")
        instructions = []
        while True:
            line = input()
            if not line and instructions:
                break
            instructions.append(line)
        llm_instructions = "\n".join(instructions)
    else:
        # Generate default instructions based on fields
        llm_instructions = "Extract information from each item:\n\n"
        llm_instructions += "Required information:\n"
        for key in required_keys:
            llm_instructions += f"- {key}: Extract the {key}\n"
        if optional_keys:
            llm_instructions += "\nAdditional information if present:\n"
            for key in optional_keys:
                llm_instructions += f"- {key}: Extract the {key}\n"

    # Create the configuration
    config = {
        "BASE_URL": base_url,
        "CSS_SELECTOR": css_selector,
        "REQUIRED_KEYS": required_keys,
        "OPTIONAL_KEYS": optional_keys,
        "CRAWLER_CONFIG": {
            "MULTI_PAGE": multi_page,
            "MAX_PAGES": max_pages,
            "DELAY_BETWEEN_PAGES": delay,
            "HEADLESS": headless,
            "CACHE_ENABLED": False,
            "VERBOSE_LOGGING": verbose,
        },
        "LLM_CONFIG": {
            "PROVIDER": "groq/deepseek-r1-distill-llama-70b",
            "EXTRACTION_TYPE": "schema",
            "INPUT_FORMAT": "markdown",
            "INSTRUCTION": llm_instructions,
        }
    }

    # Save the configuration
    print("\n💾 Saving Configuration")
    print("-" * 50)
    
    # Format the configuration as Python code
    config_str = f'"{config_name}": {{\n'
    config_str += '    **DEFAULT_CONFIG,\n'
    for key, value in config.items():
        if isinstance(value, str):
            config_str += f'    "{key}": "{value}",\n'
        else:
            config_str += f'    "{key}": {json.dumps(value, indent=8)[1:-1]},\n'
    config_str += "}"

    print("\nAdd this to your config.py file in the CONFIGS dictionary:\n")
    print(config_str)

    save = get_bool_input("\nWould you like to automatically add this to config.py?")
    if save:
        try:
            with open("config.py", "r") as f:
                content = f.read()
            
            # Find the end of the CONFIGS dictionary
            configs_end = content.rindex("}")
            
            # Insert the new configuration before the closing brace
            new_content = (
                content[:configs_end] +
                ",\n\n    # Added by configuration generator\n    " +
                config_str +
                content[configs_end:]
            )
            
            with open("config.py", "w") as f:
                f.write(new_content)
            
            print("\n✅ Configuration added to config.py successfully!")
            print(f"\nYou can now run your crawler with:\npython main.py --config {config_name}")
        except Exception as e:
            print(f"\n❌ Error saving to config.py: {str(e)}")
            print("Please manually add the configuration shown above to your config.py file.")
    
    return config

if __name__ == "__main__":
    try:
        create_config()
    except KeyboardInterrupt:
        print("\n\n❌ Configuration creation cancelled.")
