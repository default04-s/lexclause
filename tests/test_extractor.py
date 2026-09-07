import os
from utils.extractor import extract_text


BASE_FOLDER = "test_data"

CONTRACT_TYPES = [
    "employee_contract",
    "nda_contract",
    "rental_contract",
    "service_contract"
]

OUTPUT_FOLDER = os.path.join(BASE_FOLDER, "extracted")

SUPPORTED_EXTENSIONS = (".pdf", ".docx")


os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def test_extraction():

    total_contracts = 0
    successful = 0
    failed = 0

    print("\n" + "=" * 80)
    print("LEXCLAUSE - EXTRACTION TEST")
    print("=" * 80)

    for contract_type in CONTRACT_TYPES:

        contract_folder = os.path.join(
            BASE_FOLDER,
            contract_type
        )

        output_folder = os.path.join(
            OUTPUT_FOLDER,
            contract_type
        )

        os.makedirs(output_folder, exist_ok=True)

        if not os.path.exists(contract_folder):
            print(f"\nWARNING: Folder not found: {contract_folder}")
            continue

        files = sorted(
            filename
            for filename in os.listdir(contract_folder)
            if filename.lower().endswith(SUPPORTED_EXTENSIONS)
        )

        print("\n" + "-" * 80)
        print(f"CONTRACT TYPE: {contract_type}")
        print("-" * 80)

        if not files:
            print("No supported contracts found.")
            continue

        for filename in files:

            total_contracts += 1

            file_path = os.path.join(
                contract_folder,
                filename
            )

            output_name = (
                os.path.splitext(filename)[0] + ".txt"
            )

            output_path = os.path.join(
                output_folder,
                output_name
            )

            print(f"\nProcessing: {filename}")

            try:

                text = extract_text(file_path)

                if not text.strip():
                    raise ValueError(
                        "Extraction returned empty text."
                    )

                with open(
                    output_path,
                    "w",
                    encoding="utf-8"
                ) as file:
                    file.write(text)

                print("Status: PASS")
                print(f"Characters extracted: {len(text)}")
                print(f"Saved to: {output_path}")

                successful += 1

            except Exception as error:

                print("Status: FAIL")
                print(f"Error: {error}")

                failed += 1

    print("\n" + "=" * 80)
    print("EXTRACTION TEST SUMMARY")
    print("=" * 80)

    print(f"Total contracts : {total_contracts}")
    print(f"Successful      : {successful}")
    print(f"Failed          : {failed}")

    if failed == 0:
        print("\nALL EXTRACTION TESTS PASSED.")
    else:
        print("\nSOME EXTRACTION TESTS FAILED.")


if __name__ == "__main__":
    test_extraction()