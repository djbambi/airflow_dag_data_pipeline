# GitHub Branch Protection Configuration

This document outlines how to configure GitHub branch protection rules to require CI checks to pass before merging pull requests.

## Required CI Checks

The following GitHub Actions workflows must pass before merging:
- **Lint**: Runs `ruff check` to ensure code quality
- **Format**: Runs `ruff format --check` to ensure consistent code formatting
- **Type Check**: Runs `mypy` to ensure type safety

## How to Configure Branch Protection Rules

**Note**: Repository admin access is required to configure branch protection rules.

### Steps:

1. Navigate to the repository settings on GitHub
2. Go to **Settings** → **Branches** → **Branch protection rules**
3. Click **Add rule** or **Edit** an existing rule for the `main` branch
4. Configure the following settings:

   #### Basic Settings
   - **Branch name pattern**: `main`
   - ✅ Check **Require a pull request before merging**
   - ✅ Check **Require status checks to pass before merging**

   #### Required Status Checks
   Under "Status checks that are required", search for and select:
   - `Lint`
   - `Format`
   - `Type Check`

   #### Additional Recommended Settings
   - ✅ Check **Require branches to be up to date before merging**
   - ✅ Check **Do not allow bypassing the above settings**

5. Click **Create** or **Save changes**

## Local Development

Before pushing code, run these checks locally to catch issues early:

```bash
# Run all checks
make check

# Or run individually
make lint      # Lint check
make format    # Format code
make type      # Type check
```

## Workflow Files

The CI workflows are defined in:
- `.github/workflows/ci.yml` - Main CI workflow with lint, format, and typing jobs

Each job runs independently and must pass for the overall CI check to succeed.
