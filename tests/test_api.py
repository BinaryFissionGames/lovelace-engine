import os
import glob
import time
import json
import base64
import requests
import unittest

import pytest


class TestApi:
    @pytest.mark.python
    def test_all_problems_python_success(
        self, language_solutions_dir, engine_submit_uri, submit_solution
    ):
        python_solutions_dir = language_solutions_dir("python")
        solution_files = glob.glob(os.path.join(python_solutions_dir, "*.py"))
        if not solution_files:
            raise Exception("Couldn't find any python solution files to test")

        for relative_filepath in solution_files:
            absolute_filepath = os.path.join(
                python_solutions_dir, os.path.basename(relative_filepath)
            )

            print("Submitting {:}... ".format(absolute_filepath), end="", flush=True)
            t1 = time.perf_counter()
            result = submit_solution(absolute_filepath, engine_submit_uri)
            t2 = time.perf_counter()
            print("{:.6f} seconds.".format(t2 - t1))

            assert result.get("success") is True, "Failed. Engine output:\n{:}".format(
                json.dumps(result, indent=4)
            )

    @pytest.mark.javascript
    def test_all_problems_javascript_success(
        self, language_solutions_dir, engine_submit_uri, submit_solution
    ):
        javascript_solutions_dir = language_solutions_dir("javascript")
        solution_files = glob.glob(os.path.join(javascript_solutions_dir, "*.js"))
        if not solution_files:
            raise Exception("Couldn't find any javascript solution files to test")

        for relative_filepath in solution_files:
            absolute_filepath = os.path.join(
                javascript_solutions_dir, os.path.basename(relative_filepath)
            )

            print("Submitting {:}... ".format(absolute_filepath), end="", flush=True)
            t1 = time.perf_counter()
            result = submit_solution(absolute_filepath, engine_submit_uri)
            t2 = time.perf_counter()
            print("{:.6f} seconds.".format(t2 - t1))

            assert result.get("success") is True, "Failed. Engine output:\n{:}".format(
                json.dumps(result, indent=4)
            )

    @pytest.mark.julia
    def test_all_problems_julia_success(
        self, language_solutions_dir, engine_submit_uri, submit_solution
    ):
        julia_solutions_dir = language_solutions_dir("julia")

        solution_files = glob.glob(os.path.join(julia_solutions_dir, "*.jl"))
        if not solution_files:
            raise Exception("Couldn't find any julia solution files to test")

        for relative_filepath in solution_files:
            absolute_filepath = os.path.join(
                julia_solutions_dir, os.path.basename(relative_filepath)
            )

            print("Submitting {:}... ".format(absolute_filepath), end="", flush=True)
            t1 = time.perf_counter()
            result = submit_solution(absolute_filepath, engine_submit_uri)
            t2 = time.perf_counter()
            print("{:.6f} seconds.".format(t2 - t1))

            assert result.get("success") is True, "Failed. Engine output:\n{:}".format(
                json.dumps(result, indent=4)
            )

    @pytest.mark.c
    def test_all_problems_c_success(
        self, language_solutions_dir, engine_submit_uri, submit_solution
    ):
        c_solutions_dir = language_solutions_dir("c")

        solution_files = glob.glob(os.path.join(c_solutions_dir, "*.c"))
        if not solution_files:
            raise Exception("Couldn't find any c solution files to test")

        for relative_filepath in solution_files:
            absolute_filepath = os.path.join(c_solutions_dir, os.path.basename(relative_filepath))

            print("Submitting {:}... ".format(absolute_filepath), end="", flush=True)
            t1 = time.perf_counter()
            result = submit_solution(absolute_filepath, engine_submit_uri)
            t2 = time.perf_counter()
            print("{:.6f} seconds.".format(t2 - t1))

            assert result.get("success") is True, "Failed. Engine output:\n{:}".format(
                json.dumps(result, indent=4)
            )
