import json
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionHashVariant, TransactionStatus
from gltest.utils import extract_contract_address


def ok(receipt):
    assert tx_execution_succeeded(receipt)
    assert receipt.get("status_name") == TransactionStatus.FINALIZED.value
    assert receipt.get("result_name") in (None, "AGREE", "MAJORITY_AGREE")
    assert receipt.get("tx_execution_result_name") in (None, "FINISHED_WITH_RETURN")
    return receipt


@pytest.mark.integration
def test_studionet_headline_comparison(default_account, secondary_account, tertiary_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "headline_match.py")
    deployed = ok(factory.deploy_contract_tx(args=["Library begins Saturday-hours pilot", "The article reports that the library added Saturday opening for a three-month pilot after a volunteer scheduling agreement; it does not claim a permanent expansion.", "Supported facts are the Saturday pilot, three-month duration, and volunteer agreement; permanent hours and attendance results are not established."], account=default_account, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    editor = factory.build_contract(address, account=default_account)
    first = factory.build_contract(address, account=secondary_account)
    second = factory.build_contract(address, account=tertiary_account)
    ok(first.submit_headline(args=["pilot", "Library adds Saturdays in three-month pilot", "Promises only a time-limited Saturday-hours pilot."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(second.submit_headline(args=["forever", "Library permanently expands to Saturdays", "Promises that Saturday opening is permanent."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(editor.lock_headlines(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    intelligent = ok(editor.compare_headlines(args=["pilot", "forever"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    comparison = editor.get_comparison(args=["pilot", "forever"]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    assert comparison["preferred"] in ("LEFT", "RIGHT", "TIE")
    assert comparison["reason_code"] in ("FAITHFUL", "CLEARER", "BOTH_OVERREACH")
    observed = {"preferred": comparison["preferred"], "reason_code": comparison["reason_code"]}
    print("STUDIONET_RECORD=" + json.dumps({"address": address, "deploy_tx": deployed["hash"], "intelligent_tx": intelligent["hash"], "observed": observed}, sort_keys=True))
