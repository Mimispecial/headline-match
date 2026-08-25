from pathlib import Path
import json

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "Compare two candidate headlines"


def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"preferred": "LEFT", "reason_code": "FAITHFUL"})}})
    return {"validators": [validator.to_dict() for validator in validators]}


def ok(receipt):
    assert tx_execution_succeeded(receipt)


def test_five_validator_pairwise_headline_selection():
    editor_account, first_account, second_account = create_accounts(3)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "headline_match.py")
    deployed = factory.deploy_contract_tx(args=["Library begins Saturday-hours pilot", "The article reports that the library added Saturday opening for a three-month pilot after a volunteer scheduling agreement; it does not claim a permanent expansion.", "Supported facts are the Saturday pilot, three-month duration, and volunteer agreement; permanent hours and attendance results are not established."], account=editor_account, wait_transaction_status=TransactionStatus.FINALIZED)
    ok(deployed)
    address = extract_contract_address(deployed)
    editor = factory.build_contract(address, account=editor_account)
    first = factory.build_contract(address, account=first_account)
    second = factory.build_contract(address, account=second_account)
    ok(first.submit_headline(args=["pilot", "Library adds Saturdays in three-month pilot", "Promises only a time-limited Saturday-hours pilot."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(second.submit_headline(args=["forever", "Library permanently expands to Saturdays", "Promises that Saturday opening is permanent."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(editor.lock_headlines(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(editor.compare_headlines(args=["pilot", "forever"]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED))
    ok(editor.select_headline(args=["pilot", "Selected because the pairwise review keeps the headline inside the time-limited evidence boundary."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert editor.get_state(args=[]).call()["selected_headline"] == "pilot"
