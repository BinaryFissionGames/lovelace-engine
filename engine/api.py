import base64
import falcon
import json
import logging
import importlib

from engine.runners.python_runner import PythonRunner
import engine.util as util

# Config applies to all other loggers
logging.basicConfig(format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SubmitResource(object):
    def on_post(self, req, resp):
        """Handle POST requests."""
        try:
            raw_json = req.stream.read()
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex.message)

        try:
            result_json = json.loads(raw_json.decode('utf-8'))
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Invalid JSON', 'Could not decode the request body.')

        # Write user's code to file.
        code = result_json.get('code')
        if code:
            decoded_code = str(base64.b64decode(code), 'utf-8')
            code_filename = util.write_str_to_file(decoded_code)
            logger.debug("User code saved in: %s", code_filename)
        else:
            raise falcon.HTTPError(falcon.HTTP_400, 'Invalid JSON.', 'No code provided.')

        # Fetch problem ID and load the correct problem module.
        problem_id = result_json.get('problemID')
        try:
            problem = importlib.import_module('problems.' + problem_id)
            test_case_type_enum = problem.TEST_CASE_TYPE_ENUM
        except Exception:
            logger.error("Could not import module `problems.%s`", problem_id)
            logger.error("Returning HTTP 400 Bad Request due to possibly invalid JSON.")
            raise falcon.HTTPError(falcon.HTTP_400, 'Invalid JSON.', 'Invalid problemID!')

        logger.info("Generating test cases...")
        test_cases = []

        # Count number of test cases we'll be generating in total.
        n_cases = 0
        for test_type in test_case_type_enum:
            n_cases += test_type.multiplicity

        # Generate all the cases and store them in test_cases.
        n = 1
        for test_type in test_case_type_enum:
            for _ in range(test_type.multiplicity):
                logger.debug("Generating test case %d/%d...", n, n_cases)
                test_cases.append(problem.generate_input(test_type))
                n = n+1

        n = 1  # test case counter
        passes = n_cases*[None]
        test_case_details = []  # List of dicts each containing the details of a particular test case.

        for tc in test_cases:
            input_str = tc.input_str()
            user_answer, process_info = PythonRunner().run(code_filename, input_str)
            passed = problem.verify_user_solution(input_str, user_answer)

            logger.info("Test case %d/%d (%s).", n, n_cases, tc.test_type.test_name)
            logger.debug("Input string:")
            logger.debug("%s", input_str)
            logger.debug("Output string:")
            logger.debug("%s", user_answer)

            if passed:
                passes[n-1] = True
                logger.info("Test case passed!")
            else:
                passes[n-1] = False
                logger.info("Test case failed.")

            n = n+1
            test_case_details.append({
                'testCaseType': tc.test_type.test_name,
                'inputString': input_str,
                'outputString': user_answer,
                'inputDict': tc.input,
                'outputDict': tc.output,  # TODO: This is our solution. We should be using the user's soluton.
                'passed': passed,
                'processInfo': process_info
            })

        n_passes = sum(passes)  # Turns out you can sum booleans (True=1, False=0).
        all_solved = True if n_passes == n_cases else False

        logger.info("Passed %d/%d test cases.", n_passes, n_cases)

        resp_dict = {
            'success': True if all_solved else False,
            'testCaseDetails': test_case_details
        }

        resp.status = falcon.HTTP_200
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.body = json.dumps(resp_dict)

        util.delete_file(code_filename)
        logger.debug("User code file deleted: %s", code_filename)


app = falcon.API()
app.add_route('/submit', SubmitResource())
