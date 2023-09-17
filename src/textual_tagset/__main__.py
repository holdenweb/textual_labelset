"""
demo.py: show off the features of textual_tagset.
"""
from textual.app import App
from textual_tagset import TagSetSelector
from textual.containers import Horizontal, Vertical

selected = (
    "Liberty Baxter, Nevada Bray, Tasha Quinn, Teegan Mays, Omar Hendrix, "
    "Shelley Frost, Hyatt Serrano, Mariko Tyler, Grant Hernandez, Kiara Bolton, "
    "Lucy Hahn, Vladimir Mcmillan, Alvin Byrd, Melanie Coleman, Edan Brady, "
    "John Hahn, Wyatt Gross, Lionel Knapp, Montana Hoover, Ursa Kiddv, "
    "Cheyenne Elliott, Nathan Dixon, Jayme Witt, Patricia Barrett, Christen Zimmerman, "
    "Lesley Booth, Victoria Salinas, Philip Walls, Pearl Martin, Garrett Guzman, "
    "Brady Decker, Ebony Sampson, Fletcher Ellis, Stewart Crawford, Graiden Mcdowell"
).split(", ")

deselected = (
    "Isaiah Larson, Owen Leach, Carter Bowman, Cyrus Pruitt, Bernard Talley, "
    "Angelica Yates, Garth Bates, Noble Garcia, Florence Pugh, Benedict Glass, "
    "Logan Kline, Blythe Perkins, Keith Leach, Lisandra Barnes, Baxter Bruce, "
    "Alfreda Vega, Alana Reyes, Nelle Sosa, Acton Ortiz, Yoshi Wilson, "
    "Emi Rice, Kalia Washington, Channing Huber, Martina Dyer, Leilani Alford, "
    "Tucker Phillips, Belle Dodson, Vance Robertson, Conan Weaver, Felicia Huber, "
    "Kyra Oneil, Shaine Wise, Jamal Finch, Roary Noble, Rafael Stewart"
).split(", ")


def build_app(s: list[str], u: list[str]) -> App:

    class SelTestApp(App):
        CSS_PATH = "tagset.tcss"
        def compose(self):
            yield TagSetSelector(s, u)
            yield Horizontal(id="filler")

    return SelTestApp()

app = build_app(selected, deselected)

if __name__ == '__main__':
    app.run()
