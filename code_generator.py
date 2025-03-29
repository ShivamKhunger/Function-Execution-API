class ScriptMaker:
    @staticmethod
    def create_script(function_name, params=None):
        param_str = f"'{params}'" if params else ""
        
        script = f"""from automation_functions import AutomationTools
import sys

def main():
    try:
        tools = AutomationTools()
        result = tools.{function_name}({param_str})
        print(f"Done! Result: {{result}}")
    except Exception as e:
        print(f"Oops, something went wrong: {{e}}", file=sys.stderr)

if __name__ == "__main__":
    main()
"""
        return script.strip()