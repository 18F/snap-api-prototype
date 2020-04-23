import yaml
import pkgutil


class FetchProgramData:
    '''
    Small class to wrap fetching and parsing program data from static YAML files.
    '''

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def parse_data(self):
        raw_data = pkgutil.get_data(
            "snap_financial_factors.program_data", self.filename
        )

        return yaml.safe_load(raw_data)
