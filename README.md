# Axum Podman Example

This project shows an advised structure for your code when developing with
axum and podman in mind. 

## Project Structure

* **infra/** - *IaC* everything that runs your code goes here
* **infra/compose** podman-compose definitions
* **infra/compose/*/envs** environment variables necessary to run your code; should not include sensitive values
* **infra/compose/scheduled/** podman-compose definitions
* **infra/compose/services/** podman-compose definitions
* **infra/compose/tools/** podman-compose definitions
* **infra/images** podman images necessary to run your code
* **source/** all source code go here
* **source/crates** all crates go here
* **source/crates/libs** shared library crates; local dependencies to other crates
* **source/crates/scheduled** scheduled jobs that run per configuration; cannot be a crate dependency
* **source/crates/services** jobs that await & response to connections; cannot be a crate dependency
* **source/crates/tools** maintenance jobs that are neither scheduled nor await events; cannot be a crate dependency

## Requirements

* cargo + rust
* make
* podman
* podman-compose
* pyinvoke

## How to work here?

This project uses *Makefile* and *tasks.py* [pyinvoke](https://docs.pyinvoke.org/) to automate things so, be 
sure to check out those. To run the web-example, try:

`make web-example-up web-example-wlogs`

That will load the compose configuration for **dev** and reload it when source/crates is changed.

## Kudos

This project is heavely inspired by [Jeremy Chone's work](https://www.youtube.com/@JeremyChone). Do
take some time to go over his channel and projects. 