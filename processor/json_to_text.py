import json
import os

# ─── Load JSON ───


def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


# ─── Each section gets its own converter function ───

def convert_basic_info(data):
    text = f"University Name: {data['university_name']}\n"
    text += f"Admission Hotline: {data['admission_hotline']}\n"
    return text


def convert_important_links(links):
    lines = ["BUBT Important Links:\n"]
    labels = {
        "website": "Official website",
        "facebook": "Official Facebook page",
        "qs_ranking": "QS World University Ranking profile",
        "bubt_at_a_glance": "BUBT at a glance overview",
        "research_publications": "Research and publications",
        "class_routine": "Class routines",
        "admission": "Online admission portal"
    }
    for key, url in links.items():
        label = labels.get(key, key.replace("_", " ").title())
        lines.append(f"{label}: {url}")
    return "\n".join(lines)


def convert_undergraduate_programs(programs):
    lines = ["BUBT Undergraduate Programs and Fees:\n"]
    for p in programs:
        lines.append(
            f"The {p['program']} program has a total of {p['total_credit_hours']} credit hours "
            f"across {p['total_semester']} semesters. "
            f"Per credit fee is {p['per_credit_fee_tk']} BDT. "
            f"Total course fee is {p['total_course_fee_tk']} BDT. "
            f"First semester fee is {p['first_semester_fee_tk_cm']} BDT. "
            f"Other semester fees are {p['other_semester_fee_tk']} BDT. "
            f"Admission and ID card fee is {p['admission_id_card_fee_tk']} BDT. "
            f"Fees payable at admission are {p['fees_at_admission_tk']} BDT.\n"
        )
    return "\n".join(lines)


def convert_graduate_programs(programs):
    lines = ["BUBT Graduate Programs and Fees:\n"]
    for p in programs:
        lines.append(
            f"The {p['program']} program has a total of {p['total_credit_hours']} credit hours "
            f"across {p['total_semester']} semesters. "
            f"Per credit fee is {p['per_credit_fee_tk']} BDT. "
            f"Total course fee is {p['total_course_fee_tk']} BDT. "
            f"First semester fee is {p['first_semester_fee_tk_cm']} BDT. "
            f"Other semester fees are {p['other_semester_fee_tk']} BDT. "
            f"Admission and ID card fee is {p['admission_id_card_fee_tk']} BDT. "
            f"Fees payable at admission are {p['fees_at_admission_tk']} BDT.\n"
        )
    return "\n".join(lines)


def convert_evaluation_system(evaluation):
    lines = ["BUBT Evaluation System:\n"]
    for program_type, details in evaluation.items():
        lines.append(
            f"For {program_type.replace('_', ' ').title()} (Total: {details['total_marks']} marks):")
        for component in details["components"]:
            lines.append(
                f"  - {component['name']}: {component['percentage']}%")
        lines.append("")
    return "\n".join(lines)


def convert_grading_system(grades):
    lines = ["BUBT Grading System:\n"]
    for g in grades:
        lines.append(
            f"{g['numerical_grade']} corresponds to letter grade {g['letter_grade']} "
            f"with a grade point of {g['grade_point']}."
        )
    return "\n".join(lines)


def convert_gpa_computation(examples):
    lines = ["BUBT GPA Computation Example:\n"]
    # handle both list and dict
    if isinstance(examples, list):
        for ex in examples:
            lines.append(str(ex))
    elif isinstance(examples, dict):
        for key, value in examples.items():
            lines.append(f"{key}: {value}")
    return "\n".join(lines)


def convert_academic_policies(policies):
    lines = ["BUBT Academic Policies:\n"]
    if isinstance(policies, list):
        for policy in policies:
            lines.append(f"- {policy}")
    elif isinstance(policies, dict):
        for key, value in policies.items():
            lines.append(f"{key.replace('_', ' ').title()}: {value}")
    return "\n".join(lines)


def convert_admission_requirements(requirements):
    lines = ["BUBT Admission Requirements:\n"]
    if isinstance(requirements, list):
        for req in requirements:
            lines.append(f"- {req}")
    elif isinstance(requirements, dict):
        for key, value in requirements.items():
            lines.append(f"{key.replace('_', ' ').title()}: {value}")
    return "\n".join(lines)


def convert_required_documents(documents):
    lines = ["Documents Required for BUBT Admission:\n"]
    if isinstance(documents, list):
        for doc in documents:
            lines.append(f"- {doc}")
    elif isinstance(documents, dict):
        for key, value in documents.items():
            lines.append(f"{key.replace('_', ' ').title()}: {value}")
    return "\n".join(lines)


def convert_scholarships_and_waivers(scholarships):
    lines = ["BUBT Scholarships and Waivers:\n"]
    if isinstance(scholarships, list):
        for item in scholarships:
            lines.append(f"- {item}")
    elif isinstance(scholarships, dict):
        for key, value in scholarships.items():
            lines.append(f"{key.replace('_', ' ').title()}: {value}")
    return "\n".join(lines)


def convert_campus_facilities(facilities):
    lines = ["BUBT Campus Facilities:\n"]
    if isinstance(facilities, list):
        for item in facilities:
            lines.append(f"- {item}")
    elif isinstance(facilities, dict):
        for key, value in facilities.items():
            lines.append(f"{key.replace('_', ' ').title()}: {value}")
    return "\n".join(lines)


def convert_research_and_publications(research):
    lines = ["BUBT Research and Publications:\n"]
    if isinstance(research, list):
        for item in research:
            lines.append(f"- {item}")
    elif isinstance(research, dict):
        for key, value in research.items():
            lines.append(f"{key.replace('_', ' ').title()}: {value}")
    return "\n".join(lines)


def convert_accreditations(accreditations):
    lines = ["BUBT Accreditations and Memberships:\n"]
    if isinstance(accreditations, list):
        for item in accreditations:
            lines.append(f"- {item}")
    elif isinstance(accreditations, dict):
        for key, value in accreditations.items():
            lines.append(f"{key.replace('_', ' ').title()}: {value}")
    return "\n".join(lines)


# ─── Master converter — calls all section converters ─────────────────────────

def convert_all(data):
    sections = []

    sections.append(convert_basic_info(data))
    sections.append(convert_important_links(data["important_links"]))
    sections.append(convert_undergraduate_programs(
        data["undergraduate_programs"]))
    sections.append(convert_graduate_programs(data["graduate_programs"]))
    sections.append(convert_evaluation_system(data["evaluation_system"]))
    sections.append(convert_grading_system(data["grading_system"]))
    sections.append(convert_gpa_computation(data["gpa_computation_example"]))
    sections.append(convert_academic_policies(data["academic_policies"]))
    sections.append(convert_admission_requirements(
        data["admission_requirements"]))
    sections.append(convert_required_documents(data["required_documents"]))
    sections.append(convert_scholarships_and_waivers(
        data["scholarships_and_waivers"]))
    sections.append(convert_campus_facilities(data["campus_facilities"]))
    sections.append(convert_research_and_publications(
        data["research_and_publications"]))
    sections.append(convert_accreditations(
        data["accreditations_and_memberships"]))

    # Join all sections with a clear separator
    return "\n\n" + ("=" * 60) + "\n\n".join(sections)


# ─── Save to file ─────────────────────────────────────────────────────────────

def save_text(text, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    data = load_json("data/bubt_data.json")
    full_text = convert_all(data)
    save_text(full_text, "data/bubt_clean_text.txt")
    print("Done! Check data/bubt_clean_text.txt")
