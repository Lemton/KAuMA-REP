import json
import sys
from handlers.arithmetic import ArithmeticHandler
from handlers.polynomial import PolynomialHandler
from handlers.GaloisField128 import GaloisField128Handler
from handlers.sea128 import SEA128Handler
from handlers.fde import FDEHandler


ACTION_MAP = {
    "add_numbers": ArithmeticHandler.add_numbers,
    "subtract_numbers": ArithmeticHandler.subtract_numbers,
    "poly2block": PolynomialHandler.poly2block,
    "block2poly" : PolynomialHandler.block2poly,
    "gfmul" : GaloisField128Handler.gfmul,
    "sea128" : SEA128Handler.sea128,
    "xex": FDEHandler.xex 
}

def process_testcase(action, arguments):
    """Verarbeitet die Aktion basierend auf der ACTION_MAP."""
    if action in ACTION_MAP:
        return ACTION_MAP[action](arguments)
    else:
        raise ValueError(f"Unbekannte Aktion: {action}")

def main(input_file):
    with open(input_file, 'r') as file:
        data = json.load(file)
    
    #print(f"Geladene Daten: {data}")

    
    if "testcases" in data:
        responses = {}

        for testcase_id, testcase in data["testcases"].items():
            action = testcase.get("action")
            arguments = testcase.get("arguments", {})
            try:
                result = process_testcase(action, arguments)
                responses[testcase_id] = result
            except ValueError as e:
                print(f"Fehler bei Testcase {testcase_id}: {e}", file=sys.stderr)

        output = {"responses": responses}
    else:
        action = data.get("action")
        arguments = data.get("arguments", {})

        try:
            output = process_testcase(action, arguments)
        except ValueError as e:
            print(f"Fehler bei dem Testcase: {e}", file=sys.stderr)
            sys.exit(1)

    
    print(json.dumps(output))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    main(input_file)
