# Contributor's Guide on Collaborative Practices for cloe-org repositories

This document describes some best practices for collaborating on the cloe-org repositories.
Following these practices makes it easier for contributors (new and old) to understand what is expected of them.
It should be linked to in the README.md. Those are meant to be general guidelines; it is possible that some repositories have additional guidelines.

There are many good practices that this document does not cover.
These include other members of the wider community reviewing pull requests (PRs) they are interested in, and maintainers encouraging and supporting people who open issues to make PRs to solve them.
This document facilitates these other good practices by clarifying what can seem like a mysterious process to those who are unfamiliar with it.

#### Contributing PRs

*   PRs should match the existing code style present in the file.
*   PRs affecting the public API, including adding new features, must update the public documentation.
*   Comments and (possibly internal) docstrings should make the code accessible.
*   PRs that change code must have appropriate tests.
*   Changes to the code must be made via PR, not pushing to master.
*   Before starting to work on a PR, especially when including or modifying a huge chunk of code, discuss with the mantainers the change you are gonna implement and how.

#### Reviewing, Approving, and Merging PRs

*   PRs must have 1 approval before they are merged.
*   PR authors should not approve their own PRs.
*   PRs should pass CI tests before being merged.
*   PRs by people __without__ merge rights must have approval from someone who has merge rights (who will usually then merge the PR).
*   PRs by people __with__ merge rights must have approval from someone else, who may or may not have merge rights (and then may merge their own PR).
*   PRs by people with merge rights should not be merged by people other than the author (just approved).

#### Releases

*   A release should be made as soon as possible after a bugfix PR is merged.
*   Care and consideration should be given as to when to make a breaking release.
*   The person who merged the PR should register the new release of the package.

---

# ColPrac: Further Guidance

This page offers some further guidance on conventions that can be helpful when collaborating on projects.
This is an expansion on the Collaborative Practices, with more details and extra guidance.
Anything detailed here should be considered less important than the main Collaborative Practices.

## Guidance on contributing PRs

*   You should usually open an issue about a bug or possible improvement before opening a PR with a solution.
*   PRs should do a single thing, so that they are easier to review.
    *   For example, fix one bug, or update compatibility, rather than fixing a bunch of bugs, and updating compatibility, and adding a new feature.
*   PRs should add tests which cover the new or fixed functionality.

*   PRs with large improvements to style should not also change functionality.

*   PRs introducing breaking changes should make this clear when opening the PR.
*   You should not push commits with commented-out code.
    *   Commenting out tests while developing locally is okay, but committing a commented-out test increases the risk of it silently not being run when it should be.
*   You should not squash down commits while review is still ongoing.

    *   Squashing commits prevents the reviewer from seeing what commits have been added since the last review.
*   You should help __review__ your PRs, even though you cannot __approve__ your own PRs.

    *   For instance, start the review process by commenting on why certain bits of the code changed, or highlighting places where you would particularly like reviewer feedback.

## Guidance on reviewing PRs

* Review comments should be phrased as questions to encourage open dialogue. For example, "Why did you change this to X? How does it affect Y?"

* Use the suggested change feature for small fixes like typos to streamline the process.

* Reviewers should remain engaged until the PR is merged.

* The PR process is a conversation to improve code. Developers should justify their choices, and reviewers should seek clarification when needed. Both parties should approach feedback constructively and collaboratively, as the final gola of the PR is to have it merged.


### Accidental breaking releases

This section of the guidelines is specifically meant for the mantainers only.

It is important to fix it **as soon as possible**, as otherwise people start using the breaking change, and reverting it later causes more problems (c.f.[ Murphy's law](https://en.wikipedia.org/wiki/Murphy%27s_law)).

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
