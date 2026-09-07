import json
from pathlib import Path

from utils.segmenter import segment_clauses


INPUT_FOLDER = Path("test_data/cleaned")
OUTPUT_FOLDER = Path("test_data/segmented")


CONTRACT_TYPES = [
    "employee_contract",
    "nda_contract",
    "rental_contract",
    "service_contract",
]


def segment_contract_type(contract_type):
    """
    Segment all cleaned files belonging to one contract type.
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
        print(
            f"\nWARNING: No cleaned files found in "
            f"{input_folder}"
        )
        return 0, 0

    passed = 0
    failed = 0

    print("\n" + "=" * 80)
    print(f"{contract_type.upper()}")
    print("=" * 80)

    for input_path in files:

        output_path = (
            output_folder /
            f"{input_path.stem}.json"
        )

        try:

            # -------------------------------------------------
            # Read cleaned text
            # -------------------------------------------------

            with open(
                input_path,
                "r",
                encoding="utf-8"
            ) as file:
                text = file.read()

            if not text.strip():
                raise ValueError(
                    "Input file is empty."
                )

            # -------------------------------------------------
            # Segment document
            # -------------------------------------------------

            segments = segment_clauses(text)

            if not segments:
                raise ValueError(
                    "Segmenter produced no segments."
                )

            # -------------------------------------------------
            # Basic structural validation
            # -------------------------------------------------

            required_fields = {
                "clause_id",
                "parent_clause",
                "section",
                "section_title",
                "text",
                "type"
            }

            for segment in segments:

                missing_fields = (
                    required_fields -
                    set(segment.keys())
                )

                if missing_fields:
                    raise ValueError(
                        "Segment is missing fields: "
                        f"{missing_fields}"
                    )

                if not segment["text"].strip():
                    raise ValueError(
                        "Segment contains empty text."
                    )

            # -------------------------------------------------
            # Save segmented output
            # -------------------------------------------------

            with open(
                output_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    segments,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            # -------------------------------------------------
            # Print summary
            # -------------------------------------------------

            clause_count = sum(
                1
                for segment in segments
                if segment["type"] == "clause"
            )

            section_count = sum(
                1
                for segment in segments
                if segment["type"] == "section"
            )

            annexure_count = sum(
                1
                for segment in segments
                if segment["type"] == "annexure"
            )

            schedule_count = sum(
                1
                for segment in segments
                if segment["type"] == "schedule"
            )

            document_count = sum(
                1
                for segment in segments
                if segment["type"] == "document"
            )

            print(
                f"PASS  {input_path.name:<35} "
                f"segments={len(segments):<4} "
                f"clauses={clause_count:<4} "
                f"sections={section_count:<3} "
                f"annexures={annexure_count:<2} "
                f"schedules={schedule_count:<2}"
            )

            passed += 1

        except Exception as error:

            print(
                f"FAIL  {input_path.name:<35} "
                f"{error}"
            )

            failed += 1

    return passed, failed


def test_segmenter():

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    total_passed = 0
    total_failed = 0

    for contract_type in CONTRACT_TYPES:

        passed, failed = segment_contract_type(
            contract_type
        )

        total_passed += passed
        total_failed += failed

    total = total_passed + total_failed

    print("\n" + "=" * 80)
    print("SEGMENTER TEST SUMMARY")
    print("=" * 80)

    print(f"Total files : {total}")
    print(f"Passed      : {total_passed}")
    print(f"Failed      : {total_failed}")

    if total_failed == 0:

        print("\nResult: ALL SEGMENTER TESTS PASSED")

    else:

        print("\nResult: SOME SEGMENTER TESTS FAILED")


if __name__ == "__main__":
    test_segmenter()