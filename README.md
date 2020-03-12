# Prototype: SNAP Financial Factors

This is a sketchpad prototyping repo being used by 18F's [Eligibility APIs Initiative](https://github.com/18F/eligibility-rules-service/blob/master/README.md) to explore the financial factors of SNAP eligibility.

:warning: ***None of the eligibility rules expressed in this repository should be considered official interpretations of SNAP rules or policy. This is a sketchpad prototyping repo only.*** :warning:

## Environment

To run the project locally, you will need:

* [Python 3.7](https://www.python.org/downloads/).
* [Pipenv](https://pipenv.kennethreitz.org/en/latest/), for installing and managing dependencies.
* [Pyenv](https://github.com/pyenv/pyenv), for managing Python versions. (Optional but recommended.)

## Install the dependencies

```
make install
```

## Run tests

```
make test
```

## Run locally

```
make serve-local
```

## Deploy

This app includes a `manifest.yml` file with deploy configuration for [Cloud.gov](https://cloud.gov/) or another [Cloud Foundry](https://www.cloudfoundry.org/) system.

A [demo API and pre-screener](https://snap-prototype-financial-factors.app.cloud.gov/) are deployed to Cloud.gov. Since this application falls under [ATO pre-assessment](https://before-you-ship.18f.gov/ato/types/#conditions-for-pre-assessment), it is password-protected and only available to Federal staff.

Please reach out via [email](mailto:eligibility-apis-initiative@gsa.gov) if you are a Federal employee and would like a demonstration of the web API and pre-screener.

## Test the Web API locally

```sh
# IL, 1 person, no income or savings:

curl -X POST -H "Content-Type: application/json" \
  -d @./sample_input_data/il-1-person-no-income-or-savings.json \
  http://127.0.0.1:5000/calculate
```

# Modeling notes

+ See [notes/modeling_progress.md](/notes/modeling_progress.md).
