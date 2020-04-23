# Prototype: SNAP Financial Factors
[![CircleCI Build Status](https://circleci.com/gh/18F/snap-api-prototype.svg?style=shield)](https://circleci.com/gh/18F/snap-api-prototype)

This is a sketchpad prototyping repo being used by 18F's [Eligibility APIs Initiative](https://github.com/18F/eligibility-rules-service/blob/master/README.md) to explore the financial factors of SNAP eligibility.

:warning: ***None of the eligibility rules expressed in this repository should be considered official interpretations of SNAP rules or policy. This is a sketchpad prototyping repo only.*** :warning:

# What does this do?

This prototype SNAP API calculates a household's estimated eligibility for the SNAP program. The API accepts inputs about a household and returns the following:

+ an estimate of that household's SNAP eligibility
+ an estimated benefit amount
+ an explanation of the logic behind the API's decision-making
+ a link to a state website where a household could apply for SNAP

# Using the API

Our goal is to make this prototype available both as a downloadable Python package and as a web API.

See below for API documentation:

+ [Web API documentation](/docs/web_api_documentation.md)
+ [Python API documentation](/docs/python_api_documentation.md)

An [Web API instance](https://snap-prototype-financial-factors.app.cloud.gov/) is deployed to Cloud.gov. Since this application falls under [ATO pre-assessment](https://before-you-ship.18f.gov/ato/types/#conditions-for-pre-assessment), it is password-protected and only available to Federal staff.

Please reach out via [email](mailto:eligibility-apis-initiative@gsa.gov) if you are a Federal employee and would like a demonstration of the web API and pre-screener.

The API does not cover every state and every facet of SNAP eligibility at this time.

See below for more detail on state coverage and SNAP modeling progress:

+ [SNAP modeling progress](/docs/modeling_progress.md)
+ [State-by-state API coverage](/docs/states_progress.md)

# Developing the API

## Environment

To run the project locally, you will need:

* [Python 3.8.1](https://www.python.org/downloads/).
* [Pipenv](https://pipenv.kennethreitz.org/en/latest/), for installing and managing dependencies.
* [Pyenv](https://github.com/pyenv/pyenv), for managing Python versions. (Optional but recommended.)

## Install the dependencies

```
make install
```

## Run all the tests

```
make check-all
```

## Run locally

```
make serve
```

## Deploy

This app includes a `manifest.yml` file with deploy configuration for [Cloud.gov](https://cloud.gov/) or another [Cloud Foundry](https://www.cloudfoundry.org/) system.
