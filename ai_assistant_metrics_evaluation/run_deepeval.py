import subprocess
import sys


def main():
    command = ["deepeval", "test", "run", "../testcases/test_chatbot_metrics_using_deepeval.py"]
    try:
        result = subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=True,
            encoding="utf-8"
        )
        print("Command output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error while executing the command:")
        print(e.stderr)
        sys.exit(e.returncode)
    except UnicodeDecodeError as e:
        print("Unicode error:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
