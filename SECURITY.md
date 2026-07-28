# Security Policy

RepoPulse is a developer tool that scans local repositories and generates project health reports. Security is important because the tool may inspect project files, configuration files, and repository structure.

This document explains how security issues should be reported and how security-related changes are handled.

---

## Supported Versions

Security fixes are handled for the latest version of RepoPulse and the current `main` branch.

| Version | Supported |
| --- | --- |
| Latest release | Yes |
| `main` branch | Yes |
| Older versions | No |

If you are using an older version, please update to the latest version before reporting an issue.

---

## Reporting a Vulnerability

Please do not report security vulnerabilities through public GitHub issues.

If you find a security issue, use GitHub's private vulnerability reporting feature for this repository if it is available.

If private vulnerability reporting is not available, open a public issue asking for a private contact method, but do not include technical details, exploit steps, secrets, proof-of-concept code, or sensitive information in the public issue.

When reporting a vulnerability, include as much safe information as possible:

- A short summary of the issue
- The affected area of the project
- The version or commit tested
- Your operating system and Python version
- Steps to reproduce the issue
- The possible impact
- Any suggested fix, if you have one

Please avoid sharing real secrets, tokens, private keys, passwords, or private repository data.

---

## What Counts as a Security Issue?

Examples of security issues include:

- Accidental exposure of sensitive file contents
- Unsafe file handling
- Path traversal issues
- Unsafe handling of repository paths
- Unexpected writing outside the target output path
- Commands that could execute untrusted code
- Report generation that leaks secrets
- Insecure dependency usage
- Incorrect handling of hidden files or ignored files
- Crashes caused by specially crafted files or folders

---

## What Does Not Count as a Security Issue?

The following are usually not security vulnerabilities:

- General bugs with no security impact
- Missing features
- Typos in documentation
- Formatting issues in reports
- False positives in repository checks
- Suggestions for new checks
- Performance issues without a security impact

These can be reported through normal GitHub issues.

---

## Security Expectations

RepoPulse should follow these principles:

- Do not execute scanned project code
- Do not upload repository contents anywhere
- Do not require network access for normal local scans
- Do not expose secrets in reports
- Do not write files outside the requested output path
- Handle unusual file names safely
- Fail safely with clear error messages
- Keep dependencies minimal and maintained

---

## Local Scanning

RepoPulse is designed to scan local project folders.

A normal scan should only read files and folders needed to generate the repository health report. It should not execute project files, run scripts, install dependencies, or modify the scanned repository unless the user explicitly requests an output file.

---

## Sensitive Files

Repositories may contain sensitive files such as:

- `.env`
- `.env.local`
- Private keys
- API tokens
- Credentials
- Cloud configuration files
- Deployment secrets
- Local database files

RepoPulse should treat these files carefully. Reports should warn about risky files when appropriate, but they should not print secret values or expose sensitive contents.

---

## Responsible Disclosure

Please give maintainers reasonable time to review and fix reported vulnerabilities before publicly disclosing details.

A good disclosure process includes:

1. Report the issue privately.
2. Allow time for investigation.
3. Help verify the fix if possible.
4. Avoid publishing exploit details before a fix is available.

---

## Security Fix Process

When a valid security issue is reported, the expected process is:

1. Confirm the issue.
2. Assess the impact.
3. Prepare a fix.
4. Add tests when possible.
5. Release or merge the fix.
6. Document the change if needed.

Security fixes should be kept focused and should avoid unrelated changes.

---

## Dependency Security

RepoPulse uses a small dependency set to reduce risk.

Contributors should avoid adding new dependencies unless they are clearly needed. If a new dependency is added, it should be actively maintained, widely used, and compatible with the project license.

Before adding a dependency, consider whether the same result can be achieved with the Python standard library.

---

## Safe Contribution Guidelines

When contributing security-related changes:

- Do not include real secrets in tests
- Use fake example values only
- Avoid committing local environment files
- Avoid adding risky file operations
- Add tests for unsafe path or file handling
- Keep error messages useful but not revealing
- Do not introduce network calls into normal local scans

---

## Public Issues

Public issues are welcome for normal bugs and feature requests.

Do not include the following in public issues:

- Real tokens
- API keys
- Passwords
- Private keys
- Private repository contents
- Exploit instructions for an unfixed vulnerability
- Sensitive file contents

If you accidentally share sensitive information publicly, remove it immediately and rotate the affected secret.

---

## Security Scope

RepoPulse is a local repository scanner. The security scope mainly includes:

- CLI behavior
- File reading
- Report generation
- Configuration loading
- Output file writing
- Dependency handling
- Path handling

Issues outside RepoPulse's codebase, such as vulnerabilities in a scanned project, should be reported to that project's maintainers instead.

---

## Thank You

Thank you for helping keep RepoPulse safe and trustworthy.

Responsible security reports help improve the project for everyone.
