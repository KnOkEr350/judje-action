import json
import os
import base64


def main():
    assignment_type = os.getenv("ASSIGNMENT_TYPE", "basic").lower()
    max_score = 10 if assignment_type == "basic" else 20

    score = 0
    results_file = 'results.json'

    if os.path.exists(results_file):
        try:
            with open(results_file, 'r') as f:
                data = json.load(f)
                score = min(int(data.get('score', 0)), max_score)
        except Exception as e:
            print(f"Error reading results: {e}")

    test_status = "pass" if score > 0 else "fail"

    config = {"tests": [{"name": "test1", "run": "exit 0", "points": max_score}]}
    os.makedirs('.github/classroom', exist_ok=True)
    with open('.github/classroom/autograding.json', 'w') as f:
        json.dump(config, f)

    res = {
        "version": 1,
        "status": test_status,
        "max_score": max_score,
        "tests": [{
            "name": "test1",
            "status": test_status,
            "score": score,
            "max_score": max_score,
            "message": f"Final score: {score}/{max_score}",
            "test_code": f"Docker Compose Judge ({assignment_type.upper()})",
            "filename": "runner.py",
            "line_no": 1,
            "execution_time": "1"
        }]
    }

    encoded = base64.b64encode(json.dumps(res).encode('utf-8')).decode('utf-8')
    github_env = os.environ.get('GITHUB_ENV')

    if github_env:
        with open(github_env, 'a') as f:
            f.write(f"TEST1_RESULTS={encoded}\n")
    else:
        print("Warning: GITHUB_ENV not found.")


if __name__ == "__main__":
    main()