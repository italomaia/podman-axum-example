# Axum Podman Example

This project shows an advised structure for your code when developing with
axum and podman in mind. 

## Project Structure

**infra/** - *IaC* everything that runs your code goes here
**infra/compose** podman-compose definitions
**infra/compose/*/envs** environment variables necessary to run your code; should not include sensitive values
**infra/images** podman images necessary to run your code
**source/** all source code go here
**source/crates** all crates go here