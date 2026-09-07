import re


# ============================================================
# PATTERNS
# ============================================================

# Top-level numbered clauses:
#
# 1. Definitions
# 2. Confidentiality
# 1.The agreement...
#
TOP_LEVEL_PATTERN = re.compile(
    r'^(?P<number>\d+)\.(?P<separator>\s*|\t*)(?P<title>.*)$'
)

# Nested clauses:
#
# 1.1 Definitions
# 1.2.The parties...
# 1.8.1 Confidential Information
# 7.3.
#
SUBCLAUSE_PATTERN = re.compile(
    r'^(?P<number>\d+(?:\.\d+)+)\.?\s*(?P<title>.+?)\s*$'
)

# Annexures / schedules:
#
# ANNEXURE-I
# ANNEXURE I
# ANNEXURE: I
# SCHEDULE 1
# SCHEDULE 2: TECHNICAL SPECIFICATIONS
#
# Does NOT match Schedule 2.1
#
ATTACHMENT_PATTERN = re.compile(
    r'^(?P<kind>ANNEXURE|ANNEX|SCHEDULE|APPENDIX|EXHIBIT)'
    r'(?:\s*[-–—:]\s*|\s+)'
    r'(?P<number>[A-Z]+|\d+|[IVX]+)'
    r'(?!\.)'
    r'(?:\s*[-–—:]\s*|\s*:\s*|\s+|$)'
    r'(?P<title>.*)$',
    re.IGNORECASE
)

UPPERCASE_HEADING_PATTERN = re.compile(
    r'^[A-Z][A-Z0-9&/,()\-\'":; ]{2,120}$'
)

LETTER_HEADING_PATTERN = re.compile(
    r'^(?P<marker>[A-Z])[\.\)]\s+(?P<title>.+)$'
)

NUMBERED_ITEM_PATTERN = re.compile(
    r'^(?P<number>\d+)\.(?P<separator>\s+|\t*)(?P<title>.+)$'
)


# ============================================================
# CONSTANTS
# ============================================================

IGNORED_NAMED_HEADINGS = {
    "BY AND BETWEEN",
    "WHEREAS",
    "NOW THEREFORE",
    "NOW, THEREFORE",
    "IN WITNESS WHEREOF",
    "SIGNATURES",
    "SIGNATURE",
    "WITNESSES",
    "THIS AGREEMENT",
    "NON DISCLOSURE AGREEMENT",
    "NON-DISCLOSURE AGREEMENT",
    "CONFIDENTIALITY AGREEMENT",
    "EMPLOYMENT AGREEMENT",
    "SERVICE AGREEMENT",
    "SERVICE CONTRACT",
    "RENT AGREEMENT",
    "RENTAL AGREEMENT",
    "LEASE AGREEMENT",
    "CONTENTS",
    "DRAFT FORMAT",
    "DISCLAIMER",
    "COPYRIGHT",
    "NOTE",
    "HIGHLIGHTS",
    "OWNER",
    "TENANT",
    "LANDLORD",
    "LESSOR",
    "LESSEE",
    "EMAIL",
    "MOBILE",
    "PHONE",
    "ADDRESS",
    "PERMANENT ADDRESS",
    "FIRST PART",
    "SECOND PART",
    "FIRST PARTY",
    "SECOND PARTY",
    "MANAGEMENT COMPANY",
    "CONTACT DETAILS",
    "CONTACT INFORMATION",
    "BANK DETAILS",
    "BANK ACCOUNT DETAILS",
    "PROPERTY DETAILS",
    "OWNER DETAILS",
    "TENANT DETAILS",
    "EMPLOYEE DETAILS",
    "EMPLOYER DETAILS",
}

# Single-word title-case headings are dangerous because
# ordinary form fields such as "Owner", "Email", "Mobile"
# can look like headings.
#
# Therefore only known legal/document headings are allowed
# to pass the single-word title-case rule.
KNOWN_SINGLE_WORD_HEADINGS = {
    "Interpretation",
    "Position",
    "Compensation",
    "Termination",
    "Remedies",
    "Warranty",
    "Term",
    "Notices",
    "Indemnity",
    "Jurisdiction",
    "Definitions",
    "Confidentiality",
    "Arbitration",
    "Assignment",
    "Survival",
    "Miscellaneous",
    "Consideration",
    "Obligations",
    "Responsibilities",
    "Payment",
    "Termination",
    "Purpose",
    "Disclosure",
    "Exceptions",
    "Recitals",
}

CONNECTOR_WORDS = {
    "and",
    "or",
    "of",
    "the",
    "to",
    "for",
    "in",
    "on",
    "with",
    "without",
    "by",
    "from",
    "under",
    "as",
    "a",
    "an",
}

SENTENCE_WORDS = {
    "shall",
    "may",
    "will",
    "must",
    "agrees",
    "agree",
    "undertakes",
    "undertake",
    "acknowledges",
    "acknowledge",
    "represents",
    "represent",
    "provides",
    "provide",
    "means",
    "include",
    "includes",
    "is",
    "are",
    "be",
    "has",
    "have",
    "hereby",
    "whereas",
    "that",
}

LEGAL_HEADING_WORDS = {
    "agreement", "contract", "confidential", "confidentiality",
    "information", "disclosure", "exceptions", "purpose",
    "definitions", "interpretation", "term", "termination",
    "remedies", "warranty", "obligations", "obligation",
    "responsibilities", "duties", "performance", "compensation",
    "employee", "employer", "leave", "restrictive", "covenant",
    "notices", "assignment", "consideration", "payment", "rent",
    "deposit", "maintenance", "possession", "handover", "damages",
    "indemnity", "indemnification", "jurisdiction", "arbitration",
    "services", "service", "scope", "fees", "charges", "license",
    "rights", "property", "intellectual", "survival", "miscellaneous",
    "recitals", "obligations", "termination", "renewal", "lock-in",
    "notice", "execution", "acceptance", "deliverables", "payment",
}

# Headings after these markers are normally signature/execution material,
# not new contract clauses. The material itself is preserved inside the
# preceding section; only candidate detection stops.
SIGNATURE_MARKERS = {
    "SIGNATURE",
    "SIGNATURES",
    "WITNESS",
    "WITNESSES",
    "EXECUTION",
    "EXECUTED BY",
    "ACCEPTANCE",
}

TEMPLATE_MARKERS = {
    "DRAFT FORMAT BY ASSETYOGI.COM",
    "DRAFT FORMAT BY ASSETYOGI",
}


# ============================================================
# BASIC HELPERS
# ============================================================

def clean_heading_title(title):
    title = re.sub(r'\s+', ' ', title).strip()

    title = re.sub(
        r'^[\s:;.\-–—]+|[\s:;.\-–—]+$',
        '',
        title
    )

    return title


def get_parent_clause(clause_number):
    parts = clause_number.split(".")

    if len(parts) <= 1:
        return None

    return ".".join(parts[:-1])


def is_numeric_marker(text):
    text = text.strip()

    return bool(
        re.fullmatch(
            r'\d+(?:\.\d+)*\.?',
            text
        )
    )


def is_page_number(line):
    line = line.strip()

    return bool(
        re.fullmatch(
            r'(?:Page\s+)?\d+(?:\s+of\s+\d+)?',
            line,
            re.IGNORECASE
        )
    )


def is_sentence_like(title):
    title = clean_heading_title(title)

    if not title:
        return True

    if is_numeric_marker(title):
        return True

    if title.endswith((".", ",", ";", ":")):
        return True

    words = title.split()

    if len(words) > 18:
        return True

    lower_words = {
        word.strip("()'\"").lower()
        for word in words
    }

    if (
        len(words) >= 7
        and lower_words.intersection(SENTENCE_WORDS)
    ):
        return True

    return False



def is_bad_section_title(title):
    """Return True when a section title is clearly not a usable heading."""
    title = clean_heading_title(title)

    if not title:
        return True

    if is_numeric_marker(title):
        return True

    if len(title.split()) > 12:
        return True

    return is_sentence_like(title)


def infer_section_title_from_subclauses(
    lines,
    section_number,
    start,
    end
):
    """
    Recover a section title from its first nested clause when the top-level
    heading was lost/corrupted by extraction.

    Example:
        23.
        23.1.Notices: All notices ...

    -> "Notices"

    This is deliberately conservative and never invents a title from
    arbitrary body text.
    """

    if section_number is None:
        return None

    prefix = section_number + "."

    for index in range(start, min(end, start + 40)):
        parsed = parse_subclause(lines[index])

        if not parsed:
            continue

        number = parsed["number"]

        if not number.startswith(prefix):
            continue

        title = clean_heading_title(parsed["title"])

        if not title:
            continue

        # A colon often separates a short clause heading from its body.
        if ":" in title:
            heading, _ = title.split(":", 1)
            heading = clean_heading_title(heading)

            if (
                heading
                and 1 <= len(heading.split()) <= 8
                and not is_sentence_like(heading)
            ):
                return heading

        # If the nested clause itself has a concise heading, use it.
        if not is_bad_section_title(title):
            return title

    return None


# ============================================================
# TABLE OF CONTENTS
# ============================================================

def looks_like_toc_line(line):
    line = line.strip()

    if not line:
        return False

    if re.search(r'\.{2,}\s*\d+\s*$', line):
        return True

    match = re.match(
        r'^(?:\d+(?:\.\d+)*\.?)?\s*(.+?)\s+\d+\s*$',
        line
    )

    if match:
        heading = match.group(1).strip()

        if 1 <= len(heading.split()) <= 12:
            return True

    return False


def find_toc_range(lines):

    toc_indices = [
        i
        for i, line in enumerate(lines)
        if looks_like_toc_line(line)
    ]

    if len(toc_indices) < 3:
        return None

    groups = []

    start = toc_indices[0]
    previous = toc_indices[0]

    for current in toc_indices[1:]:

        if current - previous <= 3:
            previous = current
            continue

        groups.append((start, previous))
        start = current
        previous = current

    groups.append((start, previous))

    best_group = max(
        groups,
        key=lambda group: group[1] - group[0]
    )

    start, end = best_group

    count = sum(
        1
        for index in toc_indices
        if start <= index <= end
    )

    if count < 3:
        return None

    for i in range(
        max(0, start - 3),
        start
    ):
        if lines[i].strip().upper() == "CONTENTS":
            start = i
            break

    return start, end + 1


# ============================================================
# HEADING DETECTION
# ============================================================

def is_likely_section_title(title):

    title = clean_heading_title(title)

    if not title:
        return False

    if looks_like_toc_line(title):
        return False

    if is_numeric_marker(title):
        return False

    if len(title) > 180:
        return False

    words = title.split()

    if len(words) > 18:
        return False

    # A long sentence is not a heading.
    if is_sentence_like(title):
        return False

    return True


def is_named_heading(line):
    """
    Detect genuine unnumbered legal headings.

    The detector is intentionally conservative. In contract templates,
    labels such as "Email", "Permanent Address", "Second Part", and
    "Management Company" are common form fields and must not become
    sections merely because they are title-cased.
    """

    raw = line.strip()

    if not raw:
        return False

    # Preserve punctuation information before clean_heading_title() removes
    # it. A line ending in ':' is usually a field label; a line ending in
    # '.' is often ordinary prose/template text rather than a heading.
    if raw.endswith((",", ";", ":")):
        return False

    upper_raw = raw.upper()

    # Strong form-field signal: "Label: value".
    if ":" in raw:
        return False

    line = clean_heading_title(raw)

    if not line:
        return False

    upper = line.upper()

    if upper in IGNORED_NAMED_HEADINGS:
        return False

    if upper in SIGNATURE_MARKERS:
        return False

    if is_numeric_marker(line):
        return False

    if looks_like_toc_line(line):
        return False

    words = line.split()

    if len(words) > 10:
        return False

    # Strong uppercase heading. This is the most reliable unnumbered form.
    if UPPERCASE_HEADING_PATTERN.fullmatch(line):
        letters = [c for c in line if c.isalpha()]
        if letters:
            ratio = sum(c.isupper() for c in letters) / len(letters)
            if ratio >= 0.85:
                return True

    # Single-word title-case headings are allowed only from an explicit
    # legal/document vocabulary.
    if len(words) == 1:
        return line in KNOWN_SINGLE_WORD_HEADINGS

    # Title-case multi-word headings need legal vocabulary support. This is
    # stricter than the previous "70% title case" rule and prevents ordinary
    # form labels from becoming sections.
    if not (2 <= len(words) <= 8):
        return False

    if is_sentence_like(line):
        return False

    lower_words = {
        re.sub(r"^[\(\[\"']+|[\)\],;\"']+$", "", word).lower()
        for word in words
    }

    if not lower_words.intersection(LEGAL_HEADING_WORDS):
        return False

    significant = [
        word for word in words
        if word.lower() not in CONNECTOR_WORDS
    ]

    if not significant:
        return False

    title_case_count = sum(
        1 for word in significant
        if word[:1].isupper()
    )

    return title_case_count / len(significant) >= 0.7


# ============================================================
# TOP-LEVEL NUMBERED CLAUSES
# ============================================================

def parse_top_level_heading(lines, index):
    """
    Parse any simple numbered clause:

        1. Definitions
        2. Confidentiality
        1. This Agreement establishes...
        1.The Agreement...

    IMPORTANT:
    We intentionally do NOT reject sentence-like titles here.

    Whether "1. This Agreement..." is a real top-level
    contract clause or an internal numbered list is decided
    later using document context.
    """

    stripped = lines[index].strip()

    match = TOP_LEVEL_PATTERN.fullmatch(
        stripped
    )

    if not match:
        return None

    number = match.group("number")

    title = clean_heading_title(
        match.group("title")
    )

    # Number on its own line.
    if not title:

        j = index + 1

        while (
            j < len(lines)
            and not lines[j].strip()
        ):
            j += 1

        if j >= len(lines):
            return {
                "number": number,
                "title": "",
                "line_index": index,
                "title_end": index,
            }

        candidate = clean_heading_title(
            lines[j]
        )

        # A number-only line followed by another number, a nested
        # clause, or another numeric marker is not a reliable title.
        # Keep it as a candidate only when the following line is ordinary
        # prose; this preserves genuine heading-less clauses while avoiding
        # OCR/layout artifacts such as:
        #
        #   22.
        #   23.1.Notices: ...
        #
        if (
            is_numeric_marker(candidate)
            or re.match(r'^\d+(?:\.\d+)+\.?\s*', candidate)
        ):
            return {
                "number": number,
                "title": "",
                "line_index": index,
                "title_end": index,
            }

        return {
            "number": number,
            "title": candidate,
            "line_index": index,
            "title_end": j,
        }

    return {
        "number": number,
        "title": title,
        "line_index": index,
        "title_end": index,
    }


# ============================================================
# NESTED CLAUSES
# ============================================================

def parse_subclause(line):

    match = SUBCLAUSE_PATTERN.fullmatch(
        line.strip()
    )

    if not match:
        return None

    number = match.group("number")

    title = clean_heading_title(
        match.group("title")
    )

    if not title:
        return None

    return {
        "number": number,
        "title": title,
    }


# ============================================================
# SIMPLE NUMBERED ITEMS
# ============================================================

def parse_numbered_item(line):

    match = NUMBERED_ITEM_PATTERN.fullmatch(
        line.strip()
    )

    if not match:
        return None

    number = match.group("number")

    title = clean_heading_title(
        match.group("title")
    )

    if not title:
        return None

    return {
        "number": number,
        "title": title,
    }


# ============================================================
# LETTERED SUBSECTIONS
# ============================================================

def is_lettered_heading(line):

    match = LETTER_HEADING_PATTERN.fullmatch(
        line.strip()
    )

    if not match:
        return False

    title = clean_heading_title(
        match.group("title")
    )

    if not title:
        return False

    return is_likely_section_title(title)


# ============================================================
# ATTACHMENTS
# ============================================================

def parse_attachment(line):

    match = ATTACHMENT_PATTERN.fullmatch(
        line.strip()
    )

    if not match:
        return None

    title = clean_heading_title(
        match.group("title")
    )

    return {
        "kind": match.group("kind").upper(),
        "number": match.group("number"),
        "title": title,
    }


def find_attachments(
    lines,
    start_index=0
):

    attachments = []

    for index in range(
        start_index,
        len(lines)
    ):

        parsed = parse_attachment(
            lines[index]
        )

        if parsed:

            attachments.append({
                **parsed,
                "line_index": index
            })

    return attachments


def build_attachment_ranges(
    lines,
    attachments
):

    ranges = []

    for i, attachment in enumerate(
        attachments
    ):

        start = attachment["line_index"]

        end = (
            attachments[i + 1]["line_index"]
            if i + 1 < len(attachments)
            else len(lines)
        )

        ranges.append(
            (start, end)
        )

    return ranges


# ============================================================
# CANDIDATE DISCOVERY
# ============================================================

def find_numbered_section_candidates(
    lines,
    excluded_ranges=None
):

    excluded_ranges = excluded_ranges or []

    def excluded(index):

        return any(
            start <= index < end
            for start, end in excluded_ranges
        )

    candidates = []

    for index in range(len(lines)):

        if excluded(index):
            continue

        candidate = parse_top_level_heading(
            lines,
            index
        )

        if candidate:

            candidates.append(
                candidate
            )

    # Remove duplicate positions.
    unique = []
    seen = set()

    for candidate in candidates:

        position = candidate["line_index"]

        if position in seen:
            continue

        seen.add(position)
        unique.append(candidate)

    return unique


def find_named_section_candidates(
    lines,
    excluded_ranges=None
):

    excluded_ranges = excluded_ranges or []

    def excluded(index):

        return any(
            start <= index < end
            for start, end in excluded_ranges
        )

    candidates = []

    for index in range(len(lines)):

        if excluded(index):
            continue

        line = lines[index].strip()

        if not is_named_heading(line):
            continue

        candidates.append({
            "number": None,
            "title": clean_heading_title(line),
            "line_index": index,
            "title_end": index,
        })

    return candidates


# ============================================================
# NUMBERING CONTEXT
# ============================================================

def has_lettered_context(
    lines,
    index,
    section_start
):
    """
    Check whether a simple numbered item occurs beneath
    a lettered subsection.

    Example:

        5. TERMS & CONDITIONS

        A. Use & Restrictions
        1. ...
        2. ...
        3. ...

    The 1/2/3 sequence is an internal list.
    """

    checked = 0

    for i in range(
        index - 1,
        max(section_start - 1, index - 15),
        -1
    ):

        line = lines[i].strip()

        if not line:
            continue

        checked += 1

        if parse_numbered_item(line):
            continue

        if parse_subclause(line):
            continue

        if is_lettered_heading(line):
            return True

        # A strong named heading marks a new context.
        if is_named_heading(line):
            return False

        # Stop after a reasonable amount of backwards search.
        if checked >= 8:
            break

    return False


def has_recent_named_context(
    lines,
    index,
    section_start
):
    """
    Similar to lettered context, but for named subsections.

    Example:

        SPECIAL CONDITIONS

        Rent Details
        1. ...
        2. ...
        3. ...

    This is deliberately conservative.
    """

    for i in range(
        index - 1,
        max(section_start - 1, index - 8),
        -1
    ):

        line = lines[i].strip()

        if not line:
            continue

        if parse_numbered_item(line):
            continue

        if parse_subclause(line):
            continue

        if is_lettered_heading(line):
            return True

        # Only strong named headings should terminate context.
        if is_named_heading(line):
            return True

        break

    return False


def is_reset_numbered_list(
    lines,
    index,
    current_section_number,
    section_start,
    section_end
):
    """
    Determine whether "1." is an internal numbered list
    rather than a new top-level section.

    Main examples:

        5. TERMS & CONDITIONS
        A. ...
        1. ...
        2. ...
        3. ...

    and:

        6. SPECIAL CLAUSES
        1. ...
        2. ...
        3. ...

    IMPORTANT:
    A reset is NOT assumed merely because the number is 1.
    Context is checked first.
    """

    item = parse_numbered_item(
        lines[index]
    )

    if not item:
        return False

    if int(item["number"]) != 1:
        return False

    # Strong internal-list signal.
    if has_lettered_context(
        lines,
        index,
        section_start
    ):
        return True

    # Look for 2, 3, etc.
    following_numbers = []

    for j in range(
        index + 1,
        min(section_end, index + 25)
    ):

        candidate = parse_numbered_item(
            lines[j]
        )

        if not candidate:
            continue

        following_numbers.append(
            int(candidate["number"])
        )

        if len(following_numbers) >= 4:
            break

    # A clean 1 -> 2 -> 3 sequence strongly suggests
    # an internal list when it occurs after an established
    # top-level section.
    if (
        len(following_numbers) >= 2
        and following_numbers[0] == 2
        and following_numbers[1] == 3
    ):

        # If the first item is explicitly introduced by
        # a lettered subsection, definitely internal.
        if has_lettered_context(
            lines,
            index,
            section_start
        ):
            return True

        # If current section is already established and
        # there is no evidence of a new legal section title,
        # treat a reset as an internal list.
        return True

    return False


# ============================================================
# CONTRACT START DETECTION
# ============================================================

def score_contract_start(
    lines,
    index
):

    score = 0

    line = lines[index].strip()

    # --------------------------------------------------------
    # Named legal heading
    # --------------------------------------------------------

    if is_named_heading(line):
        score += 2

    # --------------------------------------------------------
    # Numbered clause
    # --------------------------------------------------------

    candidate = parse_top_level_heading(
        lines,
        index
    )

    if candidate:

        score += 2

        number = candidate["number"]

        # Nested clauses directly underneath.
        nested_count = 0

        for j in range(
            index + 1,
            min(len(lines), index + 35)
        ):

            parsed = parse_subclause(
                lines[j]
            )

            if not parsed:
                continue

            if parsed["number"].startswith(
                number + "."
            ):
                nested_count += 1

        if nested_count >= 2:
            score += 5

        # A sentence-like numbered clause can itself be a
        # legitimate contract section.
        if candidate["title"]:
            score += 1

    # --------------------------------------------------------
    # Legal-language markers
    # --------------------------------------------------------

    window = " ".join(
        lines[index:index + 10]
    ).lower()

    legal_markers = [
        "agreement",
        "contract",
        "party",
        "parties",
        "employee",
        "employer",
        "tenant",
        "landlord",
        "lessor",
        "lessee",
        "confidential",
        "service",
        "consideration",
        "term",
        "payment",
        "rent",
        "disclosure",
        "obligation",
        "termination",
    ]

    marker_count = sum(
        1
        for marker in legal_markers
        if marker in window
    )

    score += min(
        marker_count,
        4
    )

    return score


def find_main_start(
    lines,
    numbered_sections,
    named_sections
):

    candidates = []

    for section in numbered_sections:

        score = score_contract_start(
            lines,
            section["line_index"]
        )

        candidates.append(
            (
                score,
                section["line_index"],
                section
            )
        )

    for section in named_sections:

        score = score_contract_start(
            lines,
            section["line_index"]
        )

        candidates.append(
            (
                score,
                section["line_index"],
                section
            )
        )

    if not candidates:
        return 0

    # Prefer strong candidates, but among equally strong
    # candidates choose the earliest one.
    strong = [
        candidate
        for candidate in candidates
        if candidate[0] >= 4
    ]

    if strong:

        best_score = max(
            candidate[0]
            for candidate in strong
        )

        best = [
            candidate
            for candidate in strong
            if candidate[0] == best_score
        ]

        return min(
            best,
            key=lambda item: item[1]
        )[1]

    return min(
        candidates,
        key=lambda item: item[1]
    )[1]


# ============================================================
# REAL TOP-LEVEL SECTION DISCOVERY
# ============================================================

def is_next_top_level_number(
    number,
    current_number
):

    try:
        return (
            int(number)
            == int(current_number) + 1
        )
    except ValueError:
        return False


def find_signature_end(lines, start_index=0):
    """
    Return the first line containing a clear signature/execution marker.

    Numbered items after this point (for example, witness "1." and "2.")
    are not treated as contract sections. The signature block itself remains
    part of the final operative segment because we only use this boundary to
    filter candidate headings.
    """

    for index in range(start_index, len(lines)):
        line = lines[index].strip()
        if not line:
            continue

        normalized = re.sub(r"[^A-Z ]", " ", line.upper())
        normalized = re.sub(r"\s+", " ", normalized).strip()

        if normalized in SIGNATURE_MARKERS:
            return index

        # Common heading variants such as "WITNESSES:" are covered by the
        # normalization above. Keep this conservative; do not stop on every
        # occurrence of words such as "signed" inside ordinary clauses.

    return None


def discover_real_sections(
    lines,
    candidates,
    main_start,
    attachments,
    operational_end=None
):
    """
    Identify genuine top-level numbered sections while preserving the
    existing segmenter's calling convention.

    Numbered lists that reset to 1, 2, 3 inside an established section are
    treated as internal lists rather than new top-level sections.
    """

    if not candidates:
        return []

    limit = operational_end if operational_end is not None else len(lines)

    usable = [
        candidate
        for candidate in candidates
        if main_start <= candidate.get("line_index", 0) < limit
    ]

    if not usable:
        return []

    sections = []

    for candidate in usable:
        number = candidate.get("number")
        title = candidate.get("title", "").strip()

        # Only plain integer markers can be top-level sections.
        if not number or "." in number:
            continue

        # Bare "22." markers are not reliable section headings.
        if not title:
            continue

        if not sections:
            if not is_bad_section_title(title):
                sections.append(candidate)
            continue

        previous = sections[-1]

        try:
            current_num = int(number)
            previous_num = int(previous.get("number"))
        except (TypeError, ValueError):
            continue

        # Normal progression: 1 -> 2 -> 3.
        if current_num == previous_num + 1:
            sections.append(candidate)
            continue

        # Preserve genuine source numbering jumps.
        if current_num > previous_num + 1:
            if not is_bad_section_title(title):
                sections.append(candidate)
            continue

        # A lower/reset number is normally an internal numbered list.
        # Keep it inside the current section.
        if current_num <= previous_num:
            continue

    return sections
def infer_section_number(
    lines,
    section_index,
    section_end
):

    numbers = []

    for index in range(
        section_index + 1,
        min(section_end, section_index + 30)
    ):

        parsed = parse_subclause(
            lines[index]
        )

        if not parsed:
            continue

        parts = parsed["number"].split(".")

        if len(parts) >= 2:

            numbers.append(
                parts[0]
            )

    if not numbers:
        return None

    counts = {}

    for number in numbers:

        counts[number] = (
            counts.get(number, 0) + 1
        )

    return max(
        counts,
        key=counts.get
    )


# ============================================================
# SEGMENT CREATION
# ============================================================

def make_document_segment(text):

    return {
        "clause_id": None,
        "parent_clause": None,
        "section": None,
        "section_title": None,
        "text": text.strip(),
        "type": "document"
    }


def make_section_segment(
    number,
    title,
    text
):

    return {
        "clause_id": (
            number
            if number is not None
            else title
        ),
        "parent_clause": None,
        "section": number,
        "section_title": title,
        "text": text.strip(),
        "type": "section"
    }


def make_clause_segment(
    number,
    parent,
    section,
    section_title,
    text
):

    return {
        "clause_id": number,
        "parent_clause": parent,
        "section": section,
        "section_title": section_title,
        "text": text.strip(),
        "type": "clause"
    }


def make_attachment_segment(
    attachment,
    text
):

    kind = attachment["kind"]
    number = attachment["number"]
    title = attachment["title"]

    section_title = (
        f"{kind.title()} {number}"
    )

    if title:
        section_title += (
            f": {title}"
        )

    return {
        "clause_id": (
            f"{kind.title()} {number}"
        ),
        "parent_clause": None,
        "section": (
            f"{kind.title()} {number}"
        ),
        "section_title": section_title,
        "text": text.strip(),
        "type": (
            "schedule"
            if kind == "SCHEDULE"
            else "annexure"
        )
    }


# ============================================================
# MAIN SEGMENTER
# ============================================================

def segment_clauses(text):

    if not text or not text.strip():

        return [
            make_document_segment("")
        ]

    lines = text.splitlines()

    # --------------------------------------------------------
    # 1. Ignore page-number noise.
    # --------------------------------------------------------

    normalized_lines = []

    for line in lines:

        if is_page_number(line):
            normalized_lines.append("")
        else:
            normalized_lines.append(line)

    lines = normalized_lines

    # --------------------------------------------------------
    # 2. Detect table of contents.
    # --------------------------------------------------------

    toc_range = find_toc_range(
        lines
    )

    excluded_ranges = []

    if toc_range:
        excluded_ranges.append(
            toc_range
        )

    # --------------------------------------------------------
    # 3. Detect candidate sections.
    # --------------------------------------------------------

    numbered_candidates = (
        find_numbered_section_candidates(
            lines,
            excluded_ranges
        )
    )

    named_candidates = (
        find_named_section_candidates(
            lines,
            excluded_ranges
        )
    )

    # --------------------------------------------------------
    # 4. Estimate contract start.
    # --------------------------------------------------------

    preliminary_start = find_main_start(
        lines,
        numbered_candidates,
        named_candidates
    )

    # Signature/execution material is part of the document but should not
    # generate new top-level sections (e.g. witness "1." / "2.").
    signature_end = find_signature_end(
        lines,
        start_index=preliminary_start
    )

    # --------------------------------------------------------
    # 5. Detect attachments after likely contract start.
    # --------------------------------------------------------

    attachments = find_attachments(
        lines,
        start_index=preliminary_start
    )

    attachment_ranges = (
        build_attachment_ranges(
            lines,
            attachments
        )
    )

    def inside_attachment(index):

        return any(
            start <= index < end
            for start, end in attachment_ranges
        )

    numbered_candidates = [
        candidate
        for candidate in numbered_candidates
        if not inside_attachment(
            candidate["line_index"]
        )
    ]

    named_candidates = [
        candidate
        for candidate in named_candidates
        if not inside_attachment(
            candidate["line_index"]
        )
    ]

    # Do not allow signature/witness numbering to become new sections.
    if signature_end is not None:
        numbered_candidates = [
            candidate
            for candidate in numbered_candidates
            if candidate["line_index"] < signature_end
        ]
        named_candidates = [
            candidate
            for candidate in named_candidates
            if candidate["line_index"] < signature_end
        ]

    # --------------------------------------------------------
    # 6. Discover actual numbered sections.
    # --------------------------------------------------------

    real_numbered_sections = (
        discover_real_sections(
            lines,
            numbered_candidates,
            preliminary_start,
            attachments,
            operational_end=signature_end
        )
    )

    # --------------------------------------------------------
    # 7. Choose numbered structure when available.
    #
    # Otherwise use named headings.
    # --------------------------------------------------------

    if real_numbered_sections:

        sections = real_numbered_sections

    else:

        sections = [
            section
            for section in named_candidates
            if section["line_index"]
            >= preliminary_start
        ]

    # Remove obvious non-operative headings at beginning.
    while sections:

        title = (
            sections[0]["title"]
            .strip()
            .upper()
        )

        if title in {
            "AND",
            "BY AND BETWEEN",
            "WHEREAS",
            "NOW THEREFORE",
            "NOW, THEREFORE",
        }:

            sections.pop(0)

        else:
            break

    # --------------------------------------------------------
    # 8. No reliable structure.
    # --------------------------------------------------------

    if not sections:

        return [
            make_document_segment(
                text
            )
        ]

    # --------------------------------------------------------
    # 9. Recalculate attachment position using actual start.
    # --------------------------------------------------------

    main_start = sections[0][
        "line_index"
    ]

    attachments = [
        attachment
        for attachment in attachments
        if attachment["line_index"]
        >= main_start
    ]

    attachment_ranges = (
        build_attachment_ranges(
            lines,
            attachments
        )
    )

    # --------------------------------------------------------
    # 10. Build section segments.
    # --------------------------------------------------------

    segments = []

    for section_index, section in enumerate(
        sections
    ):

        start = section[
            "line_index"
        ]

        content_start = section.get(
            "title_end",
            start
        )

        # ----------------------------------------------------
        # Find end of section.
        # ----------------------------------------------------

        if (
            section_index + 1
            < len(sections)
        ):

            end = sections[
                section_index + 1
            ]["line_index"]

        else:

            future_attachments = [
                attachment["line_index"]
                for attachment in attachments
                if attachment["line_index"] > start
            ]

            if future_attachments:

                end = min(
                    future_attachments
                )

            else:

                end = len(lines)

        if end <= start:
            continue

        full_section_text = "\n".join(
            lines[start:end]
        ).strip()

        section_number = section[
            "number"
        ]

        section_title = section[
            "title"
        ]

        # ----------------------------------------------------
        # Repair a clearly corrupted/missing top-level title from the
        # first nested clause. This addresses extraction failures without
        # adding document-specific rules.
        # ----------------------------------------------------

        if is_bad_section_title(
            section_title
        ):
            inferred_title = (
                infer_section_title_from_subclauses(
                    lines,
                    section_number,
                    content_start,
                    end
                )
            )

            if inferred_title:
                section_title = inferred_title

        # ----------------------------------------------------
        # Named section:
        #
        # DEFINITIONS
        # 1.1 ...
        # 1.2 ...
        # ----------------------------------------------------

        if section_number is None:

            inferred_number = (
                infer_section_number(
                    lines,
                    start,
                    end
                )
            )

            if inferred_number:

                section_number = (
                    inferred_number
                )

        # ----------------------------------------------------
        # Find nested clauses.
        # ----------------------------------------------------

        subclauses = []

        if section_number is not None:

            for absolute_index in range(
                content_start,
                end
            ):

                parsed = parse_subclause(
                    lines[absolute_index]
                )

                if not parsed:
                    continue

                clause_number = (
                    parsed["number"]
                )

                prefix = (
                    section_number
                    + "."
                )

                if not clause_number.startswith(
                    prefix
                ):
                    continue

                parent = get_parent_clause(
                    clause_number
                )

                if parent is None:
                    continue

                # Child belongs to this section if its
                # first number matches the section.
                if not clause_number.startswith(
                    prefix
                ):
                    continue

                relative_index = (
                    absolute_index - start
                )

                subclauses.append({
                    "number": clause_number,
                    "relative_index": relative_index
                })

        # ----------------------------------------------------
        # Case A:
        # Nested numbering exists.
        # ----------------------------------------------------

        if subclauses:

            for i, clause in enumerate(
                subclauses
            ):

                start_rel = clause[
                    "relative_index"
                ]

                if (
                    i + 1
                    < len(subclauses)
                ):

                    end_rel = (
                        subclauses[i + 1][
                            "relative_index"
                        ]
                    )

                else:

                    end_rel = (
                        len(lines[start:end])
                    )

                clause_text = "\n".join(
                    lines[
                        start + start_rel:
                        start + end_rel
                    ]
                ).strip()

                if not clause_text:
                    continue

                segments.append(
                    make_clause_segment(
                        clause["number"],
                        get_parent_clause(
                            clause["number"]
                        ),
                        section_number,
                        section_title,
                        clause_text
                    )
                )

            continue

        # ----------------------------------------------------
        # Case B:
        # Internal simple numbered list.
        #
        # Example:
        #
        # 5. TERMS & CONDITIONS
        # A. Use & Restrictions
        # 1. ...
        # 2. ...
        # 3. ...
        # ----------------------------------------------------

        numbered_items = []

        for absolute_index in range(
            content_start,
            end
        ):

            item = parse_numbered_item(
                lines[absolute_index]
            )

            if not item:
                continue

            # Do not treat a number equal to the current
            # section as an internal item.
            if (
                section_number is not None
                and item["number"]
                == str(section_number)
            ):
                continue

            if is_reset_numbered_list(
                lines,
                absolute_index,
                section_number,
                start,
                end
            ):

                numbered_items.append({
                    "number": item["number"],
                    "relative_index": (
                        absolute_index - start
                    )
                })

        if len(numbered_items) >= 2:

            for i, item in enumerate(
                numbered_items
            ):

                start_rel = item[
                    "relative_index"
                ]

                if (
                    i + 1
                    < len(numbered_items)
                ):

                    end_rel = (
                        numbered_items[i + 1][
                            "relative_index"
                        ]
                    )

                else:

                    end_rel = (
                        len(lines[start:end])
                    )

                clause_text = "\n".join(
                    lines[
                        start + start_rel:
                        start + end_rel
                    ]
                ).strip()

                if not clause_text:
                    continue

                synthetic_id = (
                    f"{section_number}."
                    f"{item['number']}"
                )

                segments.append(
                    make_clause_segment(
                        synthetic_id,
                        section_number,
                        section_number,
                        section_title,
                        clause_text
                    )
                )

            continue

        # ----------------------------------------------------
        # Case C:
        # Ordinary section with no nested structure.
        # ----------------------------------------------------

        segments.append(
            make_section_segment(
                section_number,
                section_title,
                full_section_text
            )
        )

    # --------------------------------------------------------
    # 11. Add preamble.
    # --------------------------------------------------------

    first_section_start = sections[0][
        "line_index"
    ]

    preamble_start = 0

    if toc_range:

        preamble_start = toc_range[1]

    preamble = "\n".join(
        lines[
            preamble_start:
            first_section_start
        ]
    ).strip()

    if preamble:

        cleaned_upper = (
            preamble.upper()
        )

        template_only = (
            "ASSETYOGI" in cleaned_upper
            and
            (
                "DISCLAIMER" in cleaned_upper
                or
                "COPYRIGHT" in cleaned_upper
                or
                "DRAFT FORMAT" in cleaned_upper
            )
        )

        if not template_only:

            segments.insert(
                0,
                make_document_segment(
                    preamble
                )
            )

    # --------------------------------------------------------
    # 12. Add attachments.
    # --------------------------------------------------------

    for i, attachment in enumerate(
        attachments
    ):

        start = attachment[
            "line_index"
        ]

        end = (
            attachments[i + 1][
                "line_index"
            ]
            if i + 1 < len(attachments)
            else len(lines)
        )

        attachment_text = "\n".join(
            lines[start:end]
        ).strip()

        if not attachment_text:
            continue

        segments.append(
            make_attachment_segment(
                attachment,
                attachment_text
            )
        )

    # --------------------------------------------------------
    # 13. Preserve source order.
    #
    # We store the original segment order during creation,
    # so we don't need unreliable text matching to recover
    # positions.
    # --------------------------------------------------------

    return segments