#!/usr/bin/env python3

import json
import sys
import base64 
from utils.conversions import poly2block, block2poly
from handlers.gfmul import gfmul
from field_element import FieldElement  
from handlers.arithmetic import ArithmeticHandler
from handlers.sea128 import *
from handlers.fde import FDEHandler

sea128 = SEA128Handler()
xex = FDEHandler()

ACTION_MAP = {
    "add_numbers": ArithmeticHandler.add_numbers,
    "subtract_numbers": ArithmeticHandler.subtract_numbers,
    "poly2block": poly2block,
    "block2poly": block2poly,
    "gfmul": gfmul,
    "sea128": sea128.sea128,
    "xex": xex.xex
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
    
    if "testcases" in data:
        responses = {}

        for testcase_id, testcase in data["testcases"].items():
            action = testcase.get("action")
            arguments = testcase.get("arguments", {})
            try:
                result = process_testcase(action, arguments)

                # Falls der resultierende Wert ein FieldElement ist, konvertiere ihn in einen Base64-Block
                if isinstance(result, FieldElement):
                    result = {"product": base64.b64encode(result.to_bytes()).decode('utf-8')}
                    
                responses[testcase_id] = result

            except ValueError as e:
                print(f"Fehler bei Testcase {testcase_id}: {e}", file=sys.stderr)

        output = {"responses": responses}
    else:
        action = data.get("action")
        arguments = data.get("arguments", {})

        try:
            output = process_testcase(action, arguments)

            # Falls der resultierende Wert ein FieldElement ist, konvertiere ihn in einen Base64-Block
            if isinstance(output, FieldElement):
                output = {"product": base64.b64encode(output.to_bytes()).decode('utf-8')}

        except ValueError as e:
            print(f"Fehler bei dem Testcase: {e}", file=sys.stderr)
            sys.exit(1)

    print(json.dumps(output, indent=4))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    main(input_file)
