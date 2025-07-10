# Contributor's Guide on Collaborative Practices for cloe-org repositories

This document outlines the best practices for collaborating within the cloe-org repositories. By adhering to these guidelines, both new and experienced contributors can gain a clear understanding of what is expected of them. It should be linked in the README.md file as a central reference, although some repositories may include additional requirements.

The purpose of this document is to provide clarity on the review process, thereby streamlining and facilitating it.

#### General guidelines on versioning and collaborating with `git`

The repositories in this organisation use `git` for versioning. There are many online resources to learn and master `git` (e.g. [Git Real](https://www.pluralsight.com/courses/code-school-git-real) and [Git Real 2](https://www.pluralsight.com/courses/code-school-git-real-2) by Pluralsight - formerly Coursera). We use something similar to [GitHub Flow](https://githubflow.github.io) to version and collaborate on our repos. Please read below for more details on our implementation of this approach. 

A few important `git` things to keep in mind as a developer:
*   Commit often, push carefully. `git pull --rebase` first. 
*   Use `git status` often.
*   Develop on a well-named branch out of `main`.
*   Avoid long-lived branches - use PRs (see below) to resolve them frequently for specific tasks.
*   Do not `git add` files that will bloat the repo! This includes data files, binaries like images, compressed files. The most common file extensions should be automatically ignored, but you can never be too careful.

#### Contributing PRs

*   PRs should adhere to the existing code style present in the file.
*   PRs affecting the public API, including the addition of new features, must update the public documentation.
*   Comments and (potentially internal) docstrings should enhance the code's readability and ease of use.
*   PRs that modify code must include appropriate tests.
*   Changes to the code must be implemented via PR, not by pushing directly to the main branch.
*   Before initiating work on a PR, especially when incorporating or modifying a substantial portion of code, discuss the proposed changes and implementation approach with the maintainers. The list of maintainers for each repository is provided in the respective repo's README.

#### Reviewing, Approving, and Merging PRs

The responsibility for merging a PR lies with the maintainers of the repository. Maintainers must verify that the PR implements appropriate unit tests and documentation, and more crucially, assess how the new code impacts the global architecture. Additionally, in cases of concurrent PRs, maintainers will coordinate their development and merging to optimize the workflow and minimize the required effort.

*   PRs must receive at least one approval before they can be merged.
*   PR authors should refrain from approving their own PRs.
*   PRs should successfully pass CI tests prior to merging.
*   All PRs must be approved by an individual with merge rights, even if the submitter already possesses such privileges.

---

#### Releases

*   A release should be created as soon as possible following the merge of a bugfix PR.
*   Care and consideration should be exercised when deciding the timing of a breaking release.
*   The individual who merged the PR should be responsible for registering the new release of the package.
*   Version naming conventions adhere to Semantic Versioning ([semver](https://semver.org/)) principles.

---

# ColPrac: Further Guidance

This page provides additional guidance on conventions that can be useful when collaborating on projects. It serves as an expansion of the Collaborative Practices, offering more detailed information and extra guidance. Any details outlined here should be considered secondary in importance to the main Collaborative Practices.

## Guidance on contributing PRs

*   You should typically open an issue regarding a bug or potential improvement before submitting a PR with a solution.
*   PRs should focus on a single task to facilitate easier review.
    *   For example, fix one bug, update compatibility, or add a new feature, rather than combining multiple tasks in one PR.
*   PRs should include tests that cover the new or fixed functionality.

*   PRs implementing large-scale style improvements should not simultaneously alter functionality.

*   PRs introducing breaking changes should clearly indicate this when opening the PR.
*   You should avoid pushing commits with commented-out code.
    *   While commenting out tests during local development is acceptable, committing a commented-out test increases the risk of it being inadvertently ignored when it should be run.
*   You should refrain from squashing commits while the review process is ongoing.

    *   Squashing commits prevents reviewers from identifying which commits have been added since the last review.
* You should assist in the __review__ of your PRs, even though you cannot __approve__ your own PRs.

    *   For instance, initiate the review process by commenting on the rationale behind certain code changes, or highlighting areas where you particularly seek reviewer feedback.


## Guidance on reviewing PRs

* Review comments should be phrased as questions to encourage open dialogue. For example, "Why did you change this to X? How does it affect Y?"

* Use the suggested change feature for small fixes like typos to streamline the process.

* Reviewers should remain engaged until the PR is merged.

* The PR process is a conversation aimed at improving code. Developers should justify their choices, and reviewers should seek clarification when needed. Both parties should approach feedback constructively and collaboratively, as the ultimate goal of the PR is to have it merged.

### Accidental breaking releases

This section of the guidelines is specifically meant for the maintainers only.

It is important to fix breaking changes **as soon as possible**, as otherwise people start using the breaking change, and reverting it later causes more problems (c.f. [Murphy's law](https://en.wikipedia.org/wiki/Murphy%27s_law)).

To fix it:

1. Make a PR which reverts the PR that made the breaking change.
2. Bump the Patch version number in the pyproject.toml.
    The breaking API change was a bug, so a Patch release is correct to fix it.
3. Merge the PR and release the new version.

Once the change is reverted, you can take stock and decide what to do.
There are generally 2 options:

1. Make a new PR to reimplement the feature in a non-breaking way.
2. Make a new PR which reverts the reversion, bump the version number to signify it as breaking, and release the new breaking version.

#### **Example**

Consider a package which is currently on v1.14.2.
I made a PR to add a new feature and tagged release v1.15.0.
The next evening, we get bug reports that the new feature actually broke lots of real uses.

Maybe I changed what I thought was an internal function, but one that was actually part of the public API; maybe I accidentally changed the return type, and that was something people depended on.
Whatever it was, I broke it, and this was not caught in code review.

To fix it, I revert the change, and then tag release v1.15.1.
Hopefully, I can also add a test to prevent that part of the API from being broken by mistake.

Now I look at my change again.
If I can add the same functionality in a non-breaking way - for example, make a new internal function for my use - then I would do so and tag v1.15.2 or v1.16.0 depending on what had to change.
If I cannot make an equivalent non-breaking change, then I would have to make the breaking change and tag v2.0.0.
