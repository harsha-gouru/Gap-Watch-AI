"""
Module for connecting to "Jules" (GitHub Actions comments or similar).

This module provides functionality to post comments to Pull Requests,
primarily intended for use within GitHub Actions workflows.
"""
import os
import json

def post_pr_comment(message: str, pr_id: str = None, repo_slug: str = None) -> None:
    """
    Simulates posting a comment to a Pull Request on GitHub.

    It can automatically try to detect the PR ID and repository slug from
    GitHub Actions environment variables if not provided explicitly.

    Args:
        message (str): The content of the comment to post.
        pr_id (str, optional): The Pull Request ID (number). If None, attempts
                               to discover from GITHUB_EVENT_PATH. Defaults to None.
        repo_slug (str, optional): The repository slug (e.g., "owner/repo"). If None,
                                   attempts to discover from GITHUB_REPOSITORY.
                                   Defaults to None.
    """
    print("JulesConnector: Attempting to post PR comment...")

    # Attempt to auto-detect repository and PR ID from GitHub Actions environment variables
    detected_repo_slug = os.getenv("GITHUB_REPOSITORY")
    final_repo_slug = repo_slug or detected_repo_slug

    detected_pr_id = None
    github_event_name = os.getenv("GITHUB_EVENT_NAME")

    if github_event_name == "pull_request":
        github_event_path = os.getenv("GITHUB_EVENT_PATH")
        if github_event_path and os.path.exists(github_event_path):
            try:
                with open(github_event_path, "r") as f:
                    event_payload = json.load(f)
                # 'number' for the PR itself, 'issue.number' if event is issue_comment on a PR
                detected_pr_id = event_payload.get("number") or event_payload.get("issue", {}).get("number")
                if detected_pr_id:
                    detected_pr_id = str(detected_pr_id)
            except (json.JSONDecodeError, IOError) as e:
                print(f"JulesConnector: Warning - Could not read or parse GITHUB_EVENT_PATH: {e}")
        # GITHUB_REF can also be used for PR number, e.g., refs/pull/123/merge
        if not detected_pr_id:
            github_ref = os.getenv("GITHUB_REF", "")
            if github_ref.startswith("refs/pull/"):
                try:
                    detected_pr_id = github_ref.split("/")[2]
                except IndexError:
                    print(f"JulesConnector: Warning - Could not parse PR number from GITHUB_REF: {github_ref}")

    final_pr_id = pr_id or detected_pr_id

    print(f"\n--- PR Comment Simulation ---")
    if final_repo_slug:
        print(f"Repository: {final_repo_slug}")
    else:
        print("Repository: Not specified and not detected (GITHUB_REPOSITORY not set).")

    if final_pr_id:
        print(f"PR ID: {final_pr_id}")
    else:
        print("PR ID: Not specified and not detected (not a PR event or PR number couldn't be found).")

    print(f"Message:\n---\n{message}\n---")

    if final_repo_slug and final_pr_id:
        print("\nJulesConnector: If this were a real call, it would proceed with the API request.")
        # TODO: Implement actual GitHub API call to post a comment
        # Example using PyGithub:
        # from github import Github
        # try:
        #     github_token = os.getenv("GITHUB_TOKEN")
        #     if not github_token:
        #         print("JulesConnector: Error - GITHUB_TOKEN not found in environment.")
        #         return
        #
        #     g = Github(github_token)
        #     repo_obj = g.get_repo(final_repo_slug)
        #     pr_obj = repo_obj.get_pull(int(final_pr_id))
        #     pr_obj.create_issue_comment(message)
        #     print(f"JulesConnector: Successfully posted comment to PR #{final_pr_id} in {final_repo_slug}")
        # except Exception as e:
        #     print(f"JulesConnector: Error during GitHub API call - {e}")
        #
        # Example using gh CLI:
        # import subprocess
        # try:
        #    cmd = [
        #        "gh", "pr", "comment", final_pr_id,
        #        "--repo", final_repo_slug,
        #        "--body", message
        #    ]
        #    subprocess.run(cmd, check=True, capture_output=True, text=True)
        #    print(f"JulesConnector: Successfully posted comment via gh CLI to PR #{final_pr_id} in {final_repo_slug}")
        # except FileNotFoundError:
        #    print("JulesConnector: Error - 'gh' CLI command not found.")
        # except subprocess.CalledProcessError as e:
        #    print(f"JulesConnector: Error during gh CLI call - {e.stderr}")

    else:
        print("\nJulesConnector: Cannot proceed with simulated API call - Repository or PR ID is missing.")

    print("--- End of PR Comment Simulation ---\n")


if __name__ == "__main__":
    print("Running JulesConnector demonstration...\n")

    # Scenario 1: Explicitly providing repo and PR ID
    print("--- Scenario 1: Explicit repo and PR ID ---")
    post_pr_comment(
        message="This is a test comment from JulesConnector (Scenario 1).",
        pr_id="123",
        repo_slug="your-username/your-repo"
    )

    # Scenario 2: Simulating running in GitHub Actions (without event file for this test)
    print("\n--- Scenario 2: Simulating GHA environment (basic) ---")
    os.environ["GITHUB_REPOSITORY"] = "simulated/repo"
    # No GITHUB_EVENT_PATH or GITHUB_REF for PR number here, so PR ID will be None
    post_pr_comment(
        message="This is a test comment (Scenario 2 - GHA env, no PR info)."
    )
    del os.environ["GITHUB_REPOSITORY"]

    # Scenario 3: Simulating GHA pull_request event with GITHUB_REF
    print("\n--- Scenario 3: Simulating GHA PR event via GITHUB_REF ---")
    os.environ["GITHUB_REPOSITORY"] = "simulated/ref-repo"
    os.environ["GITHUB_EVENT_NAME"] = "pull_request"
    os.environ["GITHUB_REF"] = "refs/pull/456/merge"
    post_pr_comment(
        message="This is a test comment (Scenario 3 - GHA env with PR via GITHUB_REF)."
    )
    del os.environ["GITHUB_REPOSITORY"]
    del os.environ["GITHUB_EVENT_NAME"]
    del os.environ["GITHUB_REF"]

    # Scenario 4: Simulating GHA pull_request event with GITHUB_EVENT_PATH
    print("\n--- Scenario 4: Simulating GHA PR event via GITHUB_EVENT_PATH ---")
    os.environ["GITHUB_REPOSITORY"] = "simulated/event-repo"
    os.environ["GITHUB_EVENT_NAME"] = "pull_request"
    # Create a dummy event file
    dummy_event_payload = {"number": 789, "pull_request": {"head": {"ref": "feature-branch"}}}
    dummy_event_file = "dummy_event.json"
    with open(dummy_event_file, "w") as f:
        json.dump(dummy_event_payload, f)
    os.environ["GITHUB_EVENT_PATH"] = dummy_event_file
    post_pr_comment(
        message="This is a test comment (Scenario 4 - GHA env with PR via GITHUB_EVENT_PATH)."
    )
    del os.environ["GITHUB_REPOSITORY"]
    del os.environ["GITHUB_EVENT_NAME"]
    del os.environ["GITHUB_EVENT_PATH"]
    os.remove(dummy_event_file)
    
    # Scenario 5: No PR ID or repo provided, and not in GHA environment
    print("\n--- Scenario 5: No context provided ---")
    post_pr_comment(
        message="This is a test comment (Scenario 5 - No context at all)."
    )

    print("JulesConnector demonstration finished.")
