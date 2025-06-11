import json
import sys
from collections import defaultdict

def load_json_files(file_paths):
    data_list = []
    for path in file_paths:
        with open(path, 'r') as f:
            data = json.load(f)
            data_list.append(data)
    return data_list

def compare_test_results(json_dicts, file_names, names_only=False):
    results_by_test = defaultdict(lambda: defaultdict(list))
    mismatched_tests = set()

    for file_idx, jd in enumerate(json_dicts):
        runs = jd.get("runs", {})
        for test_name, test_runs in runs.items():
            for idx, test in enumerate(test_runs):
                comp_result = test.get("compilation", {}).get("result", -1)
                run_result = test.get("runtime", {}).get("result", -1)
                results_by_test[test_name][idx].append((comp_result, run_result))

    for test_name, configs in results_by_test.items():
        for idx, results in configs.items():
            if len(set(results)) > 1:
                mismatched_tests.add(test_name)
                if not names_only:
                    print(f"\n❌ Mismatch in test: {test_name}, Config {idx}")
                    for fname, (c, r) in zip(file_names, results):
                        print(f"  {fname}: Compilation={c}, Runtime={r}")
    
    if names_only:
        for name in sorted(mismatched_tests):
            print(name)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compare_tests.py file1.json file2.json ... [--names-only]")
        sys.exit(1)

    file_paths = [p for p in sys.argv[1:] if not p.startswith('--')]
    names_only = "--names-only" in sys.argv

    json_dicts = load_json_files(file_paths)
    compare_test_results(json_dicts, file_paths, names_only=names_only)
