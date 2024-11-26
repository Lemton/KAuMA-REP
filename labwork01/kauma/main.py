import json
import sys
import base64
from field_element import FieldElement
from handlers.conversions import poly2block, block2poly
from handlers.gfops import gfmul, gfdiv
from handlers.sea128 import SEA128Handler
from handlers.fde import FDEHandler
from handlers.gcm import GCMHandler
from handlers.padding_attack import decrypt_ciphertext
from handlers.gfpolyops import *

sea128 = SEA128Handler()
xex = FDEHandler()
gcm = GCMHandler()

ACTION_MAP = {
    "poly2block": poly2block,
    "block2poly": block2poly,
    "gfmul": gfmul,
    "gfdiv": gfdiv,
    "sea128": sea128.sea128,
    "xex": xex.xex,
    "padding_oracle": decrypt_ciphertext,
    "gcm_encrypt": gcm.gcm_encrypt_action,
    "gcm_decrypt": gcm.gcm_decrypt_action,
    "gfpoly_add": gfpoly_add,
    "gfpoly_divmod": gfpoly_divmod,
    "gfpoly_mul": gfpoly_mul,
    "gfpoly_pow": gfpoly_pow,
    "gfpoly_powmod": gfpoly_powmod,
    "gfpoly_sort": gfpoly_sort,
    "gfpoly_gcd": gfpoly_gcd,
    "gfpoly_make_monic": gfpoly_make_monic,
    "gfpoly_sqrt": gfpoly_sqrt,
    "gfpoly_diff": gfpoly_diff,
    "gfpoly_factor_sff": gfpoly_factor_sff,
}


def process_testcase(action, arguments):
    """Verarbeitet die Aktion basierend auf der ACTION_MAP."""
    if action in ACTION_MAP:
        return ACTION_MAP[action](arguments)
    raise ValueError(f"Unbekannte Aktion: {action}")


def handle_result(result):
    """Konvertiert ein Ergebnis in das gewünschte Format."""
    if isinstance(result, FieldElement):
        return {"product": base64.b64encode(result.to_bytes()).decode("utf-8")}
    return result


def process_all_testcases(testcases):
    """Prozessiert alle Testcases sequentiell."""
    responses = {}
    errors = {}

    for testcase_id, testcase in testcases.items():
        action = testcase.get("action")
        arguments = testcase.get("arguments", {})
        try:
            result = process_testcase(action, arguments)
            responses[testcase_id] = handle_result(result)
        except Exception as e:
            errors[testcase_id] = str(e)

    if errors:
        print(f"Fehler in Testcases: {errors}", file=sys.stderr)

    return responses


def main(input_file):
    with open(input_file, "r") as file:
        data = json.load(file)

    if "testcases" in data:
        # Mehrere Testcases
        responses = process_all_testcases(data["testcases"])
        output = {"responses": responses}
    else:
        # Einzelner Testcase
        action = data.get("action")
        arguments = data.get("arguments", {})
        try:
            result = process_testcase(action, arguments)
            output = handle_result(result)
        except ValueError as e:
            print(f"Fehler bei dem Testcase: {e}", file=sys.stderr)
            sys.exit(1)

    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    main(input_file)
