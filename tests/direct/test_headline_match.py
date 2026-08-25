from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "headline_match.py"
SDK = "v0.2.16"
PROMPT = "Compare two candidate headlines"
BRIEF = "The article reports that the neighborhood library added Saturday opening hours for a three-month pilot after a volunteer scheduling agreement. It does not claim a permanent expansion."
BOUNDARY = "Supported facts are the Saturday pilot, its three-month duration, and volunteer scheduling agreement. Permanent hours, funding changes, and attendance results are not established."


def contest(vm, direct_deploy, editor):
    vm.sender = editor
    return direct_deploy(str(CONTRACT), "Library begins Saturday-hours pilot", BRIEF, BOUNDARY, sdk_version=SDK)


def two_entries(contract, vm, first_author, second_author):
    vm.sender = first_author
    contract.submit_headline("pilot", "Library adds Saturdays in three-month pilot", "Promises only that Saturday hours begin as a time-limited pilot.")
    vm.sender = second_author
    contract.submit_headline("forever", "Library permanently expands to Saturdays", "Promises that Saturday opening is a permanent schedule change.")


def test_pairwise_consensus_and_editor_selection(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = contest(direct_vm, direct_deploy, direct_alice)
    two_entries(contract, direct_vm, direct_bob, direct_charlie)
    direct_vm.sender = direct_alice
    contract.lock_headlines()
    direct_vm.mock_llm(PROMPT, json.dumps({"preferred": "LEFT", "reason_code": "FAITHFUL"}))
    contract.compare_headlines("pilot", "forever")
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"preferred": "RIGHT", "reason_code": "CLEARER"}))
    assert direct_vm.run_validator(leader_result=leader) is False
    direct_vm.sender = direct_alice
    contract.select_headline("pilot", "Selected because the pairwise review confirms the headline stays within the time-limited evidence boundary.")
    assert contract.get_state()["selected_headline"] == "pilot"


def test_author_revision_and_reverse_pair_duplicate(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = contest(direct_vm, direct_deploy, direct_alice)
    direct_vm.sender = direct_bob
    contract.submit_headline("pilot", "Library adds weekend option", "Promises only a new weekend opening option during the pilot.")
    contract.revise_headline("pilot", "Library adds Saturdays in three-month pilot", "Promises only that Saturday hours begin as a time-limited pilot.")
    direct_vm.sender = direct_charlie
    contract.submit_headline("other", "Saturday library pilot starts with volunteers", "Promises a Saturday pilot supported by the volunteer scheduling agreement.")
    direct_vm.sender = direct_alice
    contract.lock_headlines()
    direct_vm.mock_llm(PROMPT, json.dumps({"preferred": "TIE", "reason_code": "FAITHFUL"}))
    contract.compare_headlines("pilot", "other")
    with direct_vm.expect_revert("pair_already_compared"):
        contract.compare_headlines("other", "pilot")
    assert contract.get_headline("pilot")["revision_count"] == 1


def test_editor_role_and_invalid_reason_fail_closed(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = contest(direct_vm, direct_deploy, direct_alice)
    two_entries(contract, direct_vm, direct_bob, direct_charlie)
    with direct_vm.expect_revert("only_editor"):
        contract.lock_headlines()
    direct_vm.sender = direct_alice
    contract.lock_headlines()
    direct_vm.mock_llm(PROMPT, json.dumps({"preferred": "LEFT", "reason_code": "POPULAR"}))
    with direct_vm.expect_revert("invalid_reason_code"):
        contract.compare_headlines("pilot", "forever")
    assert contract.get_state()["comparison_count"] == 0
