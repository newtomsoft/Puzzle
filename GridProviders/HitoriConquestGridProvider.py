﻿from bs4 import BeautifulSoup
import requests

from Grid import Grid
from GridProviders.GridProvider import GridProvider


class HitoriConquestGridProvider(GridProvider):
    @staticmethod
    def get_grid(source: str):
        response = requests.get(source)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'puzzleTable'})
        rows = table.find_all('tr')
        matrix = []
        for row in rows:
            cells = row.find_all('td')
            matrix_row = []
            for cell in cells:
                matrix_row.append(int(cell.text))
            matrix.append(matrix_row)
        return Grid(matrix)