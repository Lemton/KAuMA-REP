import json
import sys

from handlers.arithmetic import ArithmeticHandler

ACTION_MAP = {
    "add_numbers": ArithmeticHandler.add_numbers,
    "subtract_numbers": ArithmeticHandler.subtract_numbers,
    #"poly2block": PolynomialHandler.poly2block
}

def process_testcase(action, arguments):
    """Verarbeitet die Aktion dynamisch basierend auf der ACTION_MAP."""
    # Überprüfen, ob die Aktion in unserem Mapping existiert
    if action in ACTION_MAP:
        # Rufe die entsprechende Funktion aus dem Mapping auf
        return ACTION_MAP[action](arguments)
    else:
        raise ValueError(f"Unbekannte Aktion: {action}")
    
def main(input_file):
  
    with open(input_file, 'r') as file:
        data = json.load(file)

   
    responses = {}

 
    for testcase_id, testcase in data.get("testcases", {}).items():
        action = testcase.get("action")
        arguments = testcase.get("arguments", {})

        
        try:
            result = process_testcase(action, arguments)
            responses[testcase_id] = result
        except ValueError as e:
            print(f"Fehler bei Testcase {testcase_id}: {e}", file=sys.stderr)


    output = {"responses": responses}


    print(json.dumps(output, indent=4))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    main(input_file)
