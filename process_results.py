import json
import os


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

    autograding_data = {
        "version": 1,
        "status": test_status,
        "max_score": max_score,
        "tests": [
            {
                "name": f"Final Evaluation ({assignment_type.upper()})",
                "status": test_status,
                "score": score,
                "max_score": max_score,
                "message": f"Score: {score}/{max_score}"
            }
        ]
    }

    os.makedirs('.github/classroom', exist_ok=True)
    with open('.github/classroom/autograding.json', 'w') as f:
        json.dump(autograding_data, f, indent=4)


if __name__ == "__main__":
    main()