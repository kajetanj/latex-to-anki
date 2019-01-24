import re
import pandas as pd

tex_filename = "main.tex"
csv_filename = "anki.csv"
section_split = r"\\section"
card_split = r"\\subsection"
double_dolars = "\$\$(.*?)\$\$"
single_dolars = "\$([^\[\$\]][^\$]*?[^\/\[\$])\$"


def make_anki(string):
    double_dolars_str = re.sub(double_dolars, r"[$$]\1[/$$]", string)
    single_dolars_str = re.sub(single_dolars, r"[$]\1[/$]", double_dolars_str)
    return single_dolars_str


def prepare_card(raw_card, section_title=""):
    raw_front, raw_back = raw_card.split("\n", 1)
    front = raw_front[1:-1]  # Usuwamy { i } z tytułu karty
    raw_back = raw_back.strip("\t")  # TODO: Co to?
    # Usuwanie nowej linii z końca?
    back = re.sub(r"[\n]*$", "", raw_back.strip(" ")).rstrip("\n")
    back = back.replace("\\\n", "<br>")
    # TODO: lepsze formatowanie
    title = f"{section_title}<br>" if section_title else ""
    return title + make_anki(front), make_anki(back).replace("\n", "<br>")


def main():
    with open(tex_filename, "r") as file:
        text = file.read()

    # Usuwamy \section i dzielimy
    sections = re.split(section_split, text)[1:]

    anki_cards = []

    for section in sections:
        # Z każdego rozdziału usuwamy \card i dzielimy,
        # zapominamy o tym co było przed pierwszym \card.
        # W szczególności zapominamy o tytule rozdziału.
        section_title, section_text = section.split("\n", 1)
        section_title = section_title[1:-1]  # Usuwamy { i } z tytułu rozdziału
        section_cards = re.split(card_split, section_text)[1:]
        anki_cards += [prepare_card(card, section_title) for card in section_cards]

    df = pd.DataFrame(anki_cards)
    df.to_csv(csv_filename, header=None, index=None)


if __name__== "__main__":
    main()
