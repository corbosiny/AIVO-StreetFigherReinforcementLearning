# Introduction

### Welcome!

Thank you for considering contributing to AIVO! Any help on the project is appreciated and we hope you are able to take away new skills from contributing!

### Why we have guidelines

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project. In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.

### What contributions we are looking for

#### Adding support for new RL algorithms
Fleshing out the training platform by providing basic implementations of new RL algortihms greatly increases the accessibility of people trying to use the project for research. 

#### Data logging and visualization
The development of tools to log and visualize a variety of training data will make the results of using the training platform much clearer and accessible for those using it. A clear visualization of results is necessary to understand the effects changes to the underlying RL algorithms have on the model.

#### Front and Backend support for the tournament website
A long term goal is to be able to host streamed tournaments between community submitted models. Help creating and maintaining such a platform and integrating interfaces for users to interact will be key to fostering a great community. 

#### Bug Fixes
Patching of logged issues is always a great way to help out the project.

#### Improving documentation
Documentation is key for the longevity and accessability of this project. As the project grows in scope some documentation will need to be appended, updated, or reformatted. Any help in maintaining existing documentation or improving the documentation goes a long way to keeping the project running smoothly.

#### Writing tutorials 
Tutorials are a great ways for people to get started quicker in terms of understanding how to use this project or to use as launching off points to create new features. As the project grows new tutorials will always be needed to help new members of the community.


### What we are not looking for

If your new feature suggestions or patches just don't coincide with the milestones laid out in the README then we encourage you to fork the repo and carry the project in your own direction. This code is open source so feel free to use it in whatever form you like! 

As well please check if your support question as already been addressed in a previous issue and try to reframe from privately messaging a maintainer when others could benifit in the future from seeing your questions publicly discussed. And please use the discord first for asking questions before opening up an issue

# Ground Rules
### Contributer Responsibilities.
This includes not just how to communicate with others (being respectful, considerate, etc) but also technical responsibilities (importance of testing, project dependencies, etc). Mention and link to your code of conduct, if you have one.

Responsibilities
* Ensure cross-platform compatibility for every change that's accepted. Windows, Mac, Debian & Ubuntu Linux.
* Ensure that code that goes into src meets all style, naming, and testing requirements detailed at the bottom of this document.
* Create issues for any major changes and enhancements that you wish to make. Discuss things transparently and get community feedback.
* Don't add any classes to the codebase unless absolutely needed. Err on the side of using functions.
* Keep feature versions as small as possible, preferably one new feature per version.
* Be welcoming to newcomers and encourage diverse new contributors from all backgrounds. See the [Python Community Code of Conduct](https://www.python.org/psf/codeofconduct/).

# Your First Contribution

Unsure where to begin contributing? You can start by looking through these beginner and help-wanted issues:
> Beginner issues - issues which should only require a few lines of code, and a test or two.
> Help wanted issues - issues which should be a bit more involved than beginner issues.
> Both issue lists are sorted by total number of comments. While not perfect, number of comments is a reasonable proxy for impact a given change will have.

Issues involving updating documentation may also be a great place to start contributing and is just as important as code contributions.

Finally making examples is a great way to teach yourself and contribute something useful.

### Resources for people who have never contributed to open source before.
Here are a couple of tutorials for people new to open source: http://makeapullrequest.com/, http://www.firsttimersonly.com/, and [How to Contribute to an Open Source Project on GitHub](https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github).

As well feel free to ask for any help you need as a beginner. The maintainers will try to help to the best of their ability when available.

# Getting started
### Give them a quick walkthrough of how to submit a contribution.
For something that is bigger than a one or two line fix:

1. Create your own fork of the code 
2. Do the changes in your fork
3. If you like the change and think the project could use it:
    * Be sure you have followed the code style for the project.
    * Be sure to satisfy the testing requirements for the project.
    * Submit a pull request and add the author and any maintainers you wish to review your code.
    * If your contribution is related to a ticket that has been assigned to you than make sure to manage the lists it is in.
4. After approval of the contribution squash your commits into one commit and merge it into master

If it is a simple one or two line fix or a typo please raise an issue. As a rule of thumb, changes are obvious fixes if they do not introduce any new functionality or creative thinking. As long as the change does not affect functionality, some likely examples include the following:
* Spelling / grammar fixes
* Typo correction, white space and formatting changes
* Comment clean up
* Bug fixes that change default return values or error codes stored in constants
* Adding logging messages or debugging output
* Changes to ‘metadata’ files like .gitignore, build scripts, etc.
* Moving source files from one directory or package to another

For information on setting up your development environment please consult the "Getting Started" section of the readme.

# How to report a bug
### Security Disclosures
If you find a security vulnerability, do NOT open an issue. Email the current author(coreyohulse@gmail.com) instead. DO NOT POST THE VULNERABILITY PUBLICLY. Let the maintainers develop a release strategy once the issue has been fixed.

In order to determine whether you are dealing with a security issue, ask yourself these two questions:
* Can I access something that's not mine, or something I shouldn't have access to?
* Can I disable something for other people?

If the answer to either of those two questions are "yes", then you're probably dealing with a security issue. Note that even if you answer "no" to both questions, you may still be dealing with a security issue, so if you're unsure, just email us at coreyohulse@gmail.com.

### How to File a Bug Report.
When filing an issue, make sure to answer these five questions:

 1. What version of Python are you using?
 2. What operating system are you using?
 3. What did you do?
 4. What did you expect to see?
 5. What did you see instead?

There is already a template in the .git folder that demonstrates what information is helpful for us to solve the issue.

# How to suggest a feature or enhancement

### Aligning with our Goals.

The goal of AIVO is to provide a platform that eases the process of creating RL models to play street fighter 2 and to provide a system for organizing tournaments between user submitted agents. The current milestones and stretch goals of the project can be seen on the Trello board. Please refer to those to see if a suggested feature fits the direction of this project. 

### Best way to suggest a feature.
Follow the standard feature request template in the .git folder of the repo. Currently the current author has to sign off on any feature request before it is turned into a ticket and worked on by the community. We try to include all features we believe apply to 80% of the users that are using this platform. We encourage all suggestions as if there is a feature you are thinking you would like then others most likely are thinking of the same feature.

# Code review process

* All pull requests must be passing all tests before they are accepted
* The current owner must be added as a reviewer for every pull request
* Please wait 4 days before pinging anyone for feedback if there is no initial response
* Squash all commits into one commit with a clear and concise summary of the branches purpose before merging
* All new features must include their own new test code, features without proper coverage will be rejected
* If you opened a pull request we expect you to carry through and see it finished. It is bad form to open a pull request and abandon it
* If two weeks go by with no response to feedback then we will close the pull request
* If a maintainer asks you to rebase some of your patch or rejects it please keep things civil and know that it is not personal
* Stop by a maintainers office hours if you ever have questions regarding your request

# Community
The community trello board is open for anyone to take and manage tickets but please only allow the maintainers to generate new tickets. Link to the board: https://trello.com/invite/b/bLHQK3YK/865c2cec2043e07bcc67d283f236871d/street-fighter-ai

Here is an invite to the community discord: https://discord.gg/ZYVRXGduM9

Current Author: corbosiny
Office hours: Friday, 2-4

# Code Style, Naming, and labeling conventions

### Code Style

* The PEP 8 style guide should be consulted for any code formatting questions. The only difference is that we prefer to use camel case instead of underscore naming conventions solely based on personal preference
* Every class, script, and function should have Docstrings following the established formats in the existing code
* Line length is not enforced but do try to keep it under 100 characters

### Branch Naming Conventions

* Feature branches should start with "feature_" at the beginning of their name
* Bug Fix branches should start with "bugFix_" at the beginning of their name
* Documentation branches should start with "documentation_" at the beginning of their name
* Training branches should start with "training_" at the beginning of their name


### Labeling Issues.

**Follow these guidelines:** [1] [Atom](https://github.com/atom/atom/blob/master/CONTRIBUTING.md#issue-and-pull-request-labels)