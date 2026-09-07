import os
from pathlib import Path

from utils.cleaner import clean_text


INPUT_FOLDER = Path("test_data/extracted")
OUTPUT_FOLDER = Path("test_data/cleaned")


CONTRACT_TYPES = [
    "employee_contract",
    "nda_contract",
    "rental_contract",
    "service_contract",
]


def clean_contract_type(contract_type):
    """
    Clean all extracted text files belonging to one contract type.
    """

    input_folder = INPUT_FOLDER / contract_type
    output_folder = OUTPUT_FOLDER / contract_type

    output_folder.mkdir(parents=True, exist_ok=True)

    if not input_folder.exists():
        print(f"\nWARNING: Folder not found: {input_folder}")
        return 0, 0

    files = sorted(
        file
        for file in input_folder.iterdir()
        if file.is_file() and file.suffix.lower() == ".txt"
    )

    if not files:
        print(f"\nWARNING: No extracted files found in {input_folder}")
        return 0, 0

    passed = 0
    failed = 0

    print("\n" + "=" * 80)
    print(f"{contract_type.upper()}")
    print("=" * 80)

    for input_path in files:

        output_path = output_folder / input_path.name

        try:
            with open(
                input_path,
                "r",
                encoding="utf-8"
            ) as file:
                raw_text = file.read()

            cleaned_text = clean_text(raw_text)

            with open(
                output_path,
                "w",
                encoding="utf-8"
            ) as file:
                file.write(cleaned_text)

            # Basic validation
            if not cleaned_text.strip():
                raise ValueError("Cleaner produced empty output.")

            print(
                f"PASS  {input_path.name:<40} "
                f"{len(raw_text):>8} -> {len(cleaned_text):>8} chars"
            )

            passed += 1

        except Exception as error:

            print(
                f"FAIL  {input_path.name:<40} "
                f"{error}"
            )

            failed += 1

    return passed, failed


def test_cleaner():

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    total_passed = 0
    total_failed = 0

    for contract_type in CONTRACT_TYPES:

        passed, failed = clean_contract_type(contract_type)

        total_passed += passed
        total_failed += failed

    total = total_passed + total_failed

    print("\n" + "=" * 80)
    print("CLEANER TEST SUMMARY")
    print("=" * 80)

    print(f"Total files : {total}")
    print(f"Passed      : {total_passed}")
    print(f"Failed      : {total_failed}")

    if total_failed == 0:
        print("\nResult: ALL CLEANER TESTS PASSED")
    else:
        print("\nResult: SOME CLEANER TESTS FAILED")


if __name__ == "__main__":
    test_cleaner()