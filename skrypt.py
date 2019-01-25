import re
import pandas as pd

tex_filename = "main.tex"
csv_filename = "anki.csv"
section_split = r"\\section"
card_split = r"\\subsection"
double_dollars = "\$\$(.*?)\$\$"
single_dollars = "\$([^\[\$\]][^\$]*?[^\/\[\$])\$"
not_last_item = r"\\item(.*?)\\item"
last_item_enumerate = r"\\item(.*?)\\end{enumerate}"
last_item_itemize = r"\\item(.*?)\\end{itemize}"


def make_anki(string):
    string = re.sub(double_dollars, r"[$$]\1[/$$]", string)
    string = re.sub(single_dollars, r"[$]\1[/$]", string)
    # TODO: enumerate & itemize
    # Założenie: Jedyne zawieranie to itemize wewnątrz enumerate.
    string = string.replace("\\begin{enumerate}", "<ol>")
    string = string.replace("\\begin{itemize}", "<ul>")
    string = re.sub(not_last_item, r"<li>\1</li>\n<li>", string)
    string = re.sub(last_item_enumerate, r"<li>\1</li>\n</ol>", string)
    string = re.sub(last_item_itemize, r"<li>\1</li>\n</ul>", string)
    return string


def prepare_card(raw_card, section_title=""):
    raw_front, raw_back = raw_card.split("\n", 1)
    front = raw_front[1:-1]  # Usuwamy { i } z tytułu karty
    raw_back = raw_back.strip("\t")  # TODO: Co to?
    raw_back = re.sub('\r?\n', '<br>', raw_back)
    # Usuwanie nowej linii z końca?
    back = re.sub(r"[\n]*$", "", raw_back.strip(" ")).rstrip("\n")
    back = back.replace("\\\n", "<br>")
    # TODO: lepsze formatowanie
    title = f"{section_title}<br>" if section_title else ""
    return title + make_anki(front), make_anki(back).replace("\n", "<br>")


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
        section_cards = re.split(card_split, section_text)[1:]
        anki_cards += [prepare_card(card, section_title) for card in section_cards]

    df = pd.DataFrame(anki_cards)
    df.to_csv(csv_filename, header=None, index=None)


if __name__ == "__main__":
    main()
