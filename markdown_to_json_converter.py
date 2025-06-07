class RootObject:
    def __init__(self, document_title, document_info, table_of_contents, foreword, sections):
        self.document_title = document_title
        self.document_info = document_info
        self.table_of_contents = table_of_contents
        self.foreword = foreword
        self.sections = sections

    def to_dict(self):
        return {
            "document_title": self.document_title,
            "document_info": self.document_info.to_dict() if self.document_info else None,
            "table_of_contents": self.table_of_contents,
            "foreword": self.foreword,
            "sections": [section.to_dict() for section in self.sections]
        }

class DocumentInfo:
    def __init__(self, version, codename):
        self.version = version
        self.codename = codename

    def to_dict(self):
        return {
            "version": self.version,
            "codename": self.codename
        }

class SectionObject:
    def __init__(self, section_number, section_title, content):
        self.type = "section"
        self.section_number = section_number
        self.section_title = section_title
        self.content = content # List of SubsectionObject, ParagraphObject, or ListObject

    def to_dict(self):
        return {
            "type": self.type,
            "section_number": self.section_number,
            "section_title": self.section_title,
            "content": [item.to_dict() for item in self.content]
        }

class SubsectionObject:
    def __init__(self, subsection_number, subsection_title, content):
        self.type = "subsection"
        self.subsection_number = subsection_number
        self.subsection_title = subsection_title
        self.content = content # List of SubsubsectionObject, ParagraphObject, or ListObject

    def to_dict(self):
        return {
            "type": self.type,
            "subsection_number": self.subsection_number,
            "subsection_title": self.subsection_title,
            "content": [item.to_dict() for item in self.content]
        }

class SubsubsectionObject:
    def __init__(self, subsubsection_number, subsubsection_title, content):
        self.type = "subsubsection"
        self.subsubsection_number = subsubsection_number
        self.subsubsection_title = subsubsection_title
        self.content = content # List of ParagraphObject or ListObject

    def to_dict(self):
        return {
            "type": self.type,
            "subsubsection_number": self.subsubsection_number,
            "subsubsection_title": self.subsubsection_title,
            "content": [item.to_dict() for item in self.content]
        }

class ParagraphObject:
    def __init__(self, text):
        self.type = "paragraph"
        self.text = text

    def to_dict(self):
        return {
            "type": self.type,
            "text": self.text
        }

class ListObject:
    def __init__(self, items):
        self.type = "list"
        self.items = items

    def to_dict(self):
        return {
            "type": self.type,
            "items": self.items
        }

import re
import json

def parse_metadata_from_line(line):
    """
    Parses the document title, version, and codename from a given line.
    Expected format: EOTS vX.Y "Codename" - Comprehensive System Guide
    """
    document_title = line.strip()
    version = None
    codename = None

    # Regex to capture version (e.g., "2.5") and codename (e.g., "Apex Predator")
    # EOTS v2.5 "Apex Predator" - Comprehensive System Guide
    match = re.search(r'EOTS v(?P<version>\d+\.\d+)\s+"(?P<codename>[^"]+)"', line)

    if match:
        version = match.group("version")
        codename = match.group("codename")
    else:
        print("Warning: Could not parse version and codename from the title line.")

    return document_title, version, codename

if __name__ == "__main__":
    # This is a placeholder for where the file reading logic will go.
    # For this subtask, we'll use the example line directly.
    example_line = 'EOTS v2.5 "Apex Predator" - Comprehensive System Guide' # This will be replaced by file reading

    # --- Metadata Parsing ---
    doc_title, doc_version, doc_codename = parse_metadata_from_line(example_line)
    document_info_obj = None
    if doc_version and doc_codename:
        document_info_obj = DocumentInfo(version=doc_version, codename=doc_codename)

    if doc_title:
        print(f"Document Title: {doc_title}")
    if document_info_obj:
        print(f"Version: {document_info_obj.version}")
        print(f"Codename: {document_info_obj.codename}")

    # --- Table of Contents Parsing ---
    # Placeholder for actual file reading
    # For now, simulate file lines relevant for ToC parsing based on "EOTS V2.5 FINAL GUIDE.md"
    # In reality, this would come from:
    # with open("EOTS V2.5 FINAL GUIDE.md", "r", encoding="utf-8") as f:
    #     all_lines = f.readlines()

    # Simulate reading the first few lines of the document
    # The first line is the title, which we've already processed conceptually.
    # The actual parsing will read the whole file and then process sections.

    # For now, let's define a function to parse ToC and test it.
    # We'll integrate full file reading later.

def parse_table_of_contents(lines):
    """
    Parses the table of contents from a list of lines.
    """
    toc_items = []
    in_toc_section = False
    toc_start_marker = "Table of Contents"
    # Using the distinctive separator line as the end marker for ToC items
    toc_end_marker = "________________________________________"

    for line_num, line_content in enumerate(lines):
        line_content_stripped = line_content.strip()

        if not in_toc_section:
            if line_content_stripped == toc_start_marker:
                in_toc_section = True
                # Skip the "Table of Contents" line itself from being added to items
                continue

        if in_toc_section:
            if line_content_stripped.startswith(toc_end_marker):
                # Stop before processing the "Foreword:" line
                break
            if line_content_stripped: # Add non-empty lines
                toc_items.append(line_content_stripped)

    if not toc_items and in_toc_section: # Found start but no items before end
        print(f"Warning: Table of Contents section started but no items found before '{toc_end_marker}'.")
    elif not in_toc_section and lines: # Did not even find "Table of Contents"
        # Check if the start marker was even in the provided lines
        if not any(toc_start_marker in line for line in lines): # Check if marker exists at all
            print(f"Warning: '{toc_start_marker}' marker not found in the provided lines.")
        else: # Marker exists, but something else went wrong (e.g. end marker before start, or empty file part)
            print(f"Warning: '{toc_start_marker}' marker found, but no ToC items collected. Check structure around it and '{toc_end_marker}'.")


    return toc_items

if __name__ == "__main__":
    # --- Metadata Parsing (from previous step) ---
    # This will be driven by actual file reading in the full script.
    # For now, we keep the example for continuity of testable units.
    example_title_line = 'EOTS v2.5 "Apex Predator" - Comprehensive System Guide'
    doc_title, doc_version, doc_codename = parse_metadata_from_line(example_title_line)
    document_info_obj = None
    if doc_version and doc_codename:
        document_info_obj = DocumentInfo(version=doc_version, codename=doc_codename)

    print("--- Metadata ---")
    if doc_title:
        print(f"Document Title: {doc_title}")
    if document_info_obj:
        print(f"Version: {document_info_obj.version}")
        print(f"Codename: {document_info_obj.codename}")
    print("-----------------\n")

    # --- Table of Contents Parsing ---
    # Simulate file content for ToC parsing for now
    simulated_lines_for_toc = [
        "EOTS v2.5 \"Apex Predator\" - Comprehensive System Guide\n",
        "Table of Contents\n",
        "Foreword: The Evolution to Apex Predator - Philosophy of EOTS v2.5\n",
        "I. Introduction to EOTS v2.5\n",
        "1.1. Purpose of This Guide: Mastering the Apex Predator\n",
        "1.2. Overview of the EOTS v2.5: Adaptive Intelligence & Universal Potency\n",
        "1.2.1. Core Philosophy: From Market Understanding to Lethal Execution\n",
        "1.2.2. Key Architectural Pillars of Version 2.5\n",
        "1.3. Summary of Major Enhancements from v2.4 to v2.5\n",
        "Foreword: This is the actual foreword section start\n", # Mistake in simulation, should be the end marker
        "This is part of the foreword text.\n"
    ]

    # Corrected simulation based on the subtask description
    # The "Foreword:" line is the *end* marker for the ToC items.
    # The items themselves are *after* "Table of Contents" and *before* "Foreword:".

    # Let's use a more realistic simulation of the start of the actual file
    # based on the previously read "EOTS V2.5 FINAL GUIDE.md"
    actual_file_simulation_for_toc = [
        "EOTS v2.5 \"Apex Predator\" - Comprehensive System Guide\n", # Line 0
        "Table of Contents\n",                                     # Line 1 - TOC STARTS HERE
        "Foreword: The Evolution to Apex Predator - Philosophy of EOTS v2.5\n", # Line 2 - TOC ITEM 1
        "I. Introduction to EOTS v2.5\n",                           # Line 3 - TOC ITEM 2
        "1.1. Purpose of This Guide: Mastering the Apex Predator\n", # Line 4 - TOC ITEM 3
        # ... more items ...
        # Let's assume the actual foreword starts much later, but we need the marker
        # For testing, we'll use a truncated list and a clear end marker
        "1.5. Disclaimer\n",                                         # Example last ToC item
        "Foreword: The Evolution to Apex Predator - Philosophy of EOTS v2.5\n" # THIS IS THE END MARKER
        # "II. EOTS v2.5 System Architecture & Workflow\n" # This would be a ToC item
    ]
    # The issue with the previous simulation was that the end marker was also a ToC item.
    # Let's re-simulate based on the actual file structure provided in the prompt.
    # The ToC items are the lines *between* "Table of Contents" and the line that *starts with* "Foreword:".

    # For testing the parse_table_of_contents function, we need to pass all lines of the file.
    # We'll read the actual file content here.

    try:
        with open("EOTS V2.5 FINAL GUIDE.md", "r", encoding="utf-8") as f:
            all_lines = f.readlines()
    except FileNotFoundError:
        print("Error: 'EOTS V2.5 FINAL GUIDE.md' not found. Please ensure the file exists.")
        all_lines = [] # Ensure all_lines is defined for subsequent code

    # The first line is the title, which is handled by parse_metadata_from_line
    # parse_table_of_contents should ideally receive lines *after* the title,
    # or be robust enough to handle the title line if it's included.
    # For this subtask, let's pass all lines starting from the second line
    # if the first line is indeed the title.

    # Let's adjust: the parse_table_of_contents function should find the start and end markers
    # irrespective of where they are in the full list of lines.

    table_of_contents = []
    if all_lines:
        # The first line is the title.
        # We can pass all lines to parse_table_of_contents, it will find the marker.
        table_of_contents = parse_table_of_contents(all_lines)

    if table_of_contents:
        print("--- Table of Contents ---")
        for item in table_of_contents:
            print(item)
        print(f"Total ToC items: {len(table_of_contents)}")
        print("-------------------------\n")
    else:
        print("No Table of Contents items found or file was not read.\n")

    # In a real scenario, table_of_contents would be stored in a RootObject instance.
    # RootObject(document_title=doc_title, document_info=document_info_obj, table_of_contents=table_of_contents, ...)
    # For now, printing is sufficient for verification.


def parse_foreword(lines):
    """
    Parses the foreword paragraph from a list of lines.
    Searches for a heading that exactly matches "Foreword: The Evolution to Apex Predator - Philosophy of EOTS v2.5"
    or starts with "Foreword:". Extracts the immediate next non-empty line as the paragraph.
    """
    foreword_paragraph_lines = []
    found_heading_in_body = False

    toc_start_marker = "Table of Contents"
    toc_end_marker = "________________________________________"

    # Potential foreword headings to search for
    exact_foreword_heading = "Foreword: The Evolution to Apex Predator - Philosophy of EOTS v2.5"
    prefix_foreword_heading = "Foreword:"

    # 1. Determine the end line of the Table of Contents
    toc_end_line_num = -1
    in_toc_block = False # Flag to indicate we are currently between ToC start and end markers
    toc_start_found_once = False # Flag to see if "Table of Contents" was ever found

    for i, line_content in enumerate(lines):
        stripped_line = line_content.strip()
        if stripped_line == toc_start_marker:
            in_toc_block = True
            toc_start_found_once = True
        if in_toc_block and stripped_line == toc_end_marker:
            toc_end_line_num = i
            in_toc_block = False # Exited the ToC block
            break # Found the end of ToC

    start_search_for_foreword_from_line = 0 # Default: search all lines provided to function
    if toc_start_found_once:
        if toc_end_line_num != -1:
            # ToC block was found and properly ended, search after it
            start_search_for_foreword_from_line = toc_end_line_num + 1
        else:
            # ToC started but no clear end marker '________________________________________' was found.
            # This is an ambiguous state. For safety, we might still want to search everything
            # or log a more specific warning. The subtask implies Foreword is outside ToC.
            # If ToC doesn't end, technically all subsequent lines are "after ToC start".
            # However, a missing ToC end is a structural anomaly.
            print(f"Warning: '{toc_start_marker}' found, but its end marker ('{toc_end_marker}') was not. Foreword search will proceed through all lines after the ToC start marker, which might be inaccurate if ToC is very long and malformed.")
            # Find the line where ToC started to ensure we search after that, at least.
            for i, line_content in enumerate(lines):
                if line_content.strip() == toc_start_marker:
                    start_search_for_foreword_from_line = i + 1
                    break
    else:
        print(f"Warning: '{toc_start_marker}' not found. Foreword search will cover all provided lines.")


    # 2. Search for Foreword heading in lines *after* the Table of Contents (or from start_search_for_foreword_from_line)
    heading_line_num = -1
    for i in range(start_search_for_foreword_from_line, len(lines)):
        line_content_stripped = lines[i].strip()
        if line_content_stripped == exact_foreword_heading or \
           line_content_stripped.startswith(prefix_foreword_heading):
            found_heading_in_body = True
            heading_line_num = i
            break # Found the heading

    # 3. If heading found, extract the subsequent paragraph
    if found_heading_in_body and heading_line_num + 1 < len(lines):
        for i in range(heading_line_num + 1, len(lines)):
            line_content = lines[i] # Keep original spacing for potential multi-line paragraph
            line_content_stripped = line_content.strip()

            if not line_content_stripped: # Blank line indicates end of paragraph
                if foreword_paragraph_lines: # Only break if we have collected something
                    break
                else: # Skip leading blank lines after heading
                    continue

            # Check for common markdown heading prefixes or other section starters
            # This is a heuristic to stop paragraph collection if a new section begins.
            if re.match(r'^(#+\s|\d+\.\s|[IVX]+\.\s|[-*]\s)', line_content_stripped) and foreword_paragraph_lines:
                 break # New section or list started

            foreword_paragraph_lines.append(line_content.rstrip('\n')) # Add line, remove trailing newline

        if not foreword_paragraph_lines:
             print(f"Warning: Found Foreword heading '{lines[heading_line_num].strip()}' but no subsequent non-empty paragraph content before next blank line or heading.")

    if not found_heading_in_body:
        # This message will be printed by the main block based on return value
        pass

    return " ".join(foreword_paragraph_lines).strip() if foreword_paragraph_lines else None, found_heading_in_body

if __name__ == "__main__":
    # --- Metadata Parsing (from previous step) ---
    example_title_line = 'EOTS v2.5 "Apex Predator" - Comprehensive System Guide'
    doc_title, doc_version, doc_codename = parse_metadata_from_line(example_title_line)
    document_info_obj = None
    if doc_version and doc_codename:
        document_info_obj = DocumentInfo(version=doc_version, codename=doc_codename)

    print("--- Metadata ---")
    if doc_title:
        print(f"Document Title: {doc_title}")
    if document_info_obj:
        print(f"Version: {document_info_obj.version}")
        print(f"Codename: {document_info_obj.codename}")
    print("-----------------\n")

    all_lines = []
    try:
        with open("EOTS V2.5 FINAL GUIDE.md", "r", encoding="utf-8") as f:
            all_lines = f.readlines()
    except FileNotFoundError:
        print("Error: 'EOTS V2.5 FINAL GUIDE.md' not found. Please ensure the file exists.")

    # --- Table of Contents Parsing ---
    table_of_contents = []
    if all_lines:
        table_of_contents = parse_table_of_contents(all_lines)

    if table_of_contents:
        print("--- Table of Contents ---")
        # Only print a few items for brevity in testing
        for item in table_of_contents[:3]: # Print first 3 items
            print(item)
        if len(table_of_contents) > 3:
            print("...")
        print(f"Total ToC items: {len(table_of_contents)}")
        print("-------------------------\n")
    else:
        print("No Table of Contents items found or file was not read.\n")

    # --- Foreword Parsing (Revised Logic) ---
    foreword_content = "" # Default to empty string
    if all_lines:
        # parse_foreword now handles finding the ToC end and searching after it.
        parsed_foreword_text, found_foreword_heading_in_body = parse_foreword(all_lines)
        if found_foreword_heading_in_body and parsed_foreword_text:
            foreword_content = parsed_foreword_text
        elif found_foreword_heading_in_body and not parsed_foreword_text:
            # Heading found, but no paragraph content followed it as per parsing rules
            print("Note: A 'Foreword' heading was found in the document body, but no subsequent paragraph content was extracted.")
            foreword_content = "" # Explicitly empty
        else:
            # No distinct "Foreword" heading found in the document body after the ToC.
            print("Note: No distinct 'Foreword' section heading found in the document body after the Table of Contents.")
            foreword_content = "" # Explicitly empty as per requirement

    print("--- Foreword ---")
    if foreword_content:
        print(f"Extracted Foreword Paragraph:\n{foreword_content}")
    else:
        print("Foreword content is empty or not found as a distinct section in the document body.")
    print("----------------\n")

    # In a real scenario, foreword_content (which could be an empty string)
    # would be stored in a RootObject instance's foreword attribute.
    # Example:
    # root_object = RootObject(
    #     document_title=doc_title,
    #     document_info=document_info_obj,
    #     table_of_contents=table_of_contents,
    #     foreword=foreword_content, # This will be the parsed foreword string
    #     sections=[] # Sections to be parsed later
    # )
    # print(f"RootObject.foreword: '{root_object.foreword}'")

# Regex patterns for headings
# Main section: e.g., I. Introduction, V. Metrics, XVII. Appendix
MAIN_SECTION_REGEX = re.compile(r"^([IVXLCDM]+)\.\s+(.*)")
# Subsection: e.g., 1.1. Purpose, 2.4. Understanding, 17.1. Formulas
SUBSECTION_REGEX = re.compile(r"^(\d+\.\d+)\.\s+(.*)")
# Sub-subsection: e.g., 1.2.1. Core Philosophy, 2.2.1. Data Ingestion
SUB_SUBSECTION_REGEX = re.compile(r"^(\d+\.\d+\.\d+)\.\s+(.*)")
# List item: e.g., - An item, * An item, • An item
LIST_ITEM_REGEX = re.compile(r"^(?:[-*•])\s+(.*)")


def process_content_block(content_lines_buffer):
    """
    Processes a block of raw lines into ParagraphObjects and ListObjects.
    """
    processed_content_objects = []
    current_list_items = []
    paragraph_buffer = []

    def flush_paragraph_buffer():
        nonlocal paragraph_buffer
        if paragraph_buffer:
            # Join lines with newline to preserve multi-line paragraphs from source
            para_text = "\n".join(paragraph_buffer)
            processed_content_objects.append(ParagraphObject(text=para_text))
            paragraph_buffer = []

    def flush_list_items():
        nonlocal current_list_items
        if current_list_items:
            processed_content_objects.append(ListObject(items=current_list_items))
            current_list_items = []

    for line_content in content_lines_buffer:
        line_stripped = line_content.strip() # Stripping here for logic, but original might be needed for ParagraphObject

        list_match = LIST_ITEM_REGEX.match(line_stripped)

        if list_match:
            flush_paragraph_buffer() # Any preceding text was a paragraph
            list_item_text = list_match.group(1).strip()
            current_list_items.append(list_item_text)
        else: # Not a list item
            flush_list_items() # If we were in a list, it has now ended
            if line_stripped: # It's a paragraph line
                # For paragraphs, we use the original line (with leading/trailing whitespace removed per line)
                # but preserve internal spacing.
                paragraph_buffer.append(line_content.strip()) # Add stripped line to buffer
            else: # Blank line
                flush_paragraph_buffer() # End of current paragraph

    # After loop, flush any remaining items
    flush_paragraph_buffer()
    flush_list_items()

    return processed_content_objects


def parse_document_body(body_lines):
    """
    Parses the main content of the document, identifying sections, subsections,
    and sub-subsections, and collecting raw content lines.
    """
    root_sections = []
    current_section_obj = None
    current_subsection_obj = None
    current_subsubsection_obj = None

    current_content_block_lines = [] # Buffer for lines between headings

    def get_active_parent_content_list():
        if current_subsubsection_obj:
            return current_subsubsection_obj.content
        if current_subsection_obj:
            return current_subsection_obj.content
        if current_section_obj:
            return current_section_obj.content
        return None

    for line_num, line_content_original in enumerate(body_lines):
        line_stripped = line_content_original.strip()

        # Check for headings first
        main_section_match = MAIN_SECTION_REGEX.match(line_stripped)
        subsection_match = SUBSECTION_REGEX.match(line_stripped)
        subsubsection_match = SUB_SUBSECTION_REGEX.match(line_stripped)

        is_heading = main_section_match or subsection_match or subsubsection_match

        if is_heading:
            # Process any accumulated content block before handling the new heading
            if current_content_block_lines:
                parent_content_list = get_active_parent_content_list()
                if parent_content_list is not None:
                    processed_objects = process_content_block(current_content_block_lines)
                    parent_content_list.extend(processed_objects)
                else:
                    # This case should ideally not happen if headings are hierarchical
                    # Or it's preamble content before any section.
                    # For now, preamble content is handled by the final flush.
                    pass
                current_content_block_lines = []

            if main_section_match:
                number, title = main_section_match.groups()
                section_obj = SectionObject(section_number=number, section_title=title, content=[])
                root_sections.append(section_obj)
                current_section_obj = section_obj
                current_subsection_obj = None
                current_subsubsection_obj = None
            elif subsection_match:
                if current_section_obj is None:
                    print(f"Warning: Found subsection '{line_stripped}' without an active main section at line {line_num+1}. Skipping.")
                    continue
                number, title = subsection_match.groups()
                subsection_obj = SubsectionObject(subsection_number=number, subsection_title=title, content=[])
                current_section_obj.content.append(subsection_obj)
                current_subsection_obj = subsection_obj
                current_subsubsection_obj = None
            elif subsubsection_match:
                if current_subsection_obj is None:
                    print(f"Warning: Found sub-subsection '{line_stripped}' without an active subsection at line {line_num+1}. Skipping.")
                    continue
                number, title = subsubsection_match.groups()
                subsubsection_obj = SubsubsectionObject(subsubsection_number=number, subsubsection_title=title, content=[])
                current_subsection_obj.content.append(subsubsection_obj)
                current_subsubsection_obj = subsubsection_obj
        else: # Not a heading line
            if line_stripped: # If it's not a blank line, add to buffer
                current_content_block_lines.append(line_content_original) # Keep original for paragraph joining
            elif current_content_block_lines: # Blank line signifies end of a block
                parent_content_list = get_active_parent_content_list()
                if parent_content_list is not None:
                    processed_objects = process_content_block(current_content_block_lines)
                    parent_content_list.extend(processed_objects)
                current_content_block_lines = []


    # After the loop, process any remaining content in the buffer for the last active section
    if current_content_block_lines:
        parent_content_list = get_active_parent_content_list()
        if parent_content_list is not None:
            processed_objects = process_content_block(current_content_block_lines)
            parent_content_list.extend(processed_objects)
        elif not root_sections: # No sections were ever created, this is preamble
             # This case means the whole document might be content without recognized headings.
             # Or, lines after ToC but before the first valid section heading.
             # For now, we'll assume parse_document_body is called with lines starting from the first actual section.
             # Any content before the *first* "I. Section" will be handled if we collect it.
             # The current preamble logic in main might catch some of this.
             # We can create a "Preamble" section if needed, or let it be ignored if no parent_content_list.
            print(f"Info: {len(current_content_block_lines)} content lines found at the end of processing, outside any main section structure.")
            # For now, this content is not added if no parent section exists.

    return root_sections


if __name__ == "__main__":
    # --- Metadata Parsing (from previous step) ---
    example_title_line = 'EOTS v2.5 "Apex Predator" - Comprehensive System Guide'
    doc_title, doc_version, doc_codename = parse_metadata_from_line(example_title_line)
    document_info_obj = None
    if doc_version and doc_codename:
        document_info_obj = DocumentInfo(version=doc_version, codename=doc_codename)

    print("--- Metadata ---")
    if doc_title:
        print(f"Document Title: {doc_title}")
    if document_info_obj:
        print(f"Version: {document_info_obj.version}")
        print(f"Codename: {document_info_obj.codename}")
    print("-----------------\n")

    all_lines = []
    try:
        with open("EOTS V2.5 FINAL GUIDE.md", "r", encoding="utf-8") as f:
            all_lines = f.readlines()
    except FileNotFoundError:
        print("Error: 'EOTS V2.5 FINAL GUIDE.md' not found. Please ensure the file exists.")

    # --- Table of Contents Parsing ---
    table_of_contents_list = []
    if all_lines:
        table_of_contents_list = parse_table_of_contents(all_lines)

    if table_of_contents_list:
        print("--- Table of Contents ---")
        # Only print a few items for brevity in testing
        for item in table_of_contents_list[:3]: # Print first 3 items
            print(item)
        if len(table_of_contents_list) > 3:
            print("...")
        print(f"Total ToC items: {len(table_of_contents_list)}")
        print("-------------------------\n")
    else:
        print("No Table of Contents items found or file was not read.\n")

    # --- Foreword Parsing (Revised Logic) ---
    foreword_text_content = "" # Default to empty string
    if all_lines:
        # parse_foreword now handles finding the ToC end and searching after it.
        parsed_foreword_text, found_foreword_heading_in_body = parse_foreword(all_lines)
        if found_foreword_heading_in_body and parsed_foreword_text:
            foreword_text_content = parsed_foreword_text
        elif found_foreword_heading_in_body and not parsed_foreword_text:
            # Heading found, but no paragraph content followed it as per parsing rules
            print("Note: A 'Foreword' heading was found in the document body, but no subsequent paragraph content was extracted.")
            # foreword_text_content remains ""
        else:
            # No distinct "Foreword" heading found in the document body after the ToC.
            # print("Note: No distinct 'Foreword' section heading found in the document body after the Table of Contents.")
            # foreword_text_content remains ""
            pass # Message is handled by parse_foreword or the final print block

    print("--- Foreword ---")
    if foreword_text_content:
        print(f"Extracted Foreword Paragraph:\n{foreword_text_content}")
    else:
        print("Foreword content is empty or not found as a distinct section in the document body.")
    print("----------------\n")

    # --- Document Body Parsing (Sections, Subsections, etc.) ---
    parsed_sections = []
    if all_lines:
        # Determine where the main document body starts (after ToC)
        toc_end_line_num = -1
        in_toc_block_main = False
        toc_start_marker_main = "Table of Contents"
        toc_end_marker_main = "________________________________________"
        for i, line_content in enumerate(all_lines):
            stripped_line = line_content.strip()
            if stripped_line == toc_start_marker_main:
                in_toc_block_main = True
            if in_toc_block_main and stripped_line == toc_end_marker_main:
                toc_end_line_num = i
                break

        document_body_lines = []
        if toc_end_line_num != -1:
            document_body_lines = all_lines[toc_end_line_num + 1:]
        else:
            if any(toc_start_marker_main in line for line in all_lines):
                 print("Warning: ToC start marker found, but ToC end marker not found for body parsing. Attempting to parse from after ToC start.")
                 # Try to find start and parse after that, otherwise parse all. This is a fallback.
                 temp_toc_start_idx = -1
                 for i, line_content in enumerate(all_lines):
                     if line_content.strip() == toc_start_marker_main:
                         temp_toc_start_idx = i
                         break
                 if temp_toc_start_idx != -1:
                     document_body_lines = all_lines[temp_toc_start_idx+1:] # Risky if ToC is long & no end marker
                 else: # Should not happen if previous warning triggered, but as a safe default
                     document_body_lines = all_lines
            else:
                 print("Warning: ToC markers not found. Parsing sections from all lines, which might include ToC items as stray content.")
                 document_body_lines = all_lines

        parsed_sections = parse_document_body(document_body_lines)

    print("--- Parsed Sections Structure ---")
    if parsed_sections:
        for sec_idx, sec in enumerate(parsed_sections):
            print(f"Section {sec_idx+1}: {sec.section_number}. {sec.section_title}")
            for item_idx, item in enumerate(sec.content):
                if isinstance(item, SubsectionObject):
                    print(f"  L1 Item {item_idx+1}: Subsection - {item.subsection_number}. {item.subsection_title}")
                    for sub_item_idx, sub_item in enumerate(item.content):
                        if isinstance(sub_item, SubsubsectionObject):
                            print(f"    L2 Item {sub_item_idx+1}: Subsubsection - {sub_item.subsubsection_number}. {sub_item.subsubsection_title}")
                            for content_item_idx, content_item in enumerate(sub_item.content):
                                if isinstance(content_item, ParagraphObject):
                                    text_preview = content_item.text[:30].replace("\n", " ")
                                    print(f"      L3 Item {content_item_idx+1}: Paragraph - '{text_preview}...' ({len(content_item.text)} chars)")
                                elif isinstance(content_item, ListObject):
                                    list_preview = content_item.items[0][:20] if content_item.items else "N/A"
                                    print(f"      L3 Item {content_item_idx+1}: List - {len(content_item.items)} items. First: '{list_preview}...'")
                        elif isinstance(sub_item, ParagraphObject):
                            text_preview = sub_item.text[:30].replace("\n", " ")
                            print(f"    L2 Item {sub_item_idx+1}: Paragraph - '{text_preview}...' ({len(sub_item.text)} chars)")
                        elif isinstance(sub_item, ListObject):
                            list_preview = sub_item.items[0][:20] if sub_item.items else "N/A"
                            print(f"    L2 Item {sub_item_idx+1}: List - {len(sub_item.items)} items. First: '{list_preview}...'")
                elif isinstance(item, ParagraphObject):
                    text_preview = item.text[:30].replace("\n", " ")
                    print(f"  L1 Item {item_idx+1}: Paragraph - '{text_preview}...' ({len(item.text)} chars)")
                elif isinstance(item, ListObject):
                    list_preview = item.items[0][:20] if item.items else "N/A"
                    print(f"  L1 Item {item_idx+1}: List - {len(item.items)} items. First: '{list_preview}...'")
        print(f"Total main sections found: {len(parsed_sections)}")
    else:
        print("No main sections parsed.")
    print("-----------------------------\n")

    # --- RootObject Instantiation (Example) ---
    root_object = RootObject(
        document_title=doc_title,
        document_info=document_info_obj,
        table_of_contents=table_of_contents_list,
        foreword=foreword_text_content,
        sections=parsed_sections
    )

    print(f"RootObject created with {len(root_object.sections)} main sections.")

    # --- JSON Serialization ---
    def convert_root_to_json_string(root_obj):
        if not isinstance(root_obj, RootObject):
            raise TypeError("Expected a RootObject instance for JSON conversion.")

        root_dict = root_obj.to_dict()
        try:
            json_string = json.dumps(root_dict, indent=4)
            return json_string
        except TypeError as e:
            print(f"Error during JSON serialization: {e}")
            print("This might be due to a custom object not having a to_dict() method implemented correctly.")
            return None

    final_json_string = convert_root_to_json_string(root_object)

    print("\n--- Generated JSON (Snippet) ---")
    if final_json_string:
        print(final_json_string[:1000] + "\n...") # Print first 1000 chars for a peek
        print(f"\nTotal JSON string length: {len(final_json_string)}")

        # --- File Writing ---
        output_filename = "EOTS_V2.5_GUIDE.json"
        try:
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(final_json_string)
            print(f"\nSuccessfully wrote JSON output to {output_filename}")
        except IOError as e:
            print(f"\nError writing JSON to file {output_filename}: {e}")

    else:
        print("JSON string generation failed. File will not be written.")
    print("-------------------------------\n")
