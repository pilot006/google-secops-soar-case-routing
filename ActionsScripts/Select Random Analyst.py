from SiemplifyAction import SiemplifyAction
from SiemplifyUtils import unix_now, convert_unixtime_to_datetime, output_handler
from ScriptResult import EXECUTION_STATE_COMPLETED, EXECUTION_STATE_FAILED,EXECUTION_STATE_TIMEDOUT
import random
import json
import time

siemplify = SiemplifyAction()
IGNORE_TIME = siemplify.extract_action_param("Ignore time buffer?", print_value=True)

@output_handler
def main():

    alert_ts = siemplify.current_alert.creation_time
    epoch_time = int(time.time() * 1000)
    # 10 mins is 600,000 ms
    if epoch_time - alert_ts > 600000 and IGNORE_TIME == "false":
        status = EXECUTION_STATE_COMPLETED
        output_message = "Skipping assignment as alert is > 10 minutes old."
        result_value = "Skipping assignment as alert is > 10 minutes old."

        siemplify.LOGGER.info("\n  status: {}\n  result_value: {}\n  output_message: {}".format(status,result_value, output_message))
        siemplify.end(output_message, result_value, status)


    address = f"{siemplify.API_ROOT}/{'external/v1/settings/GetUserProfiles'}"
    p = {
        "requestedPage": 0,
        "pageSize": 10000,
        "searchTerm": "",
        "filterDisabledUsers": True,
        "filterRole": False,
        "filterPermissionTypes": [],
        "filterSupportUsers": True,
        "fetchOnlySupportUsers": False
    }
    response = siemplify.session.post(url=address, json=p)
    js = response.json()

    # Get a random user from the list of users from the API
    random_user = random.choice(js['objectsList'])
    siemplify.LOGGER.info("Chose user " + random_user['loginIdentifier'] + " with GUID " + random_user['userName'])

    # Assign the case
    case_id = siemplify.case_id
    siemplify.LOGGER.info("Case ID is: " + siemplify.case_id)
    address = f"{siemplify.API_ROOT}/{'external/v1/dynamic-cases/AssignUserToCase?format=camel'}"
    p = {
        "caseId": case_id,
        "userId": random_user['userName']
    }
    response = siemplify.session.post(url=address, json=p)

    msg = "Succesfully assigned case to: " + random_user['loginIdentifier']
    status = EXECUTION_STATE_COMPLETED
    output_message = msg
    result_value = msg

    siemplify.LOGGER.info("\n  status: {}\n  result_value: {}\n  output_message: {}".format(status,result_value, output_message))
    siemplify.end(output_message, result_value, status)


if __name__ == "__main__":
    main()
