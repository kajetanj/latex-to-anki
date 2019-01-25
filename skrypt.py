import re
import pandas as pd

SECTION_TITLES = True
tex_filename = "main.tex"
csv_filename = "anki.csv"
section_split = r"\\section"
card_split = r"\\subsection"


def prepare_card(raw_card, section_title=""):
    front, back = raw_card.split("\n", 1)
    front = front[1:-1]  # Usuwamy { i } z tytułu karty
    title = "{\\tiny %s}" % section_title if section_title else ""
    return title + front, back


def main():
    with open(tex_filename, "r", encoding="utf-8") as file:
        text = file.read()

    # Usuwamy \section i dzielimy
    sections = re.split(section_split, text)[1:]

    anki_cards = []

    for section in sections:
        # Z każdego rozdziału usuwamy \card i dzielimy.
        # Wyciągamy tytuł i zapominamy o tym co było przed pierwszym \card.
        section_title, section_text = section.split("\n", 1)
        section_title = section_title[1:-1]  # Usuwamy { i } z tytułu rozdziału
        if not SECTION_TITLES:
            section_title = ""
        section_cards = re.split(card_split, section_text)[1:]
        anki_cards += [prepare_card(card, section_title) for card in section_cards]

    df = pd.DataFrame(anki_cards)
    df.to_csv(csv_filename, header=None, index=None)


if __name__ == "__main__":
    main()
