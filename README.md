# Prototype: SNAP Financial Factors

This is a sketchpad prototyping repo being used by 18F's [Eligibility APIs Initiative](https://github.com/18F/eligibility-rules-service/blob/master/README.md) to explore the financial factors of SNAP eligibility.

:warning: ***None of the eligibility rules expressed in this repository should be considered official interpretations of SNAP rules or policy. This is a sketchpad prototyping repo only.*** :warning:

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

## Documentation

+ API documentation: [docs/web_api_documentation.md](/docs/web_api_documentation.md).
+ SNAP modeling progress: [docs/modeling_progress.md](/docs/modeling_progress.md).
+ State-by-state API coverage: [docs/states_progress.md](/docs/states_progress.md)

## Deploy

This app includes a `manifest.yml` file with deploy configuration for [Cloud.gov](https://cloud.gov/) or another [Cloud Foundry](https://www.cloudfoundry.org/) system.

An [API instance](https://snap-prototype-financial-factors.app.cloud.gov/) is deployed to Cloud.gov. Since this application falls under [ATO pre-assessment](https://before-you-ship.18f.gov/ato/types/#conditions-for-pre-assessment), it is password-protected and only available to Federal staff.

Please reach out via [email](mailto:eligibility-apis-initiative@gsa.gov) if you are a Federal employee and would like a demonstration of the web API and pre-screener.
