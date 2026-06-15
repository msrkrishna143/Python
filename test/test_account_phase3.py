import pytest
from pages.Phase3.Accounts import Accounts
from test.conftest import logger

@pytest.fixture(scope="function")
def accounts_phase3(login_user_phase3):
    pages, context = login_user_phase3
    return Accounts(pages)


@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_search_phase3(accounts_phase3):
    try:
        accounts_phase3.account_search()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)



@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_filter_assigned_to_phase3(accounts_phase3):
    try:
        accounts_phase3.account_filter_assigned()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)


@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_filter_lead_short_source_to_phase3(accounts_phase3):
    try:
        accounts_phase3.account_filter_short_source()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)


@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_filter_lead_long_source_to_phase3(accounts_phase3):
    try:
        accounts_phase3.account_filter_long_source()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)


@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_filter_category_phase3(accounts_phase3):
    try:
        accounts_phase3.account_filter_category()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_filter_state_phase3(accounts_phase3):
    try:
        accounts_phase3.account_filer_state()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)


@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_filter_types_phase3(accounts_phase3):
    try:
        accounts_phase3.account_filter_types()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)



@pytest.mark.madarasu
@pytest.mark.module("Accounts")
def test_account_filter_date_range_phase3(accounts_phase3):
    try:
        accounts_phase3.account_filter_date_from_to_date()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)


@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_export_phase3(accounts_phase3):
    try:
        accounts_phase3.accounts_export_phase3()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_bulk_actions_phase3(accounts_phase3):
    try:
        accounts_phase3.account_bulk_actions()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_actions_edit_phase3(accounts_phase3):
    try:
        accounts_phase3.account_actions_edit()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)


@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_actions_delete_phase3(accounts_phase3):
    try:
        accounts_phase3.account_actions_delete()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)


@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_actions_log_activity_phase3(accounts_phase3):
    try:
        accounts_phase3.account_actions_log_activity()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_actions_add_contacts_phase3(accounts_phase3):
    try:
        accounts_phase3.account_actions_create_contact()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_contacts_search_phase3(accounts_phase3):
    try:
        accounts_phase3.account_contacts_search()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_contacts_action_edit_phase3(accounts_phase3):
    try:
        accounts_phase3.account_contacts_action_edit()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_contacts_action_delete_phase3(accounts_phase3):
    try:
        accounts_phase3.account_contacts_action_delete()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_contacts_action_call_phase3(accounts_phase3):
    try:
        accounts_phase3.account_contacts_action_call()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_contacts_action_send_email_phase3(accounts_phase3):
    try:
        accounts_phase3.account_contact_send_email()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_contacts_action_dnc_phase3(accounts_phase3):
    try:
        accounts_phase3.account_contacts_action_dnc()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_appointment_search_phase3(accounts_phase3):
    try:
        accounts_phase3.account_appointment_search()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_appointment_actions_record_outcome_phase3(accounts_phase3):
    try:
        accounts_phase3.account_appointment_action_record_outcome()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_appointment_actions_send_email_phase3(accounts_phase3):
    try:
        accounts_phase3.account_appointment_action_send_email()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_appointment_actions_delete_phase3(accounts_phase3):
    try:
        accounts_phase3.account_appointment_action_delete()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_estimations_search_phase3(accounts_phase3):
    try:
        accounts_phase3.account_estimate_search()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_jobs_search_phase3(accounts_phase3):
    try:
        accounts_phase3.account_job_search()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_export_jobs_phase3(accounts_phase3):
    try:
        accounts_phase3.account_job_export_jobs()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_export_jobs_projects_phase3(accounts_phase3):
    try:
        accounts_phase3.account_job_project_export_phase3()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)


@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_jobs_generate_statements_phase3(accounts_phase3):
    try:
        accounts_phase3.account_jobs_generate_statements_phase3()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_jobs_action_mark_cancelled_phase3(accounts_phase3):
    try:
        accounts_phase3.account_job_action_mark_cancel()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_payment_search_phase3(accounts_phase3):
    try:
        accounts_phase3.account_payment_search()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_payment_action_edit_phase3(accounts_phase3):
    try:
        accounts_phase3.account_payment_action_edit()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_activity_search_phase3(accounts_phase3):
    try:
        accounts_phase3.account_activity_search()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)

@pytest.mark.accountsphase3
@pytest.mark.module("Accounts")
def test_account_activity_date_filters_phase3(accounts_phase3):
    try:
        accounts_phase3.account_activity_date_filter()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)