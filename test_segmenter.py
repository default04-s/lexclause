from utils.segmenter import segment_clauses

with open("data/rental_contract.txt", "r", encoding="utf-8") as f:
      text = f.read()

clauses = segment_clauses(text)

print(f"Found {len(clauses)} clauses\n")

for i, clause in enumerate(clauses, 1):
    print(f"\n--- Clause {i} ---")
    print(clause[:200])  # Print first 200 characters